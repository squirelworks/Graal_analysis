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
- **Room name is not always the constant `Zelda2`** (2026-10-24 decompile). One branch of the join routine uses `Zelda2`; the other, chosen by an argument given when the network client object is created, builds the room from the current level file's base name as `Z` + base + `2` (a level `level1.zelda` would give `Zlevel12`) and then runs a follow-up routine (not traced). Which branch normal play uses was not traced; the two-client local mode is a likely user of the per-level form. The statement in `protocol/relay-1998.md` that 1st and 2nd Graal always join `Zelda2` holds for one branch only. The client always sends the name `def` in the join line and the real nickname later in a `D` payload.

## 1.39

- Token built as eight char immediates in the login/token builder: `G N W 0 7 0 8 0`.
- Connects to port `14900`.
- **Send helper drops payloads that contain a newline** (2026-10-24 decompile; the same helper exists in 2.05 rev2). A message is `id+32`, payload, newline, so a newline inside the payload would break the framing and the helper silently discards the whole message instead of sending it. The queue is flushed when it would pass 4095 bytes. In 1.39 the client closes the connection if more than about 256 KiB of compressed output is pending (the 2.05 figure was not checked). A client built on this framing should reject or escape payloads containing a newline rather than expect an error.
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

## 1998 betas to 1.32 (added 2026-10-21)

All 25 client builds from 1st Graal to 1.32 have now been analysed, together with the bundled GServer 1.1.9, 1.21, 1.28 and 1.3 and RemoteControl 1.21, 1.28 and 1.3. See:

- `protocol/relay-1998.md`: the gen-1 text relay (lobby lines, `D` payload types per build, game names `Zelda2` and `Graal` to `Graal8`).
- `protocol/gserv-1999.md`: the GSERV007 to GSERV018 login, zlib framing, which tokens each GServer accepts, and the id ranges.
- `formats/graalsav.md`: Graalsav1 to Graalsv11 and the DES-wrapped `.code` and `.gsave` files.

Two corrections to earlier assumptions:

- `TAdventureServer` (from 15th Graal) is a hostname-to-IP cache record, not a server or a peer-to-peer mode. The 1998 clients only ever connect out to a relay.
- Port 14801 is the compiled-in local default, and 14802 is the Cyberjoueur relay that the connect dialog points at. Neither one is a listening port in the client.

In the 1998 clients the network classes are `TAdventureClient` (the relay connection), `TOtherClient` (one per relay peer) and, from 3rd Graal, `TWebClient` (the HTTP level fetcher). The script classes listed above for 1.39 (`TAdventureLevel`, `TAdventureCommand` …) are not in 1st or 3rd Graal.
