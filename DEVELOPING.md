# Developing Exchange Tides

Building, testing and packaging the game, plus a map of the repository.
For adding content (captains, items, ports, chapters, translations), see [docs/EXTENDING.md](docs/EXTENDING.md).

## Run from source
- **GameMaker IDE** (free at https://gamemaker.io): open `game/ExchangeTides/ExchangeTides.yyp` and press Run.
- **Command line** (no IDE needed; gm-cli uses a guest licence). Needs Node.js (e.g. via fnm):
  `npx @gamemaker/gm-cli@latest run game/ExchangeTides/ExchangeTides.yyp --target=windows --runtime=vm`

### Windows (PowerShell)
If the project lives in WSL, copy it to a Windows folder first: GameMaker builds faster and more reliably there
(`/MIR` keeps the copy in sync; `/XD .gmcache` skips the build cache):
```powershell
robocopy "\\wsl.localhost\Ubuntu\home\<you>\exchange-tides\game\ExchangeTides" "C:\Games\ExchangeTides" /MIR /XD .gmcache
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
- Saves, settings and logs go to `%LOCALAPPDATA%\ExchangeTides\` (Linux: `~/.config/ExchangeTides/`).

## Self-test (Linux / WSL, headless)
`tools/selftest.sh` regenerates the project manifest, builds for Linux and runs a scripted bot under Xvfb that
plays through every screen and system and checks the results (see the script header for the libraries it needs).
Screenshots land in `~/.config/ExchangeTides/shot_*.png`; `tools/readme_shots.sh` copies the README screenshots
into `docs/screenshots/`. `python3 tools/i18n_check.py es` lists texts missing from the Spanish table.

## Release packages
- **Linux (.deb):** `gm-cli package --target=linux --runtime=vm -o ExchangeTides-linux.zip` (needs `zip`), then
  `tools/make_deb.sh ExchangeTides-linux.zip 1.0.0 exchange-tides_1.0.0_amd64.deb LIBROOT`. The .deb bundles the
  OpenSSL 1.0 libraries the GameMaker runner needs and depends on `libglu1-mesa libopenal1 libpulse0`.
- **Windows (installer):** in the GameMaker IDE, signed in with your free account: Target Manager → Windows / VM /
  Default, then **Build → Create Executable**. (gm-cli's guest licence cannot package Windows builds; a signed-in
  `gm-cli login <access-key>` can.)
- Upload with `gh release create vX.Y <files>`.

## Repository layout
| Path | What |
|---|---|
| `game/ExchangeTides/` | GameMaker project (GML in `scripts/`, controller `objects/obj_game`) |
| `game/ExchangeTides/datafiles/data/*.json` | all game content: goods, ports, ships, items, captains, campaign, config |
| `game/ExchangeTides/datafiles/data/lang/es.json` | Spanish text table (English text -> Spanish) |
| `game/ExchangeTides/datafiles/sprites/*.png` | illustrated art, loaded at runtime |
| `game/ExchangeTides/datafiles/fonts/` | Alegreya (body) and Pirata One (headings), both under the SIL Open Font License |
| `game/ExchangeTides/sounds/` + `tools/music.py` | music tracks (Ogg) and the script that fetches and levels them |
| `docs/MECHANICS.md` | the game mechanics extracted from Tradewinds 2 (pricing, contraband, finance, sailing, combat, tasks) |
| `docs/EXTENDING.md` | how to add captains, NPCs, items, behaviours, chapters, translations |
| `docs/NEXT_STEPS.md` | ideas planned for later versions |
| `tools/gen_project.py` | regenerates the `.yyp`/`.yy` manifest from the folder layout (scripts, objects, sounds, datafiles) |
| `tools/selftest.sh`, `tools/make_deb.sh`, `tools/i18n_check.py` | self-test, Linux packaging, translation check |
| `tools/artgen/` | `gen.py`: a dependency-free vector rasteriser for base sprites; `comfy_gen.py` + `art_spec.json`: repaint them with a local ComfyUI server (style rules: `docs/ART_STYLE.md`); `worldmap.py`: coastline map and sea routes |
| `tools/tw2pak.py`, `tools/xml2json.py`, `tools/fn.sh`, `tools/peconst.py`, `tools/ghidra_scripts/` | reverse-engineering tools |
| `re/`, `extracted/` | (local only, not in the repository) the decompile and original assets used for reference |

## Code map (GML)
`scr_data` (loading, sprite registry) · `scr_effects` (modifier grammar) · `scr_economy` (prices, contraband,
finance, tips) · `scr_world` (state, voyages, saving) · `scr_campaign` (task engine) · `scr_combat` (battles) ·
`scr_behaviors` (enemy AI registry) · `scr_ui` (immediate-mode widgets) · `scr_screens` (every screen) ·
`scr_i18n` (translation: `tr`, `trf`, `trn`) · `scr_theme` (visual styles) · `scr_port` (harbour scene) ·
`scr_fleet` (multi-ship fleet) · `scr_contracts` (governor jobs) · `scr_fx` (battle particles) · `scr_audio` (music) ·
`scr_selftest` (the automated bot).
