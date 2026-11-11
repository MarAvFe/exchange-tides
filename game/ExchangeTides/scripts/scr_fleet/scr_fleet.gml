// ===== Fleet: up to FLEET_MAX ships ==========================================================
// G.ship is the flagship (you sail and fight from it); G.fleet holds the other ships.
// Every ship: { type, name, hp, guns, upgrades[] }. Cargo space and cannons are pooled across the
// fleet; every ship fights beside you. Refits (upgrades) belong to one ship. Special ammo is the
// fleet's stock and always travels with the flagship (G.ship.ammo): fleet_pass_flag moves it.
#macro FLEET_MAX 5

function fleet_all() {
	var G = global.G;
	var _out = [G.ship];
	var _f = struct_get_or(G, "fleet", []);
	for (var i = 0; i < array_length(_f); i++) array_push(_out, _f[i]);
	return _out;
}

function fleet_size() { return 1 + array_length(global.G.fleet); }

function ship_def_of(_s) { return variable_struct_get(global.D.pships, _s.type); }

/// Effect value for one ship: carried items plus that ship's own refits.
function ship_eff(_s, _name, _base) {
	var G = global.G;
	var _src = [];
	for (var i = 0; i < array_length(G.items); i++) array_push(_src, G.items[i].id);
	for (var i = 0; i < array_length(_s.upgrades); i++) array_push(_src, _s.upgrades[i]);
	return effect_eval_sources(_src, _name, struct_get_or(global.D.config, _name, _base));
}

function ship_max_hp_of(_s) { return floor(ship_eff(_s, "ship_health", ship_def_of(_s).hp)); }
function ship_cargo_of(_s) { return floor(ship_eff(_s, "ship_space", ship_def_of(_s).cargo)); }
function ship_value(_s) { return floor(ship_def_of(_s).price * 0.5) + _s.guns * global.D.config.cannon_sell; }

function fleet_new_ship(_type) {
	var d = variable_struct_get(global.D.pships, _type);
	var _names = global.D.config.ship_names;
	var _name = arr_pick(_names);
	var _all = fleet_all();
	for (var tries = 0; tries < 20; tries++) {
		var _dup = false;
		for (var i = 0; i < array_length(_all); i++) if (_all[i].name == _name) _dup = true;
		if (!_dup) break;
		_name = arr_pick(_names);
	}
	return { type: _type, name: _name, hp: d.hp, guns: d.guns div 2, upgrades: [] };
}

/// Swap fleet ship _i (index into G.fleet) with the flagship.
/// Hands the flag (and the ammo store) from _from to _to.
function fleet_pass_flag(_from, _to) {
	_to.ammo = struct_get_or(_from, "ammo", { firepot: 0, chains: 0, bomb: 0 });
	if (variable_struct_exists(_from, "ammo") && _from != _to) variable_struct_remove(_from, "ammo");
}

function fleet_make_flagship(_i) {
	var G = global.G;
	var _old = G.ship;
	G.ship = G.fleet[_i];
	G.fleet[_i] = _old;
	fleet_pass_flag(_old, G.ship);
	log_add("The " + G.ship.name + " is your new flagship.");
}

/// Ship by fleet index: 0 = flagship, 1.. = G.fleet.
function fleet_get(_k) { return (_k == 0) ? global.G.ship : global.G.fleet[_k - 1]; }

function fleet_remove(_k) {
	var G = global.G;
	if (_k == 0) {
		if (array_length(G.fleet) == 0) return;
		var _old = G.ship;
		G.ship = G.fleet[0];
		array_delete(G.fleet, 0, 1);
		fleet_pass_flag(_old, G.ship);
	} else array_delete(G.fleet, _k - 1, 1);
	cargo_trim();
}

/// After losing hold space: jettison goods (most plentiful first) until the cargo fits.
function cargo_trim() {
	var G = global.G;
	var _over = cargo_used() - cargo_capacity();
	var _lost = "";
	while (_over > 0) {
		var _ids = variable_struct_get_names(G.cargo);
		if (array_length(_ids) == 0) break;
		var _best = _ids[0];
		for (var i = 1; i < array_length(_ids); i++) if (cargo_qty(_ids[i]) > cargo_qty(_best)) _best = _ids[i];
		var _q = min(_over, cargo_qty(_best));
		cargo_remove(_best, _q);
		_over -= _q;
		_lost += (_lost == "" ? "" : ", ") + string(_q) + " " + variable_struct_get(global.D.goods, _best).name;
	}
	if (_lost != "") log_add("Lost " + _lost + " with the ship's hold.");
	return _lost;
}
