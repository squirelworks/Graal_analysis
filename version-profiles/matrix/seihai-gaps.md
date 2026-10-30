# Seihai's version profiles against the matrix

Date: 2026-10-30. Compared: Seihai `main` at 72ed21d (`client/src/protocol/profile.rs`, `chain.rs`, `documentation/version-profiles.md`) with `README.md` in this folder.

## What Seihai already covers

Seihai has 26 profile rows, 1.33 to 2.31, built as a version chain (1.33 written out, each later build a delta). A row sets the token, client type, cipher generation, listserver endpoint and login shape, the server→client and client→server id sets, prop limits, file and level features, the death and combat rules where traced, and UI switches (server list style, chat recall, HUD sheet layout, minimap, editor, ganis, emoticons, key config, log window, ghost mode, server name in the title, GS1 count). The 50 ms game clock, the half-tile walking step and the 8-voice sound cap are global and match every build measured (`live-runs-2026-10-30.md`), so they need no per-version switch.

## Missing, by size

### 1. Eras with no profile at all

| Era | Builds | What a profile would need |
|---|---|---|
| Z, A: 1998 (Java and 1st Graal to 1.1.9) | 21 | The gen-1 relay (lobby `N/P/C/D` lines, game names `Zelda2`, `Graal` … `Graal8`, `D` payload types per build), `.zelda` and GR-V1.00–1.03 levels, `Graalsav1`–`8`, GIF sheets of their own sizes, the 1998 start windows, two-player local mode. `protocol/relay-1998.md`, `formats/graalsav.md`. `EncryptionGen::Gen1` exists in Seihai but no row uses it. |
| B: 1.21 to 1.32 | 5 | GSERV007–018 login on gen 2 (`protocol/gserv-1999.md`), port 14804 then 14900, the 1.2x id ranges, `Graalsv11` saves, 224×49 and 224×81 HUD sheets. |
| 3D0: Graal3D (2000) | 1 | Its own client and server protocol (`graal3d/protocol.md`); a separate program, so it fits the planned Seihai suite rather than the 2D selector. |
| H: 3.x | 2 | Gen 5 as 2.22/2.31, but login tokens `G3D03014`/`G3D28015`, no tamper check, the signed `license.graal` list host, the category prefix that picks a server-list tab, 79/88 handled ids. Close to 2.22/2.31 on the wire. |
| I, J, K: 4.x to 6.x | about 20 | Login id 5 with the machine-id list, the `Login` game server instead of a listserver, update packages, GS2 bytecode and server-built GUI; 6.11's script-defined framing. A different client rather than a profile row. |

### 2. Look switches the rows do not have

| Gap | Matrix value | Seihai today |
|---|---|---|
| Name and chat text font | Bundled Tempus Sans ITC at 24 from NewMain 1.42 to 2.31; Helvetica-named before (1.38–1.41); `font=`/`fontsize=` from 1.3 test | One 5×7 bitmap font for every version (`render/font.rs`). The chat-bubble thread covers the bubble itself. |
| Start window | Distinct per era (see the matrix and the screenshots) | One launcher for every version |
| Main window size | 648×508 (1.3x) / 648×514 (1.41, 2.01–2.1) / 648×507 (2.00) / 644×507 (2.17+) | Not per version |
| HUD sheet layout | 224×81 (1.33–1.37), 224×97 (1.38–1.39), **224×145 (1.41 to 2.31)** | `HudArt::BlankButtons` covers 1.38 to 2.31 and its comment calls the later builds inferred. The HUD already draws the AP and MP bars only when the sheet has their frames, so the drawing is right; the comment is not. (Fixed in the accompanying Seihai change.) |
| Options and windows | Per-build form lists (`builds-deltas.md`) | Not modelled |
| Local multiplayer and save games | Up to 1.41 | Not modelled |

### 3. Rules that are only partly per version

* **Death and combat.** 1.41 carries the 2.05 rules from the template, 1.42 to 2.04 carry none, 2.05 and later carry them (`chain.rs` already lists this as unknown). No pre-2.05 handler was traced, so a consistent choice would be either 2.05 rules for every build from 1.41, or none before 2.05. The matrix does not settle it.
* **Bush, pot and stone respawn.** Client-side before 2.00, server-side after (release notes). The exact timers are being measured in another thread.
* **Tamper check.** Seihai has the per-build constants and resend rules opt-in; nothing new here.

### 4. Assets per version

Seihai reads each version's own asset folder (`assets.<label>=`). The matrix lists which sheets and sizes each build shipped (`builds-static-survey.tsv`). The archives for 2.00 to 2.05 hold only the exe, so those versions need the art from a neighbouring install; 1.41 rev1 and NewMain 1.42 (`graalnm26`) are the closest full installs.

## Suggested order

1. Name font per version (Tempus Sans ITC for 1.42+), since every screen shows it.
2. A 1.21–1.32 profile (GSERV login on gen 2 is a small step from Seihai's gen-2 1.33 path).
3. The 1998 relay as its own mode.
4. 3.x as two rows next to 2.22/2.31.
5. 4.x and later as a separate client in the planned suite.
