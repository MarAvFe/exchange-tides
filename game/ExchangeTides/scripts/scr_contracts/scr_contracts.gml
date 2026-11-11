// ===== Governor contracts =====================================================================
// Every governor offers a few jobs, re-rolled each month (G.offers[port] = {m, list}). You may hold
// CONTRACTS_MAX at once; they show in the journal with their deadlines. Kinds:
//   deliver : bring qty of a good to a port (completed on arrival, goods handed over)
//   courier : carry a dispatch to a port before the deadline
//   bounty  : sink n raiders anywhere
//   hunt    : a named raider waits off a port; beat it (a scripted battle when you sail there)
//   passenger: a person boards when you accept and rides along; paid on arrival at their port.
//             If the deadline passes they simply disembark at the next port you reach.
// To add a kind: generate it in contract_roll, describe it in contract_text, complete it in
// contracts_on_arrival / contracts_on_sink / contracts_on_hunt_won.
#macro CONTRACTS_MAX 3

function governor_of(_pid) {
	var _g = struct_get_or(global.D.chars, "governors", {});
	return struct_get_or(_g, _pid, { name: "The Governor", greeting: "\"Captain. The colony has work for those who can do it.\"" });
}

function contract_offers(_pid) {
	var G = global.G;
	var _m = G.t div WEEKS_PER_MONTH;
	var _o = struct_get_or(G.offers, _pid, undefined);
	if (_o == undefined || _o.m != _m) {
		_o = { m: _m, list: [] };
		var _n = 2 + irandom(1);
		for (var i = 0; i < _n; i++) array_push(_o.list, contract_roll(_pid));
		variable_struct_set(G.offers, _pid, _o);
	}
	return _o.list;
}

function contract_roll(_pid) {
	var G = global.G, D = global.D;
	var _lv = G.level;
	var _others = [];
	for (var i = 0; i < array_length(D.ports_list); i++) if (D.ports_list[i].id != _pid) array_push(_others, D.ports_list[i].id);
	var _dest = arr_pick(_others);
	var _kind = choose("deliver", "deliver", "courier", "bounty", "hunt", "passenger", "passenger");
	var c = { kind: _kind, from: _pid, port: _dest, good: "", qty: 0, enemy: "", n: 0, base: 0,
	          due: G.t + 3 + irandom(4), reward: 0, done: false };   // done = accepted
	switch (_kind) {
		case "deliver":
			var _gs = [];
			for (var k = 0; k < array_length(D.goods_list); k++) {
				var g = D.goods_list[k];
				if (variable_struct_get(G.goods, g.id).unlocked && g.forsale) array_push(_gs, g);
			}
			var g = arr_pick(_gs);
			c.good = g.id;
			c.qty = max(5, round(cargo_capacity() * random_range(0.25, 0.6) / 5) * 5);
			c.reward = round(c.qty * variable_struct_get(G.goods, g.id).base * random_range(0.35, 0.6) / 50) * 50 + 500;
			if (irandom(2) == 0) c.port = _pid;   // "bring it here"
			break;
		case "courier":
			c.due = G.t + 2 + irandom(2);
			c.reward = round((1500 + 900 * _lv) * random_range(0.8, 1.3) / 50) * 50;
			break;
		case "bounty":
			c.n = 1 + irandom(1) + (_lv div 4);
			c.base = G.stats.sunk;
			c.due = G.t + 4 + irandom(4);
			c.reward = c.n * round((2000 + 2500 * _lv) * random_range(0.8, 1.2) / 50) * 50;
			break;
		case "passenger":
			c.who = npc_roll(_pid, "passenger");
			c.due = G.t + 2 + irandom(3);
			c.reward = round((1200 + 700 * _lv) * random_range(0.8, 1.4) / 50) * 50;
			break;
		case "hunt":
			c.enemy = contract_hunt_enemy();
			c.name = arr_pick(D.config.pirate_names);
			c.reward = round(variable_struct_get(D.enemies, c.enemy).booty * random_range(1.2, 1.8) / 50) * 50 + 2000;
			c.due = G.t + 3 + irandom(4);
			break;
	}
	return c;
}

function contract_hunt_enemy() {
	var G = global.G, D = global.D;
	var _pool = [];
	for (var i = 0; i < array_length(D.ships.enemies); i++) {
		var e = D.ships.enemies[i];
		if (!struct_get_or(e, "unique", false) && e.level >= G.level && e.level <= G.level + 3) array_push(_pool, e.id);
	}
	if (array_length(_pool) == 0) return pick_enemy();
	return arr_pick(_pool);
}

function contract_text(c) {
	var D = global.D;
	var _to = port_def(c.port).name;
	switch (c.kind) {
		case "deliver": return "Deliver " + string(c.qty) + " " + variable_struct_get(D.goods, c.good).name + " to " + _to;
		case "courier": return "Carry sealed dispatches to " + _to;
		case "passenger": return "Carry " + c.who.name + " to " + _to;
		case "bounty": return "Sink " + string(c.n) + " raider" + (c.n > 1 ? "s" : "") + (c.done ? " (" + string(min(c.n, global.G.stats.sunk - c.base)) + "/" + string(c.n) + ")" : "");
		case "hunt": return "Hunt down " + struct_get_or(c, "name", "a raider") + "'s " + variable_struct_get(D.enemies, c.enemy).name + " off " + _to;
	}
	return "?";
}

function contract_due_text(c) {
	var _left = c.due - global.G.t;
	return "by " + date_name(c.due) + " (" + (_left <= 0 ? "this week" : string(_left) + " wk" + (_left > 1 ? "s" : "")) + ")";
}

function contract_accept(_pid, _i) {
	var G = global.G;
	var _list = contract_offers(_pid);
	if (array_length(G.contracts) >= CONTRACTS_MAX) return false;
	var c = _list[_i];
	if (c.kind == "bounty") c.base = G.stats.sunk;
	c.done = true;   // "accepted": shows progress in its text
	array_push(G.contracts, c);
	array_delete(_list, _i, 1);
	log_add("Contract from " + governor_of(_pid).name + ": " + contract_text(c) + " " + contract_due_text(c) + ".");
	if (c.kind == "passenger") ui_toast(c.who.name + " comes aboard.");
	return true;
}

function contract_pay(_i, _how) {
	var G = global.G;
	var c = G.contracts[_i];
	G.cash += c.reward;
	G.stats.contracts += 1;
	log_add("Contract complete: " + contract_text(c) + ". Paid " + fmt_money(c.reward) + ".");
	ui_message("Contract complete", _how + "\n\nReward: " + fmt_money(c.reward), "portrait_governor");
	array_delete(G.contracts, _i, 1);
	level_update();
}

/// Arriving in port completes deliveries and courier runs.
function contracts_on_arrival() {
	var G = global.G;
	for (var i = array_length(G.contracts) - 1; i >= 0; i--) {
		var c = G.contracts[i];
		if (c.kind == "passenger" && c.port != G.port && G.t > c.due) {
			log_add(c.who.name + " gave up waiting and went ashore at " + port_def(G.port).name + ". Contract lost.");
			ui_toast(c.who.name + " disembarks: you were too late.");
			array_delete(G.contracts, i, 1);
			continue;
		}
		if (c.port != G.port) continue;
		if (c.kind == "passenger") contract_pay(i, c.who.name + " steps ashore at " + port_def(c.port).name + " and pays the fare, with thanks.");
		else if (c.kind == "courier") contract_pay(i, "The harbourmaster takes your dispatches with a grateful nod.");
		else if (c.kind == "deliver" && cargo_qty(c.good) >= c.qty) {
			cargo_remove(c.good, c.qty);
			contract_pay(i, "Dock hands unload " + string(c.qty) + " " + variable_struct_get(global.D.goods, c.good).name + " for " + governor_of(c.from).name + ".");
		}
	}
}

function contracts_on_sink(_n) {
	var G = global.G;
	for (var i = array_length(G.contracts) - 1; i >= 0; i--) {
		var c = G.contracts[i];
		if (c.kind == "bounty" && G.stats.sunk - c.base >= c.n) contract_pay(i, "Word of your gunnery reaches " + port_def(c.from).name + ". The bounty is paid to your account.");
	}
}

/// Index of an active hunt contract waiting off _pid, or -1.
function contract_hunt_at(_pid) {
	var G = global.G;
	for (var i = 0; i < array_length(G.contracts); i++) if (G.contracts[i].kind == "hunt" && G.contracts[i].port == _pid) return i;
	return -1;
}

function contracts_on_hunt_won(_pid) {
	var _i = contract_hunt_at(_pid);
	if (_i >= 0) contract_pay(_i, struct_get_or(global.G.contracts[_i], "name", "The raider") + " will trouble these waters no more.");
}

function contracts_week_tick() {
	var G = global.G;
	for (var i = array_length(G.contracts) - 1; i >= 0; i--) {
		var c = G.contracts[i];
		if (G.t > c.due && c.kind != "passenger") {   // late passengers leave at the next port instead
			log_add("Contract failed: " + contract_text(c) + " (deadline passed).");
			ui_toast("Contract expired: " + contract_text(c));
			array_delete(G.contracts, i, 1);
		}
	}
}
