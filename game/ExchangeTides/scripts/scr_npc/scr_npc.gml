// ===== Generated townsfolk =====================================================================
// Every port's banker, barkeep, shipwright, moneylender, merchant, curio dealer and governor is a
// unique person built from trait layers (data/npc_parts.json + sprites/npc_*.png), like a set of
// paper-doll parts. A person is rolled the first time you meet them and stored in the save
// (G.npcs["<port>|<role>"]), so the moneylender of Saltmere stays the same all game.
// Governors keep their written names (characters.json -> governors); only their faces are rolled.

function npc_parts() {
	if (!variable_struct_exists(global.D, "npcparts")) global.D.npcparts = load_json("data/npc_parts.json");
	return global.D.npcparts;
}

function npc_is_local_role(_role) { return variable_struct_exists(npc_parts().roles, _role); }

/// The person holding _role at _pid (rolled once, then kept in the save). _slot tells apart several
/// people of one role in the same port (e.g. each crew member for hire in a tavern).
function npc_get(_pid, _role, _slot = "") {
	var G = global.G;
	if (!variable_struct_exists(G, "npcs")) G.npcs = {};
	var _key = _pid + "|" + _role + (_slot != "" ? "|" + _slot : "");
	var n = struct_get_or(G.npcs, _key, undefined);
	if (n == undefined) {
		n = npc_roll(_pid, _role);
		variable_struct_set(G.npcs, _key, n);
	}
	return n;
}

function npc_roll(_pid, _role) {
	var P = npc_parts();
	var R = variable_struct_get(P.roles, _role);
	var _f = (_role == "governor") ? struct_get_or(governor_of(_pid), "female", irandom(1) == 0) : (irandom(1) == 0);
	var _hat = arr_pick(R.hats);
	var t = {
		head: arr_pick(P.heads) + "_" + arr_pick(P.skins),
		coat: arr_pick(R.coats), collar: arr_pick(R.collars),
		hair: arr_contains(P.hats_hide_hair, _hat) ? "" : arr_pick(P.hairs),
		hairback: (_f ? choose("long", "long", "tail", "") : choose("", "", "", "tail")),
		beard: (_f ? "" : choose("", "", "full", "moustache", "goatee", "stubble")),
		hat: _hat, acc: arr_pick(R.accs),
		hair_col: irandom(array_length(P.hair_colours) - 1),
		cloth_col: irandom(array_length(P.cloth_colours) - 1),
		hat_col: irandom(array_length(P.cloth_colours) - 1),
		bg_col: irandom(array_length(P.bg_colours) - 1),
	};
	if (_f && t.hair == "receding") t.hair = "bun";
	if (_hat != "" && t.hair == "bun") t.hair = "short";   // a bun would poke through the hat
	var _name;
	if (_role == "governor") _name = governor_of(_pid).name;
	else _name = arr_pick(_f ? P.first_f : P.first_m) + " " + arr_pick(P.last);
	return { name: _name, role: _role, title: R.title, female: _f, t: t };
}

function npc_rgb(_arr, _i) { var c = _arr[_i]; return make_colour_rgb(c[0], c[1], c[2]); }

/// Draws a generated person centred at (x, y); scale 1 = the 160x200 portrait size.
function npc_draw(_n, _x, _y, _scale = 1, _alpha = 1) {
	var P = npc_parts(), t = _n.t;
	var _hair = npc_rgb(P.hair_colours, t.hair_col), _cloth = npc_rgb(P.cloth_colours, t.cloth_col);
	var _layers = [
		["plate_0", npc_rgb(P.bg_colours, t.bg_col)],
		[t.hairback != "" ? "hairback_" + t.hairback : "", _hair],
		["coat_" + t.coat, _cloth],
		["collar_" + t.collar, c_white],
		["head_" + t.head, c_white],
		[t.beard != "" ? "beard_" + t.beard : "", _hair],
		[t.hair != "" ? "hair_" + t.hair : "", _hair],
		[t.hat != "" ? "hat_" + t.hat : "", arr_contains(P.hats_tinted, t.hat) ? npc_rgb(P.cloth_colours, t.hat_col) : c_white],
		[t.acc != "" ? "acc_" + t.acc : "", c_white],
	];
	for (var i = 0; i < array_length(_layers); i++) {
		if (_layers[i][0] == "") continue;
		var s = spr("npc_" + _layers[i][0]);
		if (s >= 0) draw_sprite_ext(s, 0, _x, _y, _scale * 0.5, _scale * 0.5, 0, _layers[i][1], _alpha);
	}
}

/// Portrait for a dialog/header: a local role at this port draws its generated person; story
/// characters and captains draw their painted portrait.
function npc_draw_any(_npc, _x, _y, _scale = 1, _pid = undefined) {
	if (global.G != undefined && npc_is_local_role(_npc)) {
		npc_draw(npc_get(_pid == undefined ? global.G.port : _pid, _npc), _x, _y, _scale);
	} else draw_spr(npc_portrait(_npc), _x, _y, _scale);
}

function npc_display_name(_npc, _pid = undefined) {
	if (global.G != undefined && npc_is_local_role(_npc)) {
		var n = npc_get(_pid == undefined ? global.G.port : _pid, _npc);
		return (_npc == "governor") ? n.name : n.name + ", " + n.title;
	}
	return npc_name(_npc);
}
