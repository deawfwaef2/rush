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
Stage B done: dual-depth — laneZ() splits men into MID zone (z .05–.47, small) and NEAR zone (z .58–.98, big); drawBerm() at z≈.5 (posts, wire, stumps, sandbags, wheel); lit ridge gradients, birds.
Stage C done: per-soldier variety m.v (height, build, tone, stride, lean, pack, soft cap 10%, rifle hold, bandage, gait speed), stumbles w/ shouts, cheer pose, 3 death styles; MONTAGE = 4 shots (face profile+breath / pocket watch ticking to zero / officer whistle / boots+puttees on ladder) w/ push-in, hard-cut flash, captions.
TODO: multi-lane routes (ch3+), better enemy trench/insets, chapter scenery transitions, balance pass, more chatter.

---
## Feedback round 4 (2026-09-26) → v0.6
User: edge-of-screen mouse pans camera; terrain still crude; REMOVE advisor; UI too small; units must not pop/float in; trenches too simple; victory FX must be bigger/more satisfying; master-level UI; SFX + BGM (online music ok); artillery/sniper animations play only AFTER pressing CHARGE; supports selectable in quantity (multiple).
Done (v0.6a–e): no advisor; edge/arrow/drag pan (menu+plan); supports queued with −/+ and executed after CHARGE (bombardment phase with per-shot result); UI zoom (UIZ); men walk in from off-screen; music audio/calm.mp3 + audio/charge.mp3 (Kevin MacLeod CC-BY, see CREDITS.md — keep credit!); detailed trenches; v0.6e: far patchwork fields, painterly ground mottling, ruts, drifting ground fog, VICTORY FX (signal flares, gold burst+rays, tossed helmets, falling paper, jumping men, ribbon+medal banner, count-up stat tiles).
AGENT NOTES: `.git/config` is not persisted → after a workspace reset run `git remote add origin https://<user>:<token>@github.com/deawfwaef2/rush.git` and `git fetch`; ALWAYS check `git log origin/main` before pushing — remote may be ahead of the local workspace (a stopped session can still have pushed). Also set git user.name/email again. Playwright may need `python3 -m playwright install-deps chromium`.

---
## Feedback round 5 (2026-09-26) → v0.7  (verbatim-ish summary of user wishes; keep for future agents)
PERF IS TOP PRIORITY ("好卡" said 3x). Never regress perf: soldiers are drawn via sprite cache (`SPR`, drawMan→drawImage). New art for soldiers must go through drawMan0 so it gets cached. Test with 600+ men.
Gameplay wishes:
- WAVE FRAMES (冲击波帧) from LEVEL 1: player defines waves (frames); each wave = count, unit type (recruit / veteran; later elite, flamethrower, engineer), spacing (loose/normal/dense), delay. Dense → warning. Simple UI. Order matters (elites later, flamers after, engineers for wire). Too loose = lose melee; too dense = MG/shell slaughter. Real WW1 feel, no unrealistic blobs.
- Recruits & veterans are SEPARATE counts/choices. Veterans die less.
- Hit chance rises the closer to the enemy line.
- Per-soldier MORALE: low morale men go prone and stop ("pinned") = counted as LOSS.
- Melee: more exciting; numerical superiority gives ratio bonus; wave density matters; melee suppresses enemy fire.
- Trenches have DEPTH (several lines, not one line); later levels more lines, enemy outpost houses in front, a buffer zone where our side fires first (free damage).
- Victory stats clear: sent / killed / pinned / survived / held garrison / sent to rear, + a remark rating troop efficiency (overkill / efficient / pyrrhic).
- Failed attacks: the enemy position shows a record of every failed wave config per attempt.
- Charge animation differs by troop count; reinforcement arrival cinematic scaled by count.
- Soldier fill order: near → far. Far battle zone appears only when crowd is large (camera pulls out, new far zone). Same for enemy.
- Flag: master-level design, green + emblem.
- Out of troops → popup ad offer (in-world "telegram"). Ads: up to 3 per day, each = +1 day of troops.
- Better ambience: battlefield soundscape (distant artillery, MG echoes, shouts, whistles, wind, rain).
- Weather changes per chapter. Artillery shells animated (arc, flash, dirt). Longer levels.
- Historical realism over simplification.

### v0.7 done (2026-09-26)
- v0.7a PERF: `SPR` sprite cache in drawMan (poses cached per colour/state/phase bucket/scale bucket; drawManRaw = uncached). DPR≤1.5, corpses ≤600.
- v0.7b WAVES: `waves=[{r,v,f,d}]`, `wSel`, UI tabs W1..Wn (+ add, × remove, MAXW grows with level), recruits stepper/slider/presets act on selected wave, ★veterans stepper, formation Loose/Line/Dense (`FORM` fire & melee factors), delay after previous wave, warnings. `syncMen()/pushList` keeps visible men == waves; slotZ fills NEAR zone first then FAR.
- v0.7c COMBAT: hitK() = proximity^1.6 × formation × vet 0.62. Per-man morale `m.mor`, shockNear() on each death, <22 → pinMan() (prone, lost). Continuous melee: arrivals joinMelee(); meleeTick() Lanchester (sqrt ratio), vets 1.55, formation cohesion; `b.supp` suppresses enemy fire; `b.front` moves melee through trench depth. reportHTML() table + remark; S.fails[lvl] ledger shown in enemy panel + wooden markers at wire.
- v0.7d ads 3/day (adLeft(), real calendar date), adOffer() telegram when reserve < garrison. drawFlag() green regimental colour (cached FLAGC).
- v0.7e shell() animated arcs (barrage + enemy shelling, kills on impact), AU soundscape loop + rain bed, weather per chapter (stepWeather/drawWeather), trenchLines(i) extra trench lines (own behind, enemy deeper).
- v0.7f segLen longer, camera pulls out with crowd size, charge caption by count (section/platoon/company/battalion), covering fire from lvl 5 (buffer zone), reinfCinema() on payday.
TODO next: unit types (elite/flamethrower/engineer cuts wire) in waves, enemy outpost houses, far-zone terrain appearing only for big crowds, richer melee close-up inset, balance pass (lvl 5+ is hard).

---
## Feedback round 6 (2026-09-26) → v0.8
- SFX: user HATES procedural synth sounds ("低级"). Use REAL recorded sounds from the web (CC0 / public domain / CC-BY with credit in CREDITS.md). Keep total audio small (few MB). Immersion first.
- BGM: "好TM催泪" (very tear-jerking) — keep the melancholic music, do not remove it.
- NO men walking on/off screen when changing counts. There is ONE front line only; more men = camera pulls back so the line LOOKS longer. Do not split into separate near/far zones.
- Trench design was bad; men must WAIT INSIDE the trench (below parapet, helmets showing), then climb ladders over the top on the whistle.
- Charge cinematic (montage/CG) too crude → make it much richer.
- v0.8a: REAL SFX. `audio/sfx.js` = base64 CC0 recordings (works on file://, ~3.4MB). `SFX` object (init/play/loop/updLoops); AU.shot/mg/boom/whistle/bugle/cheer/clang/thud/incoming routed to recordings, synth only fallback. Ambience loops: amb_big, booms_far, wind, rain(ch1), rifle_far, amb_civil(battle). Raw files NOT in repo; to add a sound: download CC0 preview, trim with ffmpeg (pip imageio-ffmpeg), regenerate sfx.js, credit in CREDITS.md.
