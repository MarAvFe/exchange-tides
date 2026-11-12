// ===== Screens =============================================================================
// Every screen is a function drawing itself and handling its own buttons (immediate mode).

function screens_draw(_dt) {
	switch (global.UI.screen) {
		case "title":    screen_title(); break;
		case "newgame":  screen_newgame(); break;
		case "port":     screen_port(); break;
		case "market":   screen_market(); break;
		case "bank":     screen_bank(); break;
		case "lender":   screen_lender(); break;
		case "shipyard": screen_shipyard(); break;
		case "tavern":   screen_tavern(); break;
		case "governor": screen_governor(); break;
		case "curio":    screen_curio(); break;
		case "map":      screen_map(); break;
		case "sailing":  screen_sailing(_dt); break;
		case "combat":   combat_draw(); break;
		case "journal":  screen_journal(); break;
		case "help":     screen_help(); break;
		case "saves":    screen_saves(); break;
		case "fleet":    screen_fleet(); break;
		case "victory":  screen_end(true); break;
		case "gameover": screen_end(false); break;
	}
}

function screens_step(_dt) {
	var _s = global.UI.screen;
	if (_s == "combat" && array_length(global.UI.dialogs) == 0) combat_update(_dt);
	if (keyboard_check_pressed(vk_escape) && array_length(global.UI.dialogs) == 0) {
		if (_s == "market" || _s == "bank" || _s == "lender" || _s == "shipyard" || _s == "tavern"
			|| _s == "governor" || _s == "curio" || _s == "map" || _s == "journal" || _s == "fleet") ui_go("port");
		else if (_s == "help" || _s == "newgame") ui_go(global.G == undefined ? "title" : "port");
		else if (_s == "saves") ui_go(global.UI.save_mode == "save" ? "port" : "title");
	}
}

// ---- shared frame -------------------------------------------------------------------------
function draw_backdrop(_dark = 0.55) {
	draw_spr("worldmap", 640, 360, 1);
	draw_set_alpha(_dark); draw_set_colour(make_colour_rgb(10, 20, 30)); draw_rectangle(0, 0, 1280, 720, false); draw_set_alpha(1);
}

function draw_sidebar() {
	var G = global.G;
	var c = captain_def();
	ui_panel(16, 16, 300, 688);
	draw_spr(portrait_or_fallback(c), 166, 120, 0.9);
	ui_portrait_frame(166, 120, 0.9);
	ui_text(166, 208, trf("{0} {1}", c.title, c.name), 1.15, UI_INK, fa_center, fa_top, 270);
	ui_text(166, 236, date_name(G.t), 0.95, UI_ACCENT, fa_center, fa_top, 270);
	var _y = 266;
	var _rows = [
		["Cash", fmt_money(G.cash)], ["Bank", fmt_money(G.bank)], ["Debt", fmt_money(G.debt)],
		["Net worth", fmt_money(net_worth())], ["Level", string(G.level)],
	];
	for (var i = 0; i < array_length(_rows); i++) {
		ui_text(40, _y, _rows[i][0], 1.1, UI_INK, fa_left, fa_top, 130);
		ui_text(292, _y, _rows[i][1], 1.1, (_rows[i][0] == "Debt" && G.debt > 0) ? UI_BAD : UI_INK, fa_right, fa_top, 150);
		_y += 25;
	}
	_y += 6;
	// Fleet summary: click to open the ship & cargo screen.
	var _hov = ui_hover(30, _y - 4, 272, 112);
	if (_hov) { draw_set_alpha(0.25); draw_set_colour(UI_GOLD); draw_roundrect_ext(30, _y - 4, 302, _y + 108, 10, 10, false); draw_set_alpha(1); }
	var _n = fleet_size();
	ui_text(40, _y, trf("{0} ({1})", G.ship.name, ship_def().name) + (_n > 1 ? trn(_n - 1, "  +{0} ship", "  +{0} ships") : ""), 1.05, UI_INK, fa_left, fa_top, 252); _y += 30;
	ui_bar(40, _y, 252, 18, G.ship.hp / ship_max_hp(), make_colour_rgb(70, 150, 90), trf("Hull {0}/{1}", G.ship.hp, ship_max_hp())); _y += 27;
	ui_bar(40, _y, 252, 18, cargo_used() / max(1, cargo_capacity()), make_colour_rgb(170, 130, 60), trf("Hold {0}/{1}", cargo_used(), cargo_capacity())); _y += 27;
	ui_text(40, _y, trf("Guns {0}   Fire {1}  Chain {2}  Keg {3}", G.ship.guns, G.ship.ammo.firepot, G.ship.ammo.chains, G.ship.ammo.bomb), 1, UI_INK, fa_left, fa_top, 252); _y += 30;
	if (_hov && global.UI.click) { global.UI.click = false; ui_go("fleet"); }
	// cargo list
	var _ids = variable_struct_get_names(G.cargo);
	for (var i = 0; i < array_length(_ids) && i < 7; i++) {
		var _g = variable_struct_get(global.D.goods, _ids[i]);
		draw_spr("good_" + _ids[i], 52, _y + 10, 0.32);
		ui_text(70, _y + 2, trf("{0} x{1}", _g.name, variable_struct_get(G.cargo, _ids[i]).qty), 1, UI_INK, fa_left, fa_top, 220);
		_y += 22;
	}
	if (array_length(_ids) > 7) ui_text(70, _y + 2, trf("...and {0} more", array_length(_ids) - 7), 0.9, UI_ACCENT);
}

function draw_objective_bar() {
	var G = global.G;
	ui_panel(336, 610, 928, 94, make_colour_rgb(230, 218, 186));
	ui_text(356, 616, "Objective", 1.1, UI_ACCENT);
	ui_text(456, 616, campaign_objective_text(), 1.1, UI_INK, fa_left, fa_top, 790);   // one line, same baseline as its label
	var _nc = array_length(G.contracts);
	if (_nc > 0) {
		var c = G.contracts[0];
		for (var i = 1; i < _nc; i++) if (G.contracts[i].due < c.due) c = G.contracts[i];
		ui_text(356, 642, trf("Contracts {0}/{1}:  next due  {2} {3}", _nc, CONTRACTS_MAX, contract_text(c), contract_due_text(c)), 0.95, UI_WARN, fa_left, fa_top, 890);
	}
	if (array_length(G.log) > 0) ui_text(356, 664, "> " + G.log[0].text, 0.95, UI_MUTED, fa_left, fa_top, 890);
}

function building_header(_title, _npc, _who = "") {
	draw_backdrop();
	draw_sidebar();
	ui_panel(336, 16, 928, 680);
	npc_draw_any(_npc, 420, 116, 0.85);
	ui_portrait_frame(420, 116, 0.85);
	ui_text(500, 40, _title, 2.2, UI_INK, fa_left, fa_top, 590);
	ui_text(500, 86, (_who != "" ? _who : trf("{0} of {1}", npc_display_name(_npc), port_def().name)), 1.2, UI_ACCENT, fa_left, fa_top, 600);
	if (ui_button(1110, 36, 130, 44, "Back")) ui_go("port");
}

// ---- title & new game ---------------------------------------------------------------------
function screen_title() {
	var U = global.UI;
	draw_spr("title", 640, 360, 1);
	ui_text(643, 63, global.D.config.title, 4, c_black, fa_center);
	ui_text(640, 60, global.D.config.title, 4, c_white, fa_center);
	ui_text(642, 172, "A merchant's war on the trade winds", 1.4, c_black, fa_center);
	ui_text(640, 170, "A merchant's war on the trade winds", 1.4, make_colour_rgb(255, 230, 190), fa_center);
	var _x = 1000, _y = 236;
	var _last = settings_get("last_save", "autosave.json");
	if (!file_exists(_last)) _last = "autosave.json";
	// Continue: the big green button, with the save it resumes written underneath.
	var _info = file_exists(_last) ? save_peek(_last) : undefined;
	if (ui_button(_x - 20, _y - 6, 280, 74, "Continue", _info != undefined, make_colour_rgb(40, 130, 90))) { if (load_game(_last)) ui_go("port"); }
	if (_info != undefined) {
		var _sub = _info.who + "  -  " + _info.date;
		ui_text(_x + 121, _y + 80, _sub, 0.85, c_black, fa_center, fa_top, 276);
		ui_text(_x + 120, _y + 79, _sub, 0.85, make_colour_rgb(255, 240, 210), fa_center, fa_top, 276);
	}
	_y += 110;
	if (ui_button(_x, _y, 240, 48, "New Campaign")) { U.pending_mode = "campaign"; ui_go("newgame"); }
	if (ui_button(_x, _y + 56, 240, 48, "Free Trade")) { U.pending_mode = "free"; ui_go("newgame"); }
	if (ui_button(_x, _y + 112, 240, 48, "Load Game")) { U.save_mode = "load"; ui_go("saves"); }
	if (ui_button(_x, _y + 168, 240, 48, "How to Play")) ui_go("help");
	if (ui_button(_x, _y + 236, 116, 40, "Settings", true, make_colour_rgb(70, 90, 110))) U.settings_open = true;
	if (ui_button(_x + 124, _y + 236, 116, 40, "Quit", true, make_colour_rgb(120, 60, 60))) game_end();
	ui_text(21, 701, "Music: Kevin MacLeod (incompetech.com), CC BY 4.0", 0.85, c_black, fa_left, fa_bottom);
	ui_text(20, 700, "Music: Kevin MacLeod (incompetech.com), CC BY 4.0", 0.85, make_colour_rgb(230, 220, 200), fa_left, fa_bottom);
	if (struct_get_or(U, "settings_open", false)) screen_settings();
}

/// Settings panel over the title screen: music, visual style and language (saved at once).
function screen_settings() {
	var U = global.UI;
	draw_set_alpha(0.55); draw_set_colour(c_black); draw_rectangle(0, 0, 1280, 720, false); draw_set_alpha(1);
	ui_panel(390, 150, 500, 400);
	ui_text(640, 168, "Settings", 2.2, UI_INK, fa_center);
	var _rows = [["Music", music_enabled() ? tr("On") : tr("Off")], ["Style", tr(global.THEME.label)], ["Language", i18n_name()]];
	for (var i = 0; i < 3; i++) {
		var _ry = 260 + i * 76;
		ui_text(430, _ry + 22, _rows[i][0], 1.3, UI_INK, fa_left, fa_middle, 190);
		if (ui_button(630, _ry, 220, 46, _rows[i][1], true, make_colour_rgb(110, 80, 50))) {
			switch (i) {
				case 0: music_toggle(); break;
				case 1: theme_toggle(); break;
				case 2:
					var _l = i18n_langs(), _k = 0;
					for (var j = 0; j < array_length(_l); j++) if (_l[j][0] == global.LANG) _k = j;
					i18n_set(_l[(_k + 1) mod array_length(_l)][0]);
					break;
			}
		}
	}
	if (ui_button(540, 486, 200, 46, "Done") || keyboard_check_pressed(vk_escape)) U.settings_open = false;
}

function screen_newgame() {
	draw_backdrop(0.65);
	var _caps = global.D.chars.captains;
	ui_text(640, 24, global.UI.pending_mode == "campaign" ? tr("Choose your captain - Campaign") : tr("Choose your captain - Free Trade"), 2.2, c_white, fa_center);
	var _n = array_length(_caps);
	var _cols = (_n > 4) ? 3 : _n;
	var _rows = ceil(_n / _cols);
	var _w = (_cols == 3) ? 396 : 280, _gap = 16;
	var _h = (_rows > 1) ? 272 : 560;
	var _x0 = 640 - (_cols * _w + (_cols - 1) * _gap) / 2;
	for (var i = 0; i < _n; i++) {
		var c = _caps[i];
		var _x = _x0 + (i mod _cols) * (_w + _gap);
		var _y = 84 + (i div _cols) * (_h + 12);
		ui_panel(_x, _y, _w, _h);
		var _perk = variable_struct_get(global.D.items, c.perk);
		if (_rows > 1) {
			// Compact card: portrait left, details right.
			draw_spr(portrait_or_fallback(c), _x + 78, _y + 96, 0.72);
			ui_portrait_frame(_x + 78, _y + 96, 0.72);
			var _tx = _x + 152, _tw = _w - 168;
			// Right column: name, story, perk, then where you start and what is closed to you.
			// Left column: portrait with the Set sail button under it (never covers any text).
			ui_text(_tx, _y + 12, c.name, 1.3, UI_INK, fa_left, fa_top, _tw);
			ui_text_box(_tx, _y + 50, _tw, c.bio, 0.9, UI_INK, 62);
			ui_text(_tx, _y + 116, trf("Perk: {0}", _perk.name), 0.95, UI_ACCENT, fa_left, fa_top, _tw);
			ui_text_box(_tx, _y + 138, _tw, item_effect_text(c.perk), 0.8, UI_MUTED, 24);
			ui_text(_tx, _y + 166, trf("Starts in {0} with a {1}", port_def(c.port).name, variable_struct_get(global.D.pships, c.ship).name), 0.9, UI_INK, fa_left, fa_top, _tw);
			ui_text(_tx, _y + 185, trf("Cash {0}", fmt_money(c.cash)) + (c.debt > 0 ? trf("   Debt {0}", fmt_money(c.debt)) : ""), 0.9, UI_INK, fa_left, fa_top, _tw);
			if (global.UI.pending_mode == "campaign") ui_text_box(_tx, _y + 207, _tw, struct_get_or(c, "closed_reason", ""), 0.72, UI_BAD, 54);
			if (ui_button(_x + 16, _y + 184, 124, 40, "Set sail")) { new_game(global.UI.pending_mode, c.id); ui_go("port"); }
		} else {
			draw_spr(portrait_or_fallback(c), _x + _w / 2, _y + 110, 1);
			ui_portrait_frame(_x + _w / 2, _y + 110, 1);
			ui_text(_x + _w / 2, _y + 220, c.name, 1.3, UI_INK, fa_center, fa_top, _w - 30);
			ui_text_box(_x + 20, _y + 250, _w - 40, c.bio, 1, UI_INK, 96);
			ui_text(_x + 20, _y + 350, trf("Perk: {0}", _perk.name), 1, UI_ACCENT, fa_left, fa_top, _w - 40);
			ui_text_box(_x + 20, _y + 370, _w - 40, item_effect_text(c.perk), 1, UI_MUTED, 46);
			ui_text(_x + 20, _y + 420, trf("Starts in {0}", port_def(c.port).name), 1, UI_INK, fa_left, fa_top, _w - 40);
			ui_text(_x + 20, _y + 440, trf("Cash {0}", fmt_money(c.cash)) + (c.debt > 0 ? trf("   Debt {0}", fmt_money(c.debt)) : ""), 1, UI_INK, fa_left, fa_top, _w - 40);
			if (ui_button(_x + 40, _y + 490, _w - 80, 50, "Set sail")) { new_game(global.UI.pending_mode, c.id); ui_go("port"); }
		}
	}
	if (ui_button(40, 666, 160, 44, "Back")) ui_go("title");
}

// ---- save slots ---------------------------------------------------------------------------
function screen_saves() {
	var U = global.UI;
	var _save = (U.save_mode == "save");
	draw_backdrop(0.65);
	ui_panel(240, 40, 800, 640);
	ui_text(280, 60, _save ? "Save Game" : "Load Game", 2.2, UI_INK);
	if (ui_button(880, 66, 130, 44, "Back")) ui_go(_save ? "port" : "title");
	if (struct_get_or(U, "slot_cache", undefined) == undefined) {
		var _files = ["autosave.json"];
		for (var i = 1; i <= SAVE_SLOTS; i++) array_push(_files, "slot" + string(i) + ".json");
		if (file_exists("savegame.json")) array_push(_files, "savegame.json");   // saves from older versions
		U.slot_cache = [];
		for (var i = 0; i < array_length(_files); i++) array_push(U.slot_cache, { file: _files[i], info: save_peek(_files[i]) });
	}
	var _y = 130;
	for (var i = 0; i < array_length(U.slot_cache); i++) {
		var sl = U.slot_cache[i];
		var _auto = (sl.file == "autosave.json"), _old = (sl.file == "savegame.json");
		var _label = _auto ? tr("Autosave") : (_old ? tr("Old save") : trf("Slot {0}", i));
		draw_set_alpha(0.3); draw_set_colour(UI_PAPER_DARK); draw_roundrect_ext(270, _y, 1010, _y + 64, 10, 10, false); draw_set_alpha(1);
		ui_text(290, _y + 10, _label, 1.2, UI_ACCENT, fa_left, fa_top, 118);
		if (sl.info == undefined) ui_text(420, _y + 20, "- empty -", 1.1, UI_MUTED);
		else {
			ui_text(420, _y + 8, sl.info.who + "  -  " + tr(sl.info.mode), 1.1, UI_INK, fa_left, fa_top, 400);
			ui_text(420, _y + 34, sl.info.date + "  -  " + sl.info.where + "  -  " + fmt_money(sl.info.worth) + "  -  " + trn(sl.info.ships, "{0} ship", "{0} ships"), 0.95, UI_MUTED, fa_left, fa_top, 420);
		}
		if (_save) {
			if (!_auto && !_old && ui_button(860, _y + 12, 130, 40, sl.info == undefined ? "Save" : "Overwrite")) {
				save_game(sl.file);
				ui_toast(trf("Saved to {0}.", _label));
				ui_go("port");
			}
		} else if (ui_button(860, _y + 12, 130, 40, "Load", sl.info != undefined)) {
			if (load_game(sl.file)) ui_go("port");
		}
		_y += 74;
	}
}

// ---- port hub -----------------------------------------------------------------------------
// ---- market -------------------------------------------------------------------------------
function screen_market() {
	var G = global.G, D = global.D;
	building_header("Marketplace", "merchant");
	// Column headers: prices, then the two button groups. Each fits its column in any language.
	var _hs = 0.92;   // one size for every header so the row reads evenly
	ui_text(416, 204, "Good", _hs, UI_ACCENT, fa_left, fa_top, 110);
	ui_text(602, 204, "Buy", _hs, UI_ACCENT, fa_right, fa_top, 62);
	ui_text(676, 204, "Sell", _hs, UI_ACCENT, fa_right, fa_top, 62);
	ui_text(744, 204, "Hold", _hs, UI_ACCENT, fa_right, fa_top, 62);
	ui_text(812, 204, "Paid", _hs, UI_ACCENT, fa_right, fa_top, 62);
	ui_text(931, 204, "Buy (qty)", _hs, UI_ACCENT, fa_center, fa_top, 220);
	ui_text(1146, 204, "Sell (qty)", _hs, UI_ACCENT, fa_center, fa_top, 180);
	ui_text(1240, 150, trf("Free space: {0}", cargo_free()), 1.1, UI_INK, fa_right);
	var _y = 234;
	var _pm = variable_struct_get(G.portmeta, G.port);
	for (var i = 0; i < array_length(D.goods_list); i++) {
		var g = D.goods_list[i];
		var gs = variable_struct_get(G.goods, g.id);
		var _own = cargo_qty(g.id);
		if (!gs.unlocked && _own == 0) continue;
		var _price = buy_price(g.id);
		if (i mod 2 == 0) { draw_set_alpha(0.25); draw_set_colour(UI_PAPER_DARK); draw_rectangle(360, _y - 2, 1244, _y + 34, false); draw_set_alpha(1); }
		draw_spr("good_" + g.id, 388, _y + 16, 0.5);
		// Every cell is centred on the row's midline (_ym), the same line the buttons are centred on.
		var _ym = _y + 16;
		var _tag = "";
		if (port_is_contraband(G.port, g.id)) _tag = "OUTLAWED x2";
		else if (g.id == _pm.high_good && (G.t div WEEKS_PER_MONTH) == _pm.high_t) _tag = "IN DEMAND";
		else if (g.id == _pm.low_good && (G.t div WEEKS_PER_MONTH) == _pm.low_t) _tag = "GLUT";
		ui_text(416, _tag != "" ? _ym - 7 : _ym, g.name, 1.1, UI_INK, fa_left, fa_middle, 118);
		if (_tag != "") ui_text(416, _ym + 11, _tag, 0.7, UI_BAD, fa_left, fa_middle);
		ui_text(602, _ym, g.forsale ? fmt_num(_price) : "-", 1.05, UI_INK, fa_right, fa_middle, 64);
		ui_text(676, _ym, fmt_num(sell_price(g.id)), 1.05, UI_INK, fa_right, fa_middle, 64);
		ui_text(744, _ym, string(_own), 1.05, UI_INK, fa_right, fa_middle, 44);
		ui_text(812, _ym, _own > 0 ? fmt_num(variable_struct_get(G.cargo, g.id).paid) : "-", 1.05, UI_INK, fa_right, fa_middle, 66);
		var _can_buy = g.forsale && gs.unlocked && cargo_free() > 0 && G.cash >= _price;
		if (ui_button(820, _y, 64, 32, "Buy 1", _can_buy)) market_buy(g.id, 1);
		if (ui_button(890, _y, 70, 32, "Buy 10", _can_buy)) market_buy(g.id, 10);
		if (ui_button(966, _y, 76, 32, "Buy max", _can_buy)) market_buy(g.id, 9999);
		if (ui_button(1056, _y, 70, 32, "Sell 1", _own > 0, make_colour_rgb(150, 100, 40))) market_sell(g.id, 1);
		if (ui_button(1132, _y, 104, 32, "Sell all", _own > 0, make_colour_rgb(150, 100, 40))) market_sell(g.id, _own);
		_y += 37;
	}
	ui_text_box(380, 636, 840, "Prices change every month. Each port has one good in high demand and one in glut in certain months; the tavern hears about them. Outlawed goods sell for double, but customs may seize them when you arrive.", 0.9, UI_MUTED, 40);
}

// ---- bank & lender ------------------------------------------------------------------------
function screen_bank() {
	var G = global.G;
	building_header("Bank", "banker");
	var _rate = eff("bank_interest", 0.01) * 100;
	ui_text_box(500, 124, 720, trf("Savings earn {0}% interest every month and are safe from pirates.", string_format(_rate, 1, 1)), 1.2, UI_INK, 76);
	ui_text(380, 240, trf("Balance: {0}", fmt_money(G.bank)), 2, UI_INK);
	ui_text(380, 294, "Deposit", 1.2, UI_ACCENT);
	var _amts = [1000, 10000, 100000];
	for (var i = 0; i < 3; i++) if (ui_button(380 + i * 170, 330, 160, 46, fmt_num(_amts[i]), G.cash >= _amts[i])) { G.cash -= _amts[i]; G.bank += _amts[i]; campaign_check(); }
	if (ui_button(890, 330, 160, 46, "All", G.cash > 0)) { G.bank += G.cash; G.cash = 0; campaign_check(); }
	ui_text(380, 404, "Withdraw", 1.2, UI_ACCENT);
	for (var i = 0; i < 3; i++) if (ui_button(380 + i * 170, 440, 160, 46, fmt_num(_amts[i]), G.bank >= _amts[i], make_colour_rgb(150, 100, 40))) { G.bank -= _amts[i]; G.cash += _amts[i]; }
	if (ui_button(890, 440, 160, 46, "All", G.bank > 0, make_colour_rgb(150, 100, 40))) { G.cash += G.bank; G.bank = 0; }
}

function screen_lender() {
	var G = global.G;
	building_header("Moneylender", "lender");
	var _rate = eff("moneylender_interest", 0.1) * 100;
	var _max = max_loan();
	ui_text_box(500, 124, 720, trf("Loans cost {0}% interest per month, compounding. You may borrow up to {1} more.", string_format(_rate, 1, 1), fmt_money(_max)), 1.2, UI_INK, 76);
	ui_text(380, 240, trf("Debt: {0}", fmt_money(G.debt)), 2, G.debt > 0 ? UI_BAD : UI_INK);
	ui_text(380, 294, "Borrow", 1.2, UI_ACCENT);
	var _amts = [1000, 10000, 50000];
	for (var i = 0; i < 3; i++) if (ui_button(380 + i * 170, 330, 160, 46, fmt_num(_amts[i]), _max >= _amts[i], make_colour_rgb(150, 100, 40))) { G.cash += _amts[i]; G.debt += _amts[i]; }
	if (ui_button(890, 330, 160, 46, "Max", _max > 0, make_colour_rgb(150, 100, 40))) { G.cash += _max; G.debt += _max; }
	ui_text(380, 404, "Repay", 1.2, UI_ACCENT);
	for (var i = 0; i < 3; i++) if (ui_button(380 + i * 170, 440, 160, 46, fmt_num(_amts[i]), G.debt > 0 && G.cash >= min(_amts[i], G.debt))) { var _p = min(_amts[i], G.debt); G.cash -= _p; G.debt -= _p; campaign_check(); }
	if (ui_button(890, 440, 160, 46, "All", G.debt > 0 && G.cash > 0)) { var _p = min(G.cash, G.debt); G.cash -= _p; G.debt -= _p; campaign_check(); }
}

// ---- shipyard -----------------------------------------------------------------------------
// Pick a ship of your fleet (tabs), then repair, arm, refit, promote or sell it. Ships for sale
// can join the fleet (up to FLEET_MAX) or replace the selected ship as a trade-in.
function screen_shipyard() {
	var G = global.G, D = global.D, cfg = global.D.config, U = global.UI;
	building_header("Shipyard", "shipwright");
	var _all = fleet_all();
	var _sel = clamp(struct_get_or(U, "yard_sel", 0), 0, array_length(_all) - 1);
	U.yard_sel = _sel;
	// Fleet tabs.
	for (var i = 0; i < array_length(_all); i++) {
		var _s = _all[i];
		if (ui_button(500 + i * 146, 124, 140, 34, (i == 0 ? "* " : "") + _s.name, true, i == _sel ? make_colour_rgb(150, 100, 40) : make_colour_rgb(90, 110, 120))) U.yard_sel = i;
	}
	var S = fleet_get(_sel);
	var sd = ship_def_of(S);
	var _mhp = ship_max_hp_of(S);
	draw_spr(ship_sprite_hp(sd.sprite, S.hp / max(1, _mhp)), 470, 262, 0.62);
	ui_text(470, 318, sd.name + (_sel == 0 ? tr(" (flagship)") : ""), 1, UI_INK, fa_center, fa_top, 200);
	ui_text(470, 338, trf("HP {0}/{1}  Hold {2}", S.hp, _mhp, ship_cargo_of(S)), 0.95, UI_MUTED, fa_center, fa_top, 200);
	var _miss = max(0, _mhp - S.hp);
	var _rcost = _miss * cfg.repair_cost_per_hp;
	ui_text(600, 196, trf("Repairs: {0} damage", _miss), 1.0, UI_INK);
	if (ui_button(600, 224, 200, 38, trf("Repair {0}", fmt_money(_rcost)), _miss > 0 && G.cash >= _rcost)) { G.cash -= _rcost; S.hp = _mhp; }
	if (ui_button(810, 224, 150, 38, "Patch 10", _miss > 0 && G.cash >= min(10, _miss) * cfg.repair_cost_per_hp)) { var _h = min(10, _miss); G.cash -= _h * cfg.repair_cost_per_hp; S.hp += _h; }
	var _all_miss = 0;
	for (var i = 0; i < array_length(_all); i++) _all_miss += max(0, ship_max_hp_of(_all[i]) - _all[i].hp);
	if (array_length(_all) > 1 && ui_button(970, 224, 250, 38, trf("Repair fleet {0}", fmt_money(_all_miss * cfg.repair_cost_per_hp)), _all_miss > 0 && G.cash >= _all_miss * cfg.repair_cost_per_hp)) {
		G.cash -= _all_miss * cfg.repair_cost_per_hp;
		for (var i = 0; i < array_length(_all); i++) _all[i].hp = ship_max_hp_of(_all[i]);
	}
	ui_text(600, 270, trf("Cannons {0}/{1} (each uses 5 hold)", S.guns, sd.guns), 1.0, UI_INK);
	if (ui_button(600, 296, 200, 38, trf("Buy cannon {0}", fmt_num(cfg.cannon_buy)), S.guns < sd.guns && G.cash >= cfg.cannon_buy && cargo_free() >= 5)) { G.cash -= cfg.cannon_buy; S.guns += 1; }
	if (ui_button(810, 296, 150, 38, "Sell cannon", S.guns > 0, make_colour_rgb(150, 100, 40))) { G.cash += cfg.cannon_sell; S.guns -= 1; }
	if (_sel > 0) {
		if (ui_button(970, 272, 250, 30, "Make flagship", true, make_colour_rgb(46, 110, 130))) { fleet_make_flagship(_sel - 1); U.yard_sel = 0; }
		var _val = ship_value(S);
		var _fits = cargo_used() - S.guns * 5 <= cargo_capacity() - ship_cargo_of(S);
		if (ui_button(970, 306, 250, 30, trf("Sell ship {0}", fmt_num(_val)), _fits, make_colour_rgb(150, 70, 50))) {
			G.cash += _val; log_add(trf("Sold the {0} for {1}.", S.name, fmt_money(_val)));
			fleet_remove(_sel); U.yard_sel = 0;
		}
	}
	// Ammo (shared by the fleet; fired from the flagship).
	var _ax = 600;
	for (var i = 0; i < array_length(D.ships.ammo); i++) {
		var a = D.ships.ammo[i];
		if (a.price <= 0) continue;
		if (ui_button(_ax, 346, 200, 36, trf("{0} {1} ({2})", a.name, fmt_num(a.price), variable_struct_get(G.ship.ammo, a.id)), G.cash >= a.price)) {
			G.cash -= a.price;
			variable_struct_set(G.ship.ammo, a.id, variable_struct_get(G.ship.ammo, a.id) + 1);
		}
		_ax += 210;
	}
	// Refits for the selected ship.
	ui_text(380, 390, trf("Refits for the {0}", S.name), 1.05, UI_ACCENT, fa_left, fa_top, 600);
	var _ux = 380;
	for (var i = 0; i < array_length(D.items_list); i++) {
		var it = D.items_list[i];
		if (it.kind != "upgrade") continue;
		var _owned = arr_contains(S.upgrades, it.id);
		var _rp = refit_price(it, S);
		if (ui_button(_ux, 418, 205, 36, (_owned ? trf("Fitted: {0}", it.name) : it.name), !_owned && G.cash >= _rp)) { G.cash -= _rp; array_push(S.upgrades, it.id); }
		ui_text_box(_ux, 458, 200, fmt_money(_rp) + " - " + item_effect_text(it.id), 0.85, UI_MUTED, 34);
		_ux += 215;
	}
	// Ships for sale: this yard's own small stock (yard_stock), one of each.
	var _room = fleet_size() < FLEET_MAX;
	var _stock = yard_stock(G.port);
	ui_text(380, 498, trf("In the yard  -  Buy adds it to your fleet ({0}/{1}); Trade-in replaces the {2}'s hull ({3}) and keeps its cannons", fleet_size(), FLEET_MAX, S.name, fmt_money(floor(sd.price * 0.5))), 0.95, UI_INK, fa_left, fa_top, 860);
	if (array_length(_stock) == 0) ui_text(380, 540, "Nothing on the slipway. New hulls arrive every couple of months.", 1, UI_MUTED);
	for (var i = 0; i < array_length(_stock); i++) {
		var s = variable_struct_get(D.pships, _stock[i]);
		var _x = 380 + i * 430, _y = 522;
		draw_set_alpha(0.3); draw_set_colour(UI_PAPER_DARK); draw_roundrect_ext(_x - 6, _y - 4, _x + 414, _y + 150, 10, 10, false); draw_set_alpha(1);
		draw_spr(s.sprite, _x + 70, _y + 66, 0.5);
		ui_text(_x + 150, _y + 4, s.name, 1.2, UI_INK, fa_left, fa_top, 250);
		ui_text(_x + 150, _y + 32, trf("Hull {0}   Guns {1}   Hold {2}", s.hp, s.guns, s.cargo), 0.9, UI_MUTED, fa_left, fa_top, 250);
		ui_text(_x + 150, _y + 52, trf("Comes with {0} cannons", s.guns div 2), 0.85, UI_MUTED, fa_left, fa_top, 250);
		if (ui_button(_x + 150, _y + 80, 124, 36, trf("Buy {0}", fmt_num(s.price)), _room && G.cash >= s.price)) {
			G.cash -= s.price;
			var _ns = fleet_new_ship(s.id);
			array_push(G.fleet, _ns);
			array_delete(_stock, i, 1);
			log_add(trf("Bought the {0} {1}. It joins your fleet.", s.name, _ns.name));
			level_update();
			break;
		}
		var _cost = s.price - floor(sd.price * 0.5);   // the hull is traded in; cannons move across (excess ones are sold)
		var _ok = s.id != S.type && G.cash >= _cost && cargo_used() - S.guns * 5 + min(S.guns, s.guns) * 5 <= cargo_capacity() - ship_cargo_of(S) + s.cargo;
		if (ui_button(_x + 280, _y + 80, 124, 36, trf("Trade {0}", fmt_num(max(0, _cost))), _ok, make_colour_rgb(150, 100, 40))) {
			G.cash -= _cost;
			G.cash += max(0, S.guns - s.guns) * cfg.cannon_sell;
			S.type = s.id; S.guns = min(S.guns, s.guns); S.upgrades = []; S.hp = ship_max_hp_of(S);
			array_delete(_stock, i, 1);
			log_add(trf("Traded in for a {0}.", s.name));
			level_update();
			break;
		}
	}
}

/// Each shipyard has 1-2 hulls for sale (one of each type), restocked every other month.
function yard_stock(_pid) {
	var G = global.G, D = global.D;
	if (!variable_struct_exists(G, "yards")) G.yards = {};
	var _m = G.t div WEEKS_PER_MONTH;
	var _yd = struct_get_or(G.yards, _pid, undefined);
	if (_yd == undefined || _m >= _yd.m + 2) {
		var _cands = [];
		for (var i = 0; i < array_length(D.ships.player); i++) {
			var s = D.ships.player[i];
			if (s.level <= G.level + 1 && s.level >= G.level - 4) array_push(_cands, s.id);
		}
		if (array_length(_cands) == 0) array_push(_cands, D.ships.player[0].id);
		arr_shuffle(_cands);
		var _n = min(array_length(_cands), choose(1, 2, 2));
		var _list = [];
		for (var i = 0; i < _n; i++) array_push(_list, _cands[i]);
		_yd = { m: _m, stock: _list };
		variable_struct_set(G.yards, _pid, _yd);
	}
	return _yd.stock;
}

/// Each tavern has 2-3 of the crew hires on offer, changing every other month.
function tavern_stock(_pid) {
	var G = global.G, D = global.D;
	if (!variable_struct_exists(G, "taverns")) G.taverns = {};
	var _m = G.t div WEEKS_PER_MONTH;
	var _tv = struct_get_or(G.taverns, _pid, undefined);
	if (_tv == undefined || _m >= _tv.m + 2) {
		var _all = [];
		for (var i = 0; i < array_length(D.items_list); i++) if (D.items_list[i].kind == "hire") array_push(_all, D.items_list[i].id);
		arr_shuffle(_all);
		var _list = [];
		for (var i = 0; i < min(array_length(_all), choose(2, 3, 3)); i++) array_push(_list, _all[i]);
		_tv = { m: _m, stock: _list };
		variable_struct_set(G.taverns, _pid, _tv);
	}
	return _tv.stock;
}

/// Refits cost more on bigger ships (scaled from the sloop's base price).
function refit_price(_it, _s) {
	var _k = power(ship_def_of(_s).price / global.D.pships.sloop.price, 0.6);
	return round(_it.price * _k / 100) * 100;
}

// ---- ship & cargo -------------------------------------------------------------------------
function screen_fleet() {
	var G = global.G, D = global.D;
	draw_backdrop();
	ui_panel(24, 16, 1232, 688);
	ui_text(56, 30, "Fleet & Cargo", 2.2, UI_INK);
	if (ui_button(1100, 34, 130, 44, "Back")) ui_go(global.UI.screen_prev == "map" ? "map" : "port");
	ui_text(380, 50, trf("{0}/{1} ships   Hold {2}/{3}   Fleet value {4}", fleet_size(), FLEET_MAX, cargo_used(), cargo_capacity(), fmt_money(fleet_value())), 1.1, UI_ACCENT, fa_left, fa_top, 700);
	var _all = fleet_all();
	var _w = 236;
	for (var i = 0; i < array_length(_all); i++) {
		var S = _all[i], sd = ship_def_of(S);
		var _x = 44 + i * (_w + 6), _y = 92;
		draw_set_alpha(0.3); draw_set_colour(UI_PAPER_DARK); draw_roundrect_ext(_x, _y, _x + _w, _y + 300, 10, 10, false); draw_set_alpha(1);
		draw_spr(ship_sprite_hp(sd.sprite, S.hp / max(1, ship_max_hp_of(S))), _x + _w / 2, _y + 70, 0.5);
		ui_text(_x + _w / 2, _y + 128, (i == 0 ? trf("Flagship: {0}", S.name) : S.name), 1.1, UI_INK, fa_center, fa_top, _w - 16);
		ui_text(_x + _w / 2, _y + 152, sd.name, 0.95, UI_ACCENT, fa_center);
		var _m = ship_max_hp_of(S);
		ui_bar(_x + 14, _y + 178, _w - 28, 16, S.hp / _m, make_colour_rgb(70, 150, 90), trf("Hull {0}/{1}", S.hp, _m));
		var _r = [["Cannons", string(S.guns) + "/" + string(sd.guns)], ["Hold", string(ship_cargo_of(S))], ["Reload", string_format(sd.reload * 2, 1, 1) + "s"], ["Value", fmt_money(ship_value(S))]];
		for (var k = 0; k < 4; k++) {
			ui_text(_x + 14, _y + 202 + k * 20, _r[k][0], 0.9, UI_INK);
			ui_text(_x + _w - 14, _y + 202 + k * 20, _r[k][1], 0.9, UI_INK, fa_right);
		}
		var _up = "";
		for (var k = 0; k < array_length(S.upgrades); k++) _up += (k > 0 ? ", " : "") + variable_struct_get(D.items, S.upgrades[k]).name;
		ui_text(_x + 14, _y + 282, _up == "" ? "No refits" : _up, 0.8, UI_MUTED, fa_left, fa_top, _w - 28);
	}
	// Cargo manifest.
	var _y = 410;
	ui_text(56, _y, "Cargo", 1.3, UI_ACCENT);
	var _hdr = ["Good", "Qty", "Avg paid", "Price here", "Value", "Profit"];
	var _cx = [56, 300, 400, 520, 640, 760];
	for (var k = 0; k < 6; k++) ui_text(_cx[k] + (k > 0 ? 80 : 0), _y + 32, _hdr[k], 0.95, UI_ACCENT, k > 0 ? fa_right : fa_left, fa_top, k > 0 ? 96 : 200);
	_y += 56;
	var _ids = variable_struct_get_names(G.cargo);
	if (array_length(_ids) == 0) ui_text(56, _y, "The hold is empty.", 1, UI_MUTED);
	for (var i = 0; i < array_length(_ids) && i < 8; i++) {
		var c = variable_struct_get(G.cargo, _ids[i]);
		var g = variable_struct_get(D.goods, _ids[i]);
		var _p = sell_price(_ids[i]);
		draw_spr("good_" + _ids[i], 66, _y + 9, 0.3);
		ui_text(84, _y, g.name, 0.95, UI_INK, fa_left, fa_top, 200);
		ui_text(380, _y, string(c.qty), 0.95, UI_INK, fa_right);
		ui_text(480, _y, fmt_num(c.paid), 0.95, UI_INK, fa_right);
		ui_text(600, _y, fmt_num(_p), 0.95, UI_INK, fa_right);
		ui_text(720, _y, fmt_num(_p * c.qty), 0.95, UI_INK, fa_right);
		var _pl = (_p - c.paid) * c.qty;
		ui_text(840, _y, (_pl >= 0 ? "+" : "") + fmt_num(_pl), 0.95, _pl >= 0 ? UI_GOOD : UI_BAD, fa_right);
		_y += 24;
	}
	// Stores and crew.
	var _x2 = 900;
	ui_text(_x2, 410, "Stores", 1.3, UI_ACCENT);
	ui_text(_x2, 444, trf("Fire Pots {0}   Chain Shot {1}   Kegs {2}", G.ship.ammo.firepot, G.ship.ammo.chains, G.ship.ammo.bomb), 0.95, UI_INK, fa_left, fa_top, 330);
	ui_text(_x2, 474, "Aboard", 1.1, UI_ACCENT);
	var _yy = 498;
	var _shown = 0;
	for (var i = 0; i < array_length(G.items); i++) {
		if (_yy > 640) { ui_text(_x2, _yy, trf("...and {0} more (see the journal)", array_length(G.items) - _shown), 0.85, UI_MUTED); _yy += 22; break; }
		_shown++;
		var it = variable_struct_get(D.items, G.items[i].id);
		var _who = struct_get_or(G.items[i], "who", "");
		ui_text(_x2, _yy, (_who != "" ? _who + ", " : "") + it.name + (G.items[i].months > 0 ? trf(" ({0} mo left)", G.items[i].months) : ""), 0.85, UI_INK, fa_left, fa_top, 330);
		_yy += 21;
	}
	for (var i = 0; i < array_length(G.contracts) && _yy < 660; i++) {
		var c = G.contracts[i];
		if (c.kind != "passenger") continue;
		ui_text(_x2, _yy, trf("Passenger {0} for {1}", c.who.name, port_def(c.port).name), 0.9, UI_WARN, fa_left, fa_top, 330);
		_yy += 22;
	}
}

function fleet_value() {
	var _all = fleet_all(), _v = 0;
	for (var i = 0; i < array_length(_all); i++) _v += ship_value(_all[i]);
	return _v;
}

// ---- tavern / governor / curio -----------------------------------------------------------
function screen_tavern() {
	var G = global.G, D = global.D;
	building_header("Tavern", "barkeep");
	var _cost = ceil(eff("alehouse_drink_prices", 25));
	ui_panel(500, 130, 720, 84, make_colour_rgb(236, 222, 190));
	ui_text_box(516, 140, 690, global.UI.tavern_text, 1.15, UI_INK, 64);
	if (ui_button(500, 226, 280, 42, trf("Buy a round ({0})", fmt_num(_cost)), G.cash >= _cost)) global.UI.tavern_text = tavern_drink();
	ui_text(380, 280, "Looking for a berth", 1.25, UI_ACCENT);
	var _y = 316;
	var _avail = tavern_stock(G.port);
	if (array_length(_avail) == 0) ui_text(380, _y, "Nobody looking for a berth this month.", 1, UI_MUTED);
	for (var i = 0; i < array_length(D.items_list); i++) {
		var it = D.items_list[i];
		if (it.kind != "hire" || !arr_contains(_avail, it.id)) continue;
		// Each crew member for hire is a person of this port (rolled once, then kept).
		var _who = npc_get(G.port, "crew", it.id);
		var _has = item_has(it.id);
		if (_has) {   // already aboard: show the person you actually hired, wherever they came from
			for (var k = 0; k < array_length(G.items); k++) if (G.items[k].id == it.id && is_struct(struct_get_or(G.items[k], "who_npc", undefined))) _who = G.items[k].who_npc;
		}
		draw_set_alpha(0.25); draw_set_colour(UI_PAPER_DARK); draw_roundrect_ext(370, _y - 2, 1230, _y + 50, 8, 8, false); draw_set_alpha(1);
		npc_draw(_who, 404, _y + 24, 0.25);
		ui_portrait_frame(404, _y + 24, 0.25);
		ui_text(436, _y + 2, _who.name, 1.1, UI_INK, fa_left, fa_top, 210);
		ui_text(436, _y + 26, it.name, 0.9, UI_ACCENT, fa_left, fa_top, 210);
		var _fx = item_effect_text(it.id);
		ui_text_box(656, _y + 4, 370, _fx + ". " + trf("{0}-month contract.", it.months) + " " + it.desc, 0.85, UI_MUTED, 44);
		if (ui_button(1040, _y + 6, 180, 36, _has ? tr("Aboard") : trf("Hire {0}", fmt_num(it.price)), !_has && G.cash >= it.price)) {
			G.cash -= it.price; item_add(it.id);
			G.items[array_length(G.items) - 1].who = _who.name;
			G.items[array_length(G.items) - 1].who_npc = _who;
			log_add(trf("{0} joins the crew as {1}.", _who.name, it.name));
		}
		_y += 56;
	}
}

// Each port's governor has a name and offers contracts; campaign news only where it concerns them.
function screen_governor() {
	var G = global.G;
	var gv = governor_of(G.port);
	building_header("Governor's Mansion", "governor", trf("{0} of {1}", gv.name, port_def().name));
	ui_text_box(500, 120, 720, gv.greeting, 1.1, UI_INK, 84);
	var _y = 222;
	var _goal = campaign_current_goal();
	if (_goal != undefined && variable_struct_exists(_goal, "port") && campaign_resolve(_goal.port) == G.port) {
		ui_text_box(380, _y, 840, trf("\"I hear your business brings you here: {0}\"", campaign_objective_text()), 1, UI_ACCENT, 44);
		_y += 50;
	}
	ui_text(380, _y, "Contracts on offer", 1.3, UI_ACCENT);
	ui_text(1220, _y + 4, trf("Active {0}/{1}", array_length(G.contracts), CONTRACTS_MAX), 1, UI_INK, fa_right);
	_y += 34;
	var _offers = contract_offers(G.port);
	if (array_length(_offers) == 0) ui_text(380, _y, "Nothing more this month. Come back next month.", 1, UI_MUTED);
	for (var i = 0; i < array_length(_offers); i++) {
		var c = _offers[i];
		draw_set_alpha(0.3); draw_set_colour(UI_PAPER_DARK); draw_roundrect_ext(370, _y - 4, 1230, _y + 52, 10, 10, false); draw_set_alpha(1);
		ui_text(384, _y + 2, contract_text(c), 1.1, UI_INK, fa_left, fa_top, 640);
		ui_text(384, _y + 26, contract_due_text(c) + "   " + trf("Reward {0}", fmt_money(c.reward)), 0.95, UI_WARN, fa_left, fa_top, 640);
		if (ui_button(1060, _y + 4, 160, 40, "Accept", array_length(G.contracts) < CONTRACTS_MAX)) { contract_accept(G.port, i); break; }
		_y += 62;
	}
	_y += 10;
	var _mine = 0;
	for (var i = 0; i < array_length(G.contracts); i++) if (G.contracts[i].from == G.port) _mine++;
	if (_mine > 0) {
		ui_text(380, _y, trf("Your work for {0}", gv.name), 1.2, UI_ACCENT); _y += 30;
		for (var i = 0; i < array_length(G.contracts); i++) {
			var c = G.contracts[i];
			if (c.from != G.port) continue;
			ui_text(384, _y, contract_text(c) + "  " + contract_due_text(c), 1, UI_INK, fa_left, fa_top, 840);
			_y += 24;
		}
	}
	ui_text(380, 660, trf("Voyages {0}   Battles won {1}   Ships sunk {2}   Contracts done {3}", G.stats.voyages, G.stats.wins, G.stats.sunk, G.stats.contracts), 0.95, UI_MUTED, fa_left, fa_top, 840);
}

function screen_curio() {
	var G = global.G, D = global.D;
	building_header("Curio Dealer", "curio");
	ui_text_box(500, 124, 720, "Charms, trinkets and things that should not work but do. Their effects last as long as you carry them.", 1.2, UI_INK);
	var _y = 220;
	for (var i = 0; i < array_length(D.items_list); i++) {
		var it = D.items_list[i];
		if (it.kind != "curio") continue;
		var _has = item_has(it.id);
		ui_text(380, _y + 6, it.name, 1.15, UI_INK, fa_left, fa_top, 230);
		ui_text_box(620, _y + 2, 400, it.desc + "  " + item_effect_text(it.id) + ".", 0.95, UI_MUTED, 46);
		if (ui_button(1040, _y, 180, 38, _has ? "Owned" : fmt_num(it.price), !_has && G.cash >= it.price)) { G.cash -= it.price; item_add(it.id); log_add(trf("Bought the {0}.", it.name)); }
		_y += 52;
	}
}

// ---- map & voyages --------------------------------------------------------------------------
// Ships follow precomputed water routes (data/routes.json, made by tools/artgen/worldmap.py).
function route_get(_a, _b) {
	if (!variable_struct_exists(global.D, "routes")) global.D.routes = load_json("data/routes.json");
	var R = global.D.routes;
	var _fwd = _a < _b;
	var _r = is_struct(R) ? struct_get_or(R, _fwd ? _a + "|" + _b : _b + "|" + _a, undefined) : undefined;
	var _out = [];
	if (_r == undefined) {
		var pa = port_def(_a), pb = port_def(_b);
		return [[pa.x, pa.y], [pb.x, pb.y]];
	}
	var _n = array_length(_r);
	for (var i = 0; i < _n; i++) array_push(_out, _fwd ? _r[i] : _r[_n - 1 - i]);
	return _out;
}

function route_length(_r) {
	var L = 0;
	for (var i = 1; i < array_length(_r); i++) L += point_distance(_r[i - 1][0], _r[i - 1][1], _r[i][0], _r[i][1]);
	return L;
}

/// Point at fraction k of the route: [x, y, direction].
function route_at(_r, _k) {
	var _L = route_length(_r) * clamp(_k, 0, 1);
	for (var i = 1; i < array_length(_r); i++) {
		var _d = point_distance(_r[i - 1][0], _r[i - 1][1], _r[i][0], _r[i][1]);
		if (_L <= _d || i == array_length(_r) - 1) {
			var t = (_d > 0) ? min(1, _L / _d) : 0;
			return [lerp(_r[i - 1][0], _r[i][0], t), lerp(_r[i - 1][1], _r[i][1], t), point_direction(_r[i - 1][0], _r[i - 1][1], _r[i][0], _r[i][1])];
		}
		_L -= _d;
	}
	return [_r[0][0], _r[0][1], 0];
}

function draw_route(_r, _k0, _alpha, _col) {
	draw_set_colour(_col);
	var _L = route_length(_r);
	var _step = 14;
	// Dashes sit at fixed distances along the route, so they never crawl when _k0 changes.
	for (var d = ceil(_k0 * _L / _step) * _step; d < _L; d += _step) {
		var p = route_at(_r, d / _L), q = route_at(_r, min(_L, d + 7) / _L);
		draw_set_alpha(_alpha);
		draw_line_width(p[0], p[1], q[0], q[1], 2.5);
	}
	draw_set_alpha(1);
}

function draw_map_ship(_x, _y, _dir, _scale) {
	var _frac = global.G.ship.hp / max(1, ship_max_hp());
	var _flip = (_dir > 90 && _dir < 270);
	draw_set_alpha(0.35); draw_set_colour(c_white);
	draw_ellipse(_x - 34 * _scale / 0.4, _y + 8, _x + 34 * _scale / 0.4, _y + 20, false);
	draw_set_alpha(1);
	draw_spr(ship_sprite_hp(ship_def().sprite, _frac), _x, _y - 10 + sin(current_time / 300) * 2, _scale, 1, _flip);
}

/// Top-left corner for the map's 540x104 info box that hides no open port, its name or your ship.
function map_info_spot(_here) {
	var D = global.D;
	var _spots = [[24, 18], [14, 456], [370, 140], [24, 230]];
	for (var k = 0; k < array_length(_spots); k++) {
		var _x0 = _spots[k][0], _y0 = _spots[k][1], _x1 = _x0 + 540, _y1 = _y0 + 104;
		var _clear = !rectangle_in_rectangle(_here.x - 20, _here.y - 30, _here.x + 100, _here.y + 80, _x0, _y0, _x1, _y1);
		for (var i = 0; _clear && i < array_length(D.ports_list); i++) {
			var p = D.ports_list[i];
			if (!port_open(p.id)) continue;
			var _ly = (p.y < 90) ? p.y + 16 : p.y - 40;
			if (rectangle_in_rectangle(p.x - 90, min(_ly, p.y - 20) - 4, p.x + 90, max(_ly + 28, p.y + 20), _x0, _y0, _x1, _y1)) _clear = false;
		}
		if (_clear) return _spots[k];
	}
	return _spots[0];
}

function screen_map() {
	var G = global.G, D = global.D;
	draw_spr("worldmap", 640, 360, 1);
	var _here = port_def();
	var _hover = "";
	for (var i = 0; i < array_length(D.ports_list); i++) {
		var p = D.ports_list[i];
		if (p.id != G.port && port_open(p.id) && ui_hover(p.x - 46, p.y - 40, 92, 64)) _hover = p.id;
	}
	if (_hover != "") draw_route(route_get(G.port, _hover), 0, 0.85, c_white);
	for (var i = 0; i < array_length(D.ports_list); i++) {
		var p = D.ports_list[i];
		if (!port_open(p.id)) continue;   // closed to this captain: not even shown
		var _is_here = p.id == G.port;
		var _hov = p.id == _hover;
		draw_set_colour(_is_here ? UI_GOLD : (_hov ? c_white : UI_BAD));
		draw_circle(p.x, p.y, _hov ? 10 : 7, false);
		draw_set_colour(UI_INK);
		draw_circle(p.x, p.y, _hov ? 10 : 7, true);
		var _ly = (p.y < 90) ? p.y + 16 : p.y - 40;
		ui_text(p.x + 1, _ly + 1, p.name, 1.05, c_black, fa_center);
		ui_text(p.x, _ly, p.name, 1.05, _hov ? UI_GOLD : c_white, fa_center);
		var _goal = campaign_current_goal();
		var _mark = (_goal != undefined && variable_struct_exists(_goal, "port") && campaign_resolve(_goal.port) == p.id);
		for (var k = 0; k < array_length(G.contracts); k++) if (G.contracts[k].port == p.id) _mark = true;
		if (_mark) {   // a bright pulsing double ring with a dark outline, readable on sea and land
			var _r = 17 + sin(current_time / 200) * 3;
			draw_set_colour(c_black); draw_set_alpha(0.6);
			draw_circle(p.x, p.y, _r + 3, true); draw_circle(p.x, p.y, _r - 3, true);
			draw_set_alpha(1); draw_set_colour(make_colour_rgb(255, 206, 70));
			for (var w = -2; w <= 2; w++) draw_circle(p.x, p.y, _r + w, true);
		}
		if (_hov && global.UI.click) {
			global.UI.click = false;
			voyage_start(p.id);
			return;
		}
	}
	// You are here: a pulsing ring and a big ship.
	var _pr = 26 + sin(current_time / 250) * 4;
	draw_set_colour(UI_GOLD); draw_set_alpha(0.8);
	draw_circle(_here.x, _here.y, _pr, true); draw_circle(_here.x, _here.y, _pr + 1, true);
	draw_set_alpha(1);
	draw_map_ship(_here.x + 40, _here.y + 44, 0, 0.4);
	// Info box: the first spot that covers no visible port, port name or your ship.
	var _bx = map_info_spot(_here);
	var _px = _bx[0], _py = _bx[1];
	ui_panel(_px, _py, 540, 104);
	if (_hover != "") {
		var hp = port_def(_hover);
		ui_text(_px + 20, _py + 12, trf("Sail to {0}  (1 week)", hp.name), 1.4, UI_INK, fa_left, fa_top, 500);
		var _bl = "";
		for (var i = 0; i < array_length(hp.buildings); i++) _bl += (i > 0 ? ", " : "") + tr(building_label(hp.buildings[i]));
		ui_text_box(_px + 20, _py + 50, 500, _bl + (hp.lawless ? tr("  - lawless port, no customs") : ""), 0.95, UI_MUTED, 46);
	} else {
		ui_text(_px + 20, _py + 12, "Choose a destination", 1.4, UI_INK);
		ui_text_box(_px + 20, _py + 50, 500, "Each voyage takes a week. Storms and raiders may find you on the way. Gold rings mark ports where your contracts and campaign lead.", 0.95, UI_MUTED, 46);
	}
	if (ui_button(1100, 20, 160, 44, "Back to port")) ui_go("port");
	if (ui_button(930, 20, 160, 44, "Fleet & Cargo")) ui_go("fleet");
}

function voyage_start(_dest) {
	var G = global.G;
	save_game("autosave.json");
	var _plan = voyage_plan(_dest);
	// Encounters happen at random points along the way.
	var _at = [];
	for (var i = 0; i < _plan.battles; i++) array_push(_at, random_range(0.18, 0.82));
	array_sort(_at, true);
	var _r = route_get(G.port, _plan.storm == "lost" ? _dest : _dest);
	global.V = { from: G.port, to: _dest, route: _r, len: route_length(_r), prog: 0,
		plan: _plan, events_done: false, battle_at: _at, special_done: false, flash: 0, wake: [] };
	ui_go("sailing");
}

function screen_sailing(_dt) {
	var V = global.V;
	draw_spr("worldmap", 640, 360, 1);
	var _to = port_def(V.to);
	var _busy = array_length(global.UI.dialogs) > 0;
	var _dur = 1.8 + V.len / 380;
	if (!_busy) V.prog = min(1, V.prog + _dt / _dur);
	var _p = route_at(V.route, V.prog);
	draw_route(V.route, 0, 0.7, c_white);   // the whole route stays put while the ship sails along it
	// Wake: fading dots behind the ship.
	if (!_busy && irandom(2) == 0) array_push(V.wake, { x: _p[0], y: _p[1], t: 1.2 });
	for (var i = array_length(V.wake) - 1; i >= 0; i--) {
		var w = V.wake[i];
		w.t -= _dt;
		if (w.t <= 0) { array_delete(V.wake, i, 1); continue; }
		draw_set_alpha(w.t * 0.4); draw_set_colour(c_white); draw_circle(w.x, w.y + 6, 3 + (1.2 - w.t) * 6, true);
	}
	draw_set_alpha(1);
	draw_map_ship(_p[0], _p[1], _p[2], 0.4);
	ui_text(640, 24, trf("Sailing to {0}...", _to.name), 1.8, c_white, fa_center);
	ui_text(641, 71, date_name(global.G.t), 1.1, c_black, fa_center);
	ui_text(640, 70, date_name(global.G.t), 1.1, make_colour_rgb(255, 235, 200), fa_center);
	if (V.flash > 0) {   // storm: grey-out and lightning
		V.flash = max(0, V.flash - _dt * 0.6);
		draw_set_alpha(V.flash * 0.7); draw_set_colour(make_colour_rgb(40, 50, 60)); draw_rectangle(0, 0, 1280, 720, false);
		if (irandom(6) == 0) { draw_set_alpha(V.flash * 0.5); draw_set_colour(c_white); draw_rectangle(0, 0, 1280, 720, false); }
		draw_set_alpha(1);
	}
	if (_busy) return;
	if (!V.events_done && V.prog >= 0.5) {
		V.events_done = true;
		var p = V.plan;
		switch (p.storm) {
			case "outran": ui_toast("A squall on the horizon - you outrun it."); break;
			case "delay": ui_message("Storm!", "A storm batters the ship for days. You lose a week waiting it out.", "portrait_sailor"); V.flash = 1; break;
			case "lost":
				ui_message("Storm!", trf("Gales drive you far off course. When the skies clear you are near {0}.", port_def(p.dest).name), "portrait_sailor");
				V.to = p.dest;
				V.route = route_get(V.from, V.to); V.len = route_length(V.route);
				V.prog = 0.5; V.flash = 1.2;
				var _cg = campaign_current_goal();
				if (p.special_kind == "campaign" && (_cg == undefined || campaign_resolve(_cg.port) != V.to)) p.special_enemy = "";
				if (p.special_kind == "hunt" && contract_hunt_at(V.to) < 0) p.special_enemy = "";
				break;
		}
	}
	if (array_length(V.battle_at) > 0 && V.prog >= V.battle_at[0]) {
		array_delete(V.battle_at, 0, 1);
		var _eid = pick_enemy();
		ui_message("Sails ahead!", trf("A {0} bears down on you, guns run out.", variable_struct_get(global.D.enemies, _eid).name), "portrait_sailor");
		combat_start(_eid, false);
		return;
	}
	if (V.prog >= 1) {
		if (V.plan.special_enemy != "" && !V.special_done) {
			V.special_done = true;
			var e = variable_struct_get(global.D.enemies, V.plan.special_enemy);
			if (V.plan.special_kind == "hunt") {
				var c = global.G.contracts[contract_hunt_at(V.to)];
				ui_message("Your quarry!", trf("{0}'s {1} is lurking off {2}. Run out the guns!", struct_get_or(c, "name", tr("The raider")), e.name, _to.name), "portrait_sailor");
			} else ui_message("Enemy waiting!", trf("The {0} lies in wait off {1}. There's no avoiding this fight.", e.name, _to.name), "portrait_grimmer");
			combat_start(V.plan.special_enemy, true);
			global.C.special_kind = V.plan.special_kind;
			return;
		}
		advance_weeks(1 + V.plan.extra_weeks);
		arrive_at(V.to);
	}
}

function voyage_after_battle(_result) {
	if (_result == "lost") global.V.battle_at = [];
	ui_go("sailing");
}

// ---- journal / help / end -----------------------------------------------------------------
function screen_journal() {
	var G = global.G;
	draw_backdrop();
	ui_panel(40, 20, 1200, 680);
	ui_text(70, 34, "Captain's Journal", 2.2, UI_INK);
	ui_text(420, 52, date_name(G.t), 1.2, UI_ACCENT);
	if (ui_button(1090, 36, 130, 44, "Back")) ui_go("port");
	if (ui_button(880, 40, 200, 36, trf("Style: {0}", tr(global.THEME.label)), true, make_colour_rgb(110, 80, 50))) theme_toggle();
	// Left column: campaign, contracts, items.
	var _y = 100;
	ui_text(70, _y, G.mode == "campaign" ? "Campaign" : "Free Trade", 1.3, UI_ACCENT); _y += 34;
	var ch = campaign_chapter();
	if (ch != undefined) { ui_text(70, _y, trf("Chapter {0} of {1}: {2}", G.campaign.chapter + 1, array_length(global.D.campaign.chapters), ch.title), 1.05, UI_INK, fa_left, fa_top, 520); _y += 24; }
	ui_text_box(70, _y, 520, campaign_objective_text(), 1, UI_INK, 46); _y += 52;
	ui_text(70, _y, trf("Contracts ({0}/{1})", array_length(G.contracts), CONTRACTS_MAX), 1.3, UI_ACCENT); _y += 34;
	if (array_length(G.contracts) == 0) { ui_text(70, _y, "None. Governors offer work every month.", 0.95, UI_MUTED); _y += 24; }
	for (var i = 0; i < array_length(G.contracts); i++) {
		var c = G.contracts[i];
		var _late = c.due - G.t <= 1;
		ui_text(70, _y, contract_text(c), 1, UI_INK, fa_left, fa_top, 520);
		ui_text(70, _y + 20, trf("For {0}, {1}, pays {2}", governor_of(c.from).name, contract_due_text(c), fmt_money(c.reward)), 0.85, _late ? UI_BAD : UI_MUTED, fa_left, fa_top, 520);
		_y += 46;
	}
	_y += 6;
	ui_text(70, _y, "Carried items", 1.3, UI_ACCENT); _y += 34;
	for (var i = 0; i < array_length(G.items) && _y < 670; i++) {
		var it = variable_struct_get(global.D.items, G.items[i].id);
		ui_text(70, _y, it.name + (G.items[i].months > 0 ? trf(" ({0} mo)", G.items[i].months) : ""), 0.95, UI_INK, fa_left, fa_top, 230);
		var _fx = item_effect_text(it.id);
		ui_text(310, _y, _fx != "" ? _fx : it.desc, 0.85, UI_MUTED, fa_left, fa_top, 290);
		_y += 24;
	}
	// Right column: log (scroll with the mouse wheel).
	ui_text(640, 100, "Log", 1.3, UI_ACCENT);
	_y = 130;
	var _start = min(global.UI.scroll, max(0, array_length(G.log) - 1));
	for (var i = _start; i < array_length(G.log) && _y < 660; i++) {
		var _lh = max(22, ui_text_height_ext(G.log[i].text, 430, 0.95));
		if (_y + _lh > 684) break;   // the next entry would run past the frame
		ui_text(640, _y, month_name(G.log[i].t), 0.9, UI_ACCENT, fa_left, fa_top, 130);
		ui_text_box(780, _y, 430, G.log[i].text, 0.95, UI_INK);
		_y += _lh + 6;
	}
}

function screen_help() {
	draw_backdrop(0.7);
	ui_panel(120, 30, 1040, 660);
	ui_text(160, 44, "How to Play", 2.2, UI_INK);
	var _paras = [
		"BUY LOW, SELL HIGH. Prices change every month around a hidden base price. Each port also has one good that will spike and one that will crash in a coming month; buy rounds at taverns to hear about them.",
		"CONTRABAND. Tobacco and wine are outlawed in two ports each month and sell there for double. Customs may seize them when you arrive. Blackwater Cay has no customs.",
		"MONEY. Banks pay 1% a month. Moneylenders charge 10% a month, compounding.",
		"VOYAGES take a week. Storms may delay you or blow you off course; raiders attack often, sometimes in packs. In battle every cannon reloads and fires on its own. Click Fire Pot, Chain Shot or Powder Keg (keys 1-3) to load it into the next cannon; click an enemy ship to target it.",
		"FLEET. Buy up to five ships at a shipyard. Every ship adds hold space and fights beside you. Click your ship in the sidebar to see the fleet and cargo.",
		"CONTRACTS. Each governor offers jobs every month: deliveries, dispatches, bounties and pirate hunts. Keep track of deadlines in the journal.",
		"CAMPAIGN: follow the objectives to bring down Commodore Grimmer. FREE TRADE: reach 1,000,000 net worth within 3 years.",
	];
	var _t = "";
	for (var i = 0; i < array_length(_paras); i++) _t += (i > 0 ? "\n\n" : "") + tr(_paras[i]);

	ui_text_box(160, 104, 960, _t, 1.1, UI_INK, 520);
	if (ui_button(1000, 626, 140, 48, "Back")) ui_go(global.G == undefined ? "title" : "port");
}

function screen_end(_win) {
	var G = global.G;
	draw_spr("title", 640, 360, 1);
	ui_panel(290, 120, 700, 480);
	var _title = _win ? (G.mode == "campaign" ? "The Reach is Free!" : "Merchant Prince!") : "Time's Up";
	ui_text(640, 150, _title, 3, UI_INK, fa_center);
	var _t = _win ? (G.mode == "campaign" ? "Commodore Grimmer is beaten and the trade lanes are open again. Your name will be toasted in every tavern from Saltmere to Tidewell." : trf("You reached a fortune of {0}. The Reach's merchant houses beg for your custom.", fmt_money(net_worth())))
		: trf("{0} years have passed. You end your career with a net worth of {1}.", global.D.config.free_mode_years, fmt_money(net_worth()));
	ui_text_box(330, 240, 620, _t, 1.3, UI_INK, 130);
	ui_text_box(330, 380, 620, trf("Voyages {0}   Battles won {1}   Lost {2}   Ships sunk {3}\nTrades {4}   Trading profit {5}   Contracts {6}\nDate: {7}", G.stats.voyages, G.stats.wins, G.stats.losses, G.stats.sunk, G.stats.trades, fmt_money(G.stats.profit), G.stats.contracts, date_name(G.t)), 1.15, UI_INK, 120);
	if (ui_button(340, 520, 280, 52, "Keep sailing")) ui_go("port");
	if (ui_button(660, 520, 280, 52, "Main menu", true, make_colour_rgb(120, 60, 60))) { save_game("autosave.json"); ui_go("title"); }
}
