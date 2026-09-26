# CrazyGames 提交资料 / Submission kit (v1.4f, 2026-09-27)

Upload the file **`rush-crazygames.zip`**. Build it with `python3 tools/build_zips.py`; it is also attached to the GitHub Release.
The form is in English, so paste the English blocks as they are. The Chinese lines are notes only.

---

## 1. Game name 游戏名称
**Recommended / 推荐： `Charge! Over the Top`**

- 说明：只写 "Charge!" 太通用。CrazyGames 的原创性指南明确不鼓励通用名字（例如 "Chess" 不行，"Super Chess" 可以）。
  "Over the Top" 是一战俗语，指爬出战壕冲锋，正好对应游戏内容。
- 备选 / Alternatives: `Charge! 1914-1918` · `Trench Charge 1914`
- 游戏内标题现在是 CHARGE / 1914。定名后可以把游戏内 logo 改成一致。

## 2. Short description 一句话简介 (for listings / SEO)
```
Command a WWI battalion: decide how many men go over the top, time your artillery, and win the bayonet fight in the enemy trench.
```

## 3. Description 游戏介绍 (About the game)
```
Charge! Over the Top is a World War I trench-assault strategy game. You command a battalion on the Western Front, from the long summer of 1914 to the last morning of 1918. Every battle asks the same hard question: how many men do you send over the top? Send too few and the attack breaks on the wire. Send too many and you waste lives the front cannot spare. Plan each wave, choose a formation, call in artillery and smoke, then blow the whistle.

Once the charge begins, you react as it unfolds. Make a soldier dive when a sniper takes aim, fire a flare to launch the men waiting in dead ground, and send your officer forward to rally survivors in shell craters. Reach the enemy trench with enough men to win the bayonet fight, then hold it against the counter-attack. Across 40 levels and five chapters, from the Flanders lowlands to the Hindenburg Line, you face machine guns, mines, barbed wire, gas, snipers, flamethrowers and fortress lines. Reinforcements arrive every day, veterans survive to fight again, and efficient victories earn up to five stars.
```

## 4. Features 特色
```
- 40 levels in 5 chapters (1914-1918), each with a short line from a soldier's diary
- Plan every wave: recruits and veterans, loose / line / dense formations, engineers to cut the wire
- Fire support: artillery barrages, snipers, smoke screens and tanks
- React during the charge: take cover from snipers, signal flares, and an officer you control directly
- Enemy threats: machine guns, rifles, mines, artillery, barbed wire, flamethrowers and counter-attacks
- Bayonet fights in the trench, one duel at a time
- Star rating for efficient attacks, morale, and daily reinforcements
- English and Simplified Chinese
```

## 5. Controls 操作
```
Mouse / touch:
- Planning screen: set the number of men, the formation and the fire support, then press CHARGE!
- During the charge: click the box on an aimed soldier to make him take cover
- FLARE button: send the soldiers waiting in dead ground forward together
- OFFICER button (or O key): send your officer forward

Keyboard:
- W A S D: move the officer (or drag on touch screens)
- SPACE: officer halts and rallies the men / charges again
- A / D or Left / Right arrows: look along the front (resting the mouse at the screen edge also works)
```
- 说明：WASD 按的是物理键位（e.code），法语 AZERTY 键盘自动变成 ZQSD。游戏没用 Esc 或 Ctrl+W，符合 CrazyGames 的受限按键要求。

## 6. Category and tags 分类 / 标签
- **Category 主分类: `Strategy`**
- **Tags 标签（都是 CrazyGames 上已有的标签，已逐个验证）:** `War`, `Battle`, `Army`, `Soldier`, `1 Player`, `2D`, `Mouse`, `Difficult`
  - 如果只能选 5 个：`War`, `Battle`, `Army`, `Soldier`, `1 Player`
  - 同类参考：CrazyGames 上的一战游戏 *Warfare 1917* 用的是 Strategy + Battle / War / Classic。

## 7. Other form fields 其他常见字段
| 字段 | 填写 |
|---|---|
| Game type / engine 类型 / 引擎 | HTML5, plain JavaScript + Canvas 2D (no engine) |
| Orientation 方向 | Landscape 横屏 |
| Devices 设备 | Desktop: yes. Mobile: landscape works (touch + on-screen officer pad). Test on a real phone before ticking mobile; if unsure, submit desktop only first. |
| Languages 语言 | English (default), Simplified Chinese. Picked from the CrazyGames locale (`systemInfo.locale`); the player can switch in Settings. |
| Multiplayer 多人 | No, single player |
| Login / account 账号 | None. Progress is saved in the browser (localStorage). |
| In-game purchases 内购 | None |
| Ads 广告 | CrazyGames SDK v3 only: rewarded "Extra draft" button (+33 men, max 3 per day), midgame after every failed attack (the platform's own cooldown applies) and after wins (max once per 3 min), 300x250 banner on the result card. Game muted and paused during ads; keeps working with AdBlock. |
| SDK events | loadingStart / loadingStop, gameplayStart / gameplayStop, happytime on victory, CrazyGames mute setting honoured |
| Age rating 年龄 | PEGI 12 compatible: stylised 2D soldiers, no blood or gore (hit effects are mud spray), no bad language |
| Release date 发布日期 | 2026 |
| Developer 开发者 | （填你的名字或工作室名） |
| Credits 版权 | Music by Kevin MacLeod (incompetech.com), CC BY 4.0 (shown in Settings and CREDITS.md). Sound effects CC0 from freesound.org. |

## 8. Covers and preview videos 封面图 / 预览视频 (mandatory 必须)
- Images 图片: **1920x1080 (16:9)**, **800x1200 (2:3)**, **800x800 (1:1)**. All three in the same style.
  - Only the game title may appear: no "New / Play now", no borders, no icons or store logos, nothing blurry.
  - Official advice: not a plain screenshot; a strong main visual + big title.
- Videos 视频: **15-20 s**, **1080p 16:9** and **1080p portrait 2:3** (both mandatory), max 50 MB.
  - No black bars, no black-screen logo intro, no default mouse cursor, no "Play now" text, no fast-forward.
- 建议画面：黎明时分，士兵踩着梯子爬出战壕，军官吹哨，大字标题 CHARGE!（模板字体，和游戏 logo 一致）。

## 9. Checklist against CrazyGames requirements 对照要求自检
| Requirement | Status |
|---|---|
| Initial download <= 50 MB, total <= 250 MB, files <= 1500 | 4.4 MB zipped / 5.6 MB unzipped, 5 files |
| index.html at the ZIP root | yes |
| English localization; use the SDK locale, fall back to English | yes (v1.4f) |
| No custom fullscreen button | yes (none) |
| No external links / cross-promotion | yes (none) |
| Ads only through the CrazyGames SDK; works with AdBlock | yes; ad errors / adblock just continue the game |
| Mute + pause during ads | yes (frame loop paused, audio suspended) |
| Same behaviour at 60 / 144 / 165 Hz | yes (time-based updates, dt capped) |
| Readable at 907x510 ... 1920x1080 and 800x450 | UI scales with the frame (zoom 0.74-1.45) |
| Full Launch: gameplay within 1 click | Play -> planning screen (first time: short intro with SKIP) |
| PEGI 12 | no blood or gore; hit particles are mud (v1.4f) |
| Restricted keys | no Esc or Ctrl+W; physical key codes (AZERTY friendly) |

Basic Launch note: new games start in Basic Launch (monetization off, SDK optional).
The SDK integration is already done, so nothing needs changing for Full Launch.
