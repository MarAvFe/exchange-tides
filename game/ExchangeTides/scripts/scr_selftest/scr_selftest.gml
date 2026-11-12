// ===== Automated self-test (run with environment variable ET_SELFTEST=1) =====================
// A scripted bot walks every screen and system, logs "[SELFTEST]" lines and saves screenshots
// (shot_*.png in the game's save directory), then quits. Used for headless verification.

function selftest_enabled() { return environment_get_variable("ET_SELFTEST") == "1"; }

function st_log(_s) { show_debug_message("[SELFTEST] " + string(_s)); }

function st_assert(_cond, _what) {
	if (_cond) st_log("PASS " + _what);
	else { st_log("FAIL " + _what); global.ST.fails += 1; }
}

function selftest_init() {
	global.ST = { step: 0, wait: 0, shot: "", fails: 0, frame: 0 };
	st_log("start");
}

/// Called every Step. Each step performs an action and optionally requests a screenshot.
function selftest_step() {
	var S = global.ST;
	S.frame += 1;
	if (S.shot != "40_dark_dialog") global.UI.dialogs = [];   // the bot dismisses every dialog
	if (S.wait > 0) { S.wait -= 1; return; }
	var _n = S.step;
	S.step += 1;
	S.wait = 3;
	switch (_n) {
		case 0:
			i18n_set("es");   // the default language; every screenshot below is in Spanish
			st_assert(tr("Back") == "Volver" && global.D.goods.fish.name == "Pescado salado" && trf("Sail to {0}  (1 week)", "X") == "Navegar a X  (1 semana)", "Spanish table and data translation");
			st_assert(global.D.captains.vega.title == "Capitana" && global.D.captains.wren.title == "Capitán", "gendered titles");
			ui_go("title"); S.shot = "01_title";
			st_assert(array_length(global.FONTS.body) > 0 && array_length(global.FONTS.head) > 0, "custom fonts loaded");
			break;
		case 1: global.UI.pending_mode = "campaign"; ui_go("newgame"); S.shot = "02_newgame"; break;
		case 2:
			new_game("campaign", "vega");
			ui_go("port");
			S.shot = "03_port";
			st_assert(global.G.campaign.chapter == 0, "campaign chapter 1 started");
			st_assert(item_has("sealed_letter"), "chapter 1 gave sealed letter");
			break;
		case 3:
			var _cash0 = global.G.cash;
			var _bought = market_buy("sugar", 10);
			st_assert(_bought > 0 && cargo_qty("sugar") == _bought, "bought sugar x" + string(_bought));
			st_assert(global.G.cash < _cash0, "cash decreased by purchase");
			if (cargo_qty("sugar") < 10) { global.G.cash += 50000; market_buy("sugar", 10 - cargo_qty("sugar")); }
			ui_go("market"); S.shot = "04_market";
			break;
		case 4:
			campaign_check();
			var _g = campaign_current_goal();
			st_assert(_g != undefined && _g.type == "talk", "sugar goal complete, now talk goal");
			var _p = variable_struct_get(global.D.goods, "sugar");
			var _price = price_at(global.G.port, "sugar");
			st_assert(_price >= _p.min && _price <= _p.max * 2, "sugar price in band: " + string(_price));
			global.G.cash += 20000;
			ui_go("bank"); S.shot = "05_bank";
			break;
		case 5:
			var _a = npc_get("puerto_ambar", "lender"), _b = npc_get("puerto_ambar", "lender"), _c = npc_get("saltmere", "lender");
			st_assert(_a == _b && _a.name != "", "the moneylender of a port stays the same (" + _a.name + ")");
			var _diff = 0;
			for (var i = 0; i < 6; i++) if (json_stringify(npc_get(global.D.ports_list[i].id, "barkeep").t) != json_stringify(npc_get("puerto_ambar", "barkeep").t)) _diff++;
			st_assert(_diff >= 4, "barkeeps differ between ports");
			ui_go("lender"); S.shot = "06_lender"; break;
		case 6: ui_go("shipyard"); S.shot = "07_shipyard"; break;
		case 7:
			for (var i = 0; i < 8; i++) global.UI.tavern_text = tavern_drink();
			st_log("tavern says: " + global.UI.tavern_text);
			ui_go("tavern"); S.shot = "08_tavern";
			break;
		case 8: ui_go("curio"); S.shot = "09_curio"; break;
		case 9: ui_go("governor"); S.shot = "10_governor"; break;
		case 10: ui_go("journal"); S.shot = "11_journal"; break;
		case 11: ui_go("help"); S.shot = "12_help"; break;
		case 12: ui_go("map"); S.shot = "13_map"; break;
		case 13:
			// Deliver the letter: travel to p1 along a sea route.
			var _p1 = global.G.campaign.vars.p1_id;
			var _r = route_get(global.G.port, _p1);
			var _a = port_def(global.G.port), _b = port_def(_p1);
			st_assert(array_length(_r) >= 2 && route_length(_r) >= point_distance(_a.x, _a.y, _b.x, _b.y) - 1, "sea route found (" + string(array_length(_r)) + " points)");
			voyage_start(_p1);
			global.V.battle_at = [];
			global.V.prog = 0.45;
			S.shot = "14_sailing";
			S.wait = 10;
			break;
		case 14:
			var _t0 = global.G.t;
			advance_weeks(1);
			st_assert(global.G.t == _t0 + 1, "a voyage takes one week");
			global.G.port = global.G.campaign.vars.p1_id;
			ui_go("port");
			campaign_on_visit("governor");
			st_assert(global.G.campaign.chapter == 1, "chapter 2 reached after talking to governor");
			st_assert(!item_has("sealed_letter"), "letter handed over");
			st_assert(variable_struct_get(global.G.goods, "spice").unlocked, "spice unlocked");
			break;
		case 15:
			// Combat: flagship + a fleet ship (and a hired master gunner) against a pack of three.
			global.G.ship.hp = 500;
			global.G.ship.ammo.firepot = 3;
			item_add("master_gunner");
			var _cap0 = cargo_capacity();
			array_push(global.G.fleet, fleet_new_ship("schooner"));
			st_assert(cargo_capacity() > _cap0, "a second ship adds hold space");
			global.G.fleet[0].hp = 500;
			S.sunk0 = global.G.stats.sunk;
			combat_start("cutthroat_sloop", false, 2);
			st_assert(array_length(global.C.enemies) == 3, "enemy pack of 3 ships");
			st_assert(array_length(global.C.allies) == 2, "fleet ship joins the battle (crew hires are people, not ships)");
			st_assert(array_length(global.C.cannons) == global.G.ship.guns, "one reload loop per cannon");
			st_assert(combat_attach("firepot") && global.G.ship.ammo.firepot == 2, "fire pot loaded onto next cannon");
			var _probe = { x0: 0, y0: 0, x1: global.C.enemies[0].x, y1: global.C.enemies[0].y, to: global.C.enemies[0], ammo: "firepot" };
			var _ns = array_length(global.C.shots);
			combat_spread(_probe);
			st_assert(array_length(global.C.shots) - _ns == 2, "fire pot spreads to the other ships");
			array_resize(global.C.shots, _ns);
			global.C.target = 2;
			st_assert(combat_target() == 2, "target selection");
			for (var i = 0; i < 26; i++) combat_update(0.1);   // get some cannon fire and smoke on screen
			st_assert(array_length(global.C.parts) > 0, "battle particles spawned");
			S.shot = "15_combat";
			S.wait = 2;
			break;
		case 16:
			var C = global.C;
			var _t = 0;
			while (C.result == "" && _t < 600) {
				combat_update(0.1);
				_t += 0.1;
			}
			st_log("battle took " + string(_t) + "s, sunk " + string(C.sunk));
			st_assert(C.result == "won", "combat result: " + C.result);
			st_assert(global.G.stats.sunk - S.sunk0 == C.sunk, "sinkings counted for bounties");
			S.shot = "16_combat_result";
			break;
		case 17:
			voyage_after_battle(global.C.result);
			global.G.ship.hp = ship_max_hp();
			// Walk the rest of the campaign by satisfying each goal in turn.
			var _guard = 0, _ch_seen = global.G.campaign.chapter;
			while (!global.G.campaign.done && _guard < 60) {
				_guard++;
				var _g = campaign_current_goal();
				if (_g == undefined) { campaign_check(); continue; }
				st_campaign_satisfy(_g);
				global.UI.dialogs = [];
				if (global.G.campaign.chapter != _ch_seen) { _ch_seen = global.G.campaign.chapter; st_log("campaign reached chapter " + string(_ch_seen + 1)); }
			}
			st_assert(array_length(global.D.campaign.chapters) >= 7, "campaign has " + string(array_length(global.D.campaign.chapters)) + " chapters");
			st_assert(global.G.campaign.done, "campaign complete");
			st_assert(item_has("crowe_ledger") && item_has("undertow_signals") && item_has("admiralty_warrant"), "new chapters handed out their items");
			st_assert(global.G.pending_end == "victory", "victory pending");
			ui_go("port");
			S.wait = 4;
			break;
		case 18:
			st_assert(global.UI.screen == "victory", "victory screen shown (" + global.UI.screen + ")");
			S.shot = "17_victory";
			break;
		case 19:
			// Contracts: accept a delivery from this governor and complete it.
			global.G.pending_end = "";
			ui_go("port");
			var _pid = "saltmere";
			global.G.port = _pid;
			global.G.offers = {};
			var _offers = contract_offers(_pid);
			st_assert(array_length(_offers) >= 2, "governor offers contracts");
			var c = contract_roll(_pid);
			while (c.kind != "deliver") c = contract_roll(_pid);
			array_insert(_offers, 0, c);
			st_assert(contract_accept(_pid, 0), "contract accepted");
			global.G.port = c.port;
			cargo_add(c.good, c.qty, 1);
			var _cash = global.G.cash;
			contracts_on_arrival();
			global.UI.dialogs = [];
			st_assert(array_length(global.G.contracts) == 0 && global.G.cash == _cash + c.reward, "delivery contract paid " + string(c.reward));
			// A bounty and an expiry.
			global.G.port = _pid;
			var b = contract_roll(_pid);
			while (b.kind != "bounty") b = contract_roll(_pid);
			array_insert(contract_offers(_pid), 0, b);
			contract_accept(_pid, 0);
			var h = contract_roll(_pid);
			while (h.kind != "hunt") h = contract_roll(_pid);
			array_insert(contract_offers(_pid), 0, h);
			contract_accept(_pid, 0);
			// A storm can blow the ship elsewhere, so look for a plan that actually reaches the port.
			var _hp = voyage_plan(h.port);
			for (var _r = 0; _r < 30 && _hp.dest != h.port; _r++) _hp = voyage_plan(h.port);
			st_assert(_hp.special_enemy == h.enemy || h.port == global.G.port, "hunt contract plans its battle");
			// Passengers: paid at their port; if late, they get off at the next port.
			var pa = contract_roll(_pid);
			while (pa.kind != "passenger") pa = contract_roll(_pid);
			array_insert(contract_offers(_pid), 0, pa);
			contract_accept(_pid, 0);
			var _n0 = array_length(global.G.contracts);
			var _cash1 = global.G.cash;
			global.G.port = pa.port; contracts_on_arrival(); global.UI.dialogs = [];
			st_assert(array_length(global.G.contracts) == _n0 - 1 && global.G.cash == _cash1 + pa.reward, "passenger delivered and paid");
			global.G.port = _pid;
			var pb = contract_roll(_pid);
			while (pb.kind != "passenger") pb = contract_roll(_pid);
			array_insert(contract_offers(_pid), 0, pb);
			contract_accept(_pid, 0);
			var _n1 = array_length(global.G.contracts);
			var _t1 = global.G.t;
			global.G.t = pb.due + 1;
			var _other = (pb.port == "tidewell") ? "lanterna" : "tidewell";
			global.G.port = _other; contracts_on_arrival(); global.UI.dialogs = [];
			st_assert(array_length(global.G.contracts) == _n1 - 1, "late passenger disembarks at the next port");
			global.G.t = _t1; global.G.port = _pid;
			ui_go("governor"); S.shot = "18_governor";
			break;
		case 20:
			ui_go("journal"); S.shot = "19_journal";
			break;
		case 21:
			ui_go("fleet"); S.shot = "20_fleet";
			break;
		case 22:
			// Promote a fleet ship to flagship: the ammo store follows the flag.
			var _ammo0 = global.G.ship.ammo.firepot;
			if (array_length(global.G.fleet) == 0) array_push(global.G.fleet, fleet_new_ship("schooner"));
			var _new = global.G.fleet[0];
			fleet_make_flagship(0);
			st_assert(global.G.ship == _new && variable_struct_exists(global.G.ship, "ammo") && global.G.ship.ammo.firepot == _ammo0, "make flagship moves the ammo store");
			st_assert(!variable_struct_exists(global.G.fleet[0], "ammo"), "old flagship hands over its ammo");
			global.UI.yard_sel = 1;
			ui_go("shipyard"); S.shot = "21_shipyard_swap";
			break;
		case 23:
			var _t0 = global.G.t;
			advance_weeks(12);
			st_assert(array_length(global.G.contracts) == 0, "contracts expire after their deadline");
			st_assert(global.G.t == _t0 + 12, "weeks advance");
			save_game("slot2.json");
			global.UI.slot_cache = undefined;
			st_assert(save_peek("slot2.json") != undefined, "save slot written");
			global.UI.save_mode = "save";
			ui_go("saves"); S.shot = "22_saves";
			break;
		case 24:
			ui_go("map"); S.shot = "23_map";
			break;
		case 25:
			save_game("selftest_save.json");
			var _cash = global.G.cash;
			global.G = undefined;
			st_assert(load_game("selftest_save.json"), "save/load roundtrip");
			st_assert(global.G.cash == _cash, "cash survived save/load");
			break;
		case 26:
			// Free mode: simulate 3 years of trading voyages headlessly.
			new_game("free", "calder");
			var _storms = 0, _battles = 0;
			for (var m = 0; m < 36 * WEEKS_PER_MONTH / 4; m++) {
				var _dest = arr_pick(global.D.ports_list).id;
				var _pl = voyage_plan(_dest);
				if (_pl.storm != "") _storms++;
				_battles += _pl.battles;
				advance_weeks(1 + _pl.extra_weeks);
				arrive_at(_pl.dest);
				var _gid = arr_pick(global.D.goods_list).id;
				market_sell(_gid, cargo_qty(_gid));
				if (variable_struct_get(global.G.goods, _gid).unlocked && variable_struct_get(global.D.goods, _gid).forsale) market_buy(_gid, 5);
			}
			global.UI.dialogs = [];
			st_log("36 voyages (weekly): storms=" + string(_storms) + " battles=" + string(_battles) + " cash=" + string(global.G.cash) + " debt=" + string(global.G.debt) + " worth=" + string(net_worth()) + " level=" + string(global.G.level));
			st_assert(_storms > 0 && _battles > 0, "storms and battles occur");
			st_assert(global.G.debt > 3000, "debt compounds monthly");
			var _tob = variable_struct_get(global.G.goods, "tobacco");
			st_assert(array_length(_tob.contra_now) == 2, "tobacco outlawed in 2 ports");
			ui_go("port"); S.shot = "24_free_port";
			break;
		case 27:
			ui_go("market"); S.shot = "25_free_market";
			break;
		case 28:
			st_assert(abs(effect_eval("bank_interest", 0.01) - 0.01) < 0.0001, "no effect on bank interest without items");
			item_add("hagglers_tongue"); item_add("crowe_ledger");
			var _bad = 0;
			for (var k = 0; k < array_length(global.D.goods_list); k++) { var _gk = global.D.goods_list[k].id; if (buy_price(_gk) > 1 && sell_price(_gk) >= buy_price(_gk)) _bad++; }
			st_assert(_bad == 0, "selling pays less than buying in the same market");
			item_remove("hagglers_tongue"); item_remove("crowe_ledger");
			global.G.t = (global.G.t div WEEKS_PER_MONTH) * WEEKS_PER_MONTH;
			var _p0 = price_at(global.G.port, "fish");
			advance_weeks(1);
			st_assert(price_at(global.G.port, "fish") == _p0, "prices hold within a month");
			st_assert(array_length(yard_stock("ironreef")) <= 2 && array_length(yard_stock("ironreef")) >= 1, "shipyards stock 1-2 hulls");
			item_add("hex_doll");
			st_assert(abs(eff("sailing_combat_frequency", 33) - global.D.config.sailing_combat_frequency * 0.6) < 0.01, "hex doll -40% combat frequency");
			item_add("golden_tankard");
			st_assert(abs(eff("alehouse_drink_prices", 25) - 12.5) < 0.01, "tankard halves drink price");
			st_assert(eff("contraband_seizure", 35) == 10, "false papers set seizure to 10");
			combat_start("dread_manowar", false);
			for (var i = 0; i < 30; i++) combat_update(0.1);
			// Heavy broadsides knock cannons off their carriages now and then, never the last one.
			var _g0 = array_length(global.C.cannons), _fake = { from: global.C.enemies[0], to: global.C.allies[0], x1: 440, y1: 500 };
			for (var i = 0; i < 400; i++) combat_gun_hit(_fake);
			st_log("cannons " + string(_g0) + " -> " + string(global.G.ship.guns) + " after 400 heavy hits");
			var _working = 0;
			for (var i = 0; i < array_length(global.C.cannons); i++) if (!global.C.cannons[i].broken) _working++;
			st_assert(global.G.ship.guns < _g0 && global.G.ship.guns >= 1 && _working == global.G.ship.guns && array_length(global.C.cannons) == _g0, "hits knock out cannons; broken ones stay listed");
			global.C.allies[0].hp = global.C.allies[0].max_hp;
			for (var i = 0; i < 5; i++) combat_update(0.1);   // broken guns never fire (no crash on the deck)
			st_assert(month_end(5) == 7 && month_end(8) == 11, "month_end");
			var _cr = contract_roll(global.G.port);
			st_assert(_cr.due mod WEEKS_PER_MONTH == WEEKS_PER_MONTH - 1 && string_pos(string_copy(tr("by end of {0} ({1} wks left)"), 1, 6), contract_due_text(_cr)) == 1, "deadlines are month ends: " + contract_due_text(_cr));
			S.shot = "26_combat_big";
			S.wait = 4;
			global.G.ship.guns = _g0;   // re-arm for the rest of the run
			break;
		case 29:
			// Fort assault: a building on its island, guard ships beside it, no raiders on the way.
			var _pl = voyage_plan("mangrove_key");
			global.G.level = 6;
			combat_start("harbour_fort", true);
			st_assert(global.C.fort && array_length(global.C.enemies) >= 2, "fort battle with guard ships (" + string(array_length(global.C.enemies)) + " targets)");
			st_assert(global.C.enemies[0].max_hp > global.D.enemies.harbour_fort.hp, "fort scales with your level");
			for (var i = 0; i < 30; i++) combat_update(0.1);
			S.shot = "26b_fort";
			S.wait = 3;
			break;
		case 32:
			st_difficulty_sim();
			ui_message("Townsfolk", "Generated faces", "portrait_governor");
			ui_go("newgame"); S.shot = "27_newgame6";
			break;
		case 30: theme_set("storybook"); ui_go("port"); S.shot = "30_story_port"; break;
		case 31: ui_go("tavern"); S.shot = "31_story_tavern"; break;
		case 35: theme_set("darkwood"); ui_go("port"); S.shot = "35_dark_port"; break;
		case 36: ui_go("tavern"); S.shot = "36_dark_tavern"; break;
		case 37: ui_go("market"); S.shot = "37_dark_market"; break;
		case 38: global.G.ship.hp = floor(ship_max_hp() * 0.4); combat_start("pirate_schooner", false, 2); for (var i = 0; i < 20; i++) combat_update(0.1); if (array_length(global.C.allies) > 1) global.C.view = 1; S.shot = "38_dark_combat"; S.wait = 3; break;
		case 39:
			ui_go("map"); S.shot = "39_dark_map";
			var _sp = map_info_spot(port_def());
			st_assert(port_open("coralhaven") ? _sp[1] != 18 : true, "map box avoids Coralhaven (" + string(_sp[0]) + "," + string(_sp[1]) + ")");
			break;
		case 40: global.UI.dialogs = []; ui_dialog("barkeep", "Dark wood dialog test with a generated barkeep.", "Fine"); S.shot = "40_dark_dialog"; break;
		case 41: theme_set("storybook"); ui_go("journal"); S.shot = "41_story_journal"; break;
		case 42: ui_go("title"); global.UI.settings_open = true; S.shot = "42_settings"; break;
		case 43:
			global.UI.settings_open = false;
			i18n_set("en");
			st_assert(tr("Back") == "Back" && global.D.goods.fish.name == "Salt Fish", "English switch reloads data");
			ui_go("market"); S.shot = "43_en_market";
			break;
		// README screenshots (English, Storybook): copied to docs/screenshots by tools/readme_shots.sh.
		case 44:
			// A fresh English campaign a few weeks in: some cash, cargo and a second ship.
			new_game("campaign", "vega");
			global.G.cash = 42000; global.G.t = 5;
			market_buy("sugar", 10); market_buy("cotton", 20);
			array_push(global.G.fleet, fleet_new_ship("schooner"));
			global.UI.dialogs = []; global.UI.toasts = []; ui_go("port"); S.shot = "readme_town"; S.wait = 4;
			break;
		case 45: global.UI.toasts = []; ui_go("market"); S.shot = "readme_market"; break;
		case 46: global.UI.toasts = []; global.UI.tavern_text = tavern_drink(); ui_go("tavern"); S.shot = "readme_tavern"; break;
		case 47: global.UI.toasts = []; global.UI.pending_mode = "campaign"; ui_go("newgame"); S.shot = "readme_captains"; break;
		case 48:
			global.UI.toasts = [];
			global.G.ship.hp = ship_max_hp();
			if (array_length(global.G.fleet) == 0) array_push(global.G.fleet, fleet_new_ship("schooner"));
			combat_start("pirate_brigantine", false, 2);
			for (var i = 0; i < 24; i++) combat_update(0.1);
			global.C.msg_t = 0;
			S.shot = "readme_battle"; S.wait = 2;
			break;
		case 49: global.UI.toasts = []; ui_go("map"); S.shot = "readme_map"; break;
		case 50:
			i18n_set("es");
			st_log("done, fails=" + string(S.fails));
			S.wait = 2;
			break;
		case 51:
			game_end();
			break;
	}
}

/// Satisfies one campaign goal the way a player would (used to walk the whole campaign).
function st_campaign_satisfy(_g) {
	var G = global.G;
	switch (_g.type) {
		case "talk":
			G.port = campaign_resolve(_g.port);
			campaign_on_visit(struct_get_or(_g, "building", "") != "" ? _g.building : "governor");
			break;
		case "have_good": cargo_add(_g.good, _g.amount, 1); campaign_check(); break;
		case "deliver":
			cargo_add(_g.good, _g.amount, 1);
			G.port = campaign_resolve(_g.port);
			campaign_check();
			break;
		case "deposit": G.bank += _g.amount; campaign_check(); break;
		case "cash": G.cash += _g.amount; campaign_check(); break;
		case "networth": G.bank += _g.amount; campaign_check(); break;
		case "repay": G.debt = 0; campaign_check(); break;
		case "combat": G.stats.wins += _g.wins; campaign_check(); break;
		case "sink": G.stats.sunk += _g.n; campaign_check(); break;
		case "arrive": G.port = campaign_resolve(_g.port); campaign_check(); break;
		case "npccombat":
			var _pl = voyage_plan(campaign_resolve(_g.port));
			st_assert(_pl.special_enemy == _g.enemy || _pl.storm == "lost", "voyage plans the scripted fight: " + _g.enemy);
			campaign_on_battle_won(_g.enemy);
			break;
	}
}

/// Simulates batches of random encounters at several levels and logs how much hull they cost.
function st_difficulty_sim() {
	var G = global.G;
	var _setups = [[0, "sloop"], [2, "schooner"], [4, "brigantine"], [6, "barque"], [9, "frigate"]];
	var _keep = { ship: G.ship, fleet: G.fleet, items: G.items, level: G.level, cash: G.cash };
	G.items = []; G.fleet = [];
	for (var k = 0; k < array_length(_setups); k++) {
		var _lost = 0, _losses = 0, _n = 16, _time = 0, _packs = 0;
		for (var r = 0; r < _n; r++) {
			G.level = _setups[k][0];
			var d = variable_struct_get(global.D.pships, _setups[k][1]);
			G.ship = { type: d.id, name: "Sim", hp: d.hp, guns: d.guns, upgrades: [], ammo: { firepot: 0, chains: 0, bomb: 0 } };
			combat_start(pick_enemy(), false);
			if (array_length(global.C.enemies) > 1) _packs++;
			var C = global.C, _t = 0;
			while (C.result == "" && _t < 300) { combat_update(0.1); _t += 0.1; }
			_time += _t;
			if (C.result == "lost") _losses++;
			_lost += 1 - max(0, global.C.allies[0].hp) / d.hp;
		}
		st_log("difficulty L" + string(_setups[k][0]) + " " + _setups[k][1] + ": avg hull lost " + string(round(100 * _lost / _n)) + "%, defeats " + string(_losses) + "/" + string(_n) + ", packs " + string(_packs) + ", avg " + string(round(_time / _n)) + "s");
	}
	G.ship = _keep.ship; G.fleet = _keep.fleet; G.items = _keep.items; G.level = _keep.level; G.cash = _keep.cash;
	global.UI.dialogs = [];
}
