# Client feature timeline, 2.00 to 2.31

Date: 2026-10-21

Source: the release notes shipped in the Graal Reborn 2.2.2.0 folder (`newfeatures2001.txt` … `newfeatures2005.txt`, summarized). The file names are release years, not version numbers: `2001` covers 2.00–2.12 (it also repeats 1.32–1.41), `2002` covers 2.13–2.17, `2003` covers 2.18–2.21, `2004` covers 2.22, and `2005` covers 2.3–2.31. The protocol column links each note to what the binaries show (`protocol/client-versions.md`). Tags: **[doc]** release notes · **[bin]** client binaries.

| Version | Release-note highlights | Protocol anchor |
|---|---|---|
| 2.00 | Online-only: 2/3/4-player mode and save games removed. Bush rupees and pot hearts go server-side. `warpto <account>` for GPs. | |
| 2.01 | Level preloading on maps. `hitobjects` added as the fair replacement for `hitplayer`. `openurl2`. | `PLI/PLO_HITOBJECTS` (36/46) |
| 2.02 | Hats and signs with images, string parsing. Free-server limits on light effects and "complex" ganis. | |
| 2.03 | `triggeraction x,y,action,params`. RC and NC get `/` chat commands. The built-in zlib.dll is replaced by in-game compression code "because it has been abused". | `PLI/PLO_TRIGGERACTION` (38/48) |
| 2.04 | Engine work: gani `PLAYSOUND PARAM1`, `replacegani`, sound and animation changes. | |
| 2.05, 2.05 rev 2 | Mostly bug fixes. Server name in the window title. **2.05 rev 2 is the `GNW03081` build.** | type 0, gen 3, 59 PLO ids **[bin]** |
| 2.1 (rev1–3) | New start window and server list with account info. New image engine without GDI. Gani scripts (`SCRIPT … SCRIPTEND`). String arrays. `play2`. Auto-mapping. **Big map and minimap set by the gserver (`bigmap=` / `minimap=` in serveroptions) instead of the listserver.** **Ghost mode** for free players, queued until activated. Alt+0 log window. `graalversion`. | `PLO_BIGMAP` / `MINIMAP` (171/172) and ghost ids (170, 173, 174) are handled by 2.17 but not 2.05 **[bin]** |
| 2.12 (rev1) | Graal2001/Graal2002 client compatibility. Multi-level editing. `wraptext`, `wraptext2`. | |
| 2.13 (rev3–4) | Editor control-NPCs. **New RC with file browser, server list, and RC+NC in one program.** | `RemoteControl.exe` (see `tools/remotecontrol.md`) |
| 2.14 (rev4–7) | **Server list gets two tabs** (company servers, classic and playerworlds). Voice chat. **Player-list status icons** (`playerlisticons=` in serveroptions). **`serverwarp <world>`**. **Files over 64 KB can be downloaded** (`downloadpos`). Gmaps auto-download. | `PLO_STATUSLIST` (180), `SERVERWARP` (178), `LARGEFILESTART/END` (68/69), all handled from 2.17 **[bin]** |
| 2.15 (rev2) | Bug fixes, "enabling Graal2002". `showimg2`. | |
| 2.16 (rev1–7) | Real transparency (`seteffectmode`). Gani attributes `#P10`–`#P30`. More server-list features. UDP check improved, with a warning when UDP is blocked. | `PLPROP_GATTRIB10–30` (54–74) |
| 2.17 (rev1) | Graal Kingdoms speedups. **Level heights stored in level files instead of the gmap.** | `PLO_BOARDHEIGHTS` (185) **[bin]**; still type 0, gen 3; adds `PLI_TAMPERCHECK` (39) and the signed `arrays2.dat` listserver config **[bin]** |
| 2.18 (rev1) | **"New password encryption"** for stored passwords. Preloaded levels on entering a server. | |
| 2.19 (rev1) | Released alongside v3. New start screen and server list. **"Better compression"** (bz2). `this.` strings on the client. On NPC-server servers the client stops sending non-`client.` strings. | gs2lib: `GNW15053`, type 4 / gen 4 (bz2 + partial XOR) **[srv]** |
| 2.2 | Multi-byte sign text (Korean, Chinese, Japanese). **Server-side tile changes on gmaps via `updateboard2`.** | `PLO_BOARDMODIFY2` (186), handled from 2.22 **[bin]** |
| 2.21 | **"Network traffic reduced drastically"**. `triggeraction 0,0,clientside,…` reaches a weapon's client-side part. | gs2lib: `GNW01113`, the compression byte **[srv]** |
| 2.22 | **Third server-list tab** for under-construction playerworlds (gold/VIP only). `gravity`. `downloadsize`. | type 5, gen 5, `GNW03014`, listserver `GNW30123` **[bin]** |
| 2.3 | **Editor and online client split into separate exes.** `FILENAMECACHE.txt`. New timer (no 99% CPU). B-tree NPC lookup. **Classic client-side mode removed: Classic moved to the NPC-Server.** Graal3D server tab. `graal://` URL handler with `serverstartparams`. **Full-precision player and NPC positions** ("enabled once all clients are switched"). `timevar2`. More hacking checks. | `PLO_HASNPCSERVER` (44) dropped, `PLO_MOVE2` (189) and `LARGEFILESIZE` (84) added in 2.31 **[bin]** |
| 2.31 | Float-to-string fix, keyboard config saved, gmap NPC border crossing fixed. | `GNW28015` **[bin]** |

## Reading the timeline against the binaries

- Several features announced as "will be enabled later" show up in a client's receive switch one or more versions before the server used them (full-precision moves in 2.3, level heights in 2.17). A handled id is therefore not proof that servers of that era sent it. **[bin][inf]**
- The jump from 79 to 81 handled ids between 2.17 and 2.31 is small. Most 2.19–2.31 changes are cipher, compression, and scripting changes, not new packets. **[bin]**
