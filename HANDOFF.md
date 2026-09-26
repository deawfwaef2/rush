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
- v0.8b: ONE continuous battlefield (laneZ 0.06–0.96, continuous scaleZ/groundY, berm removed). Trench v2 (`drawTrench`, TR_D/TR_W, trenchOff(), traverseEnts() depth-sorted blocks, ladders each bay, flat fills). Men WAIT INSIDE trench (`m.intrench`, drawManInTrench clips at ground line), appear in place (no walking in/out), on whistle state "climb" (m.lift) up the ladder then "run". Slots fill near→far along the trench (slotZ/slotRank); more men → camera pulls back. Enemies stand inside their trench too (clipped) until melee.
- v0.8c: CINEMATIC 6.4s, 6 shots (drawMontWide dawn stand-to with star shell + breath, rows of helmets/bayonets scaled by sendN → face profile → pocket watch → whistle → boots on ladder → OVER THE TOP low angle, men pour over parapet, count scales with sendN, shell bursts). Real SFX cues: heartbeat, bolt, clock, whistle@3.25s, mud, crowd "charge"+bugle@4.8s. No synth ticks.
TODO next: plan camera should frame own trench better; unit types; enemy outposts; balance.

---
## Feedback round 7 (2026-09-26) → v0.9
- Victory FX TOO FLASHY → tone down (somber, historical).
- Battle process too crude → more immersion, historical environment (smoke, craters, wounded, MG nests, muzzle flashes...).
- MELEE: must last longer; attackers must NOT trickle in and die one by one → survivors gather at the enemy wire / dead ground, then assault together.
- Show "chapter-level" (e.g. II-3) + a chapter strip with symbols: level 3 of each chapter = chapter CG (special), fortress (special), new-mechanic unlock (special); symbols can stack.
- Chapter CG cinematic on level 3 of every chapter.
- Trench unrealistic ("just a line") → real trench system: zigzag bays/traverses, communication trenches, support line, saps.
- Map drawing has problems; game had BUGS; charge ended right after starting (bug: climbing men not counted → instant fail, fixed v0.9a).
- User prefers the ORIGINAL charge CG (v0.5 4-shot montage) over v0.8 wide shots.

## v0.9e (chapter CG)
- playChapterCG(ch,done)/drawChapterCG: 13.5s, 3 scenes per chapter (per-chapter kinds: march/trench/dig/flood/sentry/gas/masks/advance/tanks), typewriter captions CGTXT en/zh, letterbox, tap to skip. Triggered in toPlan when S.lvl%8===2 && !S.seenCG<ch>. body.cgon hides UI.
- Remaining TODO: battle immersion (smoke, craters, wounded, MG tracers), map glitch checks, balance.

---
## Feedback round 8 (2026-09-26) → v1.0
- Victory FX STILL too flashy/"失真" → minimal: no bursts, just quiet text + stats.
- Artillery support must NOT be unlocked from the start (unlock later, e.g. chapter I level 5).
- Veteran-adding mechanic has BUGS and its UI is bad → redesign.
- Level/chapter UI must NOT be on the right side → put it in the empty TOP area.
- NO EMOJI anywhere in the UI.
- NO tear-jerking BGM anymore (reverses round 6) → tense/martial/ambient instead.
- Trench v0.9 is UGLIER than before → redraw at master level.
- Melee has many TELEPORT bugs (men jump positions) → fix smooth movement.
- Chapter CG quality too low → improve; CG needs an explicit SKIP button (only the button skips, not tapping anywhere).
- Overall: wants master-level quality.

## v1.0a
- Victory: no banner/cheer/bugle/FX/count-up; flag raise only. BGM calm.mp3 = "Oppressive Gloom" (tense, not tearjerking).
- Artillery unlocks at lvl index 4 (I-5, tagged new); supports granted once on unlock (S.supU). Tutorial skips #supWrap step if none.
- Chapter strip moved to #topStrip (absolute, top centre between panels); removed from right panel.
- Emoji removed: SVI svg icons (cg/fort/new/warn); ▶ uses text variation selector.
- Veteran bug: holdBtnF auto-repeat never stopped because buildWaves destroyed the button → global HOLDS stop on window pointerup; vetRow built once (buildVetRow) w/ pips; waves clamped to available men.
- Chapter CG: only the SKIP button (#cgSkip) skips.

---
## Feedback round 9 (2026-09-26) → v1.1+  (same list as round 8 re-sent, plus NEW mechanics)
Still open from round 8: master-level trench art; melee teleport bugs; CG quality + CG slow/laggy (perf!); SKIP button only.
NEW wishes:
- Each LEVEL should feel different: terrain + classic scenery varies subtly per level (not just per chapter).
- Every NEW mechanic → popup explaining it when first met; enemy panel shows an icon/hint of what unlocks AFTER this level.
- Units too clumped → more depth spread (use the whole depth of the field).
- FORTRESS victory should be grander (normal victory stays quiet).
- FAILURE stats UI is bad → put elsewhere, clearer numbers.
- Men who reach the enemy wire must not wait too long (they were near-invulnerable while waiting).
- Performance must improve; CG slow/laggy.
- Skill/strategy: different operations with different outcomes; reward skilful play.
- MID-GAME unlock: GENERAL/OFFICER (strategic resource, 1 per charge). Player controls him with WASD; troops follow him. Terrain has safe zones (dead ground / shell craters) where you can halt, regroup, and re-order the charge. Officer can die → short cinematic, then troops continue on original order.
- MID-GAME unlock: SIGNAL FLARE: order waves to move to a buffer/safe zone and WAIT, then fire flare → all continue together.
- MID-GAME: barbed wire belts on the route; ENGINEERS unit type cuts wire (otherwise men stall at wire and die).

## v1.1a
- Melee teleports fixed: men get m.mx target, enemies en.tx; both walk smoothly (no x jumps). New enemies spawn behind and walk in.
- Gather at wire: max 3.5s (b.gatherT) then assault; gathered men take reduced rifle fire (not invulnerable).
- Depth spread: on leaving trench each man gets zt across field depth (x FORM.zw) and drifts there while running.

## v1.1b
- FORTRESS win grand: 14 coloured signal flares (white/green/red), fanfare+cheer, men cheer, banner "FORTRESS TAKEN", gold card (.fortwin), card after 6.2s. Normal wins unchanged (quiet).
- Failures: removed text from in-world markers & from reward panel; new #failBtn in enemy panel (count + closest result) → failsCard() table (date/sent/waves/fallen/pinned/enemy left/loss bar) + diagnosis tip.

## v1.1c
- NEWM(i): auto list of mechanics first appearing on level i (hazards, supports via supMaxAt, tools TOOL_AT={eng:10,flare:12,off:17}). lvlTags "new" uses it. showNewMechs() pops mechCard(k,isSup,isNew) with NEW ribbon for each unseen (S.seenM). Enemy panel #nextU lists what appears AFTER this level (clickable).
- MECH text + IC icons added for eng/flare/off (gameplay implemented in next stages).
- Remaining ★ glyphs replaced by VETI svg.

## v1.1d
- belts[] barbed-wire belts (count=cur.wr, at 0.52/0.66/0.40 SEGL) drawn by drawBelt (screw pickets, 3 strands, coils; gaps when cut). Men slow hard in uncut wire (0.18-0.34), 0.85 when cut.
- Engineers (unlock lvl 10): wave.e (<=8, from recruits), #engRow stepper. m.eng men stop at an uncut belt (state "cut"), cut progress dt/3.6 each; exposed to fire; white armband.

## v1.1e
- SIGNAL FLARE (lvl 12): wave.h hold order (#holdRow Go/Hold). Dead ground fold at deadX()=0.42 SEGL (drawn, labelled in plan; fire x0.25 there). Holding men stop there (state "hold", light rifle exposure). #tools HUD button FLARE (key F) → fireFlare(): red flare, all rise together; auto after 30s.
- SHOCK ASSAULT skill reward: if assault mass >=70% of those still coming and >= enemy garrison → b.shock, melee +30%.
- #tools also hosts OFFICER button (key O) → window.startOfficer (next stage).

## v1.1f OFFICER
- startOfficer() (O key / #tools button, lvl>=17, once per charge): officer spawns at rearmost runner; runners within 0.35 SEGL get m.fol and keep just behind him (speed modulated, z drifts toward him). WASD/arrows or on-screen #offpad move him. SPACE/H or HALT/GO toggles halt: followers go state "rally" (crouch around him, morale regen); GO → morale +25 if halted >2s, b.shock if regrouped ≥max(6,0.8·garrison). Takes fire (reduced when halted / dead ground). officerDown(): ragdoll, slowmo 0.25 + camera zoom + "THE OFFICER IS DOWN", others continue. Reaching the wire hands over. Camera follows him.
- #topStrip hidden outside plan/menu (was overlapping battle HUD).

## v1.1g CHAPTER CG v2 (quality + perf)
- drawChapterCG rewritten: per-scene baked layers (cgBake → sky/far/mid/fg offscreen canvases, cached by ch:kind:size) + live figures; parallax push-in camera per layer; painterly clouds, haze bands, ruined church/houses, poplars, dead trees, sandbag parapet, wire coils, revetment, crosses, tanks; weather (rain/snow/pollen), god rays, baked vignette. Scenes CGK per chapter (march/dig/line, rain/flood/stretcher, sentry/flare/ruins, gasfield/masks/crosses, tanks/advance/dawn).
- PERF: when chCG is active, frame() skips the whole world render (was drawing world + CG → lag).
- Only SKIP button skips (from v1.0a).

## v1.1h trench art pass
- trenchCols(): palette-aware trench colours (berm, burlap bags x4, lit/shadow strips, walls, floor, cut); winter = snow caps on top course.
- Parapet/parados now: earth berm polygon + lit crest + brick-bond sandbag courses (rounded bags w/ highlight + shadow), traverses same style; comm trenches/support line earthy with spoil lip instead of black strips/blobs.
- Men waiting in trench drawn in shadow (trenchShadeCache darkened cols). Global rim light 0.55→0.22 (men looked like pale blobs).

## v1.1i per-level set pieces
- SETP[i] per level (by level name): road, windmill, orchard, chapel/church, poplars, canal+lock, farm+crows, brewery+chimney, red house (red door), mud pools, duckboard path, crater field, railway embankment, dead wood, frozen pools, night grade + lanterns, pond, pines (snow caps), quarry cliff, gas bell post, mustard flowers, pillboxes, ghost village/town, sunken road, meadow, river, dry canal. drawSetFlat() after ground; pushSetEnts() tall objects depth-sorted (anchored at EA=bx+0.42·L so visible in plan view); setNightGrade(); ridges seeded per level.
- smoke: lvl3/200 win, lvl13/300 loss (wire+engineers level, expected hard without engineers), no errors.

## v1.1j skill reward
- Tactical merits on win (b.merits): Massed assault (b.shock), Flare timing, Officer's lead (used & survived), Low losses (<35%), Nobody broke (0 pinned). Each merit +5% survivors promoted to veterans; shown as a row in the report.
- NEXT ideas: bench perf in real browser; more unit types; polish drawMan (figures still cartoonish).

---
## Feedback round 10 (2026-09-26) → v1.2
(round 8/9 list re-sent; plus NEW:)
- MORE UNIT TYPES.
- BOOST POINTS: earn points; a boost screen lets you buy the NEXT charge's loadout (unit types, strategic resources).
- GOAL = finish the game as FAST as possible: stopwatch; show time after every level and every chapter.
- Victory effect: not flashy but NOT too plain either. Still many teleport ("瞬移") bugs.
- MORE early strategic resources, e.g. "cover": during the charge when a shot is about to hit, player clicks a unit (highlight box) to make it immune to that shot. More interactivity.
- MORE ENEMY TYPES with strategy.
- Every level should feel different. Some chapters: levels 1-4 = sub-area 1, level 5 = fade to black, big scene change.
- BUG: with more men, the trench sides get closer (camera zoom-out compresses). More men should mean MORE DEPTH, not zoom-out.
- Lag with many men; near-ground foreground unsatisfying.
(round 8/9 list re-sent; most done in v1.0–v1.1j) NEW:
- More UNIT TYPES. REINFORCEMENT POINTS (增援点) + boost SHOP: spend points to buy next charge's loadout (unit types, strategic resources).
- Goal = finish the game as fast as possible: STOPWATCH; show level time after each clear and chapter time.
- Normal victory must not be too plain either (modest but not bare). Still many teleport ("瞬移") bugs.
- More EARLY strategic resources, e.g. "take cover": when a shot is about to hit, click the marked unit (box) to make it immune to that shot → playability.
- More ENEMY types, more strategy. Each battlefield should feel different.
- Chapter structure: sub-stages 1-4, then level 5 → blackout + big scene change (unique to some chapters).
- BUG: with more men, the trench sides (own/enemy) come closer on screen (camera zoom-out shrinks field) → fix. Depth must grow with more men.
- Lag with many men; foreground/near view unsatisfying.
## v1.2a
- STOPWATCH: S.clock (run time) + S.lvlT[lvl] accumulate only in plan/charge/melee/barrage (not menu/result/CG). #cClock chip in top bar. Win card .timeRow: level time (+ "new best" via S.best), chapter time on chapter end, run time. fmtT(), chapT(ch).
- Normal win: modest but not bare — 1/3 of survivors raise rifles, soft cheer + bugle, "LINE TAKEN · name · time" caption. Fortress win stays grand.
- Plan camera no longer zooms out with more men (trenches used to come closer); instead tilt rises (cam.tt 0.25→0.6) to show more depth. Running depth spread grows with men sent (0.5+sent/140, max 0.94).
## v1.2b TAKE COVER
- From lvl idx 1: battle.cover = 3 (+S.buy.cov). Some rifle hits become telegraphed aimed shots (m.aim 1.25s, max 3 at once, 70% when charges left): gold→red corner-bracket box + timer bar (drawAimMarks). Click/tap the box (tryCover, canvas pointerdown in charge/melee) → man dives (stumble .7) + immune 1.2s, charge used. Unclicked → killed. First time: slowmo + toast. Counter shown in #tools (.covc). Merit "Quick reflexes" if ≥2 used.
- Men drift to their depth lane faster (dt*0.16) to reduce clumping.
## v1.2c SUPPLY DEPOT + unit types
- Reinforcement points S.rp (new save 2): win +2 (+3 fortress) +1 per tactical merit; loss +1. #depotB button in left plan panel → openDepot() card: SHOP items (unlock by lvl): rum (+15 morale), extra cover, Bombers x4 (melee weight 1.7, 55% clear a defender on entering trench), stretcher bearers (50% of pinned return to reserve), Lewis gun team x2 (enemy fire −12% each alive), extra shell, sapper pair (+2 eng), smoke. Max 3 each, refundable before charge. S.buy consumed by applyLoadout() at startCharge (b.loadout). Unit types via m.type ("bomb"/"lewis"), small kit marks drawUnitMarks(). Report shows RP earned + stretcher recoveries.

---
## Feedback round 11 (2026-09-26) → v1.3  (user's words, summarised; keep for future agents)
ECONOMY
- Daily reinforcement must be MUCH bigger: daily = (old daily number) x3; at game start the daily reward is 100 men.
- Rewarded ad = 1/3 of the daily reward (not a whole day).
- PERFECTION RATING per captured stronghold (1-5 stars): the SMALLER the share of men rotated to the rear (surplus survivors) out of the total sent, the HIGHER the rating. Reward only scales the level's BASE reward: 5*=300%, 4*=150%, 3*=100%, 2*=75%, 1*=50%.
- After tutorial level 1 is cleared, TEACH this (popup/tutorial card) to encourage skilful, efficient sending.
FIELD / VISUALS
- Units still clump at start (a blob in the middle) -> spread them.
- Both sides' lines feel too SHORT -> make the base length 1.5x longer.
- Near-ground and far-ground zones are EMPTY -> fill them (visual richness).
- Environment/scene too crude ("too simple, not pretty"). Check visuals yourself: mysterious HORIZONTAL STRIPES/bands on screen -> find & fix.
- Battle animation crude; VICTORY FEEDBACK insufficient (make it more rewarding).
- Mid-game: longer levels, more complex environment, enemy may have MULTIPLE trench lines, varied scenes.
CHARGE RANDOM EVENTS (strongly requested)
- Many random events during each charge so every charge feels different (not the same "movie" each time).
- Each event gives a small buff/debuff shift to the charge.
- Small & lively: a man trips and falls, a man drops into a shell hole and fires a few shots, etc. Rare LARGE events: mass rout, stall/hesitation, etc.
- Probability modified by morale; give a "dice roll" feel.
- Must be INTEGRATED/natural, not obviously scripted; must not lag or be awkward.
COMBAT / PERF
- Machine guns: the DENSER the formation, the MORE deaths.
- Still very laggy with many men -> keep optimizing performance (top priority, again).
