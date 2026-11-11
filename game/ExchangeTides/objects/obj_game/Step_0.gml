global.DT = min(delta_time / 1000000, 0.1);
ui_frame_begin();
if (variable_global_exists("ST")) selftest_step();
screens_step(global.DT);
music_update();

// Deferred end screens (campaign finale / free-mode goal) appear once back in port.
if (global.G != undefined && global.UI.screen == "port" && array_length(global.UI.dialogs) == 0) {
	var _pe = struct_get_or(global.G, "pending_end", "");
	if (_pe != "") {
		global.G.pending_end = "";
		ui_go(_pe);
	}
}
