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
	return struct_get_or(_g, _pid, { name: tr("The Governor"), greeting: tr("\"Captain. The colony has work for those who can do it.\"") });
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
	for (var i = 0; i < array_length(D.ports_list); i++) if (D.ports_list[i].id != _pid && port_open(D.ports_list[i].id)) array_push(_others, D.ports_list[i].id);
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
			// You buy the goods yourself, so pay their typical market price plus a 20-50% premium.
			var _mean = variable_struct_get(G.goods, g.id).base + g.inc * goods_steps(g) / 2;
			c.reward = round(c.qty * _mean * random_range(1.2, 1.5) / 50) * 50 + 500;
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
	c.due = month_end(c.due);   // deadlines are whole months: "by end of February"
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
		case "deliver": return (c.port == c.from ? trf("Bring {0} {1} here to {2}", c.qty, variable_struct_get(D.goods, c.good).name, _to) : trf("Deliver {0} {1} to {2}", c.qty, variable_struct_get(D.goods, c.good).name, _to));
		case "courier": return trf("Carry sealed dispatches to {0}", _to);
		case "passenger": return trf("Carry {0} to {1}", c.who.name, _to);
		case "bounty": return trn(c.n, "Sink {0} raider", "Sink {0} raiders") + (c.done ? " (" + string(min(c.n, global.G.stats.sunk - c.base)) + "/" + string(c.n) + ")" : "");
		case "hunt": return trf("Hunt down {0}'s {1} off {2}", struct_get_or(c, "name", tr("a raider")), variable_struct_get(D.enemies, c.enemy).name, _to);
	}
	return "?";
}

function contract_due_text(c) {
	var _left = c.due - global.G.t;
	var _m = month_name(c.due);
	_m = string_copy(_m, 1, string_pos(" ", _m) - 1);
	return _left <= 0 ? trf("by end of {0} (this week)", _m) : trf("by end of {0} ({1} wks left)", _m, _left + 1);
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
	log_add(trf("Contract from {0}: {1} {2}.", governor_of(_pid).name, contract_text(c), contract_due_text(c)));
	if (c.kind == "passenger") ui_toast(trf("{0} comes aboard.", c.who.name));
	return true;
}

function contract_pay(_i, _how) {
	var G = global.G;
	var c = G.contracts[_i];
	G.cash += c.reward;
	G.stats.contracts += 1;
	log_add(trf("Contract complete: {0}. Paid {1}.", contract_text(c), fmt_money(c.reward)));
	ui_message(tr("Contract complete"), _how + "\n\n" + trf("Reward: {0}", fmt_money(c.reward)), "portrait_governor");
	array_delete(G.contracts, _i, 1);
	level_update();
	campaign_check();   // story goals can ask for finished contracts
}

/// Arriving in port completes deliveries and courier runs.
function contracts_on_arrival() {
	var G = global.G;
	for (var i = array_length(G.contracts) - 1; i >= 0; i--) {
		var c = G.contracts[i];
		if (c.kind == "passenger" && c.port != G.port && G.t > c.due) {
			log_add(trf("{0} gave up waiting and went ashore at {1}. Contract lost.", c.who.name, port_def(G.port).name));
			ui_toast(trf("{0} disembarks: you were too late.", c.who.name));
			array_delete(G.contracts, i, 1);
			continue;
		}
		if (c.port != G.port) continue;
		if (c.kind == "passenger") contract_pay(i, trf("{0} steps ashore at {1} and pays the fare, with thanks.", c.who.name, port_def(c.port).name));
		else if (c.kind == "courier") contract_pay(i, "The harbourmaster takes your dispatches with a grateful nod.");
		else if (c.kind == "deliver" && cargo_qty(c.good) >= c.qty) {
			cargo_remove(c.good, c.qty);
			contract_pay(i, trf("Dock hands unload {0} {1} for {2}.", c.qty, variable_struct_get(global.D.goods, c.good).name, governor_of(c.from).name));
		}
	}
}

function contracts_on_sink(_n) {
	var G = global.G;
	for (var i = array_length(G.contracts) - 1; i >= 0; i--) {
		var c = G.contracts[i];
		if (c.kind == "bounty" && G.stats.sunk - c.base >= c.n) contract_pay(i, trf("Word of your gunnery reaches {0}. The bounty is paid to your account.", port_def(c.from).name));
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
	if (_i >= 0) contract_pay(_i, trf("{0} will trouble these waters no more.", struct_get_or(global.G.contracts[_i], "name", tr("The raider"))));
}

function contracts_week_tick() {
	var G = global.G;
	for (var i = array_length(G.contracts) - 1; i >= 0; i--) {
		var c = G.contracts[i];
		if (G.t > c.due && c.kind != "passenger") {   // late passengers leave at the next port instead
			log_add(trf("Contract failed: {0} (deadline passed).", contract_text(c)));
			ui_toast(trf("Contract expired: {0}", contract_text(c)));
			array_delete(G.contracts, i, 1);
		}
	}
}
