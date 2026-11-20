<!-- manual: kind=reference status=draft -->
# Appendix E (continued). Settled questions

> Status: draft. This file holds the settled entries of Appendix E, split out of the open questions so the open entries read on their own. Entry numbers are unchanged, so every `App. E#n` reference still resolves.

## E.12 Settled questions

These entries were answered. Each keeps its number and a short record of how it was settled, so that a reader who meets the old claim in a note can see why the manual does not follow it [doc] (docs/book/04-where-the-notes-disagree.md).

### E#2 Generation-5 step count of 5.12 and 5.00r7 (settled)

How many cipher steps a generation-5 frame advances when its compressed body is not a whole number of four-byte groups was settled for 5.12 and open for 5.00r7, a separate engine. Probe-proxy sessions with the real 5.00r7 settled it [lab] (protocol/fuzz-4x-5x-win-2026-11-19.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (holds) | 5.12 steps the iterator `len / 4` times rounded down for zlib and bz2 frames (capped at 4) and rounded up for raw frames, both ways | [bin][wire] (protocol/gen5-cipher-step-5x.md) |
| Claim B (superseded) | Every later frame of ten 5.x and 6.x captures decodes with one step per group present, rounded up; it is not a competing decoder once short compressed frames are counted | [cap] (protocol/v5v6-windows-unpacked.md) |
| Settled | The probe proxy ciphers both directions with Claim A's rule. The real 5.00r7 (native, Windows 10 lab VM), 5.24r3, 5.30r3 and 5.31r4, and before them 5.12 and 5.24r4, ran through it for 130 canary cases each: no lost client and no result different from the reference. Most zlib frames are not a multiple of four bytes long, so a wrong step rule would desynchronise the cipher at the first such frame in either direction | [lab] (protocol/fuzz-4x-5x-win-2026-11-19.md); [doc] (tools/probe/README.md) |
| Verdict | Verified by session survival on the exact builds. No single short frame was set beside both rules by hand, which is no longer needed | [lab] (protocol/fuzz-4x-5x-win-2026-11-19.md) |

### E#4 Whether 5.00r7 sends id 11 (settled)

Whether 5.00r7 sends `PLI_THROWCARRIED` (11) when the player throws was open, because two lists of its sent ids disagreed; a lab throw with the id recorded settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#throw-id-on-500r7-e4).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the send wrappers have no 11. B: the profile lists 11, and 5.12, 5.24r4 and 5.30r3 captures send it | [bin] (protocol/v5x-clients.md#client--server-ids-500r7); [bin][cap] (version-profiles/5.00-6.03.toml) |
| Before | A static read found the backup engine's throw path sending 11 with an empty body | [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#500r7-sends-id-11-when-throwing) |
| Settled | An unchanged 5.00r7, reaching the lab through a connect shim with its licence untouched, sent 11 with an empty body on each of 2 throws, after the lift's board change and ganis | [lab] (protocol/lab-appe-mirae-2026-11-20.md#throw-id-on-500r7-e4) |
| Verdict | Verified: Claim B holds; the wrapper list missed the throw path | [lab] (protocol/lab-appe-mirae-2026-11-20.md#throw-id-on-500r7-e4) |

### E#5 Meaning of id 162 from the client (settled)

Three readings of client id 162 turned out to be one message, a ping answer [srv] (protocol/packet-ids.md#client--server-pli_).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The 2026-10 gs2lib named 162 `PLI_RC_UNKNOWN162` (upstream now `PLI_PONG`): an empty message from the RC3 beta | [srv] (protocol/packet-ids.md#client--server-pli_) |
| Claim B | 4.20r8 sends 162 as the answer to S→C 108 | [bin] (protocol/v4x-clients.md#client--server-ids) |
| Claim C | 6.01r1 and 6.03r7 send 162 as a reply to a server request: `!` and a 2-byte value (two 7-bit groups, capped at `0x6FFF`) the server sent; probably the ping answer 6.11 calls `onSendPingAnswer` | [bin][inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settled | One message, a ping: 4.20r6, 4.20r8, 6.01r1 and 6.03r7 send 162 only from their 108 handler, with the same code in 4.20r8 and 6.03r7; the 2010 RC and RC3 send it empty every 60 s and have no 108 handler | [bin] (protocol/unknown-ids-2026-11-06.md) |
| Left over | A capture of a game client's answer to S→C 108 is still missing | [inf] (protocol/v4x-clients.md#client--server-ids) |

### E#6 Client-to-server constants of 1.21 and 1.32 (settled)

Whether 1.21 sends id 14 and 1.32 sends id 22 was open, because two reads of their send sites disagreed; a static read of both send routines settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Claim A: 0 and 10 to 26 in 1.21, 0 and 10 to 30 in 1.32. Claim B (profile): no 14 in 1.21, no 22 in 1.32. Best guess: neither is sent | [bin] (protocol/gserv-1999.md#message-ids); [bin] (client-internals/version-profiles/v121-v132.toml) |
| Settled | Every call to each build's send routine passes a constant id. 1.21 sends 0 to 13 and 15 to 26 (no 14). 1.32 sends 0 to 30, so it sends both 14 and 22; its 22 goes out when a list lookup finds no match, its 29 when one does | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |
| Verdict | Half right: the profile is right for 1.21 and missed 22 in 1.32. Both claims also left out 1 to 9, which both builds send | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |
| Left over | What 14 and 22 carry in these builds | [inf] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |

### E#7 Receive-branch revision discrepancy (settled for the checked inputs)

Two tables placed ids 47 and 168 in different revisions; a static check settled it for the revisions read [bin] (client-internals/cross-version-timeline.md#server--client-packets).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The timeline formerly placed 47 at 2.02 rev 2 and 168 at 2.05 rev 1; those labels are corrected | [bin] (client-internals/cross-version-timeline.md#server--client-packets) |
| Claim B | The per-build table already had 47 in 2.02 revisions 0 and 1 and 168 in 2.05 revision 0 | [bin] (version-profiles/plo-handled-ids-by-build.tsv); [bin] (client-internals/decomp-findings-2026-10-24-c/04-plo-server-to-client.md#set-growth) |
| Settled | The exact-input check backs Claim B for Windows x86 2.02 revisions 0 to 2 and 2.05 revisions 0 to 2 (→ §2.5.2) | [bin] (client-internals/receive-dispatch-revision-boundaries-2026-11-09.md#distinct-receive-routes) |
| Scope | Route presence only; runtime handling, payloads and first occurrence across all branches are not established | [bin] (client-internals/receive-dispatch-revision-boundaries-2026-11-09.md#validation-and-limits) |

### E#8 Prop parser ranges of 2.00 (settled)

Two sources disagreed on whether 2.00 parses player prop 36 and NPC prop 36; a re-read of the 2.0x jump tables settled it [bin] (protocol/player-props.md#parsers-in-200-to-205-re-read-2026-11-12-bin).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The player-prop parser gains 35 and 36 in 1.41, and the NPC-prop parser gains 36 to 40 only in 2.02 rev 2 | [bin][inf] (client-internals/cross-version-timeline.md#prop-parsers) |
| Claim B | The 2.00 layout tables have the self and other-player streams accept 0 to 35 and the NPC stream 0 to 36 | [bin] (version-profiles/plo-playerprops-layouts.tsv); [bin] (version-profiles/plo-npcprops-layouts.tsv) |
| Settled | The 2.00 and 2.01 self switch covers 0 to 36 and the NPC switch 0 to 35; NPC 36 to 40 arrive in 2.02 rev 2. Claim A holds; the other-player switch also accepts 36 (and 50, 51) | [bin] (protocol/player-props.md#parsers-in-200-to-205-re-read-2026-11-12-bin) |

### E#9 Uploads from game clients (settled)

Which game-client feature sends the file-browser and upload ids, and whether a server accepts them from a game connection, was open; a lab run and the client's own strings settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#upload-ids-from-a-game-connection-e9).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: game clients cannot upload; the ids are RC-only. B: 6.01r1 and 6.03r7 send the ids with an upload queue | [srv] (protocol/file-transfer.md#upload-rc-only); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settled | 6.03r7 describes its upload calls as working only while the scripted RC has a file browser open: they are the scripted-RC staff feature. On the GServer-v2 fork, those ids on a game connection are unknown packets; after three the player is dropped, and no file is written | [lab] (protocol/lab-appe-mirae-2026-11-20.md#upload-ids-from-a-game-connection-e9) |
| Verdict | Verified for the fork; both claims hold, for different connections. Original servers were not run | [lab] (protocol/lab-appe-mirae-2026-11-20.md#upload-ids-from-a-game-connection-e9) |

### E#11 Client-to-server ids the NewWorld betas lack (settled)

Two reads disagreed on whether the NewWorld betas send ids 8 and 20 [bin] (client-internals/version-profiles/141-217.toml).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The betas send the 2.1 test set without 7, 8, 11, 15, 16, 17 and 20 | [bin] (client-internals/version-profiles/141-217.toml) |
| Claim B | The betas send 34 ids, the 2.1 test set without 7, 11, 15, 16 and 17 only | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| Settled | Claim A: every send site in both betas was re-read; none sends 8 or 20 (nor 7, 11, 15, 16, 17), none passes the id in a register, and the betas send 32 ids | [bin] (version-profiles/pli-send-sites-141-217.md#newworld-betas-ids-8-and-20-app-e11) |
| Note | Claim B's count of 34 was 39 less five, the arithmetic that hid the gap | [inf] (client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md) |

### E#13 Gmap neighbour overwrite on classic-login 2.x clients (settled)

Whether GServer-v2's classic path makes 2.17 and older clients copy each gmap neighbour onto the player's own level was predicted by a static read; a lab run settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#neighbour-overwrite-on-2171-e13).

| Part | Discussion | Source |
| --- | --- | --- |
| Prediction | With stock framing, a 2.17.1 client on a 2 x 2 gmap shows neighbour boards on its own level; ending each neighbour reply with the player's cell name cures it | [srv][inf] (protocol/gmap-adjacent-level-target.md#what-gserver-v2-sends-srv) |
| Settled | 2.17.1 asks for the three neighbours with 35, the server answers each board with no `PLO_LEVELNAME` before it, and the player's own all-grass cell then shows neighbour walls at its edge. 2.22 on the same server gets every neighbour framed by `LEVELNAME` and draws them in place | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#neighbour-overwrite-on-2171-e13) |
| Verdict | Verified: the overwrite happens with the stock classic path | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#neighbour-overwrite-on-2171-e13) |
| Left over | The fixed-framing leg, which needs a server change; 2.17.1 sends no 35 when the `.gmap` is fetched after the warp, and sends cached modtimes when neighbours are cached | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#neighbour-overwrite-on-2171-e13) |

### E#17 The 6.1.1.3 login after the RC4 switch (settled as far as the project will take it)

What the stock 6.1.1.3 client sends as its login once the stream turns to RC4 is not fully known, and the project will not pursue it further. The handshake is read, a 6.1.1.3-shaped login works end to end in the project's own stack, and the stock client's exact login-argument order is left at a best guess (→ §2.10) [lab] (protocol/v6113-login-lab-method.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled (handshake) | The clear hello `GNP1905C` comes from the connector script; the outgoing stream is clear up to offset 287 and plain RC4 with a 16-byte session key after it; the server's key arrives RSA-wrapped in a clear `0xfc` message. The connector request is a pure function of the build, so a genuine reply stays valid on every later launch | [lab][cap] (protocol/v6113-status.md); [lab] (protocol/v6113-login-lab-method.md) |
| Settled (our stack) | The clean-room client repro builds, verifies and decrypts its own signed `conf.gs` and runs the hello and two-way key exchange; seihai-core's secure login completes against our own server. A working 6.1.1.3-shaped login exists for the project's own client, with the argument order and payload cipher chosen by us | [lab][inf] (protocol/v6113-login-lab-method.md); [lab] (protocol/conf-gs-fuzzing.md) |
| Best guess (stock client) | The stock client's post-RC4 login body is the 6.0x body (→ §2.3.5) under RC4, framed as `EILLLT` bundles: client type, key, the 8-byte token `GNP1905C`, account `str`, password `str`, then the comma-separated machine list. The connector's step names fit this split: `sendLoginNewProtocol` sends the opening and account, `sendPasswordAndIDs` the password and machine list. The same field order is what our server reads from real 4.20r8, 5.x and 6.03r7 logins. Confidence: moderate to high; an extra field added only by the official connector would not have been seen | [inf] (protocol/v6113-login-lab-method.md); [doc] (protocol/connector-script.md); [bin] (protocol/v4x-clients.md#login-packet) |
| Not pursued | Confirming the stock client's exact account and password framing would need either reading its login key out of the protected client (a key-swap shown to be a dead end in the lab) or a capture against the live official service. The project has chosen to do neither, so the best guess stands | [lab] (protocol/conf-gs-fuzzing.md) |
| Verdict | Settled as far as the project will take it: the project's own 6.1.1.3-style login works, and the stock client's exact body is left at the best guess and not chased | [inf] (protocol/v6113-login-lab-method.md) |

### E#20 The 2.31 step on `PLO_SETACTIVELEVEL` (156) (settled)

What the extra routine 2.31 calls after setting the object level on 156 does was open; a static read and two lab runs settled it [bin] (protocol/plo-156-setactivelevel-231.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Earlier guess (wrong) | The step re-binds level-scoped state, such as the gmap neighbour grid, to the new level | [inf] (protocol/unknowns-ledger.md) |
| Settled | The step sends the launch-link start parameters. A 2.31 started with `graal://SERVER/TEXT` sends `TEXT` once, after the first 156 of the session, as `PLI_TRIGGERACTION` (38) named `serverstartparams` with NPC 0 at (0, 0), then forgets it; started without a link, or with `-connect`, it sends nothing. It changes no client state | [bin] (protocol/plo-156-setactivelevel-231.md); [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md) |
| Also measured | On 2.22 and 2.31, 156 with the current level, a neighbour, an empty or an unknown name changes nothing on screen, and later board and prop messages still land; 156 with a gmap name makes both clients ask for the gmap file (`PLI_UPDATEFILE`) | [lab] (live-runs/fuzz-2026-11-19/README.md) |
| Verdict | Verified: static read confirmed by a run with and without a link | [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md) |

### E#21 Whether a compiled gani script (`PLO_GANISCRIPT`, 134) runs (settled)

Whether 4.x to 6.x run a valid compiled GS2 gani script sent in 134 was open, because no lab had sent a real compiled body [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | GServer-v2 answers `PLI_UPDATEGANI` (157) with 134 only when an NPC server runs and the checksum differs; our build sent none, and a forged 134 made 6.03r7 load the gani like a 195 | [lab][srv] (protocol/probe-targets-2026-11-18.md) |
| Settled | The body is a `GCHAR` name length, the gani name and the compiled script; the packet has no checksum field. A valid body compiled by seihai-core runs on 6.03r7, 4.20r8 and 5.24r4: the client fetches the gani (23 and 157), then `onCreated` and `onTimeout` fire. A body with one flipped byte, or an empty script part, fires nothing and crashes nothing | [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md) |
| Verdict | Verified on three builds | [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md) |
| Left over | 5.12 was not run | [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md) |

### E#22 `DEFAULT*` lines in `PLO_LOADGANI` (195) (settled)

What the `DEFAULT*` header lines do when a server sends them in 195 was open; three lab cases settled it for play [lab] (protocol/probe-targets-2026-11-18.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | `DEFAULTHEAD`, `DEFAULTBODY`, `DEFAULTATTR1` to `3`, `DEFAULTSHIELD`, `DEFAULTSWORD`, `DEFAULTHORSE` and `DEFAULTPARAM1` change nothing and fetch no file: for the player's own character on 6.03r7 and 4.20r8 (idle shots pixel-identical to the plain shot), for another player with no head or body set, and for a level NPC showing a character | [lab] (protocol/probe-targets-2026-11-18.md); [lab] (live-runs/fuzz-2026-11-19/README.md) |
| Inferred | They are the gani editor's preview images, kept in the header so the file is self-describing | [inf] (protocol/probe-targets-2026-11-18.md) |
| Verdict | Verified for play on 4.20r8 and 6.03r7, including the headless case where a default would be used; the editor-preview purpose is inferred | [lab] (live-runs/fuzz-2026-11-19/README.md) |
| Left over | A static read of the header parser's `DEFAULT*` cases; 6.1.1.3 and 6.037 | [inf] (protocol/unknowns-ledger.md) |

### E#23 What prop 81 changes in the player list (settled)

What `PLAYERLISTCATEGORY` (prop 81) changes on screen was open; the guess was that it picks the folder a player is listed under. A 5.00r7 lab run with one injected player per value settled it for that build [lab] (protocol/lab-appe-mirae-2026-11-20b.md#the-player-list-folder-that-prop-81-picks-e23).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | In the 5.00r7 built-in list (folders Staff, Buddies, Guild, Normal, Ignore, Offline): no value or 0, 8, 16, 32, 64 lists the player under Normal; 2, 4, 6, 10, 12 count the player in "Players: N online" but show them in no folder on any tab; odd values neither count nor list them | [lab] (protocol/lab-appe-mirae-2026-11-20b.md#the-player-list-folder-that-prop-81-picks-e23) |
| Verdict | Verified for 5.00r7: prop 81 does not pick a folder. Bit 0 hides the player from the count and the list, bits 1 and 2 hide the list entry only, and bits 3 to 6 change nothing visible. The other folders probably come from the staff list (47), the client's buddy and ignore lists and the guild tag | [lab] (protocol/lab-appe-mirae-2026-11-20b.md#the-player-list-folder-that-prop-81-picks-e23); [inf] (protocol/lab-appe-mirae-2026-11-20b.md#the-player-list-folder-that-prop-81-picks-e23) |
| Left over | 6.x draws its list from a script the lab server does not provide, so whether 6.x scripts give the bits the same meaning is not checked | [lab] (protocol/lab-appe-mirae-2026-11-20.md#prop-81-e23-not-settled) |

### E#24 Baddy props 11 and up (settled)

The width and effect of baddy props from 11 up, and whether an unknown id ends the message, were open because probe baddies walk on their own [lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | Linux 6.03r7's baddy-prop reader has cases for ids 0 to 10 only; an id of 11 or more ends the message and the props after it are lost (a mode-9 removal sent after id 11 or 20 never happened) | [bin][lab] (protocol/lab-baddyprops-ganiscript-156-2026-11-19.md) |
| Settled | 4.20r8 and 2.22 behave the same: a silent mode-10 baddy never resumed when ids 11 to 30, as a byte or a string, came before mode 0; `PLI_BADDYPROPS` was the observer | [lab] (live-runs/fuzz-2026-11-19/README.md) |
| Verdict | Verified on three builds. A server must never send a baddy prop above 10 | [lab] (live-runs/fuzz-2026-11-19/README.md) |

### E#25 The 2.22 start-up file checks: 13 against 17 (settled)

Why 2.22 checks 13 files with a full data folder and more with a near-empty one was open; the two runs' file lists set side by side settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#start-up-file-checks-on-222-e25).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | A full folder checks 13 files with id 34; a near-empty folder checks 17 with id 23 | [lab] (live-runs/open-issues-2026-11-19/README.md) |
| Settled | A re-run requested 18 with id 23 and update-checked 13 with id 34. Five files, `idle.gani`, `plisticononline.png`, `plisticonaway.png`, `plisticondnd.png` and `head0.png`, are requested when missing and never update-checked when present; `block.png` is a level file and appears in both | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#start-up-file-checks-on-222-e25) |
| Verdict | Verified: the best guess held, with five such files rather than four | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#start-up-file-checks-on-222-e25) |

### E#102 Tile id to pixel position on pics1 (settled)

Which formula maps a tile id to its place on `pics1.png` had two answers on record; a render test settled it [test] (formats/pics1-tile-layout-render-2026-11-19.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (false) | `col = id % 128`, `row = id / 128` | [file] (formats/tiletypes.txt) |
| Claim B (holds) | `col = (id % 16) + (id // 512) * 16`, `row = (id // 16) % 32`: eight side-by-side blocks of 512 ids, each 16 columns by 32 rows; the Windows 4.04r2 draw path computes it | [file] (client-internals/client-assets.md#tile-sheets); [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-tile-sheet-layout) |
| Settled | Two real `GR-V1.03` levels drawn with a real sheet: Claim B gives coherent rooms with every cell on the sheet; Claim A puts 2660 and 3736 of 4096 cells off the sheet and draws noise. `formats/tiletypes.txt` is corrected | [test] (formats/pics1-tile-layout-render-2026-11-19.md) |
| Verdict | Verified | [test] (formats/pics1-tile-layout-render-2026-11-19.md) |

### E#202 Which message carries GS2 bytecode (settled)

Which message carries a GS2 script body on 4.x and 5.x clients was open: three sources named 131, 197 and 140 [srv] (protocol/packet-ids.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: NPC bytecode is `PLO_NPCBYTECODE` (131) behind `PLO_RAWDATA`. B: 197 "GS2 bytecode" replaces the script prop. C: 197 is `PLO_LOADSCRIPT`, a descriptor list | [srv] (protocol/packet-ids.md); [srv] (protocol/packet-layouts.md) |
| Settled (NPCs) | 131 behind 100 carries a runnable NPC body on 4.20r8, 5.24r4 and 6.03r7: the script fuzz delivered every case that way and the scripts ran | [lab] (protocol/script-fuzz-2026-11-19.md) |
| Settled (classes and weapons) | On 6.x, 197 is the descriptor `type,name,1,key,crc` and 140 carries the body, from the cache or the wire, never inside 197 | [cap] (protocol/gs2-official-bytecode-6113.md#what-this-settles); [bin] (formats/linux-6x-class-cache.md); [lab][cap] (protocol/linux-603-network-gs2.md) |
| Verdict | Verified: two messages for two kinds of object, not three rival claims. Claim B names the class exchange by its first message | [lab] (protocol/script-fuzz-2026-11-19.md) |
| Also measured | 4.20r8 does not honour the 6.x class path as sent: ten 197 and 140 variants with a valid compiled body ran no script and drew no request, while 131 behind 100 runs NPC bodies on the same build | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs2-class-path-on-420r8-e202-leftover) |
| Left over | How 4.20r8 delivers weapon and class scripts, and 4.0x before 4.20r8 | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs2-class-path-on-420r8-e202-leftover) |

### E#204 Writing to GS1 object members (settled)

What writing to a GS1 object member does, and how the members change across builds, was open; a write-and-read-back scene on four builds settled the main part [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs1-member-writes-e204).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The 2.05 rev 2 name-to-id mapping is settled (36 records, 35 spellings); writes and fallbacks were not | [bin] (npc-library/gs1-object-members-205r2.md#parser-binding) |
| Settled | On 2.05, 2.17.1, 2.22 and 2.31, writes to `npcs[k].x`, `npcs[k].y` and `players[0].x` read back and move the object on screen; writes past the end read 0; unknown members such as `zz` and `arrows[0].dy` read 0; `players[0].power` reads 0 | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs1-member-writes-e204) |
| Build change | `npcs[k].dir = 1` does not stick on 2.05 (reads 2) and does from 2.17.1 | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs1-member-writes-e204) |
| Verdict | Verified for the members tested; the best guess held | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs1-member-writes-e204) |
| Left over | The rest of the members, setter side effects beyond position, and 1.39 | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs1-member-writes-e204) |

### E#205 Index of the hare baddy (settled)

The hare baddy is type 5, shared with the frog [file][2.05] (npc-library/gs1-reference-205.md#constants-doc; npc-library/gs1-command-reference-205.md#name-tables).

| Part | Discussion | Source |
| --- | --- | --- |
| Evidence | 2.05 ships `baddyhare.gif`, and the baddy name table has 10 names, 0 to 9 | [file][2.05] (npc-library/gs1-reference-205.md#constants-doc; npc-library/gs1-command-reference-205.md#name-tables) |
| Settled | The 2.22 client draws type 5 with `baddyhare.png` and plays `frog.wav` for it: the hare and the frog are one type | [2.22] (client-internals/baddies-222.md#types-222) |

### E#212 Whether a function-only image skips the top-level pass (settled)

Whether stock clients treat a leading jump to the end as "no top level", and re-run top-level code before every event when an image has some, was open; loopback fixtures settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs2-top-level-pass-e212).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The 19 official bodies are all function-only; a Linux 4.04r2 experiment suggested a top-level re-run | [cap][lab] (protocol/gs2-official-function-only-shape-2026-11-16.md#what-this-does-and-does-not-settle) |
| Settled | On 4.20r8 and 5.12, with bytecode in 131: a script with a top level runs it before `onCreated` and again before every later `onTimeout`; its function-only twin never runs a top level | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs2-top-level-pass-e212) |
| Verdict | Verified on two builds; the best guess held on both counts | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs2-top-level-pass-e212) |
| Left over | 6.03r7, and a handler at instruction 0 | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gs2-top-level-pass-e212) |

### E#301 Frame loop of the 3.x and 4.x clients (settled)

The frame loop of the 3.x and 4.x clients was untimed; a 2026-11 lab settled it [lab] (client-internals/update-cadence-3x-6x.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The 3.x and 4.x tick length and loop driver were unobserved; 5.x and 6.x were timed only from their 50 ms position messages | [wire] (protocol/v5v6-lab-play.md); [doc] (version-profiles/matrix/README.md#acts-timing-movement-and-rules) |
| Static | Windows 4.04r2 has three time notions: elapsed ticks via `GetTickCount`, a GS2 script clock advancing 0.05 per pass, and legacy `timeout` pass counts; the Linux follow-up ties six updater returns to a registered state predicate | [bin][cap] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-clocks); [bin] [cap] (client-internals/linux-420r6-clock-property.md) |
| Settled | 50 ms steps, one render per step, 8 pixels per walk step for every 3.04, 4.04r2, 4.20r6 and 6.03r7 client; 3.x and 4.x slow down when behind, 6.03r7 makes up one step and drops the rest; GS1 `timeout` counts whole steps rounded down on the C++ engine (→ §4.1.7) | [lab][cap] (client-internals/update-cadence-3x-6x.md#measurements) |
| Later | 1.33 to 2.31 and 5.00r7 round a GS1 `timeout` down; 2.22 and 2.31 play one walk frame per step; Linux 6.03r7 GS2 timers round up to 50 ms steps (→ §4.1.8). The `onTimeout` / `onTimeOut` spelling by client is tracked in → App. E#209 | [lab] (live-runs/open-issues-2026-11-14/README.md#2-443-gameplay-rules-timing-and-live-checks); [lab] (client-internals/gs2-vm-quirks-by-version.md#linux-603r7-timer-lab); [inf] (version-profiles/matrix/README.md#what-is-still-unknown) |

### E#303 Two unidentified lists in the blocked-point test (settled)

What fills the two object lists that the 2.05 blocked-point test reads was open; a static read of what adds to each list settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-c.md#the-two-lists-in-the-205-blocked-point-test-e303).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | One list of player-sized boxes with two flags, read only with a "client option" on; one list of 1.5 × 2 boxes with an enabled flag. Best guess: other players, and NPCs or baddies | [bin] (client-internals/decomp-findings-2026-10-25-m/open-questions.tsv) |
| Settled | The 1.5 × 2 list is the level's bombs: only placing a bomb and putting down a carried bomb add to it, each setting the enabled flag. The player-sized list is the level's list of players. The "option" is a temporary flag that a few movement routines set around their own probes and the walking step clears, and the test also needs the client to be online | [bin] (client-internals/static-reads-appendix-e-2026-11-20-c.md#the-two-lists-in-the-205-blocked-point-test-e303) |
| Verdict | Half right: the first list is players, as guessed, but ordinary walking does not test it; the second is bombs, not NPCs or baddies | [bin] (client-internals/static-reads-appendix-e-2026-11-20-c.md#the-two-lists-in-the-205-blocked-point-test-e303) |
| Left over | Which movement routines set the players flag; whether 2.22 and 2.31 keep the same lists | [inf] (client-internals/static-reads-appendix-e-2026-11-20-c.md#the-two-lists-in-the-205-blocked-point-test-e303) |

### E#306 What picks `lift2.wav` for a pull (settled)

Which flag makes a successful pull play `lift2.wav` instead of `lift.wav` was open; a static read of 2.05 settled it [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#pull-sound-e306-205).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | A player flag that was not traced; best guess a heavy-object flag | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| Settled | The choice reads a byte of the object being lifted or pulled, not a player flag: non-zero plays `lift.wav`, zero plays `lift2.wav` | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#pull-sound-e306-205) |
| Verdict | Verified by static read; the earlier note named the wrong owner of the flag | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#pull-sound-e306-205) |
| Left over | What the byte means for each object kind | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#pull-sound-e306-205) |

### E#307 Probe, nudge and step tables of 1.39 (settled)

The numeric movement tables of 1.39 were open; a static read of its constant block settled them [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#139-movement-tables-e307).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Six probes and the blocked-step counter shape were known without numbers; best guess the same tables as 2.05 | [1.39] (version-profiles/matrix/rules-139.md#wall--walk-test-bin-lab); [inf] (client-internals/first-graal-movement-2026-11-09.md#verification-and-limits) |
| Settled | 1.39 keeps 1st Graal's inner probe points (x 0.6, 1.4, 1.6, 2.4; y 1.1, 1.9, 2.1, 2.9) and its ±0.125 nudge, but uses 2.05's edge lines (y 1.0 and 3.0, x 0.5 and 2.5); points 4 and 5 (2.525, 0.475, 3.025, 0.975) and the half-tile step are the same in all three builds | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#139-movement-tables-e307) |
| Verdict | The guess was wrong: 1.39 is between 1st Graal and 2.05. 2.05 moves the inner points 0.075 outwards and makes the nudge 0.1. The 0.125 nudge agrees with the live 1.39 run | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#139-movement-tables-e307); [live][1.39] (client-internals/player-mannerisms-live.md#notes-per-build) |
| Left over | The 1.39 refusal and snap branches were not compared instruction by instruction | [inf] (client-internals/static-reads-appendix-e-2026-11-20-b.md#139-movement-tables-e307) |

### E#309 Knockback distance of 1.39 (settled)

Whether 1.39 knocks a hurt player back four or five tiles was open between a code read and one offline video; an online run on open ground settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#knockback-on-139-e309).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: one tile per tick while the hurt counter runs 39 down to 35, five steps. B: four tiles on the offline touch-NPC test | [1.39] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin); [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table) |
| Settled | On 1.39 a hurt message on open ground moved the player five tiles east (3 runs), south and north | [lab] (protocol/lab-appe-mirae-2026-11-20.md#knockback-on-139-e309) |
| Verdict | Verified: Claim A holds; the four-tile reading lost a step | [lab] (protocol/lab-appe-mirae-2026-11-20.md#knockback-on-139-e309) |

### E#310 Where the once-per-second hit stamp sits (settled)

Which hit paths share the per-attacker once-per-second stamp was open between two reads; a two-client lab on 2.05 settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#once-per-second-hit-stamp-on-205-e310).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the sword and both hit messages share the stamp, stored before the guild test. B: in 2.00 to 2.05 rev 2 the stamp is on the hurt-message path only | [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets); [2.00][2.05] (client-internals/combat-200-204.md#what-changes-by-build) |
| Settled | On 2.05 rev 2 a guild-rejected hurt message blocks a clean one from the same attacker in the same second, so that path stores the stamp before the guild test; a real swing is not blocked by that stamp and stores none of its own | [lab] (protocol/lab-appe-mirae-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |
| Verdict | Verified on 2.05 rev 2: Claim B holds | [lab] (protocol/lab-appe-mirae-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |
| Left over | 2.22, which Claim A also covers | [lab] (protocol/lab-appe-mirae-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |

### E#313 Do arrows and fireballs pass walls (settled)

Whether arrows and fireballs fly through walls in 2.05 was open from a code read; a lab shot at a wall settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | In the 2.05 shot flow, types 0 and 1 skip the blocking test that stops types 2 and 3 | [2.05] (client-internals/damage-sources.md#open) |
| Settled | On 2.05 rev 2 an arrow (type 0) and a fireball (type 1) cross a wall row and keep going; types 2 to 4 burst on the wall | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313) |
| Verdict | Verified: the code read holds | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313) |

### E#314 Gmap entry and the respawn save (settled)

Whether entering a gmap from outside saves the respawn point was open; a 2.22 lab run settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gmap-entry-on-222-e314-e13).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The order of the gmap's level list against the entry save decides it, and neither was read | [2.05] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv) |
| Settled | On 2.22, a player who walks into a 2 x 2 gmap from a plain level and then dies is sent back to the gmap entry point, not the start level | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gmap-entry-on-222-e314-e13) |
| Verdict | Verified on 2.22, and on 2.17.1 for a death in the first cell; the best guess held | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gmap-entry-on-222-e314-e13) |
| Also measured | A death after crossing a seam inside the gmap also returns to the entry point, so a seam crossing saves nothing new; 2.17.1 asks for the same entry point after a death | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#gmap-entry-on-222-e314-e13) |

### E#315 The level-entry save in the 2.1 test builds (settled)

How the 2.1 test builds save the entry point was open; a static read of their entry decision settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#level-entry-save-in-the-21-test-builds-e315).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The builds lack the name-group delimiter constant; best guess every level entry saves | [bin][inf] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test) |
| Settled | 2.1 test 2 and 3 run 2.17.1's rule: save at login or when the product of the two levels' gmap-list indices is negative, otherwise do not save; no group test; no gmap gives −1 for both | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#level-entry-save-in-the-21-test-builds-e315) |
| Verdict | The guess was wrong; ordinary level changes keep the old respawn point | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#level-entry-save-in-the-21-test-builds-e315) |
| Left over | NewWorld beta 2, which also lacks the constant, was not read | [inf] (client-internals/static-reads-appendix-e-2026-11-20-b.md#level-entry-save-in-the-21-test-builds-e315) |

### E#316 Glove power steps (settled)

Which objects each glove power can lift was open between two reads; a lab run with the power set through the props settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#glove-power-on-205-e316).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: glove 1 lifts bush, sign and pot; `glove1` adds the light stone and `glove2` the black stone. B: a bare hand lifts the first two entries, power 1 adds the pot, power 2 the light and black stones together | [2.05][srv] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table); [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#lift-a-key) |
| Settled | On 2.05 rev 2, glove power N lifts the first N + 2 entries of the lift list: 0 bush and sign, 1 adds the pot, 2 the light stone, 3 the black stone. The first object out of reach only plays the grab gani | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#glove-power-on-205-e316) |
| Verdict | Verified: Claim A's steps hold, and Claim B is right that a bare hand lifts bush and sign but wrong that power 2 adds both stones | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#glove-power-on-205-e316) |

### E#318 Level reload on re-entry offline (settled)

Whether offline 2.05 reloads a level on re-entry, bringing a cut bush back, was untested [bin] (client-internals/board-respawn.md#open).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | No reload: 2.05 rev 2 keeps the edited level in memory for the session, so cut and thrown bushes stay gone after leaving and re-entering (3 of 3) and after loading the level again (2 of 2); the files on disk are unchanged | [lab] (client-internals/lab-cells-200-205-2026-11-13.md#205-rev2-offline-re-entering-a-level) |
| Still open nearby | Whether a level NPC's GS2 state survives leaving and re-entering a gmap cell on 6.03r7 and 5.12; Seihai restarts it | [doc] (protocol/npc-gmap-reentry-status.md) |

### E#321 The 2.31 window blacklist (settled)

Which windows 2.31's blacklist names and what the client does on a match was open; a static read decoded the list and the reaction [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#the-231-window-blacklist-e321).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | An obfuscated list of window titles and classes compared every 3.2 s; best guess the period's memory editors and speed hacks, with a quit or a report on a match | [bin] (client-internals/feature-specs/README.md#settled-index-cross-cutting-items-status-as-of-the-lab-batch-c-2026-10-24) |
| Settled | A third-party Delphi anti-debugging component with all four of its switches on. It looks for 20 tool names anywhere in each window title (case-sensitive): ExeSpy, wxr95, Regmon, File Monitor, RegMonEx, Window Detective, DebugView, ResSpy, Advanced Registry Tracer, regsnap, MEMSPY, Memory Doctor, ProcDump32, Memory Editor, FrogsICE, SMU Winspector, Memory Dumper, MemoryMonitor, DeDe and OpenTrap. On a match it posts a quit message to that window and ends the client; it sends nothing to the server | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#the-231-window-blacklist-e321) |
| Verdict | The reaction guess was half right (a quit, no report); the list holds monitors, dumpers and decompilers, not game trainers or speed hacks | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#the-231-window-blacklist-e321) |
| Left over | A lab run with one listed window open, to watch the quit | [inf] (client-internals/static-reads-appendix-e-2026-11-20.md#the-231-window-blacklist-e321) |

### E#322 How others see a key emote (settled)

How other players see a Ctrl+letter emote was open, because captures showed AFK images re-sent while the 2.05 code draws the emote locally; a lab run on a script-free server settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#key-emote-on-205-e322).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Captures show `PLI_SHOWIMG` frames re-sending an AFK image about every 3 s | [2.05][cap] (client-internals/feature-specs/11-emotes-ganis.md#b-emotes) |
| Settled | On 2.05 rev 2, Ctrl+A draws the AFK bubble locally and sends only one file check (34) for its image, once per session; Ctrl+S and Ctrl+D likewise; no `PLI_SHOWIMG` and no props leave the client, so the server has nothing to relay | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#key-emote-on-205-e322) |
| Verdict | Verified: others do not see a key emote; the captured AFK frames came from a server script | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#key-emote-on-205-e322) |

### E#327 Missing chest art and menu skin in the 6.03r7 item run (settled)

Why the script-free Linux 6.03r7 run drew no chest art, and why the menu showed an orange rectangle, was open; controlled input changes settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#603r7-chest-art-and-menu-e327).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Chest collision and opening worked without chest art; an orange rectangle appeared when the menu toggled | [shot][inf] (client-internals/items-603r7-black-box.md#signs-and-chests) |
| Settled (chest) | With `chest.png` and `chestopen.png` on the server, the client fetches the first at level entry and the second on opening, and draws both | [lab] (protocol/lab-appe-mirae-2026-11-20.md#603r7-chest-art-and-menu-e327) |
| Settled (menu) | The image names no skin or window image, and the client fetches no file when the menu toggles: the orange box is the default unskinned GUI drawing, and a skin can only come from a server script | [lab] (protocol/lab-appe-mirae-2026-11-20.md#603r7-chest-art-and-menu-e327) |
| Verdict | Verified; the best guess held | [lab] (protocol/lab-appe-mirae-2026-11-20.md#603r7-chest-art-and-menu-e327) |
| Left over | A scripted skin delivered and seen to change the menu | [lab] (protocol/lab-appe-mirae-2026-11-20.md#603r7-chest-art-and-menu-e327) |

### E#328 What drives 2.22's tick (settled)

Whether 2.22's game step runs from a 50 ms multimedia timer or from the idle handler behind a 50 ms gate was open; a static read of the timer's creation settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Claim A: a multimedia timer of 50 ms, resolution 10. Claim B: no form timer, the idle handler behind a 50 ms gate. A 2026-11-19 read found no multimedia-timer import | [bin] (client-internals/rebuild-traces-2026-11-05.md#222); [bin] (version-profiles/matrix/builds-static-survey.tsv); [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#tick-source-e328-222) |
| Settled | 2.22 creates the DelphiX timer component in code, with interval 50 ms and maximum lag 10, bound to the game step. The component runs from the application's idle event: when 50 ms have passed by `timeGetTime` it resets its start to the current time and calls the step once, so late steps are not made up. 2.05 rev 2 creates it the same way | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |
| Verdict | Claim B is the mechanism; Claim A's "resolution 10" is the component's lag count, not a multimedia timer | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |
| Left over | Nothing for the tick; the tick is 50 ms either way, so no duration in the manual changes | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#what-drives-the-222-tick-e328) |

### E#405 RC token `GSERV025` (settled)

Which RC builds send `GSERV025` was open while only the earlier RC builds had been read [bin] (protocol/rc2-sessions-stock-2026-11-16.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The server knows `GSERV023` to `GSERV025`; the first RC builds read send `GSERV007` to `GSERV024` | [srv] (protocol/chat-pm-rc.md#admin-and-staff); [bin] (tools/remotecontrol-lineage.md#builds) |
| Settled | RC2 2.05, RC3 and the 2006-01-20 Linux RC send `GSERV025`; the 2005-12-09 Linux RC and the 2004 RC (login type 6) send `GSERV024`. The token changed between December 2005 and January 2006 | [bin] (protocol/rc2-sessions-stock-2026-11-16.md); [bin] (tools/remotecontrol.md#logins-bin); [lab] (protocol/rc-fuzz-2026-11-19.md) |
| Verdict | Verified for every held official RC build. A server should accept both tokens | [bin] (protocol/rc2-sessions-stock-2026-11-16.md) |
| Left over | The 2014 "custom" RC is a player modification of an official RC and the second RC3 build is catalogued only; neither is expected to change the answer | [inf] (tools/remotecontrol-lineage.md) |

### E#420 Flag and chest counts in the RC props tail (settled)

Which of the two counts in the RC props tail counts flags and which opened chests was open, because both were 0 in the only capture; four controlled accounts settled it for the fork's writer [lab] (protocol/lab-appe-mirae-2026-11-20.md#rc-props-tail-counts-e420).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The tail after the props block in 72 and 76 holds two `s` counts, then the weapons | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| Settled | The first count is flags (then the flag strings, newest first), the second opened chests (each `c` length + 2, `c` x, `c` y, level name), then the weapon count and names, and nothing after | [lab] (protocol/lab-appe-mirae-2026-11-20.md#rc-props-tail-counts-e420) |
| Verdict | Verified against the GServer-v2 fork with RC 2004; the best guess held. No original 2001–2004 server was run | [lab] (protocol/lab-appe-mirae-2026-11-20.md#rc-props-tail-counts-e420) |

### E#421 The last byte of RC_PLAYERPROPSSET2 (settled)

What the extra byte the 2004 RC puts at the end of 76 means was open; a static read of the RC's 76 builder and 72 parser settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#the-last-byte-of-rc-76-e421).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | One byte after the weapons, 0 in the only capture; best guess a dialog option | [cap] (protocol/rc-props-flags-status.md) |
| Settled | It is the length byte of an empty string. The RC keeps one optional length-prefixed string that may follow the weapon list in the server's 72, never edits it, and writes it back at the end of 76. The GServer-v2 72 has no such string, so the RC sends it empty | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#the-last-byte-of-rc-76-e421) |
| Verdict | The guess was wrong; it is an echoed field, not a dialog option | [bin] (client-internals/static-reads-appendix-e-2026-11-20-b.md#the-last-byte-of-rc-76-e421) |
| Left over | What an older server put in that string | [inf] (client-internals/static-reads-appendix-e-2026-11-20-b.md#the-last-byte-of-rc-76-e421) |

### E#500 Back clipping plane of the Graal3D client (settled)

Which back clipping plane the Graal3D client uses was open; a static re-read settled it at 5000 [bin] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The Direct3D retained-mode library's initial back plane is 100, and the February 2000 client sets none of its own | [doc] (graal3d/camera.md#field-of-view) |
| Claim B | A later public DelphiX fork calls `SetBack(5000)` during retained-mode init | [doc] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13) |
| Settled | The February 2000 exe calls `SetBack(5000)` right after `CreateViewport`, its only constant `SetBack`; Claim A's 100 is overridden | [bin] (graal3d/camera.md#back-clipping-plane-re-read-2026-11-13) |
| Left over | The value at draw time in a live run with the native `d3drm.dll` | [inf] (graal3d/camera.md#still-needed) |

### E#501 Class CRC of the 4.04r2 3D plug-in (settled)

Which class CRC a real 4.04r2 client sends in its 3D connect request was open between a stock-Torque reading and a static-table reading; a decoded capture settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#404r2-3d-connect-request-e501).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the stock Torque class CRC, so a server must match the networked classes. B: a static table holding `0xFFFFFFFF` for group 0, computed by nothing | [bin] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll); [bin] (torque/wire-by-build.md#the-handshake-per-build) |
| Settled | The connect request of native Linux 4.04r2 (`G3D19026`), decoded from a lab capture, carries net class group 0 and class CRC `0xFFFFFFFF` | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#404r2-3d-connect-request-e501) |
| Verdict | Verified for the Linux build: Claim B holds. Windows 4.04r2 page-faults at the 3D start under Wine, so it was not captured | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#404r2-3d-connect-request-e501) |

### E#600 Tile layer as GraalEditor writes it (settled)

Whether GraalEditor writes `BOARD` as decimal tile indices or as base64 runs was open; the text writer settles it [bin] (tools/graaleditor-board-format-2026-11-16.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (false) | GraalEditor 2.3.1.1 writes `BOARD 0` as 64 lines of 64 decimal tile indices | [bin] (tools/graaleditor-board-format-2026-11-16.md) |
| Claim B (holds) | The writer matches the 2.05 and 2.22 built-in base64 `BOARD` rows, emits GLEVNW01-style runs and skips all-zero rows | [bin][2.22] (tools/graaleditor-board-format-2026-11-16.md) |
| Left over | An optional file-level confirmation from a Save As `.nw` when a desktop is available | [lab] (tools/graaleditor-board-format-2026-11-16.md#open) |

### E#601 Whether link arrival offsets are evaluated (settled)

Whether the client evaluates an offset in a link's arrival field, such as `playery+10`, was open between the editors' verbatim storage and the level authors' usage; a lab link settled it [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#link-arrival-offsets-on-222-e601).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: arrival fields may hold `playerx` or `playery` plus an offset, and 21 archived arrivals do. B: the editors store the text verbatim | [2.22] (tools/level-editor/222-reference.md#8-links); [2.22] (tools/level-editor/formats-crossref.md#batch-f-decomp-findings-2026-10-25-f-pr-39) |
| Settled | On 2.22 a link with arrival `playerx playery+10`, entered at y about 20, sent the player to (30, 30); a plain `30 40` control arrived at (30, 40). The client evaluates the expression; the editors only store it | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#link-arrival-offsets-on-222-e601) |
| Verdict | Verified on 2.22; both claims hold, at different stages | [lab] (protocol/lab-appe-gwentea2-2026-11-20.md#link-arrival-offsets-on-222-e601) |

### E#602 Code width of `Z3-V1` boards (settled)

How many bits a board code uses in `Z3-V1.02` was disputed between the server source and the client readers; a check of every client's magic list settled why both are right [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#z3-v102-in-the-graal-clients-e602).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Claim A: `.02` uses 11-bit codes, `.03` and `.04` use 12. Claim B: the 2.05 and 2.31 readers use 12 bits for both versions they handle. Best guess: both right, since no Graal client reads `.02` | [srv] (formats/level-binary.md#z3-v1-differences); [2.05][2.31] (formats/level-binary-client.md) |
| Settled | Every Windows client exe held from 1st Graal to 6.00r4 lists only `Z3-V1.03` and `Z3-V1.04`; none holds `Z3-V1.02` | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#z3-v102-in-the-graal-clients-e602) |
| Verdict | Verified: no Graal client reads `.02`, so the 12-bit readers never meet an 11-bit board | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#z3-v102-in-the-graal-clients-e602) |
| Left over | The 11-bit width rests on the server source alone; a real `.02` file decoded both ways would confirm it | [inf] (docs/book/04-where-the-notes-disagree.md#how-many-bits-a-z3-code-uses) |

### E#603 Whole tiles and fractions in level records (settled for 2.05 and 4.04r2)

Which binary level-record fields hold whole tiles and which take fractions was disputed; a static read of the 2.05 reader, beside the earlier 4.04r2 read, settled it for both builds [bin] (client-internals/static-reads-appendix-e-2026-11-20-c.md#whole-tiles-and-fractions-in-205-binary-level-records-e603).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Claim A: coordinates are whole tiles. Claim B: link numbers can be halves such as `43.5`. Best guess: link boxes fractional, every other position whole | [srv] (formats/level-binary.md#records); [srv] (formats/level-binary.md#z3-v1-differences); [inf] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-binary-level-records) |
| Settled | 2.05 parses a link's x, y, width and height as numbers and rounds each to a whole tile; arrivals stay text expressions; baddy (raw byte), NPC, chest and sign (byte − 32) positions are whole. 4.04r2 keeps link boxes as floating point and the other positions whole | [bin] (client-internals/static-reads-appendix-e-2026-11-20-c.md#whole-tiles-and-fractions-in-205-binary-level-records-e603); [bin][file] (client-internals/windows-404r2-500r7-static-2026-11-09.md#404r2-binary-level-records) |
| Verdict | Build-dependent: the best guess holds for 4.04r2; in 2.05 a fractional link box is rounded, so both claims are right for different builds | [bin] (client-internals/static-reads-appendix-e-2026-11-20-c.md#whole-tiles-and-fractions-in-205-binary-level-records-e603) |
| Left over | 2.22 and 2.31, which were not read for this field | [inf] (client-internals/static-reads-appendix-e-2026-11-20-c.md#whole-tiles-and-fractions-in-205-binary-level-records-e603) |

### E#604 Where a binary sign list ends (settled)

Where the sign list in a binary level ends when a `HEIGHTS` block may follow was open, with one read saying 2.05 reads to the end of the file; a 2.05 lab settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#sign-list-end-on-205-e604).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: 2.05 reads signs to the end of the file, and 2.31 stops at the first empty line. B: the sign section runs to an empty line or the end of the file | [2.05][2.31] (formats/level-binary-client.md#agreement-with-level-binarymd); [srv] (formats/level-binary.md#layout) |
| Settled | On 2.05 rev 2 a level with three signs shows all three; with an empty line after the first, or an empty line and a `HEIGHTS` line, only the first shows | [lab] (protocol/lab-appe-mirae-2026-11-20.md#sign-list-end-on-205-e604) |
| Verdict | Verified for 2.05: Claim B holds and Claim A is wrong about 2.05, which stops at the first empty line as 2.31 does | [lab] (protocol/lab-appe-mirae-2026-11-20.md#sign-list-end-on-205-e604) |
| Settled (2.31) | A 2.31 run of the same files keeps 1 sign of 3 after an empty line, with or without a `HEIGHTS` line, so the 2.05 and 2.31 readers agree | [lab] (protocol/lab-appe-mirae-2026-11-20b.md#where-a-binary-sign-list-ends-on-231-e604) |

### E#605 Client listserver frames in two vocabularies (settled)

Whether two descriptions of the client's listserver frames describe the same bytes was open, because they use different words [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | 2.00 and 2.05 send id 0 and `newmain` in one plain zlib frame; 2.17 adds id 1 with account and password; 2.22 and 2.31 send id 7, a key byte, `GNW30123` and `newmain`, then a generation-5 frame with id 1 | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Claim B | The classic Server Lister ELF reads an edition line (id 0) and an account line (id 1) and ignores any other line; no version token, no cipher | [bin] (tools/classic-tools/serverlist3.md) |
| Settled | The two describe one layout. Both use a big-endian 16-bit length, a zlib body and newline-separated lines whose first byte is the id plus 32. The edition line is the `newmain` line (the ELF selects rows whose edition contains that text), and the account line is 2.17's id 1. The ELF ignores 2.22's id 7 line, so "no version token" and `GNW30123` describe two listserver generations, not a disagreement about one frame | [bin] (tools/classic-tools/serverlist3.md); [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Verdict | Settled by matching the two field layouts against held captures; inferred, not measured, in the sense that no single capture was replayed into the Server Lister ELF | [inf] (docs/book/04-where-the-notes-disagree.md#listserver-shapes) |

### E#606 Whether a gmap carries `HEIGHTS` blocks (settled)

Whether gmaps hold per-level `HEIGHTS` blocks as well as the coarse `HEIGHTMAP`, beyond the builds already read, was open; a read of the gmap parser in each engine component settled it [bin] (formats/gmap-heights-by-component-2026-11-19.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Windows 4.04r2 and four Mac PowerPC builds read both forms; the best guess was that every 4.x and later gmap reader does | [bin][file] (formats/gmap-heights-404r2.md); [bin] (formats/gmap-heights-mac-ppc.md#the-reader-in-all-four-builds) |
| Settled | Support follows the engine component, not the version. The Linux 2D engine library, one identical file in 4.04r2 to 5.12, reads only the level-name grid and has no `HEIGHTMAP` or `HEIGHTS` section. The 3D components (Windows `GraalEngine.dll` and `Graal3DEngine.dll` in 4.20r8 and 5.00r7, the Linux 4.20r6 3D binary) and the merged 6.03r7 client read both. 6.03r7 also adds `NOAUTOMAPPING` and `MINIMAPIMG` | [bin] (formats/gmap-heights-by-component-2026-11-19.md) |
| Verdict | Verified at the token level: whether each parser has the section, not how each stores it. The best guess was wrong | [bin] (formats/gmap-heights-by-component-2026-11-19.md) |
| Left over | Rendering, server support and the salvage author's intent | [bin][file] (formats/gmap-heights-404r2.md#correction-and-limits) |

### E#607 Leftover lines in the protocol cheat sheet (settled)

Whether the lines an old protocol cheat sheet still prints are wrong was open as a bookkeeping item [doc] (protocol/PROTOCOL-CHEATSHEET.md).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (false) | A raw byte after the version, unscrambled RC clients, 100 to 102 as file length, tiles and file blob, 1,024-byte frame slices, and ids 1, 16 and 32 for login, level request and player update | [doc] (protocol/PROTOCOL-CHEATSHEET.md); [doc] (protocol/login-recovery-start.md) |
| Claim B (holds) | No mystery byte (the extra byte is the generation-3 insertion); RC is ciphered like a client of its generation; 100, 101 and 102 are raw data, board and file; no slice size; login type 0, level request id 0, walk id 2 | [doc] (protocol/login-and-walk.md); [doc] (protocol/codec-and-framing.md) |
| Settled | The probe proxy, written to Claim B's rules, decodes and re-encodes live sessions of real 2.05 rev 2 and 2.17.1 (generation 3), 2.22, 2.31 and 4.x to 6.x (generation 5) and the 2004 RC (login type 6, generation 5) without loss; a 1,024-byte slice or a raw version byte would break every one of those sessions at the first frame | [lab] (protocol/unknowns-ledger.md); [lab] (protocol/rc-fuzz-2026-11-19.md); [lab] (protocol/fuzz-4x-5x-win-2026-11-19.md) |
| Verdict | Verified for the framing, cipher and RC lines by live sessions; the 100 to 102 names and the facing order follow the server source and the manual | [lab] (protocol/unknowns-ledger.md) |

### E#608 How many `arrays.dat` lists make a tile passable (settled)

How many `arrays.dat` lists decide whether a tile is walkable was open between a summary and a code read; a static read of the consumer settled it for 2.05 [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the first array supplies passable tiles and all others are walls. B: the old-mode 2.05 path checks arrays 0 and 1 | [doc] (CONSOLIDATED.md#tiles); [2.05] (formats/arrays-and-signatures.md#arraysdat) |
| Settled | The loader reads 25 lists; the old-mode passability test checks list 0 and, on a miss, list 1, and no other | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205) |
| Verdict | Verified by static read: Claim B holds; Claim A dropped list 1 | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#arraysdat-lists-in-the-old-mode-walk-test-e608-205) |

### E#609 macOS archive labels and application identity (settled)

Whether the Mac uploads labelled 3.04 and 3.15r2 are the historical 3.153 image was open, because the earlier comparison gave no digest to match [bin] (version-profiles/macos-client-compatibility.md#archive-labels-and-the-historical-3153-claim).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The newer collection's two v3-labelled main executables share one PowerPC digest; the earlier note said both are 3.153 but gave no digest | [bin] (version-profiles/macos-client-compatibility.md) |
| Settled | The executable studied and run as 3.153 has a SHA-256 beginning `6eb0a1f9` and an MD5 beginning `3930f663`; the "3.15r2" setup image's `readme.txt` gives version 3.153 and its token is `G3D28015`; the owner-held `MAC-CLIENTS` inventory records that same digest for both v3-labelled images. So both labels carry the 3.153 executable | [bin][lab] (version-profiles/lab-mac-ppc-315-512-flags-2026-11-14.md); [lab] (version-profiles/lab-mac-tiger-2026-10-31.md); [bin] (npc-library/gs1-commands-by-version.md) |
| Verdict | Verified by digest (prefix and suffix compared; the full digest is owner-held) | [bin] (version-profiles/lab-mac-ppc-315-512-flags-2026-11-14.md) |

### E#614 Tiledef type 4 consumer (settled)

What a type-4 tiledef line does was open: such lines are common in 2.22 install tiledefs, but the walk-kind switch names only 0, 1|2 and 5. A live 2.22 run settled it [lab] (formats/tiledef-type4-2026-11-16.md#live-result-2026-11-19).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A (holds) | Install type-4 rows store pixel x offsets (and sometimes y) beside a replacement image and a level prefix | [file][bin] (formats/tiledef-type4-2026-11-16.md) |
| Claim B (holds) | Walk kinds for tilesets are 0, 1\|2 and 5; type 4 is not among them | [2.22] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md) |
| Settled | Draw only: type 4 pastes its image into the tile sheet at pixel (x, y) and leaves the stock sheet elsewhere; walking follows the board's tile codes, so a rock row blocks the same with or without the overlay. The image must be an 8-bit palette PNG; a 24-bit one is ignored without a message, which is why the earlier tries saw nothing | [lab] (formats/tiledef-type4-2026-11-16.md#live-result-2026-11-19) |
| Left over | Water under an overlay, and type-4 lines on builds other than 2.22 | [inf] (formats/tiledef-type4-2026-11-16.md#open) |

### E#617 Whether 1.41 rev 1 loads `.nw` levels online (settled)

Whether a real 1.41 rev 1 loads a `.nw` level sent by a server, and what it does with a gmap, was open; a loopback lab settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#nw-and-gmaps-on-141-rev-1-e617).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The build carries the `GLEVNW01` loader string and no `GRMAP001`; no run had loaded a `.nw` level | [bin] (client-internals/141r1-nw-gmap-status.md#settled-from-the-catalogue) |
| Settled | 1.41 rev 1 drew and walked a `.nw` start level sent as name, board and modtime. Given a gmap start level, the server sends it a plain warp and the first cell as an ordinary level; the client never asks for the `.gmap` and plays the cell as a normal level | [lab] (protocol/lab-appe-mirae-2026-11-20.md#nw-and-gmaps-on-141-rev-1-e617) |
| Verdict | Verified; the best guess held | [lab] (protocol/lab-appe-mirae-2026-11-20.md#nw-and-gmaps-on-141-rev-1-e617) |
| Left over | Link and height messages for a `.nw` level, which the lab server did not send, and walking a seam | [lab] (protocol/lab-appe-mirae-2026-11-20.md#nw-and-gmaps-on-141-rev-1-e617) |

### E#619 Whether 5.30r3 and 5.31r4 use their built-in login host (settled)

Whether 5.30r3 and 5.31r4 ever dial their stored default login host was open; a lab run per licence case settled it [lab] (protocol/lab-appe-mirae-2026-11-20.md#built-in-login-host-of-530r3-and-531r4-e619).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The host and port sit side by side in both images; the 5.x notes say the host normally comes from `license.graal`; best guess a fallback | [bin] (protocol/client-string-fingerprints-3x-6x.md#what-the-table-shows) |
| Settled | With no licence, a signed one, a garbage one, an edited one or a plain one at the root, both builds always dialled the first built-in login host on 14900 and never the licence's address; with no answer they moved to the second built-in host. The unpacked 5.30r3 has no `license.graal` string | [lab] (protocol/lab-appe-mirae-2026-11-20.md#built-in-login-host-of-530r3-and-531r4-e619) |
| Verdict | Verified; the best guess was wrong: the built-in list is the only source, not a fallback | [lab] (protocol/lab-appe-mirae-2026-11-20.md#built-in-login-host-of-530r3-and-531r4-e619) |

### E#620 What the 1.41 rev 1 program-check handler does (settled)

What the program-check handler of 1.41 rev 1 does, and why one copy skips it, was open; a static read settled it [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#program-check-e620-141-rev-1).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | The handler builds text values and calls helpers whose effects were not identified | [bin] (client-internals/early-windows-callback-variants.md#the-new-141-rev-1-result) |
| Settled | The handler is the stock Delphi TProgramCheck 1.1 self-integrity component: on a failed check it says the program "has been modified either by a virus or by a transfer problem", that the Graal executable is corrupted, and ends the client | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#program-check-e620-141-rev-1) |
| Inferred | The component warns that an active check "not processed by stamp.exe" has nothing to compare against; the copy bound to the final return fits a build that was not stamped | [bin][inf] (client-internals/static-reads-appendix-e-2026-11-19.md#program-check-e620-141-rev-1) |
| Verdict | Verified for what the handler does; why the copies differ is inferred | [bin] (client-internals/static-reads-appendix-e-2026-11-19.md#program-check-e620-141-rev-1) |
