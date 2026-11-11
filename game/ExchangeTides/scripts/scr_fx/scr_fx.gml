// ===== Battle particles ===============================================================================
// Small CPU particle list in global.C.parts. kinds: spark (additive, gravity), flame (additive, rises),
// smoke (grows, drifts), chip (wood splinter, gravity, spins), drop (water spray, gravity), ring (foam).

function fx_add(_kind, _x, _y, _vx, _vy, _life, _size, _col) {
	var C = global.C;
	if (array_length(C.parts) > 900) return;
	array_push(C.parts, { k: _kind, x: _x, y: _y, vx: _vx, vy: _vy, t: 0, life: _life, s: _size, c: _col, r: random(360) });
}

/// Cannon fire: a short white-hot flash, a cone of sparks toward the target and a puff of gun smoke.
function fx_muzzle(_x, _y, _dir, _sc) {
	fx_add("flash", _x, _y, 0, 0, 0.09, 14 * _sc, c_white);
	repeat (9) {
		var _a = (_dir > 0 ? 0 : 180) + random_range(-28, 28) + 8 * _dir;
		var _sp = random_range(160, 420) * _sc;
		fx_add("spark", _x, _y, lengthdir_x(_sp, _a), lengthdir_y(_sp, _a), random_range(0.15, 0.35), random_range(1.5, 3) * _sc, choose(make_colour_rgb(255, 230, 140), make_colour_rgb(255, 170, 60), make_colour_rgb(255, 120, 40)));
	}
	repeat (4) fx_add("smoke", _x + _dir * random(18), _y + random_range(-6, 6), _dir * random_range(10, 40) + 12, random_range(-22, -6), random_range(1.2, 2.2), random_range(8, 14) * _sc, make_colour_rgb(220, 218, 210));
}

function fx_hit(_x, _y, _ammo, _sc) {
	var _hot = (string_pos("firepot", _ammo) > 0 || string_pos("bomb", _ammo) > 0);
	var _n = (_ammo == "bomb") ? 3 : 1;
	repeat (10 * _n) {
		var _a = random_range(20, 160), _sp = random_range(80, 260) * _sc;
		fx_add("spark", _x, _y, lengthdir_x(_sp, _a), lengthdir_y(_sp, _a), random_range(0.2, 0.45), random_range(1.5, 3) * _sc, choose(make_colour_rgb(255, 210, 120), make_colour_rgb(255, 140, 50)));
	}
	repeat (6 * _n) {
		var _a = random_range(30, 150), _sp = random_range(60, 200) * _sc;
		fx_add("chip", _x, _y, lengthdir_x(_sp, _a), lengthdir_y(_sp, _a), random_range(0.5, 0.9), random_range(2, 4) * _sc, choose(make_colour_rgb(120, 80, 45), make_colour_rgb(160, 115, 70), make_colour_rgb(80, 55, 35)));
	}
	if (_hot) repeat (8 * _n) fx_flame(_x + random_range(-20, 20), _y + random_range(-10, 10), _sc * 1.3);
	repeat (2 + _n) fx_smoke(_x + random_range(-10, 10), _y - 6, _sc * (_hot ? 1.4 : 1));
}

function fx_flame(_x, _y, _sc) {
	fx_add("flame", _x, _y, random_range(-12, 12), random_range(-70, -30) * _sc, random_range(0.3, 0.6), random_range(5, 9) * _sc, choose(make_colour_rgb(255, 190, 70), make_colour_rgb(255, 120, 40), make_colour_rgb(240, 80, 30)));
}

function fx_smoke(_x, _y, _sc) {
	fx_add("smoke", _x, _y, random_range(-10, 20), random_range(-35, -15), random_range(1.4, 2.4), random_range(9, 15) * _sc, choose(make_colour_rgb(70, 66, 64), make_colour_rgb(110, 104, 100)));
}

function fx_splash(_x, _y, _sc) {
	repeat (12) {
		var _a = random_range(60, 120), _sp = random_range(120, 300) * _sc;
		fx_add("drop", _x + random_range(-6, 6), _y, lengthdir_x(_sp, _a) * 0.5, lengthdir_y(_sp, _a), random_range(0.4, 0.8), random_range(2, 3.5) * _sc, make_colour_rgb(230, 244, 250));
	}
	fx_add("ring", _x, _y + 4, 0, 0, 0.9, 30 * _sc, c_white);
}

function fx_update(_dt) {
	var P = global.C.parts;
	for (var i = array_length(P) - 1; i >= 0; i--) {
		var p = P[i];
		p.t += _dt;
		if (p.t >= p.life) { array_delete(P, i, 1); continue; }
		p.x += p.vx * _dt; p.y += p.vy * _dt;
		switch (p.k) {
			case "spark": p.vy += 420 * _dt; p.vx *= 0.96; break;
			case "chip": p.vy += 600 * _dt; p.r += 600 * _dt; break;
			case "drop": p.vy += 700 * _dt; break;
			case "smoke": p.vx += 14 * _dt; p.vy *= 0.98; break;
			case "flame": p.vy *= 0.97; break;
		}
	}
}

function fx_draw() {
	var P = global.C.parts;
	// Smoke and debris first (normal blending), then additive fire on top.
	for (var i = 0; i < array_length(P); i++) {
		var p = P[i], k = p.t / p.life;
		switch (p.k) {
			case "smoke":
				draw_set_alpha(0.45 * (1 - k)); draw_set_colour(p.c);
				draw_circle(p.x, p.y, p.s * (1 + k * 1.8), false);
				break;
			case "chip":
				draw_set_alpha(1 - k * k); draw_set_colour(p.c);
				var _dx = lengthdir_x(p.s, p.r), _dy = lengthdir_y(p.s, p.r);
				draw_line_width(p.x - _dx, p.y - _dy, p.x + _dx, p.y + _dy, max(1.5, p.s * 0.5));
				break;
			case "drop":
				draw_set_alpha(0.9 * (1 - k)); draw_set_colour(p.c); draw_circle(p.x, p.y, p.s, false);
				break;
			case "ring":
				draw_set_alpha(0.6 * (1 - k)); draw_set_colour(p.c);
				draw_ellipse(p.x - p.s * (0.4 + k), p.y - p.s * 0.18 * (0.4 + k), p.x + p.s * (0.4 + k), p.y + p.s * 0.18 * (0.4 + k), true);
				break;
		}
	}
	gpu_set_blendmode(bm_add);
	for (var i = 0; i < array_length(P); i++) {
		var p = P[i], k = p.t / p.life;
		switch (p.k) {
			case "spark":
				draw_set_alpha(1 - k); draw_set_colour(p.c);
				draw_line_width(p.x, p.y, p.x - p.vx * 0.025, p.y - p.vy * 0.025, p.s);
				break;
			case "flame":
				draw_set_alpha(0.8 * (1 - k)); draw_set_colour(merge_colour(p.c, make_colour_rgb(120, 30, 10), k));
				draw_circle(p.x, p.y, p.s * (1 - k * 0.5), false);
				break;
			case "flash":
				draw_set_alpha(1 - k); draw_set_colour(make_colour_rgb(255, 240, 200));
				draw_circle(p.x, p.y, p.s * (1 - k * 0.3), false);
				draw_set_colour(make_colour_rgb(255, 150, 50)); draw_set_alpha(0.6 * (1 - k));
				draw_circle(p.x, p.y, p.s * 1.7, false);
				break;
		}
	}
	gpu_set_blendmode(bm_normal);
	draw_set_alpha(1);
}
