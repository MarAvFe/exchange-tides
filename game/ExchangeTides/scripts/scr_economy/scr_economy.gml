// ===== Economy (docs/MECHANICS.md §2) ======================================================
// Global base price per good (rolled at new game), per-port monthly price roll with a
// "high month" spike good and a "low month" trough good per port, contraband rotation
// (price x2 where outlawed), bank/moneylender monthly compounding, alehouse tips.

function goods_steps(g) { return max(1, g.range div g.inc); }

function economy_init() {
	var G = global.G, D = global.D;
	G.goods = {};
	for (var i = 0; i < array_length(D.goods_list); i++) {
		var g = D.goods_list[i];
		var _span = max(0, (g.max - g.range - g.min) div g.inc);
		variable_struct_set(G.goods, g.id, {
			base: g.min + g.inc * irandom(_span),
			unlocked: g.start || G.mode == "free",
			contra_now: [], contra_next: [],
		});
	}
	G.portmeta = {};
	G.markets = {};
	for (var i = 0; i < array_length(D.ports_list); i++) {
		var _p = D.ports_list[i];
		variable_struct_set(G.portmeta, _p.id, { high_good: "", high_t: -1, low_good: "", low_t: -1, high_known: false, low_known: false });
		variable_struct_set(G.markets, _p.id, {});
		port_reroll_specials(_p.id);
	}
	contraband_rotate();
	contraband_rotate();
	market_roll_all();
}

function port_reroll_specials(_pid) {
	var G = global.G;
	var _pm = variable_struct_get(G.portmeta, _pid);
	var _ids = variable_struct_get_names(G.goods);
	var _m = G.t div WEEKS_PER_MONTH;   // specials are scheduled in months (high_t/low_t = month index)
	if (_pm.high_t < _m) {
		_pm.high_good = arr_pick(_ids);
		_pm.high_t = _m + 1 + irandom(5);
		_pm.high_known = false;
	}
	if (_pm.low_t < _m) {
		var _lg = arr_pick(_ids);
		if (_lg == _pm.high_good) _lg = arr_pick(_ids);
		_pm.low_good = _lg;
		_pm.low_t = _m + 1 + irandom(5);
		_pm.low_known = false;
	}
}

function port_is_contraband(_pid, _gid) {
	var gs = variable_struct_get(global.G.goods, _gid);
	return arr_contains(gs.contra_now, _pid);
}

function market_roll_all() {
	var G = global.G, D = global.D;
	for (var i = 0; i < array_length(D.ports_list); i++) {
		var _pid = D.ports_list[i].id;
		port_reroll_specials(_pid);
		var _pm = variable_struct_get(G.portmeta, _pid);
		var _mk = variable_struct_get(G.markets, _pid);
		for (var k = 0; k < array_length(D.goods_list); k++) {
			var g = D.goods_list[k];
			var gs = variable_struct_get(G.goods, g.id);
			var _steps = goods_steps(g);
			var _step = irandom(_steps - 1);
			if (g.id == _pm.high_good && (G.t div WEEKS_PER_MONTH) == _pm.high_t) _step = _steps + irandom(max(0, (_steps div 2) - 1));
			else if (g.id == _pm.low_good && (G.t div WEEKS_PER_MONTH) == _pm.low_t) _step = 0;
			var _price = gs.base + g.inc * _step;
			if (arr_contains(gs.contra_now, _pid)) _price *= 2;
			variable_struct_set(_mk, g.id, _price);
		}
	}
}

function price_at(_pid, _gid) { return variable_struct_get(variable_struct_get(global.G.markets, _pid), _gid); }

function contraband_rotate() {
	var G = global.G, D = global.D;
	var _n = struct_get_or(D.config, "contraband_ports_per_month", 2);
	for (var k = 0; k < array_length(D.goods_list); k++) {
		var g = D.goods_list[k];
		if (!g.contraband) continue;
		var gs = variable_struct_get(G.goods, g.id);
		gs.contra_now = gs.contra_next;
		var _cands = [];
		for (var i = 0; i < array_length(D.ports_list); i++) {
			var _p = D.ports_list[i];
			if (!_p.lawless && !arr_contains(gs.contra_now, _p.id)) array_push(_cands, _p.id);
		}
		arr_shuffle(_cands);
		gs.contra_next = [];
		for (var i = 0; i < min(_n, array_length(_cands)); i++) array_push(gs.contra_next, _cands[i]);
	}
}

/// Called once per elapsed month.
function economy_month_tick() {
	var G = global.G;
	contraband_rotate();
	if (G.bank > 0) G.bank += G.bank * eff("bank_interest", 0.01);
	if (G.debt > 0) G.debt += G.debt * eff("moneylender_interest", 0.1);
	G.bank = floor(G.bank);
	G.debt = ceil(G.debt);
	// Hired crew contracts expire.
	for (var i = array_length(G.items) - 1; i >= 0; i--) {
		var _it = G.items[i];
		if (_it.months > 0) {
			_it.months -= 1;
			if (_it.months <= 0) {
				log_add(trf("{0}'s contract has ended.", variable_struct_get(global.D.items, _it.id).name));
				array_delete(G.items, i, 1);
			}
		}
	}
}

// ---- cargo ---------------------------------------------------------------------------------
function cargo_used() {
	var G = global.G;
	var _n = 0;
	var _ships = fleet_all();
	for (var i = 0; i < array_length(_ships); i++) _n += _ships[i].guns * 5;
	var _ids = variable_struct_get_names(G.cargo);
	for (var i = 0; i < array_length(_ids); i++) _n += variable_struct_get(G.cargo, _ids[i]).qty;
	return _n;
}

function cargo_capacity() {
	var _ships = fleet_all(), _n = 0;
	for (var i = 0; i < array_length(_ships); i++) _n += ship_cargo_of(_ships[i]);
	return _n;
}
function cargo_free() { return max(0, cargo_capacity() - cargo_used()); }

function cargo_qty(_gid) {
	if (!variable_struct_exists(global.G.cargo, _gid)) return 0;
	return variable_struct_get(global.G.cargo, _gid).qty;
}

function cargo_add(_gid, _qty, _unit_cost) {
	var G = global.G;
	if (!variable_struct_exists(G.cargo, _gid)) variable_struct_set(G.cargo, _gid, { qty: 0, paid: 0 });
	var c = variable_struct_get(G.cargo, _gid);
	c.paid = (c.paid * c.qty + _unit_cost * _qty) / max(1, c.qty + _qty);
	c.qty += _qty;
}

function cargo_remove(_gid, _qty) {
	var G = global.G;
	if (!variable_struct_exists(G.cargo, _gid)) return;
	var c = variable_struct_get(G.cargo, _gid);
	c.qty -= _qty;
	if (c.qty <= 0) variable_struct_remove(G.cargo, _gid);
}

function buy_price(_gid) { return max(1, round(price_at(global.G.port, _gid) * eff("trade_buy_mult", 1))); }
/// Sellers pay 2% under the asking price, and never more than it (perks could otherwise make buy-then-sell a money loop).
function sell_price(_gid) { var _b = buy_price(_gid); return max(1, min(_b - (_b > 1), floor(price_at(global.G.port, _gid) * 0.98 * eff("trade_sell_mult", 1)))); }

function market_buy(_gid, _qty) {
	var G = global.G;
	var _price = buy_price(_gid);
	_qty = min(_qty, cargo_free(), floor(G.cash / _price));
	if (_qty <= 0) return 0;
	G.cash -= _qty * _price;
	cargo_add(_gid, _qty, _price);
	G.stats.trades += 1;
	return _qty;
}

function market_sell(_gid, _qty) {
	var G = global.G;
	_qty = min(_qty, cargo_qty(_gid));
	if (_qty <= 0) return 0;
	var _price = sell_price(_gid);
	var c = variable_struct_get(G.cargo, _gid);
	G.stats.profit += (_price - c.paid) * _qty;
	G.cash += _qty * _price;
	cargo_remove(_gid, _qty);
	G.stats.trades += 1;
	return _qty;
}

/// On arrival: customs may seize contraband (docs §2 contraband rotation).
function customs_check() {
	var G = global.G;
	var _port = variable_struct_get(global.D.ports, G.port);
	if (_port.lawless) return;
	var _ids = variable_struct_get_names(G.cargo);
	for (var i = 0; i < array_length(_ids); i++) {
		var _gid = _ids[i];
		if (!port_is_contraband(G.port, _gid)) continue;
		if (roll100() < eff("contraband_seizure", 35)) {
			var _q = cargo_qty(_gid);
			cargo_remove(_gid, _q);
			var _nm = variable_struct_get(global.D.goods, _gid).name;
			ui_message(tr("Customs!"), trf("The harbour authority found {0} {1} in your hold. It is outlawed here this month and has been seized.", _q, _nm), "portrait_governor");
			log_add(trf("Customs in {0} seized {1} {2}.", _port.name, _q, _nm));
		} else {
			log_add(trf("Slipped {0} past the customs men in {1}.", variable_struct_get(global.D.goods, _gid).name, _port.name));
		}
	}
}

// ---- finance -------------------------------------------------------------------------------
function net_worth() {
	var G = global.G;
	var _v = G.cash + G.bank - G.debt;
	var _ids = variable_struct_get_names(G.cargo);
	for (var i = 0; i < array_length(_ids); i++) {
		var gs = variable_struct_get(G.goods, _ids[i]);
		_v += gs.base * variable_struct_get(G.cargo, _ids[i]).qty;
	}
	var _ships = fleet_all();
	for (var i = 0; i < array_length(_ships); i++) _v += ship_value(_ships[i]);
	return floor(_v);
}

function max_loan() {
	var G = global.G;
	// Credit is a multiple of what you are worth after debts, so borrowing never raises your own limit.
	var _cap = max(global.D.config.moneylender_min_loan, net_worth() * eff("moneylender_max_loan", global.D.config.moneylender_max_loan_mult));
	return max(0, floor(_cap - G.debt));
}

// ---- alehouse tips -------------------------------------------------------------------------
function tavern_drink() {
	var G = global.G, D = global.D;
	var _cost = ceil(eff("alehouse_drink_prices", 25));
	if (G.cash < _cost) return "You can't even afford a drink.";
	G.cash -= _cost;
	if (roll100() >= eff("alehouse_tip_frequency", 60)) {
		var _flavor = ["The barkeep shrugs. Quiet month.", "A sailor tells you about a mermaid. Probably not useful.",
			"Somebody swears Grimmer has a twin. Nobody believes him.", "The ale is warm. The gossip is cold."];
		return arr_pick(_flavor);
	}
	// Contraband tip (a third of the time), otherwise a price tip.
	if (irandom(2) == 0) {
		var _cands = [];
		for (var k = 0; k < array_length(D.goods_list); k++) {
			var g = D.goods_list[k];
			var gs = variable_struct_get(G.goods, g.id);
			if (g.contraband && gs.unlocked && array_length(gs.contra_next) > 0) array_push(_cands, g);
		}
		if (array_length(_cands) > 0) {
			var g = arr_pick(_cands);
			var gs = variable_struct_get(G.goods, g.id);
			var _names = "";
			for (var i = 0; i < array_length(gs.contra_next); i++) {
				_names += (i > 0 ? tr(" and ") : "") + variable_struct_get(D.ports, gs.contra_next[i]).name;   // (closed ports may be named: it is still news)
			}
			var _t = trf("Word is {0} will be outlawed in {1} in {2}. Smugglers will pay double there.", g.name, _names, month_name((G.t div WEEKS_PER_MONTH + 1) * WEEKS_PER_MONTH));
			log_add(trf("Tip: {0}", _t));
			return _t;
		}
	}
	for (var tries = 0; tries < 10; tries++) {
		var _p = arr_pick(D.ports_list);
		if (!port_open(_p.id)) continue;
		var _pm = variable_struct_get(G.portmeta, _p.id);
		var _high_ok = _pm.high_t >= (G.t div WEEKS_PER_MONTH) && variable_struct_get(G.goods, _pm.high_good).unlocked;
		var _low_ok = _pm.low_t >= (G.t div WEEKS_PER_MONTH) && variable_struct_get(G.goods, _pm.low_good).unlocked;
		if (!_high_ok && !_low_ok) continue;
		var _t;
		if (_high_ok && (!_low_ok || irandom(1) == 0)) {
			_pm.high_known = true;
			_t = trf("Merchants in {0} will pay a fortune for {1} in {2}.", _p.name, variable_struct_get(D.goods, _pm.high_good).name, month_name(_pm.high_t * WEEKS_PER_MONTH));
		} else {
			_pm.low_known = true;
			_t = trf("{0} will be dirt cheap in {1} in {2}.", variable_struct_get(D.goods, _pm.low_good).name, _p.name, month_name(_pm.low_t * WEEKS_PER_MONTH));
		}
		log_add(trf("Tip: {0}", _t));
		return _t;
	}
	return "Nobody has anything worth hearing tonight.";
}
