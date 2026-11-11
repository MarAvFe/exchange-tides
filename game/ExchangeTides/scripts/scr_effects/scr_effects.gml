// ===== Effect / modifier system ============================================================
// Mirrors the original engine (docs/MECHANICS.md §3): every owned item carries effect strings
// "name(value);name2(value)". Value grammar:  N = set,  +N/-N = add,  +N%/-N% = scale.
// Effects are applied in inventory order on top of a base value.

function effect_parse(_s) {
	var _ops = [];
	if (_s == "" || _s == undefined) return _ops;
	var _parts = str_split(_s, ";");
	for (var i = 0; i < array_length(_parts); i++) {
		var _p = str_trim(_parts[i]);
		var _open = string_pos("(", _p);
		var _close = string_pos(")", _p);
		if (_open <= 0 || _close <= _open) continue;
		var _name = string_copy(_p, 1, _open - 1);
		var _val = str_trim(string_copy(_p, _open + 1, _close - _open - 1));
		var _op = "set";
		var _first = string_char_at(_val, 1);
		if (_first == "+") { _op = "add"; _val = string_delete(_val, 1, 1); }
		else if (_first == "-") { _op = "sub"; _val = string_delete(_val, 1, 1); }
		var _pct = string_pos("%", _val) > 0;
		if (_pct) _val = string_replace_all(_val, "%", "");
		array_push(_ops, { name: _name, op: _op, pct: _pct, value: real(_val) });
	}
	return _ops;
}

/// All item ids currently affecting the player: inventory items + ship upgrades.
function effect_sources() {
	var G = global.G;
	var _src = [];
	for (var i = 0; i < array_length(G.items); i++) array_push(_src, G.items[i].id);
	for (var i = 0; i < array_length(G.ship.upgrades); i++) array_push(_src, G.ship.upgrades[i]);
	return _src;
}

function effect_eval(_name, _base) {
	if (!variable_global_exists("G") || global.G == undefined) return _base;
	return effect_eval_sources(effect_sources(), _name, _base);
}

function effect_eval_sources(_src, _name, _base) {
	var _v = _base;
	for (var i = 0; i < array_length(_src); i++) {
		if (!variable_struct_exists(global.EFFECTS, _src[i])) continue;
		var _ops = variable_struct_get(global.EFFECTS, _src[i]);
		for (var k = 0; k < array_length(_ops); k++) {
			var o = _ops[k];
			if (o.name != _name) continue;
			switch (o.op) {
				case "set": _v = o.value; break;
				case "add": _v = o.pct ? _v + _v * o.value / 100 : _v + o.value; break;
				case "sub": _v = o.pct ? _v - _v * o.value / 100 : _v - o.value; break;
			}
		}
	}
	return _v;
}

/// Base value from config.json (or a fallback), then modified by owned items.
function eff(_name, _fallback = 0) {
	return effect_eval(_name, struct_get_or(global.D.config, _name, _fallback));
}

function item_effect_text(_id) {
	var _it = variable_struct_get(global.D.items, _id);
	var _e = struct_get_or(_it, "effect", "");
	if (_e == "") return "";
	var _s = string_replace_all(_e, "_", " ");
	return string_replace_all(_s, ";", ", ");
}
