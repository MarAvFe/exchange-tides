// ===== Translation ================================================================================
// The game is written in English; other languages are string tables in datafiles/data/lang/<code>.json
// mapping each English text to its translation ({"Back": "Volver", ...}). Missing entries fall back to
// English, so a partial table never breaks anything. tools/i18n_check.py lists untranslated texts.
//
// - tr(s): translate a fixed text. The ui_* widgets call it on every label, so plain literals need no
//   wrapping: ui_button(..., "Back") shows "Volver".
// - trf(template, a, b, ...): texts with values inside. The template is translated, then {0}, {1}...
//   are replaced: trf("Sail to {0}  (1 week)", name). Word order can differ per language.
// - Data (goods, items, ports, story...) is translated once when it loads (i18n_apply_data), for the
//   fields listed in I18N_DATA_FIELDS. Ids are never touched.
// Default language: Spanish. The settings panel switches it at once (the data is reloaded).

#macro I18N_DEFAULT "es"

function i18n_langs() { return [["es", "Español"], ["en", "English"]]; }

function i18n_init() {
	global.LANG = settings_get("lang", I18N_DEFAULT);
	global.TR = {};
	if (global.LANG != "en") {
		var _p = "data/lang/" + global.LANG + ".json";
		if (file_exists(_p)) global.TR = load_json(_p);
	}
}

function i18n_set(_code) {
	settings_set("lang", _code);
	i18n_init();
	var _spr = global.SPR;
	data_load_all();      // re-read data so names and story come in the new language
	global.SPR = _spr;    // keep the sprites already loaded
}

function i18n_name() {
	var _l = i18n_langs();
	for (var i = 0; i < array_length(_l); i++) if (_l[i][0] == global.LANG) return _l[i][1];
	return global.LANG;
}

function tr(_s) {
	if (!is_string(_s) || global.LANG == "en") return _s;
	var _t = global.TR[$ _s];
	return (_t == undefined) ? _s : _t;
}

function trf(_tmpl) {
	var _s = tr(_tmpl);
	for (var i = 1; i < argument_count; i++) _s = string_replace_all(_s, "{" + string(i - 1) + "}", string(argument[i]));
	return _s;
}

/// Gendered form: a table may hold "Captain|f" next to "Captain" for women's titles.
function tr_g(_s, _female) {
	if (_female && global.LANG != "en") { var _t = global.TR[$ _s + "|f"]; if (_t != undefined) return _t; }
	return tr(_s);
}

/// Singular or plural form: trn(n, "{0} cannon", "{0} cannons").
function trn(_n, _one, _many) { return trf(_n == 1 ? _one : _many, _n); }

// Text fields of the data files that are shown to the player.
#macro I18N_DATA_FIELDS ["name", "desc", "title", "text", "intro", "ok", "bio", "closed_reason", "greeting", "months", "ship_names", "ship_name", "pirate_names", "label", "ending_title", "ending_text"]

/// Translates the data loaded into global.D in place (only the fields above, recursively).
function i18n_apply_data(_o) {
	if (global.LANG == "en") return;
	if (is_array(_o)) { for (var i = 0; i < array_length(_o); i++) if (is_struct(_o[i]) || is_array(_o[i])) i18n_apply_data(_o[i]); return; }
	if (!is_struct(_o)) return;
	var _keys = variable_struct_get_names(_o);
	var _fields = I18N_DATA_FIELDS;
	var _fem = struct_get_or(_o, "female", false) == true;
	for (var i = 0; i < array_length(_keys); i++) {
		var k = _keys[i], v = _o[$ k];
		var _tf = false;
		for (var j = 0; j < array_length(_fields); j++) if (_fields[j] == k) { _tf = true; break; }
		if (_tf && is_string(v)) _o[$ k] = tr_g(v, _fem);
		else if (_tf && is_array(v)) { for (var j = 0; j < array_length(v); j++) if (is_string(v[j])) v[j] = tr(v[j]); else i18n_apply_data(v[j]); }
		else if (is_struct(v) || is_array(v)) i18n_apply_data(v);
	}
}
