// ===== Music ======================================================================================
// One looping track per mood, cross-faded when the screen changes. Tracks are sound assets
// (sounds/snd_music_*, Kevin MacLeod, CC BY 4.0 - see LICENSES.md); tools/music.py fetches them.
// To add a mood: add a sound folder, rerun tools/gen_project.py, and map screens to it in music_pick.
#macro MUSIC_FADE_MS 1400
#macro MUSIC_GAIN 0.55

function music_enabled() { return settings_get("music", true); }

function music_toggle() {
	settings_set("music", !music_enabled());
	if (!music_enabled() && global.MUSIC.inst != -1) { audio_sound_gain(global.MUSIC.inst, 0, 400); global.MUSIC.cur = -1; }
}

function music_init() {
	global.MUSIC = { cur: -1, inst: -1, old: [] };
}

/// Battle tracks skip their slow intros: start somewhere inside the energetic part (seconds),
/// measured with ffmpeg's loudness meter. Other tracks start at 0.
function music_start_pos(_snd) {
	if (_snd == snd_music_battle) return choose(30, 78, 112);    // Five Armies: builds until ~30 s, peaks 112-150 s
	if (_snd == snd_music_battle2) return choose(3, 150, 220);   // Clash Defiant: full energy throughout
	return 0;
}

function music_pick() {
	var _s = global.UI.screen;
	switch (_s) {
		case "title": case "newgame": case "saves": case "help": return snd_music_title;
		case "tavern": return snd_music_tavern;
		case "map": case "sailing": return snd_music_sea;
		case "combat":
			var C = global.C;
			return (C != undefined && (C.special || array_length(C.enemies) >= 3)) ? snd_music_battle2 : snd_music_battle;
		case "victory": return snd_music_victory;
		case "gameover": return snd_music_title;
	}
	// Ports and buildings: each port keeps one of two harbour tunes.
	if (global.G != undefined && (port_hash(global.G.port) mod 2) == 1) return snd_music_port2;
	return snd_music_port;
}

function music_update() {
	var M = global.MUSIC;
	if (!music_enabled() || selftest_enabled()) return;
	for (var i = array_length(M.old) - 1; i >= 0; i--) if (current_time > M.old[i].t) { audio_stop_sound(M.old[i].inst); array_delete(M.old, i, 1); }
	var _want = music_pick();
	if (_want == M.cur) return;
	if (M.inst != -1) { audio_sound_gain(M.inst, 0, (_want == snd_music_battle || _want == snd_music_battle2) ? 300 : MUSIC_FADE_MS); array_push(M.old, { inst: M.inst, t: current_time + MUSIC_FADE_MS }); }
	M.cur = _want;
	M.inst = audio_play_sound(_want, 10, true, 0);
	var _pos = music_start_pos(_want);
	if (_pos > 0) audio_sound_set_track_position(M.inst, _pos);
	audio_sound_gain(M.inst, MUSIC_GAIN, (_pos > 0) ? 250 : MUSIC_FADE_MS);   // battles cut in hard
}
