// ===== Sea combat (docs/MECHANICS.md §5) ===================================================
// Fleet battle on two depth planes: your ships in the foreground, the enemy pack in
// the background. Hit chance = clamp(target.thaco + shooter accuracy bonus, 0, 100) (−10 in fog).
// Every cannon reloads on its own timer (randomised start phase) and fires automatically at the
// selected target. Clicking a special-ammo button loads it onto the next cannon to fire.
// Flee: base 30%, +10% per failed attempt, max 80%.

#macro ENEMY_PLANE_Y 318
#macro ENEMY_PLANE_S 0.78
#macro ALLY_PLANE_Y 505
#macro ALLY_PLANE_S 1.12
#macro RELOAD_K 2.6        // seconds of reload per point of a ship's "reload" stat

/// _extra: number of additional pack ships (-1 = roll from config).
function combat_start(_enemy_id, _special, _extra = -1) {
	var D = global.D, G = global.G;
	var _main = variable_struct_get(D.enemies, _enemy_id);
	var _weather = "";
	if (roll100() < D.config.weather_chance) _weather = choose("rain", "fog");

	// Enemy pack: the encountered ship plus optional companions of equal or lower level.
	// A fort is a building on its island; a few guard ships may be anchored beside it.
	var _fort = (_main.behavior == "stationary");
	var _defs = [_main];
	if (_extra < 0 && _fort) _extra = min(2, irandom(1) + G.level div 4);
	if (_extra < 0) {
		_extra = 0;
		if (!_special && _main.behavior != "stationary" && roll100() < struct_get_or(D.config, "extra_enemy_chance", 40) * (G.level == 0 ? 0.6 : 1))
			_extra = irandom_range(1, min(struct_get_or(D.config, "max_extra_enemies", 2), 1 + (G.level + fleet_size() - 1) div 2));
	}
	var _pool = [];
	for (var i = 0; i < array_length(D.ships.enemies); i++) {
		var e = D.ships.enemies[i];
		if (!struct_get_or(e, "unique", false) && e.level <= (_fort ? max(1, G.level) : max(0, _main.level)) && e.behavior != "stationary") array_push(_pool, e);
	}
	for (var i = 0; i < _extra && array_length(_pool) > 0; i++) array_push(_defs, arr_pick(_pool));

	// Late game: the same ships come crewed by veterans - tougher hulls and a faster rate of fire,
	// so the pressure is about out-lasting their sustained broadsides.
	var _vet = clamp(G.level, 0, 11);
	var _hp_k = 1 + 0.035 * _vet, _rof_k = 1 + 0.02 * _vet;
	var _enemies = [];
	var _n = array_length(_defs);
	for (var i = 0; i < _n; i++) {
		var d = _defs[i];
		var _hp = round(d.hp * _hp_k);
		var _guns = d.guns;
		if (d.behavior == "stationary") { _hp = round(d.hp * (1 + 0.3 * _vet)); _guns = d.guns + _vet; }   // forts grow with your level
		array_push(_enemies, {
			def: d, hp: _hp, max_hp: _hp, guns: _guns, thaco: d.thaco,
			reload: 1.2 + random(1.5), reload_time: d.reload * RELOAD_K / (eff("combat_enemy_speed", 1) * _rof_k),
			wait: 0, tried_flee: false, state: "alive", fade: 0,
			x: 1180 - (i + 0.5) * min(250, 640 / _n) + (i mod 2) * 30, y: ENEMY_PLANE_Y + (i mod 2) * 26,
			bob: random(6), shake: 0, burn: 0,
		});
	}
	if (_fort) {   // fort on the island to the right, guard ships in the water to its left
		_enemies[0].x = 1050; _enemies[0].y = ENEMY_PLANE_Y - 26;
		for (var i = 1; i < _n; i++) { _enemies[i].x = 780 - (i - 1) * 210; _enemies[i].y = ENEMY_PLANE_Y + 14 + (i mod 2) * 20; }
	}

	// Allies: your flagship plus the rest of your fleet.
	var _sd = ship_def();
	var _allies = [{ name: G.ship.name, sprite: _sd.sprite, hp: G.ship.hp, max_hp: ship_max_hp(), thaco: _sd.thaco,
	                 flagship: true, item: "", ship: G.ship, guns: G.ship.guns, reload: 0, reload_time: 0, state: "alive", fade: 0, bob: 0, shake: 0, burn: 0, cannons: [] }];
	// Your other ships fight with full broadsides on their own reload.
	for (var i = 0; i < array_length(G.fleet); i++) {
		var fs = G.fleet[i], fd = ship_def_of(fs);
		if (fs.hp <= 0) continue;
		array_push(_allies, { name: fs.name, sprite: fd.sprite, hp: fs.hp, max_hp: ship_max_hp_of(fs), thaco: fd.thaco, flagship: false,
			item: "", ship: fs, guns: fs.guns, reload: 1 + random(2), reload_time: fd.reload * RELOAD_K / max(0.2, eff("combat_speed", 1)), state: "alive", fade: 0, bob: random(6), shake: 0, burn: 0, cannons: [] });
		// Each gun of an escort runs its own reload loop too (same overall rate as a full broadside).
		var _ea = _allies[array_length(_allies) - 1];
		var _ep = _ea.reload_time * ((_weather == "rain") ? 1.1 : 1);
		for (var k = 0; k < fs.guns; k++) { var _pp = _ep * random_range(0.9, 1.1); array_push(_ea.cannons, { t: random(_pp), period: _pp, ammo: "", broken: false }); }
	}
	var _na = array_length(_allies);
	// Flagship in front; the rest of the fleet sails a row further back, spread evenly so hulls never overlap.
	var _m = _na - 1;
	for (var i = 0; i < _na; i++) {
		if (i == 0) { _allies[i].x = 440; _allies[i].y = ALLY_PLANE_Y; _allies[i].s = ALLY_PLANE_S; continue; }
		_allies[i].x = lerp(230, 1130, (i - 0.5) / _m) + ((i mod 2) ? -20 : 20);
		_allies[i].y = ALLY_PLANE_Y - 66;
		_allies[i].s = ALLY_PLANE_S * 0.64;
	}

	// Your cannons: each fires on its own loop, starting at a random point of its reload.
	var _period = _sd.reload * RELOAD_K / max(0.2, eff("combat_speed", 1));
	if (_weather == "rain") _period *= 1.1;
	var _cannons = [];
	for (var i = 0; i < G.ship.guns; i++) {
		var _p = _period * random_range(0.9, 1.1);
		array_push(_cannons, { t: random(_p), period: _p, ammo: "", broken: false });
	}
	_allies[0].cannons = _cannons;   // the same array: the flagship's gun deck

	global.C = {
		def: _main, special: _special, weather: _weather,
		enemies: _enemies, allies: _allies, cannons: _cannons, target: 0, hover: -1, fort: _fort, view: 0,
		flee_chance: eff("flee_success_base", 30), flee_cooldown: 0,
		shots: [], fx: [], parts: [], booty: 0, sunk: 0, special_kind: "", guns_lost: 0,
		result: "", result_text: "", time: 0, msg: "", msg_t: 0,
	};
	ui_go("combat");
}

function combat_hit_chance(_target_thaco, _bonus) {
	var _w = (global.C.weather == "fog") ? -10 : 0;
	return clamp(_target_thaco + _bonus + _w, 0, 100);
}

function combat_alive(_ship) { return _ship.state == "alive"; }

/// Returns the selected enemy index, retargeting to the next ship still afloat.
function combat_target() {
	var C = global.C;
	var _n = array_length(C.enemies);
	for (var k = 0; k < _n; k++) {
		var i = (C.target + k) mod _n;
		if (combat_alive(C.enemies[i])) { C.target = i; return i; }
	}
	return -1;
}

function combat_spawn_shot(_from, _to, _hit, _dmg, _ammo, _delay) {
	var C = global.C;
	var _x0 = _from.x + random_range(-50, 50), _y0 = _from.y - 10 + random_range(-10, 10);
	var _tx = _to.x, _ty = _to.y;
	if (_hit) { _tx += random_range(-60, 60); _ty += random_range(-20, 20); }
	else { _tx += random_range(-180, 180); _ty += choose(-1, 1) * random_range(40, 80); }
	array_push(C.shots, { x0: _x0, y0: _y0, x1: _tx, y1: _ty, t: -_delay, dur: 0.8 + random(0.3),
		from: _from, to: _to, hit: _hit, dmg: _dmg, ammo: _ammo, fired: false, spin: random(360) });
}

/// Fires one of your cannons at the current target (with its loaded special ammo, if any).
/// Fire pots and powder kegs ("multi" ammo) burst and spread to every other enemy ship.
function combat_spread(_s) {
	var C = global.C;
	if (_s.ammo == "cannon" || string_pos("spread", _s.ammo) == 1) return;
	var _a = variable_struct_get(global.D.ammo, _s.ammo);
	if (!_a.multi) return;
	for (var i = 0; i < array_length(C.enemies); i++) {
		var e = C.enemies[i];
		if (e == _s.to || !combat_alive(e)) continue;
		array_push(C.shots, { x0: _s.x1, y0: _s.y1, x1: e.x + random_range(-40, 40), y1: e.y + random_range(-10, 10), t: -0.05 * i, dur: 0.55,
			to: e, hit: true, dmg: max(1, round(_a.damage * 0.6)), ammo: "spread_" + _s.ammo, fired: true, spin: 0 });
	}
}

function combat_cannon_fire(_c) {
	var C = global.C, G = global.G, D = global.D;
	var _ti = combat_target();
	if (_ti < 0) return;
	var _tgt = C.enemies[_ti];
	var _acc = eff("combat_player_accuracy", 0);
	var _from = C.allies[0];
	if (_c.ammo != "") {
		var _a = variable_struct_get(D.ammo, _c.ammo);
		// Special shot never misses: it is the player's deliberate play.
		combat_spawn_shot(_from, _tgt, true, _a.damage, _c.ammo, 0);
		combat_msg(trf("{0} - a direct hit!", _a.name));
		_c.ammo = "";
	} else {
		combat_spawn_shot(_from, _tgt, roll100() < combat_hit_chance(_tgt.thaco, _acc), 1, "cannon", 0);
	}
}

/// Loads a special ammo onto the next cannon to fire. Stock is spent when it is loaded.
function combat_attach(_ammo) {
	var C = global.C, G = global.G;
	var _left = variable_struct_get(G.ship.ammo, _ammo);
	if (_left <= 0 || C.result != "") return false;
	var _best = -1, _bk = -1;
	for (var i = 0; i < array_length(C.cannons); i++) {
		var c = C.cannons[i];
		if (c.ammo != "" || c.broken) continue;
		var _k = c.t / c.period;
		if (_k > _bk) { _bk = _k; _best = i; }
	}
	if (_best < 0) { combat_msg("Every cannon is already loaded."); return false; }
	C.cannons[_best].ammo = _ammo;
	variable_struct_set(G.ship.ammo, _ammo, _left - 1);
	return true;
}

/// Picks the ally an enemy aims at: the flagship most of the time.
function combat_enemy_aim() {
	var C = global.C;
	var _alive = [];
	for (var i = 0; i < array_length(C.allies); i++) if (combat_alive(C.allies[i])) array_push(_alive, C.allies[i]);
	if (array_length(_alive) > 1 && irandom(99) >= 60) return _alive[1 + irandom(array_length(_alive) - 2)];
	return C.allies[0];
}

function combat_enemy_fire(_e) {
	var _acc = eff("combat_enemy_accuracy", 0) + struct_get_or(_e.def, "acc", 0);
	for (var i = 0; i < _e.guns; i++) {
		var _to = combat_enemy_aim();
		combat_spawn_shot(_e, _to, roll100() < combat_hit_chance(_to.thaco, _acc), 1, "cannon", i * 0.07);
	}
	_e.reload = _e.reload_time;
}

/// A hit on one of your ships may knock a cannon off its carriage for good (replace it at a shipyard).
/// The heavier the shooter's broadside, the likelier: about 2% a hit from a 4-gun sloop, 4-6% from a fort.
function combat_gun_hit(_s) {
	var C = global.C, G = global.G;
	var _fp = struct_get_or(_s, "from", undefined);
	var _guns = (_fp != undefined) ? struct_get_or(_fp, "guns", 4) : 4;
	if (random(1) >= min(0.06, 0.012 + 0.0015 * _guns)) return;
	var a = _s.to;
	// Knocked-out guns stay on the deck, marked and useless, so you can see what you have lost.
	var _ok = [];
	for (var k = 0; k < array_length(a.cannons); k++) if (!a.cannons[k].broken) array_push(_ok, k);
	if (array_length(_ok) <= 1) return;   // the last gun is never lost
	// Prefer an empty gun; a loaded special shot is lost with its cannon.
	var _empty = [];
	for (var k = 0; k < array_length(_ok); k++) if (a.cannons[_ok[k]].ammo == "") array_push(_empty, _ok[k]);
	var _pick = (array_length(_empty) > 0) ? arr_pick(_empty) : arr_pick(_ok);
	var c = a.cannons[_pick];
	c.broken = true; c.ammo = ""; c.t = 0;
	a.guns = array_length(_ok) - 1;
	a.ship.guns = a.guns;
	C.guns_lost += 1;
	fx_hit(_s.x1, _s.y1, "firepot", 1.1);
	combat_msg(trf("A cannon on the {0} is blown off its carriage!", a.name));
}

function combat_try_flee() {
	var C = global.C;
	if (C.result != "" || C.flee_cooldown > 0) return;
	if (roll100() < C.flee_chance) {
		combat_end("fled", trf("You crowd on sail and slip away from the {0}.", C.def.name));
	} else {
		C.flee_chance = min(eff("flee_success_max", 80), C.flee_chance + eff("flee_success_inc", 10));
		C.flee_cooldown = 2.0;
		combat_msg(trf("They cut you off! Next attempt: {0}%", floor(C.flee_chance)));
	}
}

function combat_msg(_s) { global.C.msg = _s; global.C.msg_t = 3; }

function combat_update(_dt) {
	var C = global.C, G = global.G;
	C.time += _dt;
	C.msg_t -= _dt;
	for (var i = 0; i < array_length(C.enemies); i++) { var e = C.enemies[i]; if (e.state != "alive") e.fade += _dt; }
	for (var i = 0; i < array_length(C.allies); i++) { var a = C.allies[i]; if (a.state != "alive") a.fade += _dt; }
	if (C.result != "") return;
	C.flee_cooldown = max(0, C.flee_cooldown - _dt);

	// Your cannons.
	for (var i = 0; i < array_length(C.cannons); i++) {
		var c = C.cannons[i];
		if (c.broken) continue;
		c.t += _dt;
		if (c.t >= c.period) { c.t -= c.period; combat_cannon_fire(c); }
	}
	// Escorts: every working gun fires at your target on its own reload.
	for (var i = 1; i < array_length(C.allies); i++) {
		var a = C.allies[i];
		if (!combat_alive(a)) continue;
		for (var k = 0; k < array_length(a.cannons); k++) {
			var c = a.cannons[k];
			if (c.broken) continue;
			c.t += _dt;
			if (c.t < c.period) continue;
			c.t -= c.period;
			var _ti = combat_target();
			if (_ti >= 0) { var _t = C.enemies[_ti]; combat_spawn_shot(a, _t, roll100() < combat_hit_chance(_t.thaco, 0), 1, "cannon", 0); }
		}
	}
	// Enemy behaviours.
	for (var i = 0; i < array_length(C.enemies); i++) {
		var e = C.enemies[i];
		if (!combat_alive(e)) continue;
		e.reload -= _dt;
		var _behave = behavior_get(e.def.behavior);
		var _act = _behave(e, C, _dt);
		if (_act == "fire") combat_enemy_fire(e);
		else if (_act == "flee" && !(C.special && i == 0)) { e.state = "fled"; combat_msg(trf("The {0} breaks off and flees.", e.def.name)); }
	}
	// Shots in flight.
	for (var i = array_length(C.shots) - 1; i >= 0; i--) {
		var s = C.shots[i];
		s.t += _dt;
		if (!s.fired && s.t >= 0) { s.fired = true; fx_muzzle(s.x0, s.y0, s.x1 > s.x0 ? 1 : -1, s.y0 < 420 ? 0.75 : 1); }
		if (s.t < s.dur) continue;
		if (s.hit) {
			fx_hit(s.x1, s.y1, s.ammo, s.y1 < 420 ? 0.8 : 1.1);
			combat_spread(s);
			if (combat_alive(s.to)) {
				s.to.hp -= s.dmg;
				var _sc = struct_get_or(s.to, "s", ENEMY_PLANE_S);
				fx_plunk(s.x1, s.y1, s.to.y + 58 * _sc, _sc);
				if (string_pos("firepot", s.ammo) > 0 || string_pos("bomb", s.ammo) > 0) s.to.burn = max(s.to.burn, 4);
				if (variable_struct_exists(s.to, "flagship")) combat_gun_hit(s);   // only your ships have "flagship"
			}
		} else fx_splash(s.x1, s.y1, s.y1 < 420 ? 0.8 : 1.1);
		array_delete(C.shots, i, 1);
	}
	fx_update(_dt);
	var _sh = [C.enemies, C.allies];
	for (var k = 0; k < 2; k++) for (var i = 0; i < array_length(_sh[k]); i++) {
		var o = _sh[k][i];
		o.shake = max(0, o.shake - _dt);
		if (o.burn > 0) {
			o.burn -= _dt;
			if (random(1) < _dt * 22) fx_flame(o.x + random_range(-60, 60) * (k == 0 ? ENEMY_PLANE_S : 1), o.y + random_range(-30, 10), k == 0 ? ENEMY_PLANE_S : 1);
		}
		if (o.state == "sunk" && o.fade < 2.5 && random(1) < _dt * 14) fx_smoke(o.x + random_range(-50, 50), o.y - 10, 1.2);
	}

	// Sinkings.
	var _afloat = 0;
	for (var i = 0; i < array_length(C.enemies); i++) {
		var e = C.enemies[i];
		if (e.state == "alive" && e.hp <= 0) {
			e.state = "sunk";
			C.sunk += 1;
			G.stats.sunk += 1;
			C.booty += floor(e.def.booty * random_range(0.75, 1.25));
			combat_msg(trf("The {0} is going down!", e.def.name));
		}
		if (e.state == "alive") _afloat++;
	}
	for (var i = 1; i < array_length(C.allies); i++) {
		var a = C.allies[i];
		a.ship.hp = max(0, a.hp);
		if (a.state == "alive" && a.hp <= 0) {
			a.state = "sunk";
			for (var k = 0; k < array_length(G.fleet); k++) if (G.fleet[k] == a.ship) { array_delete(G.fleet, k, 1); break; }
			var _lost = cargo_trim();
			log_add(trf("The {0} was sunk in battle.", a.name));
			combat_msg(trf("The {0} is going down!", a.name) + (_lost != "" ? " " + trf("Lost {0}.", _lost) : ""));
		}
	}
	G.ship.hp = max(0, C.allies[0].hp);
	if (G.ship.hp <= 0) combat_lose();
	else if (_afloat == 0) {
		if (C.sunk > 0) combat_win();
		else combat_end("enemy_fled", tr("The enemy breaks off and flees. No prize today."));
	}
}

function combat_win() {
	var C = global.C, G = global.G, D = global.D;
	var _booty = C.booty;
	G.cash += _booty;
	G.stats.wins += 1;
	var _who = (C.sunk > 1) ? trf("{0} ships strike their colours!", C.sunk) : trf("The {0} strikes her colours!", C.def.name);
	var _txt = _who + " " + trf("You take {0} in plunder.", fmt_money(_booty));
	if (irandom(99) < 40 && cargo_free() > 0) {
		var _cands = [];
		for (var k = 0; k < array_length(D.goods_list); k++) {
			var g = D.goods_list[k];
			if (variable_struct_get(G.goods, g.id).unlocked) array_push(_cands, g.id);
		}
		var _gid = arr_pick(_cands);
		var _q = min(cargo_free(), irandom_range(2, 10) * C.sunk);
		cargo_add(_gid, _q, 0);
		_txt += " " + trf("Their holds yield {0} {1}.", _q, variable_struct_get(D.goods, _gid).name);
	}
	log_add(C.sunk > 1 ? trf("Defeated the {0} and {1} more ({2}).", C.def.name, C.sunk - 1, fmt_money(_booty)) : trf("Defeated the {0} ({1}).", C.def.name, fmt_money(_booty)));
	level_update();
	combat_end("won", _txt);
	contracts_on_sink(C.sunk);
	if (C.special && C.enemies[0].state == "sunk") {
		if (C.special_kind == "hunt") contracts_on_hunt_won(global.V != undefined ? global.V.to : G.port);
		else campaign_on_battle_won(C.def.id);
	}
}

function combat_lose() {
	var C = global.C, G = global.G;
	G.stats.losses += 1;
	G.cargo = {};
	var _lost = floor(G.cash / 2);
	G.cash -= _lost;
	G.ship.hp = 1;
	log_add(trf("Boarded by the {0}. Lost all cargo and {1}.", C.def.name, fmt_money(_lost)));
	combat_end("lost", tr("Your ship is boarded. They strip your hold and half your purse, then leave you drifting with a shattered hull."));
}

function combat_end(_result, _text) {
	var C = global.C;
	if (C.guns_lost > 0) {
		_text += " " + trn(C.guns_lost, "{0} cannon was knocked out; a shipyard can replace it.", "{0} cannons were knocked out; a shipyard can replace them.");
		log_add(trn(C.guns_lost, "{0} cannon knocked out in the fight.", "{0} cannons knocked out in the fight."));
	}
	C.result = _result;
	C.result_text = _text;
}

// ---- drawing -----------------------------------------------------------------------------
/// Ships look more battered as they lose hull: sprite variants _d1 (<=80%), _d2 (<=50%), _d3 (<=25%).
/// Slim hull bar with no numbers, centred on (_x, _y).
function combat_hp_bar(_s, _x, _y, _w, _col) {
	var _f = clamp(_s.hp / max(1, _s.max_hp), 0, 1);
	draw_set_alpha(0.75); draw_set_colour(c_black);
	draw_rectangle(_x - _w / 2 - 1, _y - 1, _x + _w / 2 + 1, _y + 5, false);
	draw_set_alpha(1);
	draw_set_colour(_f > 0.5 ? _col : (_f > 0.25 ? make_colour_rgb(230, 180, 60) : make_colour_rgb(220, 60, 50)));
	if (_f > 0) draw_rectangle(_x - _w / 2, _y, _x - _w / 2 + _w * _f, _y + 4, false);
}

function ship_sprite_hp(_base, _frac) {
	var _k = (_frac <= 0.25) ? 3 : ((_frac <= 0.5) ? 2 : ((_frac <= 0.8) ? 1 : 0));
	if (_k > 0 && spr(_base + "_d" + string(_k)) >= 0) return _base + "_d" + string(_k);
	return _base;
}

function combat_ship_draw(_s, _sprite, _scale, _flip, _phase) {
	var C = global.C;
	_sprite = ship_sprite_hp(_sprite, max(0, _s.hp) / max(1, _s.max_hp));
	var _d = struct_get_or(_s, "def", undefined);   // allies have no def
	if (_d != undefined && struct_get_or(_d, "behavior", "") == "stationary") {
		// A building: no bobbing; when destroyed it crumbles into smoke instead of sinking.
		var _gone = (_s.state != "alive") ? min(1, _s.fade / 3) : 0;
		if (_gone >= 1) return;
		draw_spr(_sprite, _s.x, _s.y + _gone * 18, 0.95, 1 - _gone, false, 0);
		return;
	}
	var _sink = (_s.state == "sunk") ? min(1, _s.fade / 2.5) : 0;
	var _flee = (_s.state == "fled") ? min(1, _s.fade / 2.5) : 0;
	var _x = _s.x + (_flee * 500) * (_flip ? 1 : -1);
	var _y = _s.y + sin(C.time * 1.5 + _phase) * 5 * _scale + _sink * 60;
	var _a = 1 - max(_sink, _flee);
	if (_a <= 0) return;
	draw_spr(_sprite, _x, _y, _scale, _a, _flip, sin(C.time * 1.5 + _phase) * 2 + _sink * (_flip ? -18 : 18));
}

function combat_draw() {
	var C = global.C, G = global.G, D = global.D, U = global.UI;
	// Sky, distant sea, near sea (depth darkens toward the viewer).
	draw_rectangle_colour(0, 0, 1280, 250, make_colour_rgb(110, 165, 210), make_colour_rgb(110, 165, 210), make_colour_rgb(222, 232, 236), make_colour_rgb(222, 232, 236), false);
	draw_rectangle_colour(0, 250, 1280, 720, make_colour_rgb(70, 150, 185), make_colour_rgb(70, 150, 185), make_colour_rgb(16, 52, 92), make_colour_rgb(16, 52, 92), false);
	draw_set_colour(c_white);
	for (var i = 0; i < 60; i++) {
		var _wy = 262 + power((i * 37) mod 100 / 100, 1.4) * 440;
		var _k = (_wy - 250) / 470;
		var _wx = (i * 197 + C.time * (14 + 30 * _k)) mod 1320 - 20;
		draw_set_alpha(0.12 + 0.22 * _k);
		draw_line_width(_wx, _wy, _wx + 10 + 26 * _k, _wy, 1 + 2 * _k);
	}
	draw_set_alpha(1);

	if (struct_get_or(C, "fort", false)) combat_draw_island();
	// Enemy plane (background), with target selection by click.
	C.hover = -1;
	for (var i = 0; i < array_length(C.enemies); i++) {
		var e = C.enemies[i];
		combat_ship_draw(e, e.def.sprite, ENEMY_PLANE_S, e.def.sprite != "fort", e.bob);
		if (!combat_alive(e)) continue;
		var _hw = 105, _hh = 85;
		if (e.def.behavior == "stationary") { _hw = 130; _hh = 110; }
		if (C.result == "" && ui_hover(e.x - _hw, e.y - _hh, _hw * 2, _hh * 2)) {
			C.hover = i;
			if (U.click) { C.target = i; U.click = false; }
		}
	}
	var _ti = combat_target();
	for (var i = 0; i < array_length(C.enemies); i++) {
		var e = C.enemies[i];
		if (!combat_alive(e)) continue;
		var _sel = (i == _ti);
		if (_sel || i == C.hover) {
			var _r = 74 + sin(C.time * 5) * 4;
			draw_set_colour(_sel ? make_colour_rgb(230, 60, 50) : c_white);
			draw_set_alpha(_sel ? 0.9 : 0.5);
			draw_circle(e.x, e.y + 10, _r, true); draw_circle(e.x, e.y + 10, _r - 2, true);
			if (_sel) for (var k = 0; k < 4; k++) {
				var _ang = k * 90 + C.time * 30;
				draw_line_width(e.x + lengthdir_x(_r - 10, _ang), e.y + 10 + lengthdir_y(_r - 10, _ang), e.x + lengthdir_x(_r + 10, _ang), e.y + 10 + lengthdir_y(_r + 10, _ang), 3);
			}
			draw_set_alpha(1);
		}
		var _top = (e.def.behavior == "stationary") ? 130 : 96;
		combat_hp_bar(e, e.x, e.y + sin(C.time * 1.5 + e.bob) * 5 * ENEMY_PLANE_S - _top, 96, make_colour_rgb(214, 70, 56));
		ui_text(e.x + 1, e.y - _top - 21, e.def.name, 0.8, c_black, fa_center);
		ui_text(e.x, e.y - _top - 22, e.def.name, 0.8, c_white, fa_center);
	}

	// Ally plane (foreground). Click one of your ships to show its guns on the left.
	if (!combat_alive(C.allies[C.view])) C.view = 0;
	if (C.result == "" && U.click) for (var i = 0; i < array_length(C.allies); i++) {   // front ship first
		var a = C.allies[i];
		if (combat_alive(a) && ui_hover(a.x - 110 * a.s, a.y - 100 * a.s, 220 * a.s, 170 * a.s)) { C.view = i; U.click = false; break; }
	}
	var _multi = array_length(C.allies) > 1;
	for (var i = array_length(C.allies) - 1; i >= 0; i--) {
		var a = C.allies[i];
		if (_multi && i == C.view && combat_alive(a)) {   // the ship whose guns are shown: a gold ring on the water
			draw_set_colour(UI_GOLD); draw_set_alpha(0.7);
			draw_ellipse(a.x - 100 * a.s, a.y + 44 * a.s, a.x + 100 * a.s, a.y + 74 * a.s, true);
			draw_ellipse(a.x - 99 * a.s, a.y + 45 * a.s, a.x + 99 * a.s, a.y + 73 * a.s, true);
			draw_set_alpha(1);
		}
		combat_ship_draw(a, a.sprite, a.s, false, a.bob);
		if (combat_alive(a)) combat_hp_bar(a, a.x, a.y + sin(C.time * 1.5 + a.bob) * 5 * a.s - 112 * a.s, 120 * a.s, make_colour_rgb(80, 196, 100));
	}

	// Cannonballs on parabolic arcs; fire pots and kegs glow.
	for (var i = 0; i < array_length(C.shots); i++) {
		var s = C.shots[i];
		if (s.t < 0) continue;
		var k = s.t / s.dur;
		var _x = lerp(s.x0, s.x1, k);
		var _arc = (string_pos("spread", s.ammo) == 1) ? 40 : 110;
		var _y = lerp(s.y0, s.y1, k) - sin(k * pi) * _arc;
		if (s.ammo == "chains") {
			// Two balls joined by a chain, tumbling slowly in flight.
			var _ang = s.spin + s.t * 240, _r = 11;
			var _ax = _x + lengthdir_x(_r, _ang), _ay = _y + lengthdir_y(_r, _ang);
			var _bx = _x - lengthdir_x(_r, _ang), _by = _y - lengthdir_y(_r, _ang);
			draw_set_colour(make_colour_rgb(90, 90, 96));
			for (var q = 0; q <= 6; q++) draw_circle(lerp(_ax, _bx, q / 6), lerp(_ay, _by, q / 6) + sin(q / 6 * pi) * 2, 1.4, false);
			draw_set_colour(make_colour_rgb(28, 28, 30));
			draw_circle(_ax, _ay, 4.5, false); draw_circle(_bx, _by, 4.5, false);
			continue;
		}
		var _big = s.ammo != "cannon";
		if (_big) {   // burning projectile: flickering flame tail
			gpu_set_blendmode(bm_add);
			for (var k = 1; k <= 4; k++) {
				var kk = max(0, k - 0.0) * 0.025;
				var _px = lerp(s.x0, s.x1, max(0, (s.t / s.dur) - kk)), _py = lerp(s.y0, s.y1, max(0, (s.t / s.dur) - kk)) - sin(max(0, (s.t / s.dur) - kk) * pi) * 110;
				draw_set_alpha(0.5 - k * 0.1); draw_set_colour(make_colour_rgb(255, 140 - k * 20, 40));
				draw_circle(_px + random_range(-2, 2), _py + random_range(-2, 2), 7 - k, false);
			}
			gpu_set_blendmode(bm_normal); draw_set_alpha(1);
		}
		draw_set_colour(_big ? make_colour_rgb(255, 200, 90) : make_colour_rgb(28, 28, 28));
		draw_circle(_x, _y, _big ? 5 : 4, false);
	}
	fx_draw();
	if (C.weather == "fog") { draw_set_alpha(0.35); draw_set_colour(c_white); draw_rectangle(0, 0, 1280, 720, false); draw_set_alpha(1); }
	if (C.weather == "rain") {
		draw_set_colour(make_colour_rgb(200, 220, 240)); draw_set_alpha(0.5);
		for (var i = 0; i < 120; i++) {
			var _rx = (i * 113 + C.time * 400) mod 1280;
			var _ry = (i * 71 + C.time * 900) mod 720;
			draw_line(_rx, _ry, _rx - 6, _ry + 16);
		}
		draw_set_alpha(1);
	}

	if (C.msg_t > 0) ui_text(640, 150, C.msg, 1.3, c_white, fa_center);
	if (_ti >= 0 && C.result == "") {
		var _hit = combat_hit_chance(C.enemies[_ti].thaco, eff("combat_player_accuracy", 0));
		ui_text(1240, 30, trf("Target: {0}  ({1}% to hit)", C.enemies[_ti].def.name, floor(_hit)), 1, c_white, fa_right);
		if (array_length(C.enemies) > 1) ui_text(1240, 54, "Click a ship to change target", 0.9, make_colour_rgb(220, 230, 240), fa_right);
		if (C.weather != "") ui_text(1240, 76, trf("Weather: {0}", tr(C.weather)), 0.9, make_colour_rgb(220, 230, 240), fa_right);
		if (array_length(C.allies) > 1) ui_text(1240, 98, "Click your ships to see their guns", 0.9, make_colour_rgb(220, 230, 240), fa_right);
	}

	if (C.result == "") {
		// Gun deck: a queue of reload dials down the left edge; when it fills the screen height it
		// continues in another column to the right.
		// Shows the guns of whichever of your ships you clicked (the flagship by default).
		var _va = C.allies[C.view];
		var _guns = _va.cannons;
		var _n = array_length(_guns);
		var _pitch = 38, _rad = 15, _top = 50, _per = floor((590 - _top) / _pitch);
		var _cols = max(1, ceil(_n / _per)), _rows = min(_n, _per);
		var _title = (array_length(C.allies) > 1) ? _va.name : "Guns";
		var _tw = min(300, ui_text_width(_title, 0.85) + 20);
		draw_set_alpha(0.55); draw_set_colour(c_black);
		draw_roundrect(10, 10, 30 + _cols * _pitch, _top + max(1, _rows) * _pitch - 8, false);
		if (_title != "Guns" && _tw > 20 + _cols * _pitch) draw_roundrect(10, 10, 10 + _tw, 40, false);
		draw_set_alpha(1);
		ui_text(20, 16, _title, 0.85, UI_GOLD, fa_left, fa_top, 280);
		for (var i = 0; i < _n; i++) {
			var c = _guns[i];
			var _cx = 20 + _pitch / 2 + (i div _per) * _pitch, _cy = _top + _pitch / 2 - 4 + (i mod _per) * _pitch;
			var _k = c.t / c.period;
			var _ri = _rad * 0.82;
			draw_set_colour(make_colour_rgb(30, 24, 20)); draw_circle(_cx, _cy, _rad, false);
			draw_set_colour(_k > 0.85 ? make_colour_rgb(250, 210, 90) : make_colour_rgb(160, 140, 110));
			for (var s = 0; s < 24 * _k; s++) {
				var _a0 = 90 - s * 15;
				draw_line_width(_cx + lengthdir_x(_ri, _a0), _cy + lengthdir_y(_ri, _a0), _cx + lengthdir_x(_ri, _a0 - 15), _cy + lengthdir_y(_ri, _a0 - 15), max(2, _rad * 0.24));
			}
			if (c.ammo != "") {
				draw_set_colour(c.ammo == "firepot" ? make_colour_rgb(255, 120, 40) : (c.ammo == "chains" ? make_colour_rgb(170, 180, 200) : make_colour_rgb(150, 90, 50)));
				draw_circle(_cx, _cy, _rad * 0.47, false);
			} else { draw_set_colour(make_colour_rgb(20, 20, 20)); draw_circle(_cx, _cy, _rad * 0.35, false); }
			if (c.broken) {   // knocked out: kept on the list so you know, but it no longer fires
				draw_set_colour(make_colour_rgb(30, 24, 20)); draw_circle(_cx, _cy, _rad, false);
				draw_set_colour(make_colour_rgb(225, 50, 40));
				var _q = _rad * 0.62;
				draw_line_width(_cx - _q, _cy - _q, _cx + _q, _cy + _q, 4);
				draw_line_width(_cx - _q, _cy + _q, _cx + _q, _cy - _q, 4);
			}
		}
		if (_n == 0) ui_text(20, 60, "No cannons!", 0.9, make_colour_rgb(255, 200, 180));
		// Special ammo (click or keys 1-3 load it onto the next gun to fire) and Flee, in one bar at the bottom.
		var _na = array_length(D.ships.ammo) - 1;
		var _bw = _na * 160 + 190;
		var _ax = 640 - _bw / 2 + 20;
		ui_panel(_ax - 20, 616, _bw + 30, 84, make_colour_rgb(70, 52, 40));
		for (var i = 0; i < array_length(D.ships.ammo); i++) {
			var a = D.ships.ammo[i];
			if (a.id == "cannon") continue;
			var _left = variable_struct_get(G.ship.ammo, a.id);
			if (ui_button(_ax, 628, 150, 52, trf("{0} ({1})", a.name, _left), _left > 0, make_colour_rgb(150, 80, 40))
				|| (keyboard_check_pressed(ord(string(i))) && ui_enabled())) combat_attach(a.id);
			_ax += 160;
		}
		if (ui_button(_ax + 10, 628, 150, 52, trf("Flee {0}%", floor(C.flee_chance)), C.flee_cooldown <= 0, make_colour_rgb(90, 90, 110))) combat_try_flee();
	} else {
		ui_panel(320, 190, 640, 330);
		var _t = (C.result == "won") ? "Victory!" : ((C.result == "lost") ? "Defeat" : "Disengaged");
		ui_text(640, 212, _t, 2.4, UI_INK, fa_center);
		ui_text_box(350, 276, 580, C.result_text, 1.15, UI_INK, 160);
		if (ui_button(540, 448, 200, 50, "Continue")) voyage_after_battle(C.result);
	}
}

/// The fort's island on the horizon plane: shallows, beach, green hills and palms.
function combat_draw_island() {
	var _y = ENEMY_PLANE_Y + 34;
	draw_set_alpha(0.45); draw_set_colour(make_colour_rgb(120, 200, 205));
	draw_ellipse(700, _y - 30, 1420, _y + 44, false);
	draw_set_alpha(1);
	draw_set_colour(make_colour_rgb(222, 200, 146)); draw_ellipse(740, _y - 46, 1380, _y + 22, false);
	// Hills: overlapping mounds (half-ellipses), lighter at the top.
	var _base = _y - 30;
	var _hills = [[1120, 220, 120], [910, 170, 80], [1270, 150, 90], [1010, 130, 60]];   // [x, half width, height]
	for (var i = 0; i < array_length(_hills); i++) {
		var h = _hills[i];
		var _top = make_colour_rgb(124, 162, 92), _bot = make_colour_rgb(70, 108, 62);
		draw_primitive_begin(pr_trianglefan);
		draw_vertex_colour(h[0], _base, _bot, 1);
		for (var a = 0; a <= 20; a++) {
			var _t = a / 20 * pi;
			var _hy = _base - sin(_t) * h[2];
			draw_vertex_colour(h[0] - cos(_t) * h[1], _hy, merge_colour(_bot, _top, sin(_t)), 1);
		}
		draw_primitive_end();
	}
	draw_set_colour(make_colour_rgb(110, 150, 84));
	draw_ellipse(760, _y - 60, 1360, _y - 8, false);
	// Palms along the beach.
	for (var i = 0; i < 7; i++) {
		var _px = 790 + i * 82 + (i mod 2) * 24, _py = _y - 30 - (i mod 3) * 6;
		draw_set_colour(make_colour_rgb(110, 80, 50)); draw_line_width(_px, _py, _px + 6, _py - 40, 3);
		draw_set_colour(make_colour_rgb(46, 110, 60));
		for (var k = 0; k < 5; k++) {
			var _a = 200 + k * 35;
			draw_line_width(_px + 6, _py - 40, _px + 6 + lengthdir_x(22, _a + 160), _py - 40 + lengthdir_y(12, _a + 160) + 4, 3);
		}
	}
}
