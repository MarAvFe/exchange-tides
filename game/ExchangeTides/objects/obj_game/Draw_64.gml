// Self-test screenshots: render the frame into a surface and save it.
var _shot = variable_global_exists("ST") ? global.ST.shot : "";
var _surf = -1;
if (_shot != "") {
	_surf = surface_create(1280, 720);
	surface_set_target(_surf);
	draw_clear(c_black);
}
global.UI.block = array_length(global.UI.dialogs) > 0;
screens_draw(global.DT);
global.UI.block = false;
ui_draw_overlays(global.DT);
if (_shot != "") {
	surface_reset_target();
	draw_surface(_surf, 0, 0);
	surface_save(_surf, "shot_" + _shot + ".png");
	surface_free(_surf);
	global.ST.shot = "";
}
