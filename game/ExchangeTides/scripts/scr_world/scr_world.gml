// ===== Game state, time, travel, saving =====================================================

function new_game(_mode, _captain_id) {
	var D = global.D;
	var c = variable_struct_get(D.captains, _captain_id);
	var _ship = variable_struct_get(D.pships, c.ship);
	global.UI.toasts = [];
	global.UI.dialogs = [];
	global.G = {
		version: 3,
		mode: _mode,                 // "campaign" | "free"
		captain: _captain_id,
		t: D.config.start_month * WEEKS_PER_MONTH,   // absolute week counter
		port: c.port,
		cash: c.cash, bank: c.bank, debt: c.debt,
		ship: { type: c.ship, name: c.ship_name, hp: _ship.hp, guns: c.guns, upgrades: [],
		        ammo: { firepot: struct_get_or(c.ammo, "firepot", 0), chains: struct_get_or(c.ammo, "chains", 0), bomb: struct_get_or(c.ammo, "bomb", 0) } },
		fleet: [],                   // extra ships (flagship is G.ship); see scr_fleet
		contracts: [], offers: {},   // governor contracts (scr_contracts)
		cargo: {},
		items: [ { id: c.perk, months: 0 } ],
		log: [],
		level: 0,
		visited: [ c.port ],
		stats: { wins: 0, losses: 0, trades: 0, profit: 0, voyages: 0, storms: 0, sunk: 0, contracts: 0 },
		campaign: { id: (_mode == "campaign") ? campaign_for_captain(_captain_id).id : "", chapter: -1, step: 0, vars: {}, wins_at_step: 0, done: false },
		// Each captain's story happens in its own year (1694-1708); free trade uses config.start_year.
		start_year: (_mode == "campaign") ? struct_get_or(campaign_for_captain(_captain_id), "year", D.config.start_year) : D.config.start_year,
		victory_shown: false,
		closed: (_mode == "campaign") ? struct_get_or(c, "closed_ports", []) : [],   // ports this captain can never visit (campaign only)
		pending_end: "",
		goods: {}, portmeta: {}, markets: {},
	};
	economy_init();
	var _p = variable_struct_get(D.ports, c.port);
	log_add(trf("{0} {1} takes command of the {2} at {3}.", c.title, c.name, c.ship_name, _p.name));
	if (_mode == "campaign") campaign_start();
	else log_add(trf("Free trade: reach a net worth of {0} within {1} years.", fmt_money(D.config.free_mode_goal), D.config.free_mode_years));
}

function ship_def() { return variable_struct_get(global.D.pships, global.G.ship.type); }
function ship_max_hp() { return ship_max_hp_of(global.G.ship); }
function captain_def() { return variable_struct_get(global.D.captains, global.G.captain); }
function port_def(_pid = undefined) { return variable_struct_get(global.D.ports, _pid == undefined ? global.G.port : _pid); }
function port_has(_pid, _building) { return arr_contains(port_def(_pid).buildings, _building); }

/// False for ports closed to this captain (hidden on the map, never chosen for jobs or storms).
function port_open(_pid) { return global.G == undefined || !arr_contains(struct_get_or(global.G, "closed", []), _pid); }

function log_add(_text) {
	var G = global.G;
	array_insert(G.log, 0, { t: G.t, text: _text });
	if (array_length(G.log) > 60) array_resize(G.log, 60);
}

function item_add(_id) {
	var _def = variable_struct_get(global.D.items, _id);
	array_push(global.G.items, { id: _id, months: struct_get_or(_def, "months", 0) });
}

function item_has(_id) {
	var G = global.G;
	for (var i = 0; i < array_length(G.items); i++) if (G.items[i].id == _id) return true;
	return false;
}

function item_remove(_id) {
	var G = global.G;
	for (var i = 0; i < array_length(G.items); i++) if (G.items[i].id == _id) { array_delete(G.items, i, 1); return; }
}

/// Level drives which ships the shipyard sells and which enemies you meet.
function level_update() {
	var G = global.G, D = global.D;
	var _from_wins = G.stats.wins div D.config.level_battles_per_level;
	var _from_worth = floor(log2(max(1, net_worth() / 20000)));
	G.level = clamp(max(G.level, _from_wins, _from_worth), 0, 11);
}

/// Time runs in weeks: prices move every week; interest, contraband and crew contracts every month.
function advance_weeks(_n = 1) {
	repeat (_n) {
		global.G.t += 1;
		if (global.G.t mod WEEKS_PER_MONTH == 0) { economy_month_tick(); market_roll_all(); }   // prices hold for a month
		contracts_week_tick();
	}
	level_update();
}

function advance_month(_n = 1) { advance_weeks(_n * WEEKS_PER_MONTH); }

// ---- voyages ------------------------------------------------------------------------------
/// Resolve sailing events for a trip (docs §4). Returns a struct describing what happens.
function voyage_plan(_dest) {
	var G = global.G, D = global.D;
	var _plan = { dest: _dest, storm: "", battles: 0, extra_weeks: 0, special_enemy: "", special_kind: "", contract: -1 };
	if (roll100() < eff("sailing_storm_frequency", 12)) {
		G.stats.storms += 1;
		if (roll100() < eff("sailing_lost", 10)) _plan.storm = "outran";
		else if (roll100() < eff("sailing_delay", 45)) { _plan.storm = "delay"; _plan.extra_weeks = 1; }
		else {
			_plan.storm = "lost";
			var _cands = [];
			for (var i = 0; i < array_length(D.ports_list); i++) if (D.ports_list[i].id != _dest && D.ports_list[i].id != G.port && port_open(D.ports_list[i].id)) array_push(_cands, D.ports_list[i].id);
			_plan.dest = arr_pick(_cands);
		}
	} else {
		var c = eff("sailing_combat_frequency", 33);
		if (c > 100) {
			var _extra = ((c - 101) div 80) + 1;
			_plan.battles += _extra;
			c -= 80 * _extra;
		}
		if (roll100() < c) _plan.battles += 1;
	}
	// Campaign: a scripted fight waits at the destination.
	var _goal = campaign_current_goal();
	if (_goal != undefined && _goal.type == "npccombat" && campaign_resolve(_goal.port) == _plan.dest) { _plan.special_enemy = _goal.enemy; _plan.special_kind = "campaign"; }
	// Assaulting a fort: no random raiders on the way in.
	if (_plan.special_enemy != "" && variable_struct_get(D.enemies, _plan.special_enemy).behavior == "stationary") _plan.battles = 0;
	// Contracts: a pirate hunt waits off its port.
	if (_plan.special_enemy == "") {
		var _ci = contract_hunt_at(_plan.dest);
		if (_ci >= 0) { _plan.special_enemy = global.G.contracts[_ci].enemy; _plan.special_kind = "hunt"; _plan.contract = _ci; }
	}
	return _plan;
}

function pick_enemy() {
	var G = global.G, D = global.D;
	var _pool = [];
	for (var i = 0; i < array_length(D.ships.enemies); i++) {
		var e = D.ships.enemies[i];
		if (struct_get_or(e, "unique", false)) continue;
		if (e.level <= G.level + 1 && e.level >= G.level - 3) array_push(_pool, e.id);
	}
	if (array_length(_pool) == 0) _pool = [ D.ships.enemies[0].id ];
	return arr_pick(_pool);
}

/// Called when the ship docks at the destination after all events.
function arrive_at(_pid) {
	var G = global.G;
	G.port = _pid;
	G.stats.voyages += 1;
	if (!arr_contains(G.visited, _pid)) array_push(G.visited, _pid);
	log_add(trf("Arrived at {0}.", port_def().name));
	customs_check();
	contracts_on_arrival();
	campaign_check();
	save_game("autosave.json");
	ui_go("port");
	free_mode_check();
}

function free_mode_check() {
	var G = global.G, D = global.D;
	if (G.mode != "free" || G.victory_shown) return;
	if (net_worth() >= D.config.free_mode_goal) {
		G.victory_shown = true;
		G.pending_end = "victory";
	} else if (G.t >= D.config.free_mode_years * 12) {
		G.victory_shown = true;
		G.pending_end = "gameover";
	}
}

// ---- save / load ---------------------------------------------------------------------------
// Five manual slots (slot1..slot5.json) plus autosave.json. settings.json remembers the last file used.
#macro SAVE_SLOTS 5

function save_game(_file = "autosave.json") {
	global.G.saved_at = date_current_datetime();
	save_text(_file, json_stringify(global.G));
	if (_file != "selftest_save.json") settings_set("last_save", _file);
	global.UI.slot_cache = undefined;
}

function load_game(_file = "autosave.json") {
	if (!file_exists(_file)) return false;
	var _g = load_json(_file);
	if (!is_struct(_g)) return false;
	global.G = _g;
	save_migrate();
	if (_file != "selftest_save.json") settings_set("last_save", _file);
	global.PORT_LAYOUTS = {};
	return true;
}

function has_save(_file = "autosave.json") { return file_exists(_file); }

/// Saves from older versions: months -> weeks, and fields added since.
function save_migrate() {
	var G = global.G;
	if (struct_get_or(G, "version", 1) < 2) {
		G.t *= WEEKS_PER_MONTH;   // v1 counted months; its price specials were already in months
		G.version = 3;
	}
	if (G.version == 2) {         // v2 scheduled price specials in weeks
		var _ids = variable_struct_get_names(G.portmeta);
		for (var i = 0; i < array_length(_ids); i++) {
			var _pm = variable_struct_get(G.portmeta, _ids[i]);
			_pm.high_t = _pm.high_t div WEEKS_PER_MONTH; _pm.low_t = _pm.low_t div WEEKS_PER_MONTH;
		}
		G.version = 3;
	}
	if (!variable_struct_exists(G, "fleet")) G.fleet = [];
	if (!variable_struct_exists(G.campaign, "id")) G.campaign.id = (G.mode == "campaign") ? "grimmer_debt" : "";   // saves from before per-captain stories
	if (!variable_struct_exists(G, "start_year")) G.start_year = global.D.config.start_year;
	if (!variable_struct_exists(G, "closed")) G.closed = [];
	if (!variable_struct_exists(G.ship, "ammo")) G.ship.ammo = { firepot: 0, chains: 0, bomb: 0 };   // saves from the flagship-swap bug
	if (!variable_struct_exists(G, "contracts")) G.contracts = [];
	if (!variable_struct_exists(G, "offers")) G.offers = {};
	if (!variable_struct_exists(G.stats, "sunk")) G.stats.sunk = 0;
	if (!variable_struct_exists(G.stats, "contracts")) G.stats.contracts = 0;
	// Items removed from the game since the save was made (e.g. the old hired escort ships).
	for (var i = array_length(G.items) - 1; i >= 0; i--) if (!variable_struct_exists(global.D.items, G.items[i].id)) array_delete(G.items, i, 1);
}

/// Summary of a save file for the slot list (undefined if empty).
function save_peek(_file) {
	if (!file_exists(_file)) return undefined;
	var _g = load_json(_file);
	if (!is_struct(_g)) return undefined;
	var _c = struct_get_or(global.D.captains, _g.captain, undefined);
	var _t = (struct_get_or(_g, "version", 1) < 2) ? _g.t * WEEKS_PER_MONTH : _g.t;
	var _p = struct_get_or(global.D.ports, _g.port, undefined);
	return {
		who: (_c != undefined ? _c.name : _g.captain),
		mode: (_g.mode == "campaign" ? "Campaign" : "Free Trade"),
		date: date_name(_t),
		where: (_p != undefined ? _p.name : ""),
		worth: _g.cash + _g.bank - _g.debt,
		ships: 1 + array_length(struct_get_or(_g, "fleet", [])),
	};
}

// ---- settings ------------------------------------------------------------------------------
function settings_get(_k, _def) {
	if (!variable_global_exists("SETTINGS")) global.SETTINGS = file_exists("settings.json") ? load_json("settings.json") : {};
	if (!is_struct(global.SETTINGS)) global.SETTINGS = {};
	return struct_get_or(global.SETTINGS, _k, _def);
}

function settings_set(_k, _v) {
	settings_get(_k, 0);
	variable_struct_set(global.SETTINGS, _k, _v);
	save_text("settings.json", json_stringify(global.SETTINGS));
}
