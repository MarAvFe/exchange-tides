# Tradewinds 2 — extracted mechanics (reference for the remake)

Source: static analysis of `tw2_vista.exe` (Ghidra 12.1.4 via REA) plus the decoded XML configs.
Addresses refer to `tw2_vista.exe` (image base 0x400000). The full decompile is in `re/decomp.c`; use
`tools/fn.sh FUN_xxxxxxxx` to print a single function.
This document describes **mechanics and numbers only**. The remake uses its own names, text, characters and art.

Confidence: **observed** = read directly from code/data. **inferred** = decompiler lost operands; the
meaning comes from context.

## 0. Data pipeline

| Item | Detail |
|---|---|
| Archives | `TW2_00.data` (25 XML configs) and `TW2_01.data` (2,774 jpg/png/ogg/fm files). Layout: `u32 0x0000DCAC`, `u32 count`, then per entry `name\0, u32 offset, u32 size`. Reader at `0x45d110`. |
| XML obfuscation | `plain[i] = (cipher[i] - KEY[i % 20]) & 0xFF`, with `KEY = "klxd8794lkds87934poi"` (set in the TWApp ctor `0x4438c0`). Only `*.txt` entries are obfuscated. |
| Tools | `tools/tw2pak.py list|extract`, `tools/xml2json.py` (tolerant parser), `tools/peconst.py` (reads exe constants). |

## 1. Time

- The calendar is **months** (`app.txt` has 12 `<month>` entries). The global current month is read via `DAT_0049b008`.
- One voyage = one week (7 days) regardless of distance, confirmed by playing the original (docs/TW2_PLAYTEST.md). A storm can cost an extra week (`lost_turn`). The calendar is shown by month; monthly events (interest, contraband) tick every 4 weeks.
- Monthly tick `FUN_0042b020` runs over every port: hidden-port reveal countdown, alehouse refresh, bank tick,
  market re-roll (`FUN_0041d8c0`), shipyard refresh. Finance interest is applied by `FUN_004105d0` when the
  month changes.

## 2. Economy (observed)

### Good definition (`goods.txt`, loader `FUN_00417450`)
`min, max, increment, range`; `steps = range / increment`; flags `canbecontraband`, `forsale`, `startgood`.

| good | min | max | inc | range | contraband | start | forsale |
|---|---|---|---|---|---|---|---|
| fish | 10 | 100 | 5 | 50 | – | ✔ | ✔ |
| cotton | 10 | 150 | 5 | 100 | – | ✔ | ✔ |
| timber | 50 | 250 | 25 | 150 | – | ✔ | ✔ |
| cocoa | 150 | 600 | 25 | 300 | – | ✔ | ✔ |
| sugar | 300 | 1000 | 25 | 500 | – | ✔ | ✔ |
| arms | 1000 | 3000 | 25 | 1000 | – | – | ✔ |
| textiles | 2000 | 6000 | 50 | 2000 | – | – | ✔ |
| tobacco | 3000 | 8000 | 500 | 3000 | ✔ | – | ✔ |
| wine | 5000 | 10000 | 500 | 3500 | ✔ | – | ✔ |
| gem | 10000 | 25000 | 3000 | 15000 | – | ✔ | ✘ (sell-only) |

### Global base price (new game, `FUN_0041dc50`)
```
base = min + inc * randint(0, (max - range - min) / inc)      // inferred: rand scaled into that many steps
unlocked = startgood || globalUnlockFlag                       // other goods unlock via story progress
```

### Per-port monthly price (`FUN_004175e0`), per (port, good)
```
step = rand() % steps
if month == entry.highMonth: step = steps + rand() % (steps/2)   // spike: above the normal band
elif month == entry.lowMonth: step = 0                           // trough: the base price
price = base + inc * step
if entry.contrabandHere: price *= 2
```
Each port's market saves one "high" good with its month and one "low" good with its month (`MarketplaceData`).

### Contraband rotation (`FUN_00428bf0`, monthly)
Each contraband-capable good keeps two port lists: `current` (illegal now, so price ×2) and `next`.
Each month: ports in `current` drop out; ports in `next` become `current`; then **2 random other ports** go
into `next`. Port authorities can seize contraband (`contraband_seizure` effect, `FUN_00428750`).

### Alehouse tips (`FUN_004020d0`, `FUN_00401a90`)
- Contraband tip: names next month's contraband ports for a good (`contraport`, `contramonth`, `contragood`).
- Price tip: picks up to 10 random ports looking for one with a high or low entry. If both exist, it is a 50/50
  choice. It reveals "good X will be high/low in port P in month M". Tip frequency uses the `alehouse_tip_frequency` effect.

### Finance (`FUN_004105d0`, base rates in `app.txt`)
```
monthly: bank   += bank * effect("bank_interest", 0.01)
         debt   += debt * effect("moneylender_interest", 0.10)
max loan = effect("moneylender_max_loan", 2.0) × (something)    // multiplier observed (2.0); its base is not traced
```

## 3. Effect / modifier system (observed: `FUN_00438ad0`, `FUN_004381b0`)
Every owned item carries effect strings like `name(value);name2(value)`. To evaluate an effect, start
from the base value and apply **each owned item in order**:

| value form | operation |
|---|---|
| `N` | set = N |
| `+N` / `-N` | add / subtract N |
| `+N%` / `-N%` | multiply by (1 ± N/100) |

Effect names used: `sailing_combat_frequency, sailing_storm_frequency, sailing_lost, sailing_delay,
combat_player_accuracy, combat_enemy_accuracy, combat_speed, combat_enemy_speed, ship_space, ship_health,
bank_interest, moneylender_interest, moneylender_max_loan, alehouse_tip_frequency, alehouse_drink_prices,
contraband_seizure, flee_success_base/max/inc`.

Item durations: `indefinite`, `contract` (hired, expires after N weeks or months; the UI says "expires in x weeks"),
or `ship` (an upgrade lost when the ship changes).

## 4. Sailing (observed: `FUN_0044f470`, `FUN_00450640`; values from `worldmap.txt`)
```
on depart: autosave
storm  = roll100 <= effect("sailing_storm_frequency", 12)
if not storm:
  c = effect("sailing_combat_frequency", 33)
  if c > 100: extra = (c - 101) / 80 + 1 battles queued; c -= 80 * extra
  battle if roll100 <= c
storm resolution:
  if roll100 <= effect("sailing_lost", 10): "outran storm"
  elif roll100 <= effect("sailing_delay", 10): lose a week (calendar +1)
  else: blown off course to a random port ("lost_in_storm")
```
Note: the storm thresholds are as observed. A >80% chance of being blown off course feels harsh, so the remake exposes these in config.

## 5. Combat (observed: `FUN_0040b450`, `FUN_0040b730`, `FUN_00409820`, ships loader `FUN_00430ff0`)
- Ship stats: `hitpoints, maxguns, firespeed` (reload time, lower = faster), `thaco` (how easy the ship is
  to hit, in %), `cargospace, spacepergun (5), price range, unlockdifficulty`; enemies add `booty, startdifficulty`.
- **Hit chance** = `clamp(target.thaco + shooterAccuracyBonus, 0, 100) / 100`. Bonuses come from
  `combat_player_accuracy` / `combat_enemy_accuracy` (base 0).
  Player ships have thaco 50; enemies have 70–100.
- Ammo (`ships.txt supplies`): cannon (dmg 1 per gun, a gun costs 5 cargo), firepot (5, hits all targets), chains (10),
  tiki bomb (25, hits all targets). Special ammo takes no cargo space.
- **Flee**: base 30%, +10% per attempt, max 80% (from `flee_success_*` effects). In port battles, flee is fixed at 100%.
  The UI has a race: `flee/min 50, random 250, marker 720`.
- Weather: 10% of sea battles get weather (50/50 rain or fog).
- Port battles: forts/cannon emplacements in tiers 0–5 (hp 10–200, guns 2–40, booty 1k–100k).

| ship | hp | guns | reload | thaco | cargo | price | unlock lvl |
|---|---|---|---|---|---|---|---|
| sloop | 30 | 6 | 15 | 50 | 75 | 20–40k | 0 |
| schooner | 60 | 10 | 10 | 50 | 125 | 30–50k | 4 |
| brigantine | 100 | 15 | 9 | 50 | 200 | 70–90k | 8 |
| barque | 200 | 20 | 8 | 50 | 250 | 200–250k | 16 |
| galleon | 250 | 20 | 7 | 50 | 300 | 0.9–1M | 24 |
| frigate | 300 | 25 | 6 | 50 | 400 | 2.05–2.25M | 30 |
| man-o-war | 350 | 30 | 6 | 50 | 250 | 2.0–2.52M | 40 |

## 6. Tasks / campaign (data: `tasks.txt`, 110 tasks; engine `TaskMaster`)
```
<task level name reward character levelup>
  <variables>  port vars chosen by filters (here,new,visible,governor_access,alehouse,shipyard),
               npc vars (location = port + building, or filters for a procedural NPC), location vars
  <steps>      okbox(npc,text,ok)  goal(type, npc|port|good|amount)  pushtask/poptask  addlogentry
               get/give(item,amount)  unlockship  makehostile(port)  accessgovernor  tasklevel  command
```
Goal types and frequency: `talk` 399, `npccombat` 82, `arrive` 19, `have` 17, `deposit` 9, `buy` 8, `combat` 3,
`withdraw` 1, `repay` 1. Text uses `{var}` substitution.

## 7. Save format (observed: `FUN_004431e0`, primitives `FUN_0040f3b0..0040f620`)
Raw little-endian stream: `u8`, `i32`/`f32`, `i64`/`f64`, and NUL-terminated strings. **Packets** consist of
`name\0`, then the body, then a trailing `u32 byteLength` (written on close; the name is checked on load).
The top-level packet `"TW2 Savegame"` holds a header string (`"<char> - <port> <date>"`) and a u8, then these sections:
`SpecialItemMgr, CharacterMgr, Calendar(i32×3), PortMgr{Port{AlehouseData, TraderData, BankData, GovernorData,
MoneylenderData, Shipyard, WarehouseData, MarketplaceData}…, Marketplace}, log, FinanceMgr(f64 bank, f64 debt…),
TaskMaster, …, TWApp{Sidebar}`.
Location: `CSIDL_COMMON_APPDATA\Sandlot Games\Tradewinds 2\Saved Games\` (`auto.sav` is the autosave).
The remake uses its own JSON save, so this section is a reference only.
