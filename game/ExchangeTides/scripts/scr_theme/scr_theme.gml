// ===== Visual themes =============================================================================
// One style used everywhere: panels, frames, buttons, text colours and portrait frames all come from
// global.THEME. Two themes exist as an MVP to compare: "storybook" (cream paper, honey-oak frames,
// earthy ink) and "darkwood" (walnut cabin panels, brass fittings, lantern-gold text).
// Textures: sprites/tex_*.png (tools/artgen/art_spec.json). Switch with theme_set(); saved in settings.
// To add a theme: add a case to theme_make with the same fields.

function theme_make(_name) {
	switch (_name) {
		case "darkwood":
			return {
				name: "darkwood", label: "Dark Wood",
				ink: make_colour_rgb(242, 228, 200), muted: make_colour_rgb(196, 176, 146),
				accent: make_colour_rgb(236, 186, 92), gold: make_colour_rgb(240, 196, 100),
				good: make_colour_rgb(150, 210, 130), bad: make_colour_rgb(240, 120, 100), warn: make_colour_rgb(236, 170, 110),
				paper: make_colour_rgb(150, 110, 80), paper_dark: make_colour_rgb(30, 20, 14),
				panel_tex: "tex_wood_dark", panel_tint: make_colour_rgb(150, 120, 100),
				frame_tex: "tex_wood_carved", frame_tint: make_colour_rgb(120, 90, 70), frame_w: 14,
				line_hi: make_colour_rgb(110, 80, 56), line_lo: make_colour_rgb(16, 10, 8),
				corner: "brass", btn_text: make_colour_rgb(36, 24, 14), btn_brass: true,
				stripe_alpha: 0.35,
			};
	}
	return {
		name: "storybook", label: "Storybook",
		ink: make_colour_rgb(52, 38, 30), muted: make_colour_rgb(110, 92, 74),
		accent: make_colour_rgb(160, 84, 44), gold: make_colour_rgb(214, 170, 70),
		good: make_colour_rgb(50, 120, 60), bad: make_colour_rgb(170, 44, 40), warn: make_colour_rgb(150, 84, 30),
		paper: make_colour_rgb(242, 230, 202), paper_dark: make_colour_rgb(214, 196, 158),
		panel_tex: "tex_paper_cream", panel_tint: c_white,
		frame_tex: "tex_wood_light", frame_tint: make_colour_rgb(230, 200, 160), frame_w: 12,
		line_hi: make_colour_rgb(250, 232, 196), line_lo: make_colour_rgb(92, 62, 40),
		corner: "peg", btn_text: c_white, btn_brass: false,
		stripe_alpha: 0.25,
	};
}

function theme_init() { global.THEME = theme_make(settings_get("theme", "storybook")); }

function theme_set(_name) {
	global.THEME = theme_make(_name);
	settings_set("theme", _name);
}

function theme_toggle() { theme_set(global.THEME.name == "storybook" ? "darkwood" : "storybook"); }

/// Tiles a texture over a rectangle (texture drawn at half size for a finer grain).
function theme_tile(_tex, _x, _y, _w, _h, _tint, _alpha = 1) {
	var s = spr(_tex);
	if (s < 0) { draw_set_colour(_tint); draw_set_alpha(_alpha); draw_rectangle(_x, _y, _x + _w, _y + _h, false); draw_set_alpha(1); return; }
	var _k = 0.5, _tw = sprite_get_width(s), _th = sprite_get_height(s);
	for (var yy = 0; yy < _h; yy += _th * _k) {
		for (var xx = 0; xx < _w; xx += _tw * _k) {
			var _pw = min(_tw, (_w - xx) / _k), _ph = min(_th, (_h - yy) / _k);
			draw_sprite_part_ext(s, 0, 0, 0, _pw, _ph, _x + xx, _y + yy, _k, _k, _tint, _alpha);
		}
	}
}

/// A wooden frame of thickness fw around (x, y, w, h) (outside edge), with bevel lines and corner fittings.
function theme_frame(_x, _y, _w, _h, _fw = -1) {
	var T = global.THEME;
	if (_fw < 0) _fw = T.frame_w;
	theme_tile(T.frame_tex, _x, _y, _w, _fw, T.frame_tint);
	theme_tile(T.frame_tex, _x, _y + _h - _fw, _w, _fw, T.frame_tint);
	theme_tile(T.frame_tex, _x, _y + _fw, _fw, _h - 2 * _fw, T.frame_tint);
	theme_tile(T.frame_tex, _x + _w - _fw, _y + _fw, _fw, _h - 2 * _fw, T.frame_tint);
	draw_set_colour(T.line_lo);
	draw_rectangle(_x, _y, _x + _w, _y + _h, true);
	draw_rectangle(_x + _fw, _y + _fw, _x + _w - _fw, _y + _h - _fw, true);
	draw_set_colour(T.line_hi);
	draw_rectangle(_x + 1, _y + 1, _x + _w - 1, _y + _h - 1, true);
	var _cs = [[_x, _y], [_x + _w, _y], [_x, _y + _h], [_x + _w, _y + _h]];
	for (var i = 0; i < 4; i++) {
		var cx = _cs[i][0] + (i mod 2 == 0 ? _fw / 2 : -_fw / 2), cy = _cs[i][1] + (i < 2 ? _fw / 2 : -_fw / 2);
		if (T.corner == "brass") {
			draw_set_colour(make_colour_rgb(90, 64, 24)); draw_circle(cx, cy, _fw * 0.62, false);
			draw_set_colour(make_colour_rgb(214, 170, 80)); draw_circle(cx - 1, cy - 1, _fw * 0.48, false);
			draw_set_colour(make_colour_rgb(250, 226, 150)); draw_circle(cx - 2, cy - 2, _fw * 0.18, false);
		} else {
			draw_set_colour(make_colour_rgb(110, 74, 44)); draw_circle(cx, cy, _fw * 0.32, false);
			draw_set_colour(make_colour_rgb(190, 146, 96)); draw_circle(cx - 1, cy - 1, _fw * 0.2, false);
		}
	}
}

/// Frame around a 160x200 portrait drawn centred at (cx, cy) with the given scale.
function ui_portrait_frame(_cx, _cy, _scale) {
	var _w = 160 * _scale, _h = 200 * _scale;
	var _fw = max(4, round(9 * _scale));
	theme_frame(_cx - _w / 2 - _fw + 2, _cy - _h / 2 - _fw + 2, _w + 2 * _fw - 4, _h + 2 * _fw - 4, _fw);
}
