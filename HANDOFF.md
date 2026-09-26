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
