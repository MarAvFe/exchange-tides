// ===== Data loading + sprite registry ======================================================
// Everything gameplay-relevant lives in datafiles/data/*.json and datafiles/sprites/*.png.
// To add content: edit the JSON (new captain, port, good, item, enemy, campaign chapter) and
// drop a PNG into datafiles/sprites. See docs/EXTENDING.md.

function data_load_all() {
	var _dir = "data/";
	global.D = {
		config:     load_json(_dir + "config.json"),
		goods_list: load_json(_dir + "goods.json"),
		ports_list: load_json(_dir + "ports.json"),
		ships:      load_json(_dir + "ships.json"),
		items_list: load_json(_dir + "items.json"),
		chars:      load_json(_dir + "characters.json"),
		campaign:   load_json(_dir + "campaign.json"),
	};
	var D = global.D;
	i18n_apply_data(D);   // player-visible text in the chosen language (ids untouched)
	D.goods   = index_by_id(D.goods_list);
	D.ports   = index_by_id(D.ports_list);
	D.items   = index_by_id(D.items_list);
	D.pships  = index_by_id(D.ships.player);
	D.enemies = index_by_id(D.ships.enemies);
	D.ammo    = index_by_id(D.ships.ammo);
	D.captains = index_by_id(D.chars.captains);
	D.npcs    = index_by_id(D.chars.npcs);
	// Stories: campaign.json holds one campaign per captain ({"campaigns": [...]}); an old single
	// campaign file ({"chapters": [...]}) still loads as one story.
	if (variable_struct_exists(D.campaign, "campaigns")) D.campaigns = index_by_id(D.campaign.campaigns);
	else { D.campaigns = {}; variable_struct_set(D.campaigns, D.campaign.id, D.campaign); }

	// Pre-parse every item's effect string into ops.
	global.EFFECTS = {};
	for (var i = 0; i < array_length(D.items_list); i++) {
		var _it = D.items_list[i];
		variable_struct_set(global.EFFECTS, _it.id, effect_parse(struct_get_or(_it, "effect", "")));
	}
	global.SPR = {};
}

/// Lazily load a sprite PNG from datafiles/sprites (centred origin). Returns -1 if missing.
function spr(_name) {
	if (variable_struct_exists(global.SPR, _name)) return variable_struct_get(global.SPR, _name);
	var _path = "sprites/" + _name + ".png";
	var _s = -1;
	if (file_exists(_path)) {
		_s = sprite_add(_path, 1, false, true, 0, 0);
		if (_s >= 0) sprite_set_offset(_s, sprite_get_width(_s) div 2, sprite_get_height(_s) div 2);
	}
	variable_struct_set(global.SPR, _name, _s);
	return _s;
}

function draw_spr(_name, _x, _y, _scale = 1, _alpha = 1, _flip = false, _rot = 0) {
	var _s = spr(_name);
	if (_s < 0) {
		draw_set_alpha(_alpha);
		draw_set_color(c_fuchsia);
		draw_rectangle(_x - 20, _y - 20, _x + 20, _y + 20, true);
		draw_set_alpha(1);
		return;
	}
	draw_sprite_ext(_s, 0, _x, _y, _flip ? -_scale : _scale, _scale, _rot, c_white, _alpha);
}

/// Portrait sprite for an NPC or captain; "portrait_fallback" is used until the art exists.
function npc_portrait(_npc_id) {
	var _d = struct_get_or(global.D.npcs, _npc_id, struct_get_or(global.D.captains, _npc_id, undefined));
	if (_d == undefined) return "portrait_sailor";
	return portrait_or_fallback(_d);
}

function portrait_or_fallback(_d) {
	if (spr(_d.portrait) >= 0) return _d.portrait;
	return struct_get_or(_d, "portrait_fallback", "portrait_sailor");
}

function npc_name(_npc_id) {
	if (variable_struct_exists(global.D.npcs, _npc_id)) return variable_struct_get(global.D.npcs, _npc_id).name;
	if (variable_struct_exists(global.D.captains, _npc_id)) return variable_struct_get(global.D.captains, _npc_id).name;
	return _npc_id;
}
