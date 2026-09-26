# Ads and portal integration (v1.4e)

All ad and portal code is in the `AD` object in `index.html` (search `ADS + PLATFORM wrapper`). The old name `CG` is an alias.
The provider is picked per build with `window.PLATFORM`:

| PLATFORM | Provider | SDK tag |
|---|---|---|
| `crazygames` | CrazyGames HTML5 SDK v3 | `https://sdk.crazygames.com/crazygames-sdk-v3.js` |
| `playgama` | Playgama Bridge v2 | `https://bridge.playgama.com/v2/stable/playgama-bridge.js` + `playgama-bridge-config.json` next to index.html |
| `web` | none (offline, no SDK) | none |
| `auto` (repo / GitHub Pages) | CrazyGames if its SDK reports `crazygames`/`local`, then Playgama if `window.bridge` exists, else none | CrazyGames tag |

The tags sit between `<!--PLATFORM:BEGIN-->` and `<!--PLATFORM:END-->` in `index.html`; `tools/build_zips.py` swaps that block.

## Building the ZIPs
```
python3 tools/build_zips.py            # writes ../zips/rush-crazygames.zip, rush-playgama.zip, rush-web.zip
```
Each ZIP has `index.html` at the root + `audio/` + `CREDITS.md` (+ `playgama-bridge-config.json` for Playgama), about 4.4 MB.
Never commit the ZIPs to git.

## Ad spots
- **[AD SPOT A] Rewarded** `AD.rewarded(cb)`: top-bar "Extra draft" button `#bAd` (+33 men, 3 per real day) and the telegram offer `adOffer()`.
  The reward is granted only on CrazyGames `adFinished` / Playgama state `rewarded`. The web build shows a 2 s countdown and grants it.
- **[AD SPOT B] Interstitial** `AD.midgame(cb,{force,tag})`, shown when ▶ is pressed on the result card:
  - **every failed attack** → `force:true`: no game-side throttle. The card shows "An ad will play before you continue"; the button locks until the ad closes or fails.
  - victories: at most 1 per 180 s (game-side).
  - Portal caps still apply. CrazyGames enforces about 3 min between midgames on its side and answers `adCooldown`; the game then just continues.
    Playgama: `minimumDelayBetweenInterstitial: 0` and `initialInterstitialDelay: 0` in the config, plus `setMinimumDelayBetweenInterstitial(0)`; the host platform may still skip.
- **[AD SPOT C] Banner**: result card only. CrazyGames uses a 300x250 container `#adbanner` (outside the zoomed `#ui`, so it is really 300x250); Playgama uses `showBanner("bottom","result")` / `hideBanner()`.

While any full-screen ad is open: sound is muted (`muteForAd`) and the frame loop is paused (`AD.paused`); both resume on close, finish or error.
Watchdogs mean a broken ad never strands the player: if the ad hasn't opened within 7-9 s, or is still open after 150 s, the game continues.

## Portal lifecycle
- CrazyGames: `SDK.init()` (late init is still adopted), `loadingStart/Stop`, `gameplayStart` on the plan screen, `gameplayStop` on menu/result and before a midgame, `happytime` on victory, portal mute setting via `settings.muteAudio` + `addSettingsChangeListener`.
- Playgama: `bridge.initialize()` is awaited before the menu (9 s timeout, late init adopted), the save is read with `bridge.storage.get` and written with `bridge.storage.set` (debounced; flushed when the tab is hidden; never directly to localStorage unless Bridge storage fails), `platform.language` sets zh/en unless the player chose a language (`S.langPicked`), `sendMessage("game_ready")`, and `level_started` / `level_completed` / `level_failed`; host audio and pause events are honoured.

## Tested (headless Chromium, 2026-09-27)
- CrazyGames ZIP on localhost (SDK 3.8.0, environment `local`): fail → notice → ▶ → demo midgame (game paused) → next plan; rewarded → paused → +33; banner renders.
- Playgama ZIP on localhost (Bridge 2.2.0, mock platform): init, storage save/reload and the fail flow all work (the mock has no ads, so the game continues at once).
  `?platform_id=playgama` outside Playgama never finishes init, so the game falls back to no ads and stays playable.
- Web ZIP (file://): no SDK, no notice, rewarded countdown works, save persists.
