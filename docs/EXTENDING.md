# Extending Exchange Tides

Almost everything is data. Content lives in `game/ExchangeTides/datafiles/` and is loaded at runtime,
so new content needs **no IDE work**. After adding or removing *files*, rerun the manifest generator so
GameMaker packages them:

```sh
python3 -I tools/gen_project.py          # rewrites ExchangeTides.yyp + .yy files from the folder layout
```

Editing an existing JSON file does not require this step.

## Add a captain (playable character)
1. Add a portrait PNG (about 160×200) to `datafiles/sprites/`, e.g. `portrait_morgan.png`. To generate one in the
   house style, add an entry to `people` in `tools/artgen/gen.py` and run
   `python3 -I tools/artgen/gen.py game/ExchangeTides/datafiles/sprites`.
2. Add an entry to `datafiles/data/characters.json → captains`:
   ```json
   {"id":"morgan","name":"Elise Morgan","title":"Captain","portrait":"portrait_morgan",
    "bio":"...","port":"tidewell","cash":2500,"bank":0,"debt":0,"ship":"sloop",
    "ship_name":"Night Heron","guns":5,"ammo":{"firepot":2,"chains":2},"perk":"my_perk"}
   ```
3. Give them a perk in `items.json` (`"kind":"perk"`) with an effect string (see below).
The captain-select screen lays out however many captains exist.

## Add an NPC
Add `{"id":"harbourmaster","name":"Harbourmaster","portrait":"portrait_x"}` to `characters.json → npcs`.
Campaign `say` steps and `talk` goals can then use `"npc":"harbourmaster"`.

## Add an item / effect
`items.json` entries use `kind`: `perk` (starting trait), `curio` (sold by curio dealers), `hire`
(a tavern crew member with a `months` contract: a generated person of that port who gives the effect while aboard), `upgrade` (shipyard refit, lost when you change ships) or `quest`.

The effect grammar is the original game's (`docs/MECHANICS.md §3`): `name(value);name2(value)` where the value is
`N` (set), `+N`/`-N` (add) or `+N%`/`-N%` (scale). Every effect is read through `eff("name", base)`, so a new
effect name only needs one `eff()` call wherever the game should respect it. Existing names:

`sailing_storm_frequency, sailing_combat_frequency, sailing_lost, sailing_delay, combat_player_accuracy,
combat_enemy_accuracy, combat_speed, combat_enemy_speed, ship_space, ship_health, bank_interest,
moneylender_interest, moneylender_max_loan, alehouse_tip_frequency, alehouse_drink_prices, contraband_seizure,
flee_success_base, flee_success_inc, flee_success_max`

## Add a good, port or ship
- **Good**: `goods.json` (`min/max/inc/range` drive the pricing model) plus an icon `good_<id>.png`.
- **Port**: `ports.json` with `buildings` (`market, bank, lender, shipyard, tavern, governor, curio`), then add a
  rough coastal spot to `PORT_SPOTS` in `tools/artgen/worldmap.py` and run `python3 -I tools/artgen/worldmap.py`. It
  snaps the port onto the coast, rewrites its `x,y`, redraws the map and recomputes every sea route. Give the port a
  governor in `characters.json → governors` (name + greeting).
- **Player ship**: `ships.json → player` (`level` gates the shipyard).
- **Enemy**: `ships.json → enemies`, using `level` for random encounters, `"unique":true` for story-only ships,
  and a `behavior`.

## Add an enemy behaviour (AI)
In GML, from any script (or in `scr_behaviors`):
```gml
behavior_register("boarder", function(e, C, dt) {
    // e: hp, max_hp, reload, reload_time, guns, wait, tried_flee   C: the combat state
    if (e.hp < e.max_hp * 0.3) return "flee";
    if (e.reload <= 0 && C.time > 2) return "fire";
    return "";
});
```
Then set `"behavior":"boarder"` on any enemy in `ships.json`.

## Add campaign chapters
`campaign.json → chapters[]`. Each chapter has `vars` (port pickers: `other`, `new`, `has:<building>`) and
ordered `steps`:

| step | fields |
|---|---|
| `say` | `npc, text, ok` (text supports `{p1}`, `{captain}`, `{here}`) |
| `log` | `text` |
| `get` / `give` | `item` |
| `reward` | `cash` |
| `unlock_good` | `good` |
| `set_level` | `level` |
| `take` | `good, amount` (removes cargo, e.g. after a `deliver` goal) |
| `goal` | `type` + fields: `talk(npc,port,building)`, `arrive(port)`, `have_good(good,amount)`, `deliver(good,amount,port)`, `deposit(amount)`, `cash(amount)`, `networth(amount)`, `repay`, `combat(wins)`, `sink(n)`, `npccombat(enemy,port)` |
| `end` | finishes the campaign |

To add a new step or goal type, add a `case` to `campaign_run_step` / `campaign_goal_met` in `scr_campaign`.

## Art and fonts
- **Style:** follow `docs/ART_STYLE.md`.
- **Painted sprites:** generated with `tools/artgen/comfy_gen.py` from a local ComfyUI server running DreamShaper XL Lightning.
  1. Add an entry to `tools/artgen/art_spec.json`:
     - `txt2img` for new illustrations; set `out` to the size in pixels when there is no existing sprite.
     - `img2img` with a vector reference in `tools/artgen/vector/` when the layout or transparency must be kept.
  2. Generate the variants, then install the ones you choose:
     ```sh
     python3 -I tools/artgen/comfy_gen.py --host http://127.0.0.1:8188 --only portrait_morgan --variants 3
     python3 -I tools/artgen/comfy_gen.py --install --pick portrait_morgan=2
     ```
     Candidates are saved to `tools/artgen/out/`.
- **Panel texture:** `ui_parchment.png` is optional. When it exists, every paper panel uses it.
- **Fonts:** `datafiles/fonts/`. Body text is Alegreya and headings (text scale 1.6 and above) are Pirata One, both under the SIL Open Font License. Loading and size selection are in `ui_fonts_load` / `ui_font` in `scr_ui`.

## Tuning
`config.json` holds every base rate (interest, storm and combat odds, flee chances, repair and cannon prices,
free-mode goal).

## Governor contracts
`scr_contracts` rolls 2-3 jobs per governor each month (`deliver`, `courier`, `bounty`, `hunt`, `passenger`). A passenger boards on accept and is paid on arrival; if late they disembark at the next port. To add a kind,
generate it in `contract_roll`, describe it in `contract_text`, and complete it in `contracts_on_arrival`,
`contracts_on_sink` or `contracts_on_hunt_won`. Pirate captain names for hunts are in `config.json → pirate_names`.

## Music
Each mood is a sound asset `sounds/snd_music_<mood>/`. `tools/music.py` downloads and levels the tracks; rerun
`tools/gen_project.py` after adding one, then map screens to it in `music_pick()` (`scr_audio`).

## Portraits for new characters
A character's `portrait` sprite can be added later: until `sprites/<portrait>.png` exists the game shows
`portrait_fallback`. Add a prompt to `tools/artgen/art_spec.json` and generate it with `comfy_gen.py --only <name>`.

## Townsfolk (generated NPCs)
Each port's governor, banker, moneylender, barkeep, shipwright, merchant and curio dealer is assembled from trait
layers the first time you meet them, then stored in the save (`G.npcs["<port>|<role>"]`, see `scr_npc`).
- Trait tables, colours, names and per-role clothing rules: `datafiles/data/npc_parts.json`.
- Layer art: `sprites/npc_<layer>_<variant>.png`, all 320×400 on one shared frame. Draw a new variant in
  `tools/artgen/npcparts.py`, run it, paint it with `comfy_gen.py --only npc_<layer>_<variant>` (spec entry in
  `art_spec.json`), copy the result into `sprites/`, and add the variant name to `npc_parts.json`.
- Hair, clothes and some hats are drawn in light grey and tinted in game; heads are painted per skin tone.
- Preview random combinations: `python3 -I tools/artgen/npc_preview.py out.png [parts_dir]`.
- A new role: add it under `roles` in `npc_parts.json`; campaign `say` steps and building headers with that npc id
  then show the local person.
