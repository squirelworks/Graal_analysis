# Per-version profile matrix, 1998 to 2014

Date: 2026-10-30

This is the one-page view of how each Graal client **thinks** (protocol, scripting), **acts** (timing, movement, rules, sound) and **looks** (window, start screen, HUD, fonts, menus), from the Java Zelda Online of 1998 to the 6.11 Mac client of 2014, plus the Graal3D side project. Each cell is short and points at the note that has the detail. It is meant as the checklist for a client that wants to *be* a chosen version, such as Seihai's version selector.

New in this pass (2026-10-30):

* A static survey of all 57 Delphi client executables (1st Graal to 2.31): forms, main window, frame timer, fonts, sound names, config keys and shipped sheets. Per-build values are in `builds-static-survey.tsv`, and what each build adds or drops is in `builds-deltas.md`.
* Live runs under Wine of 1st Graal, 1.0, 1.1, 1.32, 1.41 and 2.00, with screenshots and a walking-speed measurement (`live-runs-2026-10-30.md`).
* A comparison with Seihai's per-version profiles (`seihai-gaps.md`).

Tags, as elsewhere in this repo: **[bin]** read from the client binary · **[file]** shipped files · **[live]** seen in a running client · **[cap]** packet capture · **[srv]** server source · **[doc]** release notes · **[inf]** inferred.

## Eras

The builds fall into eleven eras. Inside an era the clients share their engine and wire format, so a profile can be one era row plus the per-build deltas listed in the linked notes.

| Era | Builds | Dates | Engine | Detail |
|---|---|---|---|---|
| Z | Zelda Online 1 and 2 (Java applets), GServ Standalone | May–Jul 1998 | Java | `../../client-internals/zelda-online-1998.md`, `../../client-internals/precursors-and-fan-builds.md` |
| A | 1st Graal to 1.1.9 Gold (20 builds) | Sep 1998 – Feb 1999 | Delphi 2-level compiler (2nd Graal: Delphi 4), DelphiX | `../../client-internals/build-catalogue.md`, `../../protocol/relay-1998.md` |
| B | 1.21, 1.28 beta 2, 1.3 test, 1.31, 1.32 | May 1999 – Jan 2000 | Delphi 4 from 1.28b2, DelphiX | `../../protocol/gserv-1999.md` |
| 3D0 | Graal3D | Feb 2000 | Delphi, DelphiX Direct3D retained mode | `../../graal3d/README.md` |
| C | 1.33 to 1.39 | Feb – Aug 2000 | Delphi 4, DelphiX | `../../client-internals/versions-133-139.md` |
| D | 1.41 rev1 | Nov 2000 | as C | `../../client-internals/version-profiles/README.md` |
| E | NewMain 1.42, 2.00 to 2.05 rev2, 2.1 tests, NewWorld betas | Jan – Oct 2001 | as C, plus DirectDraw 7 | `../../client-internals/cross-version-timeline.md`, `../../client-internals/newworld-betas.md` |
| F | 2.1 to 2.17 (only 2.17.1 survives as a binary) | Oct 2001 – 2002 | as E, BASS audio from 2.17 at the latest | `../../client-internals/version-profiles/141-217.toml` |
| G | 2.22, 2.3 (no binary), 2.31 | 2004 – 2005 | as F | `../2.22-2.31.md` |
| H | 3.04 Linux, 3.153 Mac | 2004 – 2005 | C++ on the Torque Game Engine | `../../protocol/v3x-clients.md` |
| I | 4.04r2, 4.20r6/r8 | 2006 – 2007 | Delphi launcher + C++ `GraalEngine.dll` (+ `Graal3DEngine.dll`) | `../../protocol/v4x-clients.md` |
| J | 5.00r7, 5.12; then 5.24 to 5.31 | 2007 – 2011 | 5.00/5.12 as I; from 5.24 one MSVC exe (`quattro_lib`) | `../../protocol/v5x-clients.md`, `../../protocol/v5v6-windows-unpacked.md` |
| K | 6.00 betas to 6.03r7, 6.11 Mac | 2010 – 2014 | one native C++ program per platform, no Torque layer | `../../protocol/v6x-clients.md` |

## Thinks: wire and scripting

| Era | Login token | Cipher gen | Server discovery | Ids handled / sent | Props parsed | Scripting |
|---|---|---|---|---|---|---|
| Z | none | text lines | `host:14801` | text lobby lines | – | none |
| A | none | 1 (no zlib) | connect dialog, the loopback address on 14801, Cyberjoueur relay 14802 | relay lobby `N/P/C/D` lines, `D` payload types per build | relay `D` types | GS1-like, `this.` vars from 1.1 beta1 **[bin][doc]** |
| B | `GSERV007`–`018` (a protocol revision, not a date) | 2 (zlib, no cipher) | connect dialog, `<list-host-classic>:14804`, `:14900` from 1.31 | GSERV id ranges (`gserv-1999.md`) | – | GS1, NPC weapons from 1.21 |
| 3D0 | `GR3DV002` | own (2D codec, no key byte) | the loopback address on 14901, UDP 14898 peer to peer | own renumbered ids | 3D floats, 24-bit colours | none |
| C | `GNW` + date (`GNW20020` … `GNW07080`) | 2 | connect dialog `<list-host-classic>:14900`, guest/guest | 1.33: S→C 0–41, 100; C→S 0–31; grows to 45 / 35 ids by 1.39 | own 0–33/34, others 21–23 ids | GS1, 88 → 111 commands |
| D | `GNW13110` | **3** (key byte + LCG insertion) | first server-list window | +1.41 deltas | props to 36 | GS1, 126 commands |
| E | `GNW08011` … `GNW03081`; NW betas `G2N15041`; 2.1 tests keep `GNW03081` | 3 | listserver, host DES-hidden from 2.00, `:14921` (2.1 tests `:14922`) | 2.05: 59 S→C ids | to 42 (2.05), 50, 51 | GS1 134 → 161 commands, ganis from 1.42 |
| F | `GNW31101` (2.1) … `GNW22122` (2.17) | 3 | 2.17: signed `arrays2.dat`, id 0 then id 1 | 2.17: 79 S→C, 61 C→S; TAMPERCHECK (39) from 2.17 | to 74 (gani attrs `#P10`–`#P30` from 2.16) | GS1 + gani scripts (2.1), `this.` client strings (2.19) |
| G | `GNW03014`, `GNW14015`, `GNW28015`; list `GNW30123` | **5** (compression byte, partial XOR, bz2) | listserver id 7 `GNW30123newmain` | 2.22: 80, 2.31: 81 | to 74 (2.22), 80 with X2/Y2/Z2 (2.31) | GS1; classic client-side NPC mode removed in 2.3 |
| H | `G3D03014`, `G3D28015`; list `G3D30123` | 5 | RSA-signed `license.graal` → `<list-host-3x>:14922` | 79 (3.04), 88 (3.153) | as G | GS1 native + TorqueScript `.dso` for menus; NPC bytecode ids (3.153) |
| I | `G3D17026`, `G3D27076`, `G3D20126` | 5 | `license.graal` → `<login-host-4x>:14900`; server named `Login`, no separate list protocol | 98–101 | – | GS2 bytecode, server-pushed ganis (195), update packages `GRPKG001` |
| J | `G3D22067`, `G3D14097`, `G3D15010`, `G3D26090` | 5 | as I; from 5.24 the hosts are compiled in, no license file | 95–100 | – | GS2, `GRESCR01` script cache; anti-cheat process scan (182/183) |
| K | `G3D0108A`/`G3D0511C` (Linux), `G3D0311C` (Win 6.03); 6.11 set by script | 5; 6.11 can switch to a **script-defined** header with RC4/AES/TLS | compiled-in `loginserver*:14900`; 6.11 HTTPS connector to `con.quattroplay.com` | 91–97 | – | GS2; in 6.11 even the packet id tables come from the server's script |

Login-time extras that a faithful client must send: `PLI_LANGUAGE` (37) from 2.02 rev2 **[bin]**; `PLI_TAMPERCHECK` (39) once (2.17), on gmap crossings and level links (2.22), or every 3.2 s (2.31) **[cap]**; machine-id MD5s after the password from 4.x on **[bin]**.

## Acts: timing, movement and rules

| What | Value by era | Source |
|---|---|---|
| Game tick | **50 ms** in every Delphi build. A through D drive it from a DelphiX `TDXTimer` (interval 50 in the main form); from NewMain 1.42 the form has no DX timer and the frame runs from the idle handler behind a 50 ms gate. Graal3D: 50 ms `TDXTimer`. | **[bin]** survey; `../../client-internals/rendering-observations.md` |
| Walking | **0.5 tile per tick, 10 tiles per second**, from the first beta on. Measured live in 1st Graal, 1.0, 1.1, 1.32, 1.41; the 2.05 trace and the 2.05/2.17/2.22/2.31 walking routine agree. | **[live]** `live-runs-2026-10-30.md`; `../../client-internals/decomp-findings-2026-10-25-m/01-walking-rule.md` |
| Wall test | 2.05–2.31: six probe points per facing, corner nudge 0.1, flush snap. In 1.1 a position with a 0.025 offset (x = 26.925) showed up after bumping furniture, which fits a similar rule; the pre-2.05 rule was not read. | **[bin]** 2.x; **[live]** 1.1 |
| Death and respawn | 2.05 rules (30-tick timer, input lock to 27, respawn hearts by AP); 2.22 lab-confirmed; earlier builds not traced. | `../../client-internals/feature-specs/04-death-respawn.md` |
| Combat | 2.05: hurt 40 ticks, knockback 1 tile per tick for 5 ticks, sword reach 0–4 tiles. Not traced before 2.05. | `../../client-internals/decomp-findings-2026-10-24-d/` |
| Ledges, push/pull, carry-hide | 2.05: jump on the 18th blocked step; `canbepushed`/`canbepulled` from 1.1 beta1, separated in 1.34; hiding under a carried object (mode 14). | `../../client-internals/ledges-push-pull.md`, `../../client-internals/carry-hide-and-glove.md` |
| Bush, pot and stone respawn | Client-side before 2.00 **[inf]**; server-side from 2.00 ("bush rupees and pot hearts go server-side"). Exact timers are being measured in a separate thread. | **[doc][inf]** |
| Local multiplayer | Two players from 1st Graal; Two/Three/Four Players to 1.41; removed in NewMain 1.42 / 2.00. | **[bin][live]** start windows |
| Sleep on start | 1.1 starts the offline game with the player asleep in bed (a key wakes the player). | **[live]** |
| Sound engine | none in 1st–4th Graal; DelphiX DirectSound from 4th alpha (12 named `.wav`s), 29 by 8th Graal, 24–27 named through 2.31; MCI MIDI, plus Winamp control from 1.41 until BASS replaced it; BASS from 2.17 (no Winamp, adds volumes, radio, voice chat); fmod in 3.x–5.x, SDL_mixer on 6.x Linux. Max 8 effects at once (2.05). | **[bin]** survey; `../../client-internals/sound-and-music.md` |
| Save games | `Graalsav1` … `Graalsv11`; F2/F3 to 1.41; gone in 2.00. | `../../formats/graalsav.md` |

## Looks: window, screens, HUD and text

| What | Value by era | Source |
|---|---|---|
| Main window | Caption "Graal". Outer size 648×521 (1st Graal), 648×516 (2nd Graal to 1.1.9), 648×508–509 (1.21–1.39), 648×514 (1.41), 648×507 (NewMain, 2.00), 648×514 (2.01–2.1 tests), 644×507 (2.17–2.31). Form font MS Sans Serif 14 px throughout. 2.05+ add the server name to the title. | **[bin]** |
| Start window | 1st Graal: "Graal - The Adventure", radio buttons One Player / Two Player / One Player Online with host the loopback address and port `14801`. 1.0: "Select the game mode" with the grail picture, character pick per player, "Online At Cyberjoueur" box with port 14802. 1.1 to 1.32: the rider-on-horse picture, mode and character drop-downs; 1.32 adds Language and Nick Name and "Managed by: Stéphane Portha". 1.41: Language, Game mode (One Player … Four Players), Character, Nick Name, "Lead programmer: Stefan Knorr". 2.00: dark-green "Graal 2001" window with the GraalOnline logo, Training / Options / Start. 2.1: new start window and server list. 2.22: Start Online / Training / Options; 2.31: Start Online / Editor / Options. 3.x on: Torque GUI or server-scripted screens. | **[live]** screenshots; **[bin]** forms |
| HUD sheet (`state`) | 448×96 GIF (1st, 2nd Graal) → 448×137 (3rd–5th) → 298×96 (6th) → 427×109 (7th, 8th) → 427×125/132 (9th, 1.0–1.1.9) → 224×49 (1.21) → 224×81 (1.28b2–1.37, PNG from 1.33) → 224×97 (1.38–1.39) → **224×145 (1.41 to 2.31)**. The NewWorld betas ship the older 224×97 sheet. | **[file]** survey; `../../client-internals/status-display.md` |
| HUD layout | Spiral (yin-yang) hearts at the top right in every build seen. 1st Graal shows three rupee digits (`000`), 1.0 drops leading zeros (`0`). The A/S/D item buttons appear by 1.32; 1.41 adds the AP bar under them. | **[live]** |
| Tileset (`pics1`) | 1024×512 (1st–4th Graal) → 1280×512 (5th–1.21) → 1856×512 (1.28b2–1.41) → 2048×512 (NewMain 1.42 on). | **[file]** |
| Name and chat text font | 1.3 test adds `font=`/`fontsize=`. 1.38–1.41 executables name Helvetica; the 1.41 install has `font=Helvetica`, `fontsize=24`, the 1.32 install `font=Dialog`, `fontsize=28`. **NewMain 1.42 to 2.31 register the bundled `tempsitc.ttf` (Tempus Sans ITC) at start-up**, and the installs set `font=Tempus Sans ITC`, `fontsize=24`. Live: 1.32 and 1.41 draw NPC names large, bold and white with a dark-blue outline; 2.00 draws them smaller in the rounded face. The chat bubble itself is in a separate thread. | **[bin][file][live]** |
| Other fonts | Courier New from 1.34 (the F6 debugger), Arial Black in 2.17–2.31 forms. | **[bin]** |
| Options | Options form from 1st Graal; More Options from 5th Graal; Controls from 15th Graal; player list from 1.28b2; profile from 1.39; server list from 1.41; log window, RPG window and tile-array dialog by 2.17 (no 2.1x binary to place them earlier); 2.31 drops the editor forms (29 → 18). | **[bin]** `builds-deltas.md` |
| Keys | Arrows or IJKL, A/S/D, M map, Q items, P pause, Tab chat; fixed to 1.37, rebindable from 1.38; F1–F7 and Alt+1–9 per `versions-133-139.md`. | **[bin][doc]** |
| Heads and characters | Pick list with named characters (Nick, Mandi …) from `heads.gif` in 3rd Graal to 1.1.9; `headsconfig.txt` (Fung Si Yan, Nick, Mandi, Bad Max …) with one image per head from 1.21. | **[file][live]** |

## What is still unknown

Ranked by how much it changes what a player would notice.

1. **The 1998 to 1.41 rules.** Death, hurt and knockback, sword reach and the wall test were only read for 2.05 and later. Walking speed is now known to match; the rest is assumed.
2. **2.1 to 2.16 and 2.3.** No binaries. Everything in era F before 2.17 is from release notes and server source.
3. **5.x and 6.x look.** The screens come from the server (`Login` server GUI scripts, update packages), so the look is whatever that server sent. A capture of a real `Login` session is the only source.
4. **Graal3D movement and camera.** Not mapped (`../../graal3d/README.md`, open points).
5. **Default name font before 1.38.** The exes from 1st Graal to 1.37 contain no font family name for the game text; 1.32's install says `Dialog`, which Windows does not have, so a substitute was used.

## Files in this folder

| File | What |
|---|---|
| `README.md` | This matrix. |
| `builds-static-survey.tsv` | One row per executable: MD5, size, form count, main window, form font, frame timer, sound/config/image name counts, sheet sizes. |
| `builds-deltas.md` | Per-build additions and removals of config keys, sounds, images, forms and fonts. |
| `live-runs-2026-10-30.md` | The Wine runs: how, what was measured, screenshots. |
| `seihai-gaps.md` | Seihai's profiles against this matrix. |

The survey script, the form parser, the Wine helpers and the screenshots are in the project folder under `graal-decompile/version-matrix/`, not in this repo.
