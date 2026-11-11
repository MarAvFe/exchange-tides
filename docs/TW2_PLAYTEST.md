# Tradewinds 2 playtest notes (partial)

From an agent playing the original on 2026-11-11 for about 25 minutes. It was stopped before it wrote its report.
These notes are read off its 33 screenshots (they were in `C:\Games\tw2_tools\`). The screenshots are for internal
reference only; nothing from them goes into the remake.

The session played one captain (Russell Van Gregor) from 1 January to 2 April 1700. It took about 6 voyages:
Port Royal, Great Cayman, St. Thomas, Curaçao and Cartagena.

## Observed
- **Voyage length depends on distance and takes 1 to 2 weeks.** The log dates go Jan 1 → Feb 12 → Feb 26 → Mar 12 → Mar 26 → Apr 2.
  Most hops took 14 days, and one took 7. Exchange Tides now uses a flat 1 week.
- **Encounters are very frequent.** "Encountered pirates on the way to …" appears on nearly every voyage in the log
  (at least 4 of about 6), which is higher than our old 33%. Our new 55% is closer.
- **Battle:**
  - It is one enemy ship against your one ship. The enemy is far off and small on the horizon; your ship is large in
    the foreground.
  - On-screen hint: "Click on a target to begin combat. Your ship will automatically fire on the selected enemy."
    So you target by clicking and firing is automatic, the same model as ours.
  - A vertical brass gauge on the right is probably the reload or hull meter. A big "FLEE" button sits bottom right,
    and special-ammo icons sit on the water at the lower left.
  - Battles end quickly with a parchment "Victory!" box. Typical booty is about 900–1,100 gold early on
    ("You comb the remains and recover 977 gold").
- **Map:**
  - It is the real Caribbean: a continuous mainland coast (Colombia) plus big and small islands, with a dotted route
    line between ports.
  - A storm event appears on the map itself: "A storm has blown you off course to Curaçao" with a swirl icon.
  - Hint: "Press SPACE to change sailing speed".
- **Port screen:**
  - A painted harbour with buildings that are clickable hotspots.
  - The left sidebar has a portrait, Cash, Bank and Debt, and buttons for TASKS, LOG, ITEMS, CARGO, SHIP and MENU,
    so the ship and cargo each have dedicated screens.
  - The bottom bar shows the last 4 log lines with dates, with "SET SAIL" at bottom right.
- **Crew:** tavern characters join you after you buy them drinks, e.g. "Ms. Charlotte Bouvier has agreed to join
  your crew" (she gives tips). These are named NPCs with portraits.
- **Economy flavour from the log:** "Bought 50 crates of Cotton for 1,000 gold" and "Sold entire Cocoa stock for
  30,000 gold". The agent also bought a cannon for 6,000, fire pots for 1,000 each, and deposited 5,000 in the bank.
- **Running log:** every action (drinks, loans, purchases, battles, arrivals) is written to the bottom log as it
  happens.

## Differences that matter for Exchange Tides
1. Voyage time: TW2 scales it with distance (1–2 weeks). We could make long routes take 2 weeks using
   `route_length`.
2. TW2 battles are one-on-one and quick. Ours, with packs, a fleet and per-cannon loops, are deliberately richer and
   more tense.
3. TW2 uses the bottom log constantly. Our port screen only shows the latest log line in the objective bar.
4. Sailing speed toggle (SPACE): we have none.
5. Named crew recruited in taverns: ours are generic hires.
6. TW2 has dedicated SHIP and CARGO screens; we now have Fleet & Cargo.

Not yet observed (the session was stopped first): free mode, governor quests, the shipyard and buying ships, save
slots, music.

---

# Session 2: first-hand notes from the playing agent

These notes come from the agent that played. Where they disagree with the partial notes above, these are correct.

## Corrections to the partial notes
- **Every voyage takes exactly 7 days, whatever the distance.** The full sequence of arrival dates was
  Jan 29 (Port Royale) → Feb 5 (St. Thomas) → Feb 12 (storm, back to St. Thomas) → Feb 19 (storm, Curaçao)
  → Feb 26 (Cartagena) → Mar 5 (Curaçao) → Mar 12 (Cartagena) → Mar 19 (Port Royale) → Mar 26 (Great Cayman)
  → Apr 2 (St. Thomas).
  - Short hops (Cartagena–Curaçao) and long ones (St. Thomas–Cartagena, Great Cayman–St. Thomas) are the same
    one week.
  - A storm that blows you off course also costs exactly one week, and you land at another port.
  - The "14 days" in the partial notes came from reading only every other log line.
  - The flat 1-week voyage in Exchange Tides therefore **matches TW2**. (Note that MECHANICS.md says "month"; this
    build uses weeks.)
- **Encounters are not near-constant.** The tally for session 1 was 13 voyages:
  - 3 random pirate battles (voyages 1, 7 and 11);
  - 1 scripted story-NPC battle (a named pirate from the campaign task);
  - 2 storms, both of which blew the ship off course.

  That gives about 23% random fights and 15% storms per voyage. These are close to the extracted 33% and 12%.
  The partial notes overcounted because the log line "Encountered pirates on the way to X" names the **departure**
  port, not the destination. This looks like a TW2 text quirk.

## Session 1 facts (Story mode, captain Russell Van Gregor, sloop "Luisa")
- **New game:** Story Mode → pick one of several preset captains (portrait grid), or a custom one → intro text →
  you start in Great Cayman with a sloop. Each captain has a different storyline (see `character=` in `tasks.txt`).
- **Port buildings:**
  - Governor's mansion
  - Alehouse/tavern, which has a bartender, "Buy a Round of Drinks" and visiting NPCs such as a Trader who sells
    items
  - Bank
  - Moneylender
  - Marketplace
  - Shipyard
  - Warehouse
  - Beach/docks

  Each building opens a parchment dialog over the port painting: a portrait and NPC name, text that types out, and
  stacked scroll buttons. The building's name shows on hover.
- **Governors:** you can only see a port's governor once you've been granted access.
  - Locked governors turn you away with a one-liner, e.g. "Captain Van Who? … not on the guest list" (St. Thomas) or
    "You do not have an appointment. Good day." (Port Royale).
  - Access is a quest reward ("You now have access to the Governor of X").
  - An open governor shows **Task: <name>** and **Reward: <amount or Unknown>** in red, with Accept This Task and Leave.
  - Each governor has a name and a portrait.
  - Example job: an escort task, "let my niece sail with you for ten weeks", so deadlines are counted in weeks.
  - Story tasks are generated from templates with variables (port, NPC).
- **TASKS screen:** a red task title, with the current step indented under it ("Speak with Ms. Bouvier at the Alehouse
  in St. Thomas"). It is a stack, like `pushtask`/`poptask`.
- **LOG screen:** a full-page dated journal of every action. The bottom bar shows its last 4 lines.
- **Tavern:**
  - "Buy a Round of Drinks" costs 60 gold and gives a market tip, e.g. "Learned the price of Cocoa is HIGH in
    Cartagena in March".
  - **The tip was true:** Cartagena cocoa was 425 on Feb 26 and 600 on Mar 12.
  - The trader NPC "Wilson" sells special items, e.g. a "Battle Doll" with an Info popup.
- **Crew/passenger:** Ms. Charlotte Bouvier comes from a governor task and is collected at the St. Thomas alehouse.
  - She has no wage, but she "is expensive" and is said to make sailors volunteer information when you buy rounds.
  - So she is a tip-frequency modifier tied to drinks, and lasts for 10 weeks.
- **Bank:** shows Interest 1.00%, Cash and Bank, with a deposit box + max and a withdraw box + max.
  - Interest is credited monthly: 5,000 became 5,050 at the Apr 2 rollover.
- **Moneylender:** borrow and repay boxes with a max button. The loan was repaid in the next port.
- **Market** ("Mercado Cartagena", "Bloom's Marketplace"):
  - It lists 9 rows. The 5 unlocked goods (Fish, Cotton, Timber, Cocoa, Sugar) show price and owned. The other 4
    show as "???" until the story unlocks them.
  - A ship icon shows "Cargo: x / 75" with a fill bar.
  - Buttons are Buy, Sell and Leave.
  - To trade: select a row, press Buy or Sell, then type a quantity or press max, and confirm "for ship".
  - The log records "Sold entire Cotton stock for 5,000 gold".
- **Price samples:**

  | port | date | fish | cotton | timber | cocoa | sugar |
  |---|---|---|---|---|---|---|
  | St. Thomas | Feb 5 | 90 | 100 | 75 | 250 | 525 |
  | Cartagena | Feb 26 | 50 | 110 | 200 | 425 | 950 |
  | Cartagena | Mar 12 | 55 | 105 | 200 | **600** (tipped HIGH month) | 800 |
- **Shipyard:** Repair Ship, Buy Ship, Guns & Ammunition, Leave.
  - Buy Ship offers **one** named ship with these stats: "Recruit", Sloop, Hull 30, Max Guns 6, Attack Speed 15,
    Cargo 75, Special Ability "Heavy Cannon", Price 32,000. The choices are Buy This Ship or Don't Buy.
  - Each ship has a named special ability (ours: "Reinforced Oak", which adds +9 hull).
  - **Guns & Ammunition:**

    | item | buy | sell | effect | ammo |
    |---|---|---|---|---|
    | Cannon | 6,000 | 3,000 | takes 5 cargo space | unlimited |
    | Fire Pot | 1,000 | 500 | light damage to all ships | limited |
    | Chain Ammo | 1,000 | 500 | medium damage to one ship | limited |
    | Tiki Bomb | 25,000 | 12,500 | heavy damage to all ships | limited |

    Each row has −/+ arrows and an amount box. The bottom shows "Cargo: 25/75".
- **SHIP screen:** ship name, picture and type, then:
  - Hull Strength 36/30 (+9), with a bar
  - Cargo Capacity 75/75, with a bar
  - Cannons 5 (6 max)
  - Attack Speed 15
  - Special Ability
  - an Ammunition table (Fire Pot 2, Chain Ammo 2)
- **Battle (seen in 4 fights):**
  - It is real time and always 1 vs 1 so far. Your sloop sits in the foreground and the enemy on the horizon.
  - The banner says "Click on a target to begin combat. Your ship will automatically fire on the selected enemy."
    The clock is effectively paused until you click.
  - Clicking puts a red ring reticle on the enemy, with a small parchment hull bar above it.
  - **The column of cannon icons at top left has one icon per gun.** Each icon greys and brightens on its own as
    that gun reloads, so it really is per-cannon auto-fire.
  - The special-ammo icons sit on the water at the bottom: a fire pot and chain shot, each with a count badge.
    Click one to use it.
  - A tall green vertical gauge on the right is **your own hull**.
  - A pirate sloop died in about 6–8 seconds after targeting with 5–6 guns. Hull loss was small, a few points.
  - At the end the sea darkens, then a "Victory!" parchment appears with the booty (977 and 927 gold), followed by
    OK and a return to the map.
  - Clicking FLEE before targeting did nothing. Clicking it during a fight did not register before the enemy sank.

## Free Trade mode (session 2)
- **Start:** Main menu → Free Trade Mode → pick from the same 6 portraits. The 6th is a "?" for a custom captain.
  The character page shows a lore blurb on hover.
- After you pick, a short alternative-history intro plays. For Christine McGowan, the free game starts **January 1,
  1705**, versus **1700** in story mode.
- **Starting state:**
  - Cash 1,000, no bank, no debt.
  - Port Royale.
  - A sloop ("Rasputina") with 25/75 cargo already used, i.e. 5 cannons at 5 space each.
- **All 9 goods are unlocked from the start.** Port Royale prices on Jan 1: Fish 45, Cotton 30, Timber 50, Cocoa 250,
  Sugar 425, Arms 1,975, Textiles 3,000, Tobacco 4,500, Wine 5,000.
- **No governors at all.** Clicking the mansion gives a joke one-liner (the free mode has no governors), and that
  text runs off the right edge of the box. TASKS shows two flavour lines saying "Play Story Mode to get tasks…".
- **The map has a different port set from story mode.** Story mode had St. Thomas and Curaçao. Free mode has Havana,
  Belize, Trujillo, Great Cayman, Port Royale, Cartagena, Nevis, Guadeloupe, Martinique and Barbados (10 ports).
- **First voyage (Port Royale → Cartagena):** a storm hit immediately, with the message "You nearly lose your ship and
  crew in the mighty storm, but emerge alive in Belize" and a Continue button. The ship arrived in Belize on Jan 8,
  again exactly one week.
- **First trade:** 33 cotton bought at 30 in Port Royale and sold at 100 in Belize, turning 990 into 3,300 in one week.
  - In the market list, a good you own is shown with its price **in blue** at the port where you can sell it.
  - Cargo was 58/75 after the purchase.
- **CARGO screen ("Ship's CARGO"):**
  - A table of Item / Quantity / **Unit Cost** (your average purchase price) / **Market** (the local price), with up
    to 10 rows.
  - Below it, a ship card with the name, a picture and "Cargo: 58 / 75" with a bar, plus Leave.
- **Market buy panel:** pressing Buy opens a column for every row at once. Each row has a −/+ arrow, a typed amount
  box and a **max** button. One "Buy for Ship" button commits all rows together (tooltip: "Cargo will go to your
  Ship"). Sell works the same way.
- **The bank interest rate varies by port:** Port Royale Bank pays 1.20% and Cartagena's Bloom Bank pays 1.00%. The
  welcome text is cut off ("How may I be of assistanc").
- **Warehouse** (e.g. "Port Royale Store More"):
  - It shows "Your space: None", "Can upgrade to: 250 Cargo" and "Upgrade price: 100,000 Gold".
  - Its buttons are Purchase Warehouse and Visit Warehouse.
  - A warehouse is per-port storage you buy.
- **Voyage timing in free mode** (dates from the log):

  | route | departed | arrived | note |
  |---|---|---|---|
  | Port Royale → (Cartagena) | Jan 1 | Belize, Jan 8 | storm, blown off course |
  | Belize → Trujillo | Jan 8 | Jan 15 | short hop |
  | Trujillo → Barbados | Jan 15 | Jan 22 | the whole width of the Caribbean, with a storm outrun and a battle on the way |

  **Every voyage is exactly 7 days, regardless of distance or events.**
- **Storm outcomes seen:**
  1. "You nearly lose your ship and crew in the mighty storm, but emerge alive in Belize": blown off course to a
     random port.
  2. "A storm! Luck was with you, Captain. You have successfully outrun it.": no effect.

  Both appear as a dark-blue banner with a swirl icon and a Continue button over the map, and the ship pauses
  mid-route.
- **Ship movement on the map:**
  - A sailing-ship sprite moves along a **dotted route line**, which is a curved polyline routed around land, from
    the port to the destination.
  - At normal speed the trip takes about 3–6 s of real time. "Press SPACE to change sailing speed" sits on a scroll
    at the top right; it toggles a faster animation, and in-game time is unaffected.
  - Encounters happen **mid-route**: the ship is replaced by a black pirate flag on the line, the screen fades to
    dark, and the battle scene loads.
- **The SHIP screen shows the bonus from the ship's ability:** the free-mode sloop "Rasputina" has the **Speed Cannon**
  ability, displayed as "Attack Speed 15 (+3)". The story sloop had Reinforced Oak, "Hull 36/30 (+9)". Abilities
  seen so far are Heavy Cannon, Speed Cannon and Reinforced Oak.
- **Starting ammo:** 2 Fire Pots and 2 Chain Ammo (in both modes).
- **Prices do not move when you trade.** Buying 9 sugar at 475 left the price at 475. Buy turns grey when you can't
  afford more.
- **Barbados prices on Jan 22:**

  | good | Barbados | Port Royale (Jan 1) |
  |---|---|---|
  | Fish | 90 | |
  | Cotton | 95 | 30 |
  | Timber | 150 | |
  | Cocoa | 425 | |
  | Sugar | 475 | |
  | Arms | 2,850 | |
  | Textiles | 3,500 | 3,000 |
  | Tobacco | 4,500 | |
  | Wine | 7,500 | 5,000 |

  The Belize prices on Jan 8 were Fish 90, Cotton 100, Timber 125, Cocoa 325, Sugar 575, Arms 2,850,
  Textiles 3,100, Tobacco 6,000 and Wine 7,000. **The spread for the same good between ports is often 2–3×**
  (cotton 30 vs 100).
- **Port building names vary per port and show on hover:** "Bloom Bank" (a chain shared by several ports), "Pine Place
  Market", "Fernandez's Mansion", "The Blowfish" (alehouse), "Barbados Ships" (shipyard). Not every port has every
  building: Belize and Barbados had no visible moneylender.
- **Free-mode tavern:** only the bartender (a named woman with a portrait) plus "Buy a Round of Drinks". There is no
  trader and no recruit. With 25 gold the bartender says you can't afford it, and the log adds "You cannot afford to
  buy a round of drinks."
- **Shipyard Buy Ship in free mode:** it offers exactly one ship, a named sloop ("Navigator": Hull 30, 6 guns,
  Attack Speed 15, Cargo 75, Heavy Cannon, 32,000).
  - Buy This Ship is greyed when you can't afford it.
  - **You own one ship at a time.** Buying replaces your current ship; there is no fleet list anywhere in the UI.
- **Fight #5** (session 2, Trujillo → Barbados), measured with 95 ms frame captures:
  - 1 pirate sloop (black sails) against us.
  - After the target click, the red reticle and the enemy hull bar appeared above the enemy.
  - **5 guns fired staggered, not as a broadside.** Each cannon icon flashes orange when it fires, goes dim grey, and
    slowly refills to blue. One gun's cycle was ≈ 28 frames ≈ **2.7 s** (Attack Speed 15, +3 from Speed Cannon).
  - The pirate's hull bar went from full to empty in **≈ 4.0 s**. Our hull gauge (the tall green bar on the right)
    did not visibly drop: 0 damage.
  - The end: the wreck sinks, the scene dims, and a "Victory!" box says "You have liberated 990 gold". The log adds
    "We sank their ship, Captain!" and "Victory! Salvaged 990 gold from the battle."
  - We then continued to the destination in the same week.
- **Barbados → Martinique** (a neighbouring island): Jan 22 → Jan 29, again 7 days, with no event. The log line
  for an uneventful arrival is "Found Martinique to be a hospitable port."
- **Martinique prices, Jan 29:** Fish 55, Cotton 30, Timber 175, Cocoa 325, **Sugar 900**, Arms 2,150,
  Textiles 4,100, Tobacco 6,500, Wine 7,000.
  - Sugar bought at 475 in Barbados sold here for 900, so 4,275 became 8,100 in one week.
  - In both the CARGO screen and the market, the "Market" price of a good you hold shows **in light blue** when it is
    above your unit cost.
- **The multi-row buy panel** let me queue Arms and Cotton and commit them separately. Each commit writes its own log
  line ("Bought 2 crates of Arms for 4,300 gold", "Bought 48 crates of Cotton for 1,440 gold").
- **Martinique buildings:** Governor Wright's mansion, Martinique Creditors (moneylender), The Bronze Bar,
  Merchant's Wharf and the Dutch Bank of Martinique. Clicking your own ship sprite in the harbour opens the CARGO
  screen.
- **Fight #6 (Martinique → Port Royale): special ammo test.**
  - **How it's used:** click the target, then click the **Fire Pot icon** on the water at the lower left. Our ship
    immediately throws a flaming volley; it shows as fireball sprites arcing to the enemy and explosions on impact.
    Its count badge went 2 → 1.
    - With only one enemy, "hits all ships" can't be distinguished from a single-target hit.
    - The fire pot plus normal guns killed the pirate in ≈ 25 frames ≈ **2.4 s**, versus ≈ 4 s without it.
  - **Our damage:** hull 30 → 28. **The enemy also destroyed one of our cannons.** Its icon in the gun column turned
    into a red-crossed cannon, and the log said "We'll need to replace that cannon, Sir!".
    - After the fight the SHIP screen showed Cannons 4 (6 max). Cargo dropped 75 → 70 because the cannon's 5 cargo
      slots were freed.
    - **Losing guns is the real attrition in TW2 fights**, more than hull loss.
  - The log during a fight streams lines like "Captain! The enemy is destroyed!" (highlighted in blue).
  - Victory text: "Well done, Captain McGowan! 931 gold is yours!" **Victory text varies at random** between fights.
  - **Booty so far:** 977, 927, 990, 931. That is always ≈ 900–1,000 for a pirate sloop, so it is not scaled to the
    player's wealth.
- **Martinique → Port Royale** (across the Caribbean): Jan 29 → Feb 5, 7 days.
- **Selling:** the Sell panel has a per-row −/+/max column plus **"Sell from Ship"** and **"Sell All Ship's Cargo"**,
  which is one click. Cotton bought at 30 in Martinique sold for 100 in Cartagena, and Arms bought at 2,150 sold
  for 2,825.
  - Free-mode cash: 1,000 → 13,766 in 6 weeks with a 75-cargo sloop, so the economy snowballs quickly.
- **Cannons are sold back at half price** (6,000 to buy, 3,000 to sell). Selling all 4 freed 20 cargo
  (5 per gun). Fire Pot, Chain Ammo and Tiki Bomb don't take cargo.
- **Saves:** Menu → Save Game shows **9 slots**. Each slot is labelled "<Captain> – <Port> <Date>", e.g.
  "Russell Van Gregor – Curacao January 15th, 1700". Clicking a slot saves immediately with no confirmation and
  returns to the in-game menu. There is also an autosave on departure (`auto.sav`, per MECHANICS.md).
  - **In-game menu:** Resume, Save Game, Load Game, Options, Quit to Main Menu.
  - **Main menu:** Story Mode, Free Trade Mode, Load Game, Options, Quit.
- **Options:**
  - Music Volume slider
  - Sound FX Volume slider
  - Switch to FULL SCREEN (the game was windowed 800×600)
  - Graphic Detail High/Low
  - **Sailing Speed Fast/Slow**, the same setting the SPACE key toggles on the map
  - **Dialogue Speed Fast/Slow**, the speed of the typewriter text
  - Tutorial ON/OFF
  - Help, which opened nothing visible
- **Music and sound** (from `audio.txt`/`scenes.txt` plus the sound files; the agent could not hear the output):
  - **Music:**
    - a looping main-menu theme;
    - **6 port themes**, each port picking one of port1–port6;
    - a sailing theme on the map;
    - 3 combat variants, plus a "to combat" sting and victory and defeat stings.
  - **Ambience:** 3 ambient loops, rain and thunder.
  - **SFX:** each building has its own entry sound (bank, moneylender, shipyard, warehouse, trader, marketplace,
    alehouse pour, port authority). There are also separate sounds for player and enemy cannon (3 each), impacts on
    wood, metal and sails, splashes, ship sinking, cannon destroyed, fire pot, chains, tiki bomb, contraband seizure,
    off course, discover port, map fold and unfold, and buy/sell.
  - There are also sea-shanty stingers ("yo ho ho", "ninety-nine bottles", "oh danny boy"), presumably for the tavern.

## Not covered (stopped at the coordinator's request)
- **Losing a fight.** A save with 0 cannons and cocoa cargo is ready in slot 2 (Cartagena, Feb 12 1705, free mode),
  but no unarmed fight was played. The defeat penalty was not observed.
- **FLEE during a fight.** Earlier clicks didn't register before the pirate sank, so the flee odds and message were
  not observed. MECHANICS.md has the formula: 30% base, +10% per try, 80% max.
- **Chain ammo and Tiki Bomb** effects in a fight. Multi-enemy fights never happened: all 6 fights were 1 vs 1.
- **A governor task completed end to end in this session.** Session 1 did complete the first story task (reward
  claimed at the Great Cayman governor) and accepted a second (escort Ms. Bouvier for 10 weeks). Missed deadlines
  were not seen.
- **Contraband and customs.** No seizure or contraband notice came up in the ports visited.
- **The free-mode win condition.** The intro gives no goal or time limit, and the TASKS screen only says to play
  Story Mode.
- Warehouse use, beach/docks, the trader's full item list, ship upgrades, and later ship unlocks.

## Final tallies (both sessions)
- **Voyages: about 20, every one exactly 7 days** regardless of distance.
- **Random pirate fights: 6** (story 3 + free 3), plus 1 scripted story fight. That is about 30% of voyages.
- **Storms: 4.** Three blew the ship off course to another port and one was outrun.
- **Fights:**
  - All were 1 pirate sloop versus our sloop.
  - All were won in 3–8 s of real time.
  - Hull loss was 0–2 points of 30.
  - One cannon was destroyed once.
  - Booty was 927–990 gold.

## Differences that matter for Exchange Tides (final)
1. **Voyage length: keep the flat 1 week.** TW2 uses exactly 7 days per voyage for every route, short or long, and a
   storm detour still lands in 7 days at a different port. Our planned 1-week voyage matches; don't add
   distance-scaled time. (Note that MECHANICS.md §1 says "one voyage = one month"; update it to "one week".)
2. **Fleet of up to 5 is a real departure.** TW2 has **one ship only**:
   - The shipyard offers exactly one named ship at a time ("Buy This Ship / Don't Buy"), and buying it replaces
     yours.
   - There is no fleet UI, no ship swapping and no selling a ship separately.
   - Our fleet screen, per-ship cargo and multi-ship battles have no TW2 precedent, so design them fresh (and keep
     buying a ship a single, clear decision, as TW2 does).
3. **Per-cannon auto-fire matches TW2, so copy the feel:**
   - one icon per gun in a column;
   - each gun cycles on its own (flash → grey → refill), staggered rather than as a broadside;
   - about 2.7 s per gun at Attack Speed 15;
   - firing starts when you **click a target**, and nothing happens until you do.

   Add **cannon loss** as attrition: enemy hits can destroy a gun ("need to replace that cannon"), and you rebuy it
   for 6,000 at a shipyard. TW2 relies on this, not on hull, to make fights cost something.
4. **Battles should be harder or larger than TW2's.** Early TW2 fights are trivial: 1 enemy, 3–8 s, about 0 hull
   loss, roughly 950 gold of booty. That makes them a toll, not a threat. Our packs and fleet battles should keep
   real risk; scale booty with enemy class rather than using a flat ~950.
5. **Special ammo as on-water click icons with count badges** (fire pot = all ships, light; chain = one ship, medium;
   tiki bomb = all ships, heavy). Ammo is bought at the shipyard's Guns & Ammunition panel, takes no cargo, and sells
   back at half price. Our action-bar ammo should show counts the same way.
6. **Governor contracts:**
   - In TW2 they are story-only. Free mode has **no governors** ("no governors in free mode").
   - In story mode, a governor is locked until a previous task grants "access", and each one shows a single
     Task/Reward offer (red text) with Accept/Leave.
   - Deadlines are counted in weeks (a 10-week escort).
   - For our governor contracts:
     - Make them available in free mode too (TW2 leaves that mode thin).
     - Show the reward and the deadline up front in the same offer box.
     - Consider access gating as progression.
7. **Coastline map with routed sailing matches TW2.**
   - TW2 draws the real Caribbean: mainland coasts plus islands, about 10 ports per mode, and a **dotted curved route
     around land**.
   - The ship sprite moves along the route in 3–6 s, and encounters interrupt it mid-route with a pirate flag and a
     fade to the battle.
   - Storms appear as a banner over the map with a Continue button.
   - Add a **sailing-speed toggle** (SPACE and an Options setting) that only changes the animation.
8. **Market UX worth matching:**
   - Prices don't move when you trade.
   - Owned goods' local prices show **blue when above your average cost**.
   - The CARGO screen shows **Unit Cost against Market** per good.
   - The sell panel has a one-click **"Sell All Ship's Cargo"**.
   - The buy/sell panel has a per-row −/+/max with a typed amount.
   - Every trade writes a dated log line.
9. **Running log:** a dated, always-visible 4-line log strip at the bottom of every screen (port, map, battle), plus a
   full LOG page. Ours shows only the latest line, so add the multi-line strip.
10. **Tavern tips are bought** (a 60-gold round) and are **truthful and month-specific** ("Cocoa HIGH in Cartagena in
    March" was correct: 425 became 600). With too little cash the bartender quips and the log records "cannot
    afford". Named crew such as Ms. Bouvier come **from quests** and act as modifiers (tip frequency) with a duration.
11. **Building identity:** every port names its buildings ("Bloom Bank", "The Blowfish", "Merchant's Wharf") and shows
    the name on hover, and **not every port has every building**. Bank interest varies by port (1.0% vs 1.2%).
    Warehouses are bought per port (250 cargo for 100,000).
12. **Ship special abilities:**
    - Each purchasable ship rolls a named ability (Heavy Cannon, Speed Cannon, Reinforced Oak).
    - The SHIP screen shows the result as a bonus, e.g. "Attack Speed 15 (+3)" or "Hull 36/30 (+9)".
    - This is cheap variety we could adopt for the ships in our fleet.
13. **Saves:** 9 manual slots labelled "Captain – Port Date", saved with one click and no confirmation, plus an
    autosave on departure. Options cover music and SFX volume, sailing speed, dialogue (typewriter) speed, the
    tutorial toggle and graphic detail. Make sure ours has the dialogue-speed and sailing-speed options.
14. **Audio structure to mirror with original music:**
    - several port themes, one chosen per port;
    - a separate sailing theme;
    - 3 combat variants, with to-combat, victory and defeat stings;
    - a distinct entry sound for each building;
    - separate player and enemy cannon sounds and material-specific impacts.
15. **UI text overflow exists in TW2 too:** the free-mode governor line and the bank greeting both clip. Keep our
    fixed-width parchment boxes wrapping or shrinking text.
16. **Still to check in TW2 if needed:**
    - the defeat penalty (slot 2 is set up for it);
    - flee odds in practice;
    - contraband seizure;
    - multi-enemy fights at higher levels;
    - the free-mode win condition.
