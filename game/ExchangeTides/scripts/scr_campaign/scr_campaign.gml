// ===== Campaign task engine (docs/MECHANICS.md §6) ==========================================
// A chapter = {vars, steps}. Variables pick ports by filters; steps run in order:
//   say(npc,text,ok) | log(text) | get/give(item) | reward(cash) | unlock_good(good)
//   set_level(level) | take(good,amount) | goal(type,...) | end
// Goal types: talk(npc,port,building) arrive(port) have_good(good,amount) deposit(amount)
//             cash(amount) networth(amount) repay combat(wins) npccombat(enemy,port)
//             deliver(good,amount,port) sink(n) fleet(n: ships owned) contracts(n: governor jobs done)
// New step or goal types: add a case in campaign_run_step / campaign_goal_met.

/// The story a captain plays (characters.json -> captains[].campaign), falling back to the first one.
function campaign_for_captain(_cid) {
	var D = global.D;
	var c = struct_get_or(D.captains, _cid, undefined);
	var _id = (c != undefined) ? struct_get_or(c, "campaign", "") : "";
	if (_id != "" && variable_struct_exists(D.campaigns, _id)) return variable_struct_get(D.campaigns, _id);
	return variable_struct_get(D.campaigns, variable_struct_get_names(D.campaigns)[0]);
}

/// The story of the game in progress.
function campaign_def() {
	var D = global.D, G = global.G;
	var _id = struct_get_or(G.campaign, "id", "");
	if (_id != "" && variable_struct_exists(D.campaigns, _id)) return variable_struct_get(D.campaigns, _id);
	return campaign_for_captain(G.captain);
}

function campaign_start() {
	var G = global.G;
	G.campaign.chapter = -1;
	log_add(campaign_def().intro);
	campaign_next_chapter();
}

function campaign_chapter() {
	var G = global.G;
	if (G.mode != "campaign" || G.campaign.done || G.campaign.chapter < 0) return undefined;
	var _ch = campaign_def().chapters;
	if (G.campaign.chapter >= array_length(_ch)) return undefined;
	return _ch[G.campaign.chapter];
}

function campaign_next_chapter() {
	var G = global.G, D = global.D;
	G.campaign.chapter += 1;
	G.campaign.step = 0;
	var _chs = campaign_def().chapters;
	if (G.campaign.chapter >= array_length(_chs)) { G.campaign.done = true; return; }
	var ch = _chs[G.campaign.chapter];
	G.level = max(G.level, ch.level);
	// Resolve chapter variables (port filters). Ports picked in earlier chapters stay picked for the rest of
	// the story, so a later chapter can send you back to someone you met ("{p2}" is still Nan's town).
	var _vars = { here: port_def().name, captain: captain_def().name };
	var _old = G.campaign.vars;
	if (is_struct(_old)) {
		var _ok = variable_struct_get_names(_old);
		for (var i = 0; i < array_length(_ok); i++) if (_ok[i] != "here" && _ok[i] != "captain") variable_struct_set(_vars, _ok[i], variable_struct_get(_old, _ok[i]));
	}
	var _used = [ G.port ];
	var _keys = variable_struct_get_names(ch.vars);
	array_sort(_keys, true);
	for (var i = 0; i < array_length(_keys); i++) {
		var _pid = campaign_pick_port(variable_struct_get(ch.vars, _keys[i]), _used);
		array_push(_used, _pid);
		variable_struct_set(_vars, _keys[i] + "_id", _pid);
		variable_struct_set(_vars, _keys[i], port_def(_pid).name);
	}
	G.campaign.vars = _vars;
	log_add(trf("Chapter {0}: {1}", G.campaign.chapter + 1, ch.title));
	ui_toast(trf("Chapter {0}: {1}", G.campaign.chapter + 1, ch.title));
	campaign_run();
}

/// Filters: other (not here), new (not used by this chapter yet), has:<building>
function campaign_pick_port(_filter, _used) {
	var D = global.D, G = global.G;
	var _f = str_split(_filter, ",");
	var _cands = [];
	for (var i = 0; i < array_length(D.ports_list); i++) {
		var p = D.ports_list[i];
		var ok = true;
		for (var k = 0; k < array_length(_f); k++) {
			var f = str_trim(_f[k]);
			if (f == "other" && p.id == G.port) ok = false;
			if (f == "new" && arr_contains(_used, p.id)) ok = false;
			if (string_pos("has:", f) == 1 && !arr_contains(p.buildings, string_delete(f, 1, 4))) ok = false;
		}
		if (p.lawless || !port_open(p.id)) ok = false;
		if (ok) array_push(_cands, p.id);
	}
	if (array_length(_cands) == 0) return D.ports_list[0].id;
	return arr_pick(_cands);
}

/// Resolve "{p1}" -> port id, or pass a literal port id through.
function campaign_resolve(_ref) {
	if (_ref == undefined) return undefined;
	if (string_char_at(_ref, 1) == "{") {
		var _k = string_copy(_ref, 2, string_length(_ref) - 2) + "_id";
		return struct_get_or(global.G.campaign.vars, _k, _ref);
	}
	return _ref;
}

function campaign_text(_s) { return fill_text(_s, global.G.campaign.vars); }

function campaign_current_step() {
	var ch = campaign_chapter();
	if (ch == undefined) return undefined;
	if (global.G.campaign.step >= array_length(ch.steps)) return undefined;
	return ch.steps[global.G.campaign.step];
}

function campaign_current_goal() {
	var s = campaign_current_step();
	if (s == undefined || s[$ "do"] != "goal") return undefined;
	return s;
}

function campaign_objective_text() {
	var G = global.G;
	if (G.mode != "campaign") return trf("Free trade: reach {0} net worth by {1}", fmt_money(global.D.config.free_mode_goal), month_name(global.D.config.free_mode_years * 12 * WEEKS_PER_MONTH));
	if (G.campaign.done) return "Campaign complete! Keep trading as long as you like.";
	var s = campaign_current_goal();
	if (s == undefined) return "";
	return campaign_text(s.text);
}

/// Run non-goal steps until a goal blocks or the chapter ends.
function campaign_run() {
	var G = global.G;
	var _guard = 0;
	while (_guard < 100) {
		_guard++;
		var ch = campaign_chapter();
		if (ch == undefined) return;
		if (G.campaign.step >= array_length(ch.steps)) { campaign_next_chapter(); return; }
		var s = ch.steps[G.campaign.step];
		if (s[$ "do"] == "goal") {
			if (!campaign_goal_met(s)) return;
		} else {
			campaign_run_step(s);
		}
		G.campaign.step += 1;
		G.campaign.wins_at_step = G.stats.wins;
		G.campaign.sunk_at_step = G.stats.sunk;
		G.campaign.contracts_at_step = G.stats.contracts;
	}
}

function campaign_run_step(s) {
	var G = global.G;
	switch (s[$ "do"]) {
		case "say":   // optional "name" overrides the speaker's title for this story ("Commander Ada Hale")
			ui_dialog(s.npc, campaign_text(s.text), campaign_text(struct_get_or(s, "ok", "Continue")), struct_get_or(s, "name", ""));
			break;
		case "log": log_add(campaign_text(s.text)); break;
		case "get":
			item_add(s.item);
			ui_toast(trf("Received: {0}", variable_struct_get(global.D.items, s.item).name));
			break;
		case "give": item_remove(s.item); break;
		case "reward":
			G.cash += s.cash;
			ui_toast(trf("Reward: {0}", fmt_money(s.cash)));
			break;
		case "unlock_good":
			variable_struct_get(G.goods, s.good).unlocked = true;
			ui_toast(trf("New trade good: {0}", variable_struct_get(global.D.goods, s.good).name));
			break;
		case "set_level": G.level = max(G.level, s.level); break;
		case "take": cargo_remove(s.good, s.amount); break;
		case "end":
			G.campaign.done = true;
			G.pending_end = "victory";   // shown once the player is back in port
			break;
	}
}

/// talk goals are completed by visiting the building; see campaign_on_visit.
function campaign_goal_met(s) {
	var G = global.G;
	switch (s.type) {
		case "arrive": return G.port == campaign_resolve(s.port);
		case "have_good": return cargo_qty(s.good) >= s.amount;
		case "deposit": return G.bank >= s.amount;
		case "cash": return G.cash >= s.amount;
		case "networth": return net_worth() >= s.amount;
		case "repay": return G.debt <= 0;
		case "combat": return G.stats.wins - G.campaign.wins_at_step >= s.wins;
		case "talk": return struct_get_or(s, "_done", false);
		case "npccombat": return struct_get_or(G.campaign, "npc_won", "") == s.enemy;
		case "deliver": return G.port == campaign_resolve(s.port) && cargo_qty(s.good) >= s.amount;
		case "sink": return G.stats.sunk - struct_get_or(G.campaign, "sunk_at_step", G.stats.sunk) >= s.n;
		case "fleet": return fleet_size() >= s.n;
		case "contracts": return G.stats.contracts - struct_get_or(G.campaign, "contracts_at_step", G.stats.contracts) >= s.n;
	}
	return false;
}

function campaign_check() { if (global.G.mode == "campaign") campaign_run(); }

/// Called when the player opens a building in port.
function campaign_on_visit(_building) {
	var G = global.G;
	var s = campaign_current_goal();
	if (s == undefined || s.type != "talk") return;
	if (G.port != campaign_resolve(s.port)) return;
	var _b = struct_get_or(s, "building", "");
	if (_b == "") _b = (s.npc == "governor") ? "governor" : "";
	if (_b != "" && _b != _building) return;
	s._done = true;
	campaign_run();
	s._done = false;   // chapter data is shared; reset the transient flag
}

function campaign_on_battle_won(_enemy_id) {
	var G = global.G;
	G.campaign.npc_won = _enemy_id;
	campaign_check();
	G.campaign.npc_won = "";
}
