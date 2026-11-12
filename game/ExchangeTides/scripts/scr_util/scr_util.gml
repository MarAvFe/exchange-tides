// ===== Generic helpers ==================================================================

function load_json(_path) {
	if (!file_exists(_path)) {
		show_debug_message("Missing data file: " + _path);
		return undefined;
	}
	var _buf = buffer_load(_path);
	if (_buf < 0) return undefined;
	var _txt = buffer_read(_buf, buffer_string);
	buffer_delete(_buf);
	return json_parse(_txt);
}

function save_text(_path, _txt) {
	var _buf = buffer_create(string_byte_length(_txt) + 1, buffer_fixed, 1);
	buffer_write(_buf, buffer_string, _txt);
	buffer_save(_buf, _path);
	buffer_delete(_buf);
}

function str_split(_s, _sep) {
	var _out = [];
	var _cur = "";
	var _n = string_length(_s);
	for (var i = 1; i <= _n; i++) {
		var _ch = string_char_at(_s, i);
		if (_ch == _sep) { array_push(_out, _cur); _cur = ""; }
		else _cur += _ch;
	}
	array_push(_out, _cur);
	return _out;
}

function str_trim(_s) {
	var _a = 1, _b = string_length(_s);
	while (_a <= _b && (string_char_at(_s, _a) == " " || string_char_at(_s, _a) == "\t")) _a++;
	while (_b >= _a && (string_char_at(_s, _b) == " " || string_char_at(_s, _b) == "\t")) _b--;
	if (_b < _a) return "";
	return string_copy(_s, _a, _b - _a + 1);
}

/// Format an integer amount with thousands separators: 1234567 -> "1,234,567"
function fmt_num(_v) {
	var _neg = _v < 0;
	var _s = string(floor(abs(_v)));
	var _out = "";
	var _n = string_length(_s);
	for (var i = 0; i < _n; i++) {
		if (i > 0 && (i mod 3) == 0) _out = "," + _out;
		_out = string_char_at(_s, _n - i) + _out;
	}
	return (_neg ? "-" : "") + _out;
}

function fmt_money(_v) { return fmt_num(_v) + " g"; }

function arr_contains(_a, _v) {
	for (var i = 0; i < array_length(_a); i++) if (_a[i] == _v) return true;
	return false;
}

function arr_remove(_a, _v) {
	for (var i = array_length(_a) - 1; i >= 0; i--) if (_a[i] == _v) array_delete(_a, i, 1);
}

function arr_pick(_a) {
	if (array_length(_a) == 0) return undefined;
	return _a[irandom(array_length(_a) - 1)];
}

function arr_shuffle(_a) {
	for (var i = array_length(_a) - 1; i > 0; i--) {
		var j = irandom(i);
		var _t = _a[i]; _a[i] = _a[j]; _a[j] = _t;
	}
	return _a;
}

function struct_get_or(_s, _k, _def) {
	if (is_struct(_s) && variable_struct_exists(_s, _k)) return variable_struct_get(_s, _k);
	return _def;
}

/// Index an array of {id:...} structs into a struct keyed by id.
function index_by_id(_arr) {
	var _out = {};
	for (var i = 0; i < array_length(_arr); i++) variable_struct_set(_out, _arr[i].id, _arr[i]);
	return _out;
}

/// Replace {key} tokens with values from a struct (missing keys stay untouched).
function fill_text(_s, _vars) {
	var _keys = variable_struct_get_names(_vars);
	for (var i = 0; i < array_length(_keys); i++) {
		_s = string_replace_all(_s, "{" + _keys[i] + "}", string(variable_struct_get(_vars, _keys[i])));
	}
	return _s;
}

function roll100() { return irandom(99); }

#macro WEEKS_PER_MONTH 4

/// _t is a week counter. "March 1702"
function month_name(_t) {
	var _mo = _t div WEEKS_PER_MONTH;
	var _m = global.D.config.months;
	return _m[_mo mod 12] + " " + string(global.D.config.start_year + (_mo div 12));
}

/// Last week of the month that week _t falls in.
function month_end(_t) { return (_t div WEEKS_PER_MONTH) * WEEKS_PER_MONTH + WEEKS_PER_MONTH - 1; }

/// "Week 2, March 1702"
function date_name(_t) { return trf("Week {0}, {1}", (_t mod WEEKS_PER_MONTH) + 1, month_name(_t)); }

/// Fits text into a width by shrinking the scale (never grows).
function fit_scale(_s, _scale, _maxw) {
	var _w = ui_text_width(_s, _scale);
	return (_w > _maxw && _w > 0) ? _scale * _maxw / _w : _scale;
}

/// Debug trace that survives a hang or crash (appends to dbg.log in the save folder).
function dbg(_s) { var f = file_text_open_append("dbg.log"); file_text_write_string(f, string(current_time) + " " + string(_s)); file_text_writeln(f); file_text_close(f); }
