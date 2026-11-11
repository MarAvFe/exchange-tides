// ===== Immediate-mode UI toolkit ==============================================================

#macro UI_INK make_colour_rgb(44, 34, 30)
#macro UI_PAPER make_colour_rgb(242, 230, 202)
#macro UI_PAPER_DARK make_colour_rgb(214, 196, 158)
#macro UI_ACCENT make_colour_rgb(46, 110, 130)
#macro UI_GOLD make_colour_rgb(214, 170, 70)

function ui_init() {
	global.UI = {
		screen: "title", click: false, mx: 0, my: 0, block: false,
		dialogs: [], toasts: [], scroll: 0,
		pending_mode: "campaign", tavern_text: "", hover_port: "",
		screen_prev: "", save_mode: "load", yard_sel: 0, slot_cache: undefined,
	};
	ui_fonts_load();
}

// ---- fonts -----------------------------------------------------------------------------------
// Body text: Alegreya. Headings (scale >= UI_HEADING_SCALE): Pirata One. Both are OFL fonts in datafiles/fonts.
// Each is rasterised at several pixel sizes; ui_font() picks the closest size at or above the
// requested one, so text is downscaled slightly instead of blurrily upscaled.
#macro UI_BODY_PX 17
#macro UI_HEADING_SCALE 1.6

function ui_fonts_load() {
	global.FONTS = { body: [], head: [] };
	var _body = working_directory + "fonts/Alegreya.ttf";
	var _head = working_directory + "fonts/PirataOne-Regular.ttf";
	var _bs = [14, 16, 18, 20, 22, 25, 28, 32];
	var _hs = [28, 34, 40, 48, 58, 70, 86];
	if (file_exists(_body)) for (var i = 0; i < array_length(_bs); i++) array_push(global.FONTS.body, { px: _bs[i], f: font_add(_body, _bs[i], false, false, 32, 255) });
	if (file_exists(_head)) for (var i = 0; i < array_length(_hs); i++) array_push(global.FONTS.head, { px: _hs[i], f: font_add(_head, _hs[i], false, false, 32, 255) });
}

/// Sets the font for a logical text scale and returns the residual draw scale.
function ui_font(_scale) {
	var _list = (_scale >= UI_HEADING_SCALE && array_length(global.FONTS.head) > 0) ? global.FONTS.head : global.FONTS.body;
	if (array_length(_list) == 0) { draw_set_font(-1); return _scale; }
	var _px = UI_BODY_PX * _scale;
	var _pick = _list[array_length(_list) - 1];
	for (var i = 0; i < array_length(_list); i++) if (_list[i].px >= _px - 0.5) { _pick = _list[i]; break; }
	draw_set_font(_pick.f);
	return _px / _pick.px;
}

function ui_text_width(_s, _scale = 1) {
	var _r = ui_font(_scale);
	return string_width(_s) * _r;
}

function ui_text_height_ext(_s, _w, _scale = 1) {
	var _r = ui_font(_scale);
	return string_height_ext(_s, -1, _w / _r) * _r;
}

function ui_go(_screen) {
	if (global.UI.screen != _screen) global.UI.screen_prev = global.UI.screen;
	global.UI.screen = _screen;
	global.UI.scroll = 0;
}

function ui_enabled() { return !global.UI.block; }

function ui_frame_begin() {
	var U = global.UI;
	U.mx = device_mouse_x_to_gui(0);
	U.my = device_mouse_y_to_gui(0);
	U.click = mouse_check_button_pressed(mb_left);
	if (mouse_wheel_up()) U.scroll = max(0, U.scroll - 1);
	if (mouse_wheel_down()) U.scroll += 1;
}

function ui_hover(_x, _y, _w, _h) {
	var U = global.UI;
	return !U.block && U.mx >= _x && U.mx < _x + _w && U.my >= _y && U.my < _y + _h;
}

/// _maxw > 0 shrinks the text to fit that width.
function ui_text(_x, _y, _s, _scale = 1, _col = UI_INK, _halign = fa_left, _valign = fa_top, _maxw = 0) {
	if (_maxw > 0) _scale = fit_scale(_s, _scale, _maxw);
	draw_set_halign(_halign);
	draw_set_valign(_valign);
	draw_set_colour(_col);
	var _r = ui_font(_scale);
	draw_text_transformed(_x, _y, _s, _r, _r, 0);
	draw_set_halign(fa_left);
	draw_set_valign(fa_top);
}

/// Wrapped text. _maxh > 0 shrinks the text until it fits that height.
function ui_text_box(_x, _y, _w, _s, _scale = 1, _col = UI_INK, _maxh = 0) {
	if (_maxh > 0) {
		var _guard = 0;
		while (_scale > 0.6 && ui_text_height_ext(_s, _w, _scale) > _maxh && _guard < 12) { _scale *= 0.92; _guard++; }
	}
	draw_set_halign(fa_left);
	draw_set_valign(fa_top);
	draw_set_colour(_col);
	var _r = ui_font(_scale);
	draw_text_ext_transformed(_x, _y, _s, -1, _w / _r, _r, _r, 0);
}

function ui_panel(_x, _y, _w, _h, _col = UI_PAPER) {
	draw_set_alpha(0.35);
	draw_set_colour(c_black);
	draw_roundrect_ext(_x + 5, _y + 6, _x + _w + 5, _y + _h + 6, 18, 18, false);
	draw_set_alpha(1);
	draw_set_colour(_col);
	draw_roundrect_ext(_x, _y, _x + _w, _y + _h, 18, 18, false);
	// Optional painted paper texture (sprites/ui_parchment.png), tinted by the panel colour.
	var _tex = (_col == UI_PAPER) ? spr("ui_parchment") : -1;
	if (_tex >= 0) draw_sprite_ext(_tex, 0, _x + _w / 2, _y + _h / 2, (_w - 18) / sprite_get_width(_tex),
		(_h - 18) / sprite_get_height(_tex), 0, c_white, 0.85);   // sprites are centre-origin (see spr())
	draw_set_colour(UI_INK);
	draw_roundrect_ext(_x, _y, _x + _w, _y + _h, 18, 18, true);
	draw_roundrect_ext(_x + 4, _y + 4, _x + _w - 4, _y + _h - 4, 14, 14, true);
}

/// Returns true on click. Disabled buttons render greyed out and never fire.
function ui_button(_x, _y, _w, _h, _label, _enabled = true, _col = undefined) {
	var U = global.UI;
	var _hov = _enabled && ui_hover(_x, _y, _w, _h);
	var _base = (_col == undefined) ? UI_ACCENT : _col;
	var _c = _enabled ? (_hov ? merge_colour(_base, c_white, 0.25) : _base) : make_colour_rgb(150, 145, 140);
	draw_set_colour(merge_colour(_c, c_black, 0.45));
	draw_roundrect_ext(_x, _y + 3, _x + _w, _y + _h + 3, 12, 12, false);
	draw_set_colour(_c);
	draw_roundrect_ext(_x, _y, _x + _w, _y + _h, 12, 12, false);
	draw_set_colour(merge_colour(_c, c_white, 0.35));
	draw_roundrect_ext(_x + 3, _y + 3, _x + _w - 3, _y + _h * 0.45, 9, 9, false);
	var _sc = (_h >= 44) ? 1.25 : 1.05;
	var _tw = ui_text_width(_label, _sc);
	if (_tw > _w - 14) _sc *= (_w - 14) / max(1, _tw);
	ui_text(_x + _w / 2, _y + _h / 2, _label, _sc, c_white, fa_center, fa_middle);
	if (_hov && U.click) {
		U.click = false;
		return true;
	}
	return false;
}

function ui_bar(_x, _y, _w, _h, _frac, _col, _label) {
	_frac = clamp(_frac, 0, 1);
	draw_set_colour(make_colour_rgb(40, 34, 34));
	draw_roundrect_ext(_x - 2, _y - 2, _x + _w + 2, _y + _h + 2, 8, 8, false);
	draw_set_colour(_col);
	if (_frac > 0) draw_roundrect_ext(_x, _y, _x + _w * _frac, _y + _h, 6, 6, false);
	if (_label != "") ui_text(_x + 8, _y + _h / 2, _label, 1, c_white, fa_left, fa_middle);
}

// ---- dialogs & toasts --------------------------------------------------------------------
function ui_dialog(_npc, _text, _ok = "Continue") {
	var _pid = (global.G != undefined) ? global.G.port : "";
	array_push(global.UI.dialogs, { portrait: npc_portrait(_npc), npc: _npc, pid: _pid, name: npc_display_name(_npc), text: _text, ok: _ok });
}

function ui_message(_title, _text, _portrait = "portrait_sailor") {
	// "portrait_governor" means this port's (generated) governor.
	var _npc = (_portrait == "portrait_governor" && global.G != undefined) ? "governor" : "";
	array_push(global.UI.dialogs, { portrait: _portrait, npc: _npc, pid: (global.G != undefined ? global.G.port : ""), name: _title, text: _text, ok: "Continue" });
}

function ui_toast(_text) {
	array_push(global.UI.toasts, { text: _text, t: 3.5 });
	while (array_length(global.UI.toasts) > 4) array_delete(global.UI.toasts, 0, 1);
}

function ui_draw_overlays(_dt) {
	var U = global.UI;
	if (array_length(U.dialogs) > 0) {
		var d = U.dialogs[0];
		draw_set_alpha(0.55); draw_set_colour(c_black); draw_rectangle(0, 0, 1280, 720, false); draw_set_alpha(1);
		ui_panel(200, 180, 880, 340);
		if (struct_get_or(d, "npc", "") != "" && global.G != undefined) npc_draw_any(d.npc, 310, 340, 1.1, d.pid);
		else draw_spr(d.portrait, 310, 340, 1.1);
		ui_text(410, 210, d.name, 1.8, UI_INK, fa_left, fa_top, 640);
		ui_text_box(410, 262, 630, d.text, 1.25, UI_INK, 170);
		if (ui_button(760, 440, 280, 52, d.ok) || keyboard_check_pressed(vk_enter)) array_delete(U.dialogs, 0, 1);
	}
	var _y = (U.screen == "combat") ? 548 : 556;
	for (var i = array_length(U.toasts) - 1; i >= 0; i--) {
		var t = U.toasts[i];
		t.t -= _dt;
		if (t.t <= 0) { array_delete(U.toasts, i, 1); continue; }
		draw_set_alpha(min(1, t.t));
		var _w = min(1000, ui_text_width(t.text, 1.2) + 40);
		draw_set_colour(make_colour_rgb(30, 40, 50));
		draw_roundrect_ext(640 - _w / 2, _y, 640 + _w / 2, _y + 40, 14, 14, false);
		ui_text(640, _y + 20, t.text, 1.2, UI_GOLD, fa_center, fa_middle, _w - 30);
		draw_set_alpha(1);
		_y -= 48;
	}
}
