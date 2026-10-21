# Early Graal clients — extracted details

Date: 2026-10-14

Derived from the decompile corpus. Raw exports stay in `/shdecompiling/`. This note is cleaned.

## Lineage

| Era | Binary | Port | Levels | Token |
|-----|--------|------|--------|-------|
| Zelda Online (Java, 1997–98) | applet | 14801 | `.zelda` (Z3-V1 RLE) | none |
| 1st Graal (Delphi) | 1st Graal.exe | 14801 | `.zelda` (24 refs) + `.graal` (4 refs) | none |
| 1.39 | Graal 139.exe | 14900 | transitional | `GNW07080` |
| 2.05 | Graal.exe v2.05 | — | `.nw` (GLEVNW01) | `GNW03081` |

## 1st Graal

- 505 functions. No version token. No `GNW` string.
- Default host `127.0.0.1`, port `14801` (same as the Java precursor).
- Save format magic: `Graalsav1`.
- Level names hard-coded: `level1.zelda`, `cave2.zelda`, `house1.graal`, `village1.zelda`, and others. Both extensions coexist.
- Sign text present: `"Sign at ("`.
- String table includes `NZelda2#def`.

## 1.39

- Token built as eight char immediates in `FUN_004c7208`: `G N W 0 7 0 8 0`.
- Connects to port `14900`.
- Dhrake recovered ~390 names. Preferred corpus is `graal-139-dhrake/`.

### Recovered classes
- `TAdventureClient_Create` / `InitTable`
- `TAdventureLevel_Create` / `InitTable`
- `TAdventureCommand_Create` / `InitTable`
- `TAdventureOperation_Create` / `InitTable`
- `TAdventureVariable_Create` / `InitTable`
- `TAdventureWeapon_InitTable`
- `TAdventureServer_InitTable`
- `TAdventureBoolOperation_InitTable`
- `TAdventure_DXDrawFinalize` / `DXDrawRestoreSurface` / `DXTimer`
- UI: `TAdventure_PlayButtonClick`, `SpeedButton`, `StatusBar`, `TabControl`, `HorzScrollBar`, `PaintBox`, `FormCanResize`

### Script events present
`playerenters`, `playertouchsme`, `playerendsreading`, `playerlaysitem`, `playerisfemale`, `playerismale`, `playeronhorse`, `playerswimming`, `wasshot`, `shotbybaddy`, `shotbyplayer`, `compusdied`, `timeout`, `created`, `gotheart_`, `drawoverplayer`, `drawunderplayer`, `followsplayer`.

### Properties
`hearts`, `rupees`, `shield`, `shieldpower`, `hasweapon`, `isweapon`, `weaponsenabled`, `playerx`, `playery`, `carriesnpc`.

### Sounds
`arrow.wav`, `arrowon.wav`, `axe.wav`, `bomb.wav`, `chest.wav`, `compudead.wav`, `crush.wav`, `dead.wav`, `extra.wav`, `fire.wav`, `frog.wav`, `goal.wav`, `item.wav`, `item2.wav`, `jump.wav`, `nextpage.wav`, `put.wav`, `sign.wav`, `steps.wav`, `stonemove.wav`, `sword.wav`, `swordon.wav`, `thunder.wav`, `water.wav`.

### Config keys (`graalconfig.txt`)
`serveraddr=`, `fixedport=`, `fixedudpport=`, `dontconnectlevels=`, `dontloadlistheads=`, `loadcolorsfromserver=`, `sortplayersbyname=`, `limitnicknames=`, `nicknamelimit=`, `gamemode=`, `language=`, `font=`, `fontsize=`, `musicon=`, `joystickon=`, `nodirectinput=`, `noudp=`, `nodecompressionerror=`, `nohtmlimages=`, `nohtmlinpms=`, `nomassmessages=`, `notoalls=`, `reversestereo=`, `saveimages=`, `compabilitydraw=`.

### Files
`graal.bmp`, `graal.png`, `graalmap.bmp`, `levels\recordpos.txt`, `weblevels\`. Extensions: `.code`, `.gif`, `.graal`.

### Rendering
DirectDraw and DirectSound. `TAdventure_DXDraw*` handles surface restore and the timer. `compabilitydraw=` is a config toggle.

## 2.05

- Token built as char immediates in `TAdventureClient_Create`: `GNW03081`.
- `DispatchGs1.txt` is the GS1 interpreter, not the packet dispatcher.
- Levels are GLEVNW01 `.nw`. Framing is length + zlib. Post-login uses the Borland LCG.

## Protocol transition summary

1. Java precursor: text lines on 14801, `.zelda` RLE.
2. 1st Graal: same port, Delphi, `.zelda` dominant, no token, `Graalsav1` saves.
3. 1.39: port 14900, token `GNW07080`, full event set, DirectX, config file.
4. 2.05+: length + zlib, `.nw`, token `GNW03081`, post-login LCG.

Correction (2026-10-21, from `build-catalogue.md`): zlib packet compression starts with 1.2 (May 1999), and the post-login LCG insertion (gen 3) is already in 1.41 rev1 and every 2.0x build, not only 2.05+. 1.39 has no LCG insertion. `.nw` is in NewMain 1.42 and 2.05 but not in 2.00–2.04.
