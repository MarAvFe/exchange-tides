/// Exchange Tides - single controller object. All game state lives in global structs:
/// global.D (static data), global.G (save game), global.UI, global.V (voyage), global.C (combat).
randomize();
global.G = undefined;
global.V = undefined;
global.C = undefined;
global.DT = 1 / 60;
data_load_all();
behaviors_init();
ui_init();
music_init();
display_set_gui_size(1280, 720);
gpu_set_texfilter(true);
draw_set_font(-1);
if (selftest_enabled()) selftest_init();
