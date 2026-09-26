# HANDOFF — RUSH (read before coding; APPEND, never overwrite)

## User constraints (MUST follow)
1. Save to GitHub OFTEN (stage by stage). Repo: github.com/deawfwaef2/rush (token given by user in chat; do not commit it).
2. Always keep a playable build: `index.html` in root, double-click to play (no build step, no server needed).
3. Package/ship HTML FIRST, polish later. Every commit must be playable.
4. Workspace < 128MB. No huge assets. Prefer procedural graphics/audio.
5. Never overwrite this HANDOFF; append a new dated section at the bottom.
6. Check this file before each coding session.

## Design brief (user's idea)
- Name: RUSH. WW1 art style. Side-view (大侧面), deep scene, far visibility, big near figures, camera rises on charge. Cinematic close-up montage cuts OK. Must NOT look like a copy of Flash "Warfare 1917".
- Soldiers: multi-color solid silhouettes with slight gradient; normal proportions; 2D ragdoll on death. Backgrounds detailed.
- Minimal text, icon-first UI, no "AI feel". English default, Chinese in settings.
- CrazyGames style, mobile landscape.
- Daily troops: login income + countdown timer to next wave. 1x/day rewarded ad = instant next day's troops.
- Left = own trench, right = enemy intel: hazard types/counts, reward (daily troop upgrade).
- Hazards: mines (death zones), MG fire (per-second random kills), rifle fire, garrison N (need N survivors to win) ... more.
- Stepwise resolution at nodes: split-screen enemy attack effect, own side loses men.
- Choose how many to send (+ / ++ buttons); see soldiers pushed onto field one by one with sound.
- Central CHARGE! button → bugle, charge animation, MG fire, deaths, results. Fail if all die. Win → history story text.
- Survivors become veterans (different uniform) — stronger in melee (probabilistic melee).
- Advisor: flavor text estimate of odds (no numbers).
- Strategic supports refresh daily: artillery (stackable, more uses = better reduction), sniper (split-screen counter-sniper), more.
- No level select/skip. Fortress nodes: warn high difficulty, suggest waiting days.
- 8 levels per chapter; mechanics & scenery & color grading change each chapter. Later: multiple lanes w/ different terrain, split troops; tanks etc.
- After win, leftover troops are sent to rear (consumed) → management challenge.
- One continuous world (no scene cuts): main menu = current front line; camp moves forward after each win. Scroll left to see captured strongholds with day + casualties.
- Ads: only "skip 1 day" rewarded + classic static/midgame ad. CrazyGames SDK v3. Document ad spots.
- Speedrun: track total time.
- Unit chatter for immersion.

## Tech
- Single file `index.html` (vanilla JS canvas). Audio: WebAudio procedural (bugle, gunfire, BGM drone). Save in localStorage.
- Ad integration points: see `ADS.md`.

---
## Session log 2026-09-26 (v0.1–0.2)
- Built single-file `index.html`: menu (current front, drag/edge-scroll left to see captured flags with day ☼ + fallen ✝), plan (SEND −−/−/+/++/0/MAX, soldiers run into trench one by one), enemy intel panel w/ bars, supports (Artillery stackable, Sniper split-screen counter, Smoke, Tank), advisor words via Monte-Carlo, CHARGE montage (whistle close-up → bugle → wide, camera rises), node split-screen insets, mines/MG/rifles/shelling/wire/gas, melee rounds (vets 62% vs 42%), win card w/ story, 40 levels / 5 chapters w/ palettes, EN/ZH, procedural audio, CrazyGames SDK (ADS.md).
- Win rule: survivors → some stay to hold trench (25% of garrison), rest return as veterans. Unsent reserve kept.
- Test: `?debug` in URL → settings has +1 day / +1 lvl buttons. Headless test script used playwright.
- TODO next: multi-lane routes (ch3+), better soldier art, more chatter, real BGM option, balance pass, end-of-chapter scenery transition.

---
## Feedback round 2 (2026-09-26) → v0.4
User said: figures & scenes too crude; icons unclear → ALWAYS show text name + one-line mechanic next to icons; default ENGLISH always; split-screen must NOT pause/slow the game; after a win go straight to the next level (no main menu); write info as text; title = "CHARGE" (EN) / "冲锋" (ZH).
Done: new tapered-limb soldiers w/ rim light, puttees, pack, vet red scarf; scene: clouds, god rays, town/church skyline, windmills, smoke columns, treeline, telegraph poles, craters/puddles/debris/grass; trench planks. Save key now `charge_save_v2`.
Note for agents: read_file may not see freshly written screenshots — copy them to a new filename in ~/shots first.

---
## Feedback round 3 (2026-09-26) → v0.5 (stage A: systems/UI)
User: background ugly; needs TUTORIAL; icons ugly/small; +/- crude; levels longer; DEV MODE in settings (+1 day); "dual depth / 4-band" composition (sky / far / mid battle zone / near battle zone); UI not good; enemy defense & support trigger mechanics must be detailed; start with 100 men; men sent are CONSUMED (teach player to estimate); MORALE system (win up, decays toward middle, affects stats, 0 = refuse); detailed daily reinforcement UI; montage & soldier animation too crude/same-looking.
Stage A done: START 100; segLen grows per level (+38/level, fortress +500), hazard rates scaled by 1500/seg; all sent men consumed, 1 in 4 survivors return as veterans; morale (S.morale, drift to 50 half-life 6h, win +18/fort +30, loss −20, mf=0.75..1.25 affects speed/fire losses/melee, ±10% income at >=70/<30, <=2 refuse); new UI (brass/canvas panels, badges, stepper w/ hold-repeat, slider, ×garrison presets); tap hazard/support "i" → MECH detail card; tap reserve/timer chip → reinforcement card; morale chip → morale card; 9-step spotlight tutorial (S.tut); Settings → Developer mode → DEV +1d button in top bar + tools. Save key charge_save_v3.
