# Ad integration points (CrazyGames SDK v3)
All ad code lives in the `CG` object in `index.html` (search "AD SPOT").
- SDK script tag: `<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js">` in <head>/body bottom.
- **AD SPOT A – Rewarded** `CG.rewarded()` : top-bar film icon button `#bAd`. Up to 3 times per real calendar day (S.adDate/S.adN, adLeft()), each gives one day of reinforcements instantly. Also offered by the in-world TELEGRAM popup adOffer() when reserve < garrison on the plan screen.
- **AD SPOT B – Midgame** `CG.midgame()` : after pressing ▶ on battle result card (win or fail). Throttled to 1 per 3 min.
- **AD SPOT C – Banner 300x250** `CG.banner()` : div `#adbanner`, bottom-right, shown only while result card is open.
- Gameplay events: `gameplayStart` on plan screen, `gameplayStop` on menu/result, `happytime` on victory, `loadingStop` at boot.
- Offline / no SDK: rewarded shows a 2s fake countdown and grants reward; midgame & banner skipped.
To use another ad network: replace the bodies of CG.rewarded / CG.midgame / CG.banner only.
