/// Exchange Tides - single controller object. All game state lives in global structs:
/// global.D (static data), global.G (save game), global.UI, global.V (voyage), global.C (combat).
// Unhandled errors: log them (and in the headless self-test, quit instead of showing a modal dialog).
exception_unhandled_handler(function(_ex) {
	dbg("EXCEPTION " + string(_ex.longMessage) + " | " + string(_ex.stacktrace));
	show_debug_message("[SELFTEST] EXCEPTION " + string(_ex.longMessage));
	return 0;
});
randomize();
global.G = undefined;
global.V = undefined;
global.C = undefined;
global.DT = 1 / 60;
i18n_init();       // language first: the data is translated as it loads
data_load_all();
behaviors_init();
ui_init();
music_init();
display_set_gui_size(1280, 720);
gpu_set_texfilter(true);
draw_set_font(-1);
if (selftest_enabled()) selftest_init();

