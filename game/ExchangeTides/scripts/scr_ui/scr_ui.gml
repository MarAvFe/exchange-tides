// ===== Immediate-mode UI toolkit ==============================================================

// Colours come from the active theme (scr_theme).
#macro UI_INK global.THEME.ink
#macro UI_PAPER global.THEME.paper
#macro UI_PAPER_DARK global.THEME.paper_dark
#macro UI_ACCENT global.THEME.accent
#macro UI_GOLD global.THEME.gold
#macro UI_MUTED global.THEME.muted
#macro UI_GOOD global.THEME.good
#macro UI_BAD global.THEME.bad
#macro UI_WARN global.THEME.warn

function ui_init() {
	global.UI = {
		screen: "title", click: false, mx: 0, my: 0, block: false,
		dialogs: [], toasts: [], scroll: 0,
		pending_mode: "campaign", tavern_text: "", hover_port: "",
		screen_prev: "", save_mode: "load", yard_sel: 0, slot_cache: undefined,
	};
	ui_fonts_load();
	theme_init();
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
	return string_width(tr(_s)) * _r;
}

function ui_text_height_ext(_s, _w, _scale = 1) {
	var _r = ui_font(_scale);
	return string_height_ext(tr(_s), -1, _w / _r) * _r;
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
	_s = tr(_s);
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
	_s = tr(_s);
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

/// A themed panel: textured fill inside a wooden frame. _col is accepted for old call sites; a
/// colour other than the default paper draws the panel slightly darker (an "inset").
function ui_panel(_x, _y, _w, _h, _col = undefined) {
	var T = global.THEME;
	draw_set_alpha(0.35); draw_set_colour(c_black);
	draw_rectangle(_x + 6, _y + 7, _x + _w + 6, _y + _h + 7, false);
	draw_set_alpha(1);
	var _inset = (_col != undefined && _col != UI_PAPER);
	theme_tile(T.panel_tex, _x, _y, _w, _h, _inset ? merge_colour(T.panel_tint, c_black, 0.12) : T.panel_tint);
	var _fw = (_w < 200 || _h < 80) ? max(6, T.frame_w * 0.6) : T.frame_w;
	theme_frame(_x - 2, _y - 2, _w + 4, _h + 4, _fw);
}

/// Returns true on click. Disabled buttons render greyed out and never fire.
function ui_button(_x, _y, _w, _h, _label, _enabled = true, _col = undefined) {
	var U = global.UI;
	var _hov = _enabled && ui_hover(_x, _y, _w, _h);
	var _base = (_col == undefined) ? UI_ACCENT : _col;
	var T = global.THEME;
	if (T.btn_brass) _base = merge_colour(_base, make_colour_rgb(216, 170, 84), 0.72);   // brass plates, hinting the action colour
	var _c = _enabled ? (_hov ? merge_colour(_base, c_white, 0.25) : _base) : (T.btn_brass ? make_colour_rgb(96, 82, 68) : make_colour_rgb(150, 144, 136));
	draw_set_colour(merge_colour(_c, c_black, 0.5));
	draw_roundrect_ext(_x, _y + 3, _x + _w, _y + _h + 3, 8, 8, false);
	draw_set_colour(_c);
	draw_roundrect_ext(_x, _y, _x + _w, _y + _h, 8, 8, false);
	// A faint wood grain over the plate (normal blending, low alpha, so the colour stays clear).
	var _tex = spr("tex_wood_light");
	if (_tex >= 0) draw_sprite_part_ext(_tex, 0, 0, 0, min(512, _w * 2), min(512, _h * 2), _x + 2, _y + 2, (_w - 4) / min(512, _w * 2), (_h - 4) / min(512, _h * 2), c_white, T.btn_brass ? 0.18 : 0.14);
	draw_set_colour(merge_colour(_c, c_white, 0.4)); draw_set_alpha(0.55);
	draw_line_width(_x + 6, _y + 3, _x + _w - 6, _y + 3, 2);
	draw_set_alpha(1);
	draw_set_colour(merge_colour(_c, c_black, 0.6));
	draw_roundrect_ext(_x, _y, _x + _w, _y + _h, 8, 8, true);
	var _sc = (_h >= 44) ? 1.25 : 1.05;
	_label = tr(_label);
	var _tw = ui_text_width(_label, _sc);
	if (_tw > _w - 14) _sc *= (_w - 14) / max(1, _tw);
	ui_text(_x + _w / 2, _y + _h / 2, _label, _sc, _enabled ? T.btn_text : (T.btn_brass ? make_colour_rgb(170, 156, 136) : make_colour_rgb(236, 232, 226)), fa_center, fa_middle);
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
	array_push(global.UI.toasts, { text: tr(_text), t: 3.5 });
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
		ui_portrait_frame(310, 340, 1.1);
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
		var _w = min(1000, ui_text_width(tr(t.text), 1.2) + 40);
		draw_set_colour(make_colour_rgb(30, 40, 50));
		draw_roundrect_ext(640 - _w / 2, _y, 640 + _w / 2, _y + 40, 14, 14, false);
		ui_text(640, _y + 20, t.text, 1.2, UI_GOLD, fa_center, fa_middle, _w - 30);
		draw_set_alpha(1);
		_y -= 48;
	}
}
