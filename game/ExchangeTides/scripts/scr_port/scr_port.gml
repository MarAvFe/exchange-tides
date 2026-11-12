// ===== Port scene ============================================================================
// Each port is a painted harbour (sprites/port_<id>.png) with its buildings (sprites/bld_<type>.png)
// placed on two depth rows. The arrangement is a deterministic per-port shuffle of PORT_SLOTS, or
// ports.json "layout": [{"b":"tavern","x":700,"y":470,"s":0.8,"flip":false}, ...] to place by hand.
// Building sprites are 320x280 with the door at (160, 262): doors glow, hovered buildings light up.

#macro BLD_DOOR_DY 122   // door offset below the sprite centre, in sprite pixels

function port_slots() {
	// [x, door y, scale]: back row first.
	return [
		[440, 392, 0.58], [610, 386, 0.6], [790, 390, 0.58], [965, 384, 0.6], [1140, 392, 0.58],
		[520, 476, 0.76], [760, 470, 0.78], [1000, 474, 0.76], [1200, 480, 0.72],
	];
}

function port_hash(_s) {
	var h = 2166136261;
	for (var i = 1; i <= string_length(_s); i++) h = ((h ^ ord(string_char_at(_s, i))) * 16777619) & $7FFFFFFF;
	return h;
}

/// Returns [{b, x, y (door), s, flip}] sorted back to front.
function port_layout(_p) {
	if (variable_struct_exists(global.PORT_LAYOUTS, _p.id)) return variable_struct_get(global.PORT_LAYOUTS, _p.id);
	var _out = [];
	var _manual = struct_get_or(_p, "layout", undefined);
	if (is_array(_manual)) {
		for (var i = 0; i < array_length(_manual); i++) {
			var m = _manual[i];
			array_push(_out, { b: m.b, x: m.x, y: m.y, s: struct_get_or(m, "s", 0.7), flip: struct_get_or(m, "flip", false) });
		}
	} else {
		var _slots = port_slots();
		var _h = port_hash(_p.id);
		// Fisher-Yates with a tiny LCG so every port has its own stable arrangement.
		for (var i = array_length(_slots) - 1; i > 0; i--) {
			_h = (_h * 1103515245 + 12345) & $7FFFFFFF;
			var j = _h mod (i + 1);
			var _t = _slots[i]; _slots[i] = _slots[j]; _slots[j] = _t;
		}
		var _bs = _p.buildings;
		for (var i = 0; i < array_length(_bs) && i < array_length(_slots); i++) {
			_h = (_h * 1103515245 + 12345) & $7FFFFFFF;
			var sl = _slots[i];
			array_push(_out, { b: _bs[i], x: sl[0], y: sl[1], s: sl[2], flip: (_h mod 3) == 0 });
		}
	}
	array_sort(_out, function(a, b) { return a.y - b.y; });
	variable_struct_set(global.PORT_LAYOUTS, _p.id, _out);
	return _out;
}

function port_enter_building(_b) {
	ui_go(_b);
	campaign_on_visit(_b);
	if (_b == "tavern") global.UI.tavern_text = "The tavern is loud, smoky and full of rumours.";
}

function screen_port() {
	var G = global.G, U = global.UI;
	if (!variable_global_exists("PORT_LAYOUTS")) global.PORT_LAYOUTS = {};
	var p = port_def();
	var _bg = spr("port_" + p.id);
	if (_bg >= 0) draw_spr("port_" + p.id, 640, 360, 1280 / sprite_get_width(_bg));
	else draw_backdrop(0.2);

	var _lay = port_layout(p);
	var _t = current_time / 1000;

	// Hover: of the buildings under the mouse, the one whose body centre is closest wins (front rows
	// would otherwise swallow the buildings behind them). Hit boxes hug the painted building.
	var _hov = -1, _best = 1000000000;
	for (var i = array_length(_lay) - 1; i >= 0; i--) {
		var L = _lay[i];
		var _w = 210 * L.s, _h = 230 * L.s;
		if (ui_hover(L.x - _w / 2, L.y - _h, _w, _h + 6)) {
			var _d = point_distance(global.UI.mx, global.UI.my, L.x, L.y - _h * 0.45);
			if (_d < _best) { _best = _d; _hov = i; }
		}
	}

	for (var i = 0; i < array_length(_lay); i++) {
		var L = _lay[i];
		var _name = "bld_" + L.b;
		var _cy = L.y - BLD_DOOR_DY * L.s;
		// Soft contact shadow.
		draw_set_alpha(0.25); draw_set_colour(c_black);
		draw_ellipse(L.x - 130 * L.s, L.y + 8 * L.s, L.x + 130 * L.s, L.y + 26 * L.s, false);
		draw_set_alpha(1);
		draw_spr(_name, L.x, _cy, L.s, 1, L.flip);
		// Door glow: a gentle pulse, brighter when hovered.
		var _hot = (i == _hov);
		var _pulse = 0.5 + 0.5 * sin(_t * 2.4 + i);
		gpu_set_blendmode(bm_add);
		draw_set_alpha((_hot ? 0.75 : 0.22 + 0.18 * _pulse));
		draw_circle_colour(L.x, L.y - 26 * L.s, (_hot ? 62 : 44) * L.s, make_colour_rgb(255, 190, 90), c_black, false);
		if (_hot) {
			draw_set_alpha(0.22);
			draw_spr(_name, L.x, _cy, L.s, 0.22, L.flip);
		}
		draw_set_alpha(1);
		gpu_set_blendmode(bm_normal);
	}
	// Name banner above the hovered building; click to enter.
	if (_hov >= 0) {
		var L = _lay[_hov];
		var _lbl = building_label(L.b);
		var _tw = ui_text_width(_lbl, 1.3) + 36;
		var _by = L.y - 262 * L.s - 30;
		draw_set_colour(UI_PAPER); draw_roundrect_ext(L.x - _tw / 2, _by - 20, L.x + _tw / 2, _by + 20, 12, 12, false);
		draw_set_colour(UI_INK); draw_roundrect_ext(L.x - _tw / 2, _by - 20, L.x + _tw / 2, _by + 20, 12, 12, true);
		ui_text(L.x, _by, _lbl, 1.3, UI_INK, fa_center, fa_middle);
		if (U.click) { U.click = false; port_enter_building(L.b); }
	}

	draw_sidebar();
	// Port name banner.
	var _nw = min(560, ui_text_width(p.name, 2.2) + 80);
	ui_panel(800 - _nw / 2, 14, _nw, 62);
	ui_text(800, 45, p.name, 2.2, UI_INK, fa_center, fa_middle, _nw - 40);
	if (p.lawless) ui_text(800, 88, "Lawless port - no customs", 1, make_colour_rgb(255, 210, 190), fa_center);

	var _by = 540;
	if (ui_button(1082, _by, 170, 50, "Set Sail", true, make_colour_rgb(40, 120, 90))) ui_go("map");
	if (ui_button(336, _by + 6, 120, 40, "Journal")) ui_go("journal");
	if (ui_button(462, _by + 6, 150, 40, "Fleet & Cargo")) ui_go("fleet");
	if (ui_button(618, _by + 6, 110, 40, "Save")) { global.UI.save_mode = "save"; ui_go("saves"); }
	if (ui_button(734, _by + 6, 80, 40, "Help")) ui_go("help");
	if (ui_button(820, _by + 6, 110, 40, "Menu", true, make_colour_rgb(120, 60, 60))) { save_game("autosave.json"); ui_go("title"); }
	draw_objective_bar();
}

/// Display name of a building type (translated when drawn).
function building_label(_b) {
	var _labels = { market: "Marketplace", bank: "Bank", lender: "Moneylender", shipyard: "Shipyard", tavern: "Tavern", governor: "Governor's House", curio: "Curio Dealer" };
	return struct_get_or(_labels, _b, _b);
}
