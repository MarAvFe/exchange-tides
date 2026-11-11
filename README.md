# Exchange Tides

A pirate-era trading game made in **GameMaker**. Its mechanics were reverse-engineered from *Tradewinds 2*
(Sandlot Games, 2005); every character, name, line of dialogue and piece of art is original.

- **Campaign**: *The Grimmer Debt*, a seven-chapter story against Commodore Silas Grimmer.
- **Free Trade**: reach a net worth of 1,000,000 within 3 years.
- 6 playable captains with perks, 12 ports with named governors, 11 goods, 7 player ships, 10 enemy types.
- Every port's townsfolk (banker, barkeep, moneylender...) are unique people composed from painted trait layers, rolled once per game.
- Voyages take a week along sea routes around the coasts. Own a fleet of up to 5 ships.
- Governors offer contracts every month: deliveries, dispatches, bounties and pirate hunts.
- Real-time fleet battles: every cannon reloads on its own; load special shot into the next gun.
- 5 save slots plus an autosave. Music by Kevin MacLeod (CC BY 4.0).

## Play / build
- **GameMaker IDE** (free at https://gamemaker.io): open `game/ExchangeTides/ExchangeTides.yyp` and press Run.
- **Command line** (no IDE needed; gm-cli uses a guest licence). Needs Node.js (e.g. via fnm).

### Windows (PowerShell)
The project lives in WSL; GameMaker builds faster and more reliably from a Windows folder, so copy it first
(`/MIR` keeps the copy in sync; `/XD .gmcache` skips the build cache):
```powershell
robocopy "\\wsl.localhost\Ubuntu\home\mavila\exchange-tides\game\ExchangeTides" "C:\Games\ExchangeTides" /MIR /XD .gmcache
cd C:\Games\ExchangeTides
npx.cmd --yes @gamemaker/gm-cli@latest run .\ExchangeTides.yyp --target=windows --runtime=vm
```
- Use `npx.cmd` (not `npx`): PowerShell's default execution policy blocks `npx.ps1`. Alternatively run
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.
- `npx.cmd is not recognized` (e.g. after a reboot): Node comes from fnm, which only puts it on PATH in shells that
  ran `fnm env`. For the current window:
  ```powershell
  fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
  fnm use default
  ```
  To make it permanent, add the first line to your PowerShell profile:
  ```powershell
  if (!(Test-Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
  Add-Content $PROFILE 'fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression'
  ```
  The profile only loads if scripts are allowed (`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`).
- Re-run the `robocopy` line after every update to the project, then the `npx.cmd` line to play.
- Saves, settings and logs go to `%LOCALAPPDATA%\ExchangeTides\`.

### Linux / WSL (headless self-test)
`tools/selftest.sh` builds for Linux and runs a scripted bot under Xvfb (see the script header for the libraries it
needs). Screenshots land in `~/.config/ExchangeTides/shot_*.png`.

Controls: mouse. In battle, keys `1`-`3` load special shot and clicking an enemy targets it. `Enter` closes dialogs, `Esc` goes back.

## Layout
| Path | What |
|---|---|
| `game/ExchangeTides/` | GameMaker project (GML in `scripts/`, controller `objects/obj_game`) |
| `game/ExchangeTides/datafiles/data/*.json` | all game content: goods, ports, ships, items, captains, campaign, config |
| `game/ExchangeTides/datafiles/sprites/*.png` | generated illustrated art, loaded at runtime |
| `docs/MECHANICS.md` | the extracted Tradewinds 2 mechanics (pricing, contraband, finance, sailing, combat, tasks, save format) |
| `docs/EXTENDING.md` | how to add captains, NPCs, items, behaviours, chapters |
| `tools/artgen/` | `gen.py`: a dependency-free vector rasteriser that draws the base sprites. `comfy_gen.py` + `art_spec.json`: repaint them with a local ComfyUI server (style rules: `docs/ART_STYLE.md`) |
| `game/ExchangeTides/datafiles/fonts/` | Alegreya (body) and Pirata One (headings), both under the SIL Open Font License |
| `tools/gen_project.py` | regenerates the `.yyp`/`.yy` manifest from the folder layout (scripts, objects, sounds, datafiles) |
| `tools/artgen/worldmap.py` | draws the coastline map, places the ports and precomputes water-only sea routes (`data/routes.json`) |
| `game/ExchangeTides/sounds/` + `tools/music.py` | music tracks (Ogg) and the script that fetches and levels them |
| `tools/tw2pak.py`, `tools/xml2json.py`, `tools/fn.sh`, `tools/peconst.py`, `tools/ghidra_scripts/` | reverse-engineering tools |
| `re/` | Ghidra decompile of `tw2_vista.exe` (`decomp.c`) and its string cross-reference table |
| `extracted/` | unpacked original assets (reference only; not used by the game, not for redistribution) |

## Code map (GML)
`scr_data` (loading, sprite registry) · `scr_effects` (modifier grammar) · `scr_economy` (prices, contraband,
finance, tips) · `scr_world` (state, voyages, saving) · `scr_campaign` (task engine) · `scr_combat` (battles) ·
`scr_behaviors` (enemy AI registry) · `scr_ui` (immediate-mode widgets) · `scr_screens` (every screen) ·
`scr_port` (harbour scene) · `scr_fleet` (multi-ship fleet) · `scr_contracts` (governor jobs) · `scr_fx` (battle
particles) · `scr_audio` (music).

## Credits
Music by Kevin MacLeod (incompetech.com), licensed under Creative Commons: By Attribution 4.0
(https://creativecommons.org/licenses/by/4.0/): "Teller of the Tales", "Thatched Villagers", "Folk Round",
"Master of the Feast", "Achaidh Cheide", "Five Armies", "Clash Defiant", "Lord of the Land".
Changes: volume levelled and converted to Ogg Vorbis. Fonts: Alegreya and Pirata One (SIL OFL).
