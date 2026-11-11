// ===== Enemy behaviour registry =============================================================
// Each enemy in ships.json names a "behavior". A behaviour is a function(enemy_state, combat, dt)
// that returns "fire", "flee" or "" for this frame. To add a behaviour, register a new function
// here (or from any script) with behavior_register("name", function(e, C, dt) { ... }).
//
// enemy_state fields: hp, max_hp, reload (seconds left), reload_time, guns, wait (scratch timer)

function behavior_register(_name, _fn) { variable_struct_set(global.BEHAVIORS, _name, _fn); }

function behaviors_init() {
	global.BEHAVIORS = {};

	// Fires the moment the guns are loaded; never retreats.
	behavior_register("aggressive", function(e, C, dt) {
		if (e.reload <= 0) return "fire";
		return "";
	});

	// Waits for a steady shot; once committed it rarely breaks off (only when nearly sunk).
	behavior_register("cautious", function(e, C, dt) {
		if (e.hp < e.max_hp * 0.15 && !e.tried_flee) { e.tried_flee = true; if (irandom(99) < 20) return "flee"; }
		if (e.reload <= 0) {
			e.wait += dt;
			if (e.wait > 0.6) { e.wait = 0; return "fire"; }
		}
		return "";
	});

	// Smugglers: the only raiders that may cut and run, and only when badly hurt.
	behavior_register("skittish", function(e, C, dt) {
		if (e.hp < e.max_hp * 0.3 && !e.tried_flee) { e.tried_flee = true; if (irandom(99) < 35) return "flee"; }
		if (e.reload <= 0) return "fire";
		return "";
	});

	// Faster reloads, never flees.
	behavior_register("relentless", function(e, C, dt) {
		e.reload -= dt * 0.15;
		if (e.reload <= 0) return "fire";
		return "";
	});

	// Forts: slow, steady.
	behavior_register("stationary", function(e, C, dt) {
		if (e.reload <= 0) return "fire";
		return "";
	});
}

function behavior_get(_name) {
	if (variable_struct_exists(global.BEHAVIORS, _name)) return variable_struct_get(global.BEHAVIORS, _name);
	return variable_struct_get(global.BEHAVIORS, "aggressive");
}
