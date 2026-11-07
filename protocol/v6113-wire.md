# Windows 6.1.1.3 has no wire of its own

Date: 2026-11-07. Static read. Nothing was run. Tags: **[bin]** this image · **[bin]** the neighbour notes cited below · **[cap]** the Windows captures those notes already record.

`client-internals/engine-6113.md` identifies the file. It is the `QPlay.exe` packer stub. This page is what that means for login, framing, packet ids, property streams and file transfer, and where `protocol/v6x-clients.md` and `protocol/v5v6-windows-unpacked.md` disagree. 6.00r2, 6.00r4, 6.01r1, 6.03r7 and the 6.00 betas are used only as that diff. No 6.113 behaviour below is invented from them.

## What 6.113 cannot show

The listing has no login builder, no version token, no key byte, no compression or cipher constant, no PLO or PLI switch, no property parser, and no file-cache magic. A search finds no `G3D` string, no `GRESCR01`, no `.code`, no `creationtime.dat`, no `basepackage`, no `setprotocol`, no `setindatahandlers`, and no `onSend` event. The CyaSSL, AES-CBC, ARC4, HMAC and zlib names are the export directory in `engine-6113.md`. Their bodies are not the library, and nothing in the recovered stub calls them from a socket. They are not a game cipher and not the 6.11 connector. **[bin]**

## Login, token, key, framing

Neighbours, not this file:

| Build | Token | Platform field | Where |
| --- | --- | --- | --- |
| 6.00 beta1 | `G3D03048` | `win` | Windows capture |
| 6.00 beta2 | `G3D15010`, same as 5.24r3 and 5.24r4 | `win` | Windows capture |
| 6.00r2 and 6.00r4 | `G3D26090`, same as 5.30r3 and 5.31r4 | `win` | Windows capture |
| 6.01r1 Linux | `G3D0108A` | `linux` | Linux binary |
| 6.03r7 Windows | `G3D0311C` | `win` | Windows capture |
| 6.03r7 Linux | `G3D0511C` | `linux` | Linux binary |
| 6.11 Mac | chosen by the connector script | — | Mac binary |
| 6.1.1.3 Windows | none in the image | none in the image | this listing |

**[cap]** (`protocol/v5v6-windows-unpacked.md#tokens`) **[bin]** (`protocol/v6x-clients.md#login-message-601-and-603`)

Do not stamp 6.113 with `G3D26090` or with either 6.03 token. The fixed version is 6.1.1.3 and the publisher and year match Mac 6.11 more closely than they match 6.00, and Mac 6.11 does not use a compiled-in token. This Windows file does not contain the connector either, so it does not show a replacement. **[bin]**

The Windows captures, including 6.00r2, 6.00r4 and 6.03r7, log in as guest in a gen-5 login frame: a 16-bit length, zlib, no cipher, no compression byte. The body is id 5, then the key as a GCHAR (the wire byte minus 32 is the cipher key, and the wire byte can sit above the 7-bit range), then the 8-character token, then account and password lengths, then the platform list. Id 37 follows. **[cap]** (`protocol/v5v6-windows-unpacked.md#login-message`)

The Linux note describes the same id 5 for 6.01 and 6.03, in a mode-3 frame (zlib, no cipher, no type byte), and then id 37. It calls the first field the key byte, the random value kept to 7 bits, not a GCHAR. See the contradictions below. **[bin]** (`protocol/v6x-clients.md#login-message-601-and-603`, `protocol/v6x-clients.md#cipher-and-framing-classic-mode`)

After login, both notes describe gen-5 framing for 6.00 through 6.03: the shared seed and the Borland multiplier, type 2 raw, type 4 zlib, type 6 bzip2, a short XOR, then mode 0. A frame that does not fit in 16 bits is a sentinel length plus a 4-byte length. Packets are still id plus 32, body, newline. 6.11 can leave that path when a script calls `setprotocol`. 6.113 shows none of these constants. **[bin][cap]**

## PLO and PLI

6.113 has no receive switch and no send method.

The Windows unpacked switch counts, which include the property messages 2, 3, 8 and 9: **[bin]** (`protocol/v5v6-windows-unpacked.md#server--client-ids`)

| Builds | S→C ids in the switch | Change from the previous row |
| --- | --- | --- |
| 6.00 beta1 and beta2 (with 5.24) | 97 | against 5.12: drops 75, 132, 133, 171, 193; adds 109 and 198 |
| 6.00r2 and 6.00r4 | 93 | against 5.31: drops 165 and 169. 41 and 181 are already gone |
| 6.03r7 | 92 | against 6.00r4: drops 175 and 184; adds 111 |

Linux 6.03's switch list matches that Windows 6.03 list. Linux 6.01 is that list without 111. The Linux note also says both Linux builds take 100 and 108 before the switch, so the switch count is short by two. The Windows table does not add those two. 6.113 cannot settle that. **[bin]** (`protocol/v6x-clients.md#server--client-ids-601-603`)

Outgoing, Linux 6.03 sends 0–20, 22–24, 26–30, 32–38, 41, 44–48, 50, 79, 92, 93, 96–98, 130, 152, 154–162. Linux 6.01 omits 160. Ids 93 and 163 are preceded by id 50. Not sent: 21, 25, 31, 39 and 40, so there is no 10-byte tamper check after the language packet. The Windows lab note's own sends are the login, the language packet and the file requests, not this full list. **[bin]** (`protocol/v6x-clients.md#client--server-ids-601-603`) **[cap]** (`protocol/v5v6-windows-unpacked.md#login-message`)

Nothing in 6.113 adds an id to either list.

## Property streams

A property stream is still the classic run of id-then-value on `PLO_BADDYPROPS` (2), `PLO_NPCPROPS` (3), `PLO_OTHERPLPROPS` (8) and `PLO_PLAYERPROPS` (9), and the client sends its own on id 2. Those four server ids are inside every 6.00 and 6.03 switch list above. **[srv]** (`protocol/player-props.md`) **[bin]** (`protocol/v5v6-windows-unpacked.md#server--client-ids`)

What changes from 6.00 to 6.03, on the evidence in hand, is not a new property encoding. It is the packet set: 111 arrives and writes `creationtime.dat`, and 175 and 184 leave. Ids 109 and 198, a file redirect and one stored integer, are already in the January 2010 betas, not new at 6.03. **[bin]** (`protocol/v6x-clients.md#server--client-ids-601-603`, `protocol/v5v6-windows-unpacked.md#server--client-ids`)

Unpacked 6.00's plaintext names include script fields such as `rupees`, `swordpower`, `shieldpower` and `sprite`. Those are object fields. They are not a wire-id table, and they are absent from the 6.113 listing. 6.11 names `tclient_setplayerprops` as one native handler behind `setindatahandlers`. 6.113 does not contain that handler list, so it does not show a property id added after 6.00. **[bin]** (`client-internals/engine-600r2.md`, `protocol/v6x-clients.md#611-mac-the-connector-and-a-server-defined-protocol`)

## File transfer and the script cache

Unpacked 6.00r2 and 6.00r4 compare a `GRESCR01` magic on a `.code` file of at least eight bytes. The class and weapon paths are the cache note's. The string extract of those two images contains `.code` and a `GRESCR01`-shaped token. 6.113 contains neither. **[bin]** (`protocol/gs2-client-vm.md#script-cache`)

`creationtime.dat` is the body of S→C 111, present as a string in Windows 6.03r7 and absent in Windows 6.00r2. 6.113 does not have the string. **[bin]** (`protocol/v6x-clients.md#chat-and-nickname-drawing-603`)

The Windows captures' first file requests, for the Themida builds including 6.00r2 and 6.03r7, are id 23 for `basepackage.gupd`. 6.113 has no such name. The Linux upload queue (id 155, then id 93 chunks, then id 156) is not in this listing. **[cap]** (`protocol/v5v6-windows-unpacked.md#login-message`) **[bin]** (`protocol/v6x-clients.md#client--server-ids-601-603`)

Level magics are part of the same gap. The Linux note's three builds carry `GR-V1.03` through `GR-V1.05` and no newer magic. Unpacked Windows 6.00 still carries `GR-V1.00` through `GR-V1.05`, and Windows 6.03r7 drops the reader strings for `GR-V1.00` through `GR-V1.02` and for `GLEVNW01`. 6.113 has none of them. **[bin]** (`protocol/v6x-clients.md#file-formats`, `protocol/v5v6-windows-unpacked.md#file-formats-and-bundled-files`, `client-internals/engine-600r2.md#drawing`)

## Server-defined protocol

Both neighbour notes agree that `setprotocol`, the script-set id tables, RC4 or AES on the game socket, and the connector request are 6.11, not 6.01 or 6.03. The Windows dumps through 6.03r7 have no connector host and no `onSend` events. LibTomCrypt is linked in those Windows images, including 6.00, and is not what the game socket uses. **[bin]** (`protocol/v6x-clients.md#611-mac-the-connector-and-a-server-defined-protocol`, `protocol/v5v6-windows-unpacked.md#cipher-and-framing`)

6.113 does not add the missing connector. It also does not show that 6.11's template (`I` counter, `L` length, `T` packet id, `E` the extra field) or the 0xFE script-instead-of-wire slot had arrived in this Windows build. The export names include TLS 1.0 through 1.2, DTLS and AES-CBC, which is a later crypto surface than 6.037's, and the code at those names is not a TLS stack. **[bin]** (`client-internals/engine-6113.md#the-export-surface`)

## Contradictions

These are disagreements between `protocol/v6x-clients.md` and `protocol/v5v6-windows-unpacked.md`. 6.113's bytes pick neither side.

| Topic | Linux and Mac note (`v6x-clients.md`) | Windows unpacked note (`v5v6-windows-unpacked.md`) |
| --- | --- | --- |
| What the Windows exes are | Wrappers only. 6.01 and 6.03 Linux stand in for Windows 6.01 and 6.03 | The ten Windows builds were unpacked and run, including 6.00r2, 6.00r4 and 6.03r7 |
| 6.03 token | Linux `G3D0511C` | Windows `G3D0311C`. A server that accepts one need not accept the other |
| 6.00 token | Not given. The note had not read the Windows engine | `G3D26090`, shared with 5.30r3 and 5.31r4, not with Linux 6.01 |
| Key byte on id 5 | The key itself, random, 7 bits, as the first field | A GCHAR. The wire byte minus 32 is the key, and the wire byte can exceed 7 bits. Seen on 6.00 and 6.03 Windows captures |
| S→C 100 and 108 | Handled before the switch on Linux 6.01 and 6.03, so the published switch list is short by two | Not added to the Windows 6.00 or 6.03 switch tables |
| Level readers | `GR-V1.03` through `GR-V1.05` for the builds that note read | Windows 6.00 still has `GR-V1.00` through `GR-V1.05`. Windows 6.03 drops `.00` through `.02` and `GLEVNW01` |
| Login frame words | Mode 3: zlib, no cipher, no type byte | 16-bit length, zlib, no cipher, no compression byte |

The last row is the same frame described two ways, if mode 3 means "no compression byte". The token, the key byte, ids 100 and 108, and the old level magics are not the same claim. **[bin][cap]**

They agree on the 6.03 switch list itself, on gen-5 framing for 6.00 through 6.03, on `creationtime.dat` being 6.03 and not 6.00r2, and on the connector being absent before 6.11. **[bin][cap]**
