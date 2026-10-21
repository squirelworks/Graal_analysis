# NPC Control (RC 1.41, 2002)

Date: 2026-10-21

Source: static read of the Delphi `rc141.exe` ("GServer2 Remote Control 2002/05/02"), the first RemoteControl build that contains NPC Control. Also `NPCControl1.3` (a 2001 docs bundle with no binary). Tags: **[bin]** read from the binary · **[doc]** from the 2001 text files · **[inf]** inferred.

The later 2004 RemoteControl is in `remotecontrol.md` on the cross-version branch. This note covers the 2002 build, which is where NPC Control first appears.

## What the NPCControl 1.3 bundle is **[doc]**

It has no executable. It holds:

- `npccontrol.txt`: NPC Control connects to port 14950 on the NewWorld game server. Every NewWorld account could connect there; on the main server only accounts with admin level 4 or higher could.
- `npcserverdoc.txt`: the 2001 NPC server document. It is byte-identical to the separately uploaded "NPC Server Document Graal2001" (notes in `npcserver-2001.md`).
- `waytracker.txt` / `waytracker-show.txt`: two small NPCs. One records the player's walk as `dir - length` pairs into a string (for `this.ways` arrays of police NPCs), and the other displays it.
- `graal2001classes/`: ten class scripts that NPCs `join`: bomys, bomypolice, police, horses, gralats, minerocks, housecontrols3, castlecontrols, ctfcontrols, ctfflags.

The bundle says "Adding/Viewing/Changing classes doesn't work yet", so at 1.3 class editing was still missing from the tool.

## Program shape **[bin]**

RC 1.41 is RC and NC in one window. NPC Control adds these forms to the older RC: `NPCList`, `AddNPCFrame`, `LocalNPCs`, `ClassesList`, `AddClass`, `WeaponsList`. The same release also adds `ServerList` (listserver login), `FileBrowser`, and `ShortMessage`.

Two `TGraalClient` sockets: one to the game server (RC) and one to the NPC server (NC). A third subclass, `TServerListClient`, talks to the listserver.

## Framing (both sockets) **[bin]**

- Message: `GCHAR id` + payload + `\n`. Messages are batched and flushed when the buffer reaches 0x1000 bytes.
- Frame: `u16be length` + zlib body (Delphi zlib 1.1.2). There is no type byte, no cipher, and no per-message junk byte on either socket in this build.
- Large uploads: the client first sends id 50 (`PLI_RAWDATA`) with a GINT3 length, flushes, then sends one frame that holds `GCHAR id` + header + raw bytes with no newline.
- Receive: id 100 (`PLO_RAWDATA`) switches the reader into raw mode for the next *length* bytes.
- If more than 256 KB is queued unsent, the socket is dropped.

## Logins **[bin]**

| Socket | First message | Notes |
|---|---|---|
| RC | id **1**, `GSERV023`, `str account`, `str password` | no key byte |
| NC | id **3**, `NCL11012`, `str account`, `str password` | no key byte; sent right after the NC socket connects |

The id is the client type that later gs2lib names: 1 = RC, 3 = NC. The 2004 RC moved to type 6 (`GSERV024`, gen 5); the NC login did not change between 2002 and 2004.

Straight after the RC login the client sends one `PLI_PLAYERPROPS` (2):
- prop 33 (ADDITFLAGS) = 1, only when "Ignore mass messages" is ticked,
- prop 0 (NICKNAME) = the nickname from the options,
- prop 53 (PSTATUSMSG) = the selected status index.

## Finding the NPC server **[bin]**

The RC never asks the user for an NPC-server address. It finds it like this:

1. Any player in the RC player list whose **nickname contains `(Server)`** is treated as an NPC server.
2. For each such player the RC sends id **94** (`PLI_NPCSERVERQUERY`): `GSHORT player id` + the text `location`. It does this when the player appears, and again whenever the NC socket drops.
3. The server answers with id **79** (`PLO_NPCSERVERADDR`): `GSHORT player id`, then `ip,port`. The RC acts on it only if the NC socket is not already open and only if that player's nickname contains `(Server)`.
4. The RC opens the NC socket to that address and sends the NC login above. The status bar shows "Connected to NPC-Server".

The defaults `127.0.0.1` and `14804` in the binary are unused leftovers of the old start dialog. **[inf]** The 2001 doc's "(NPC Admin)" PM interface (see `npcserver-2001.md`) is the older channel that this socket replaced.

## Routing on the NC socket **[bin]**

Received ids 33, 80, 157–164, and 167 on the NC socket go to the NC handler. Everything else, including 16, goes to the normal RC handler.

### NC → client (ids handled)

| Id | gs2lib name | Layout as parsed | UI |
|---:|---|---|---|
| 16 | DISCMESSAGE | rest = text | disconnect box |
| 33 | NPCWEAPONADD | `str name`, `str image`, `GSHORT len`, `len` bytes of script | weapon script editor |
| 80 | NC_LEVELLIST | rest = level list, one per line | level list editor |
| 157 | NC_NPCATTRIBUTES | rest = attribute text, one per line | attribute viewer |
| 158 | NC_NPCADD | `GINT3 id`, then props: `GCHAR 50` + `str name`, `GCHAR 51` + `str type`, `GCHAR 52` + `str level` (any order, any subset) | adds or updates a row in the NPC list |
| 159 | NC_NPCDELETE | `GINT3 id` | removes the row |
| 160 | NC_NPCSCRIPT | `GINT3 id`, rest = script | script editor |
| 161 | NC_NPCFLAGS | `GINT3 id`, rest = flags, one per line | flag editor |
| 162 | NC_CLASSGET | `str name`, rest = script | class editor |
| 163 | NC_CLASSADD | rest = class name | adds to the class list |
| 164 | NC_LEVELDUMP | rest = text | dump viewer |
| 167 | NC_WEAPONLISTGET | repeated `str name` | weapon list |

Id 188 (`NC_CLASSDELETE`) is not handled in 2002; it arrived with the 2004 build.

### Client → NC (ids sent)

| Id | gs2lib name | From | Payload |
|---:|---|---|---|
| 3 | (login) | connect | see Logins |
| 79 | RC_CHAT | console line typed in NC mode | text |
| 103 | NC_NPCGET | NPC list: double-click, Enter, Attributes | `GINT3 id` |
| 104 | NC_NPCDELETE | NPC list: Delete (with confirm) | `GINT3 id` |
| 105 | NC_NPCRESET | NPC list: Reset | `GINT3 id` |
| 106 | NC_NPCSCRIPTGET | NPC list: Script | `GINT3 id` |
| 107 | NC_NPCWARP | NPC list: Quick warp, or the warp dialog | `GINT3 id`, `GCHAR x*2`, `GCHAR y*2`, level |
| 108 | NC_NPCFLAGSGET | NPC list: Edit flags | `GINT3 id` |
| 109 | NC_NPCSCRIPTSET | script editor: Save | `GINT3 id`, script |
| 110 | NC_NPCFLAGSSET | flag editor: Save | `GINT3 id`, flags |
| 111 | NC_NPCADD | Add NPC dialog | comma text of name, id, type, scripter, start level, x, y. Type is a drop-down: `OBJECT`, `ANIMAL`, `POLICE`, `HORSE`, `BOAT`, `HOUSEC` |
| 112 | NC_CLASSEDIT | class list: open | class name |
| 113 | NC_CLASSADD | class editor: Save | `str name`, rest = script |
| 114 | NC_LOCALNPCSGET | Local NPCs dialog | level name |
| 115 | NC_WEAPONLISTGET | console button | — |
| 116 | NC_WEAPONGET | weapon list: open | weapon name |
| 117 | NC_WEAPONADD | weapon editor: Save | `str name`, `str image`, rest = script |
| 118 | NC_WEAPONDELETE | weapon list: Delete | weapon name |
| 150 | NC_LEVELLISTGET | console button | — |
| 151 | NC_LEVELLISTSET | level list editor: Save | level list |

Id 119 (`NC_CLASSDELETE`) is not sent; there is no class delete button yet.

All NC texts (scripts, flags, classes, weapons, level list, dumps) open in one shared editor window with a mode number. Save sends 109 (NPC script), 110 (NPC flags), 113 (class), 117 (weapon), or 151 (level list) according to that mode. Attributes (157) and dumps (164) are view-only and can be saved as `.rtf`.

The Add NPC dialog has the same fields as the 2001 PM command `add npc` (name, id, type, scripter, level, x, y), so id 111 is that command moved onto its own packet. **[inf]**

## Local settings **[bin]**

- `controlconfig.txt` next to the exe: `nickname=`, `nomassmessages=`, `nohtmlinpms=`, `nohtmlimages=`, `attachaway=`.
- Registry `HKCU\Software\Graal`, section `RemoteControl`: values `accountname` (plain) and `password` (obfuscated, below).

### Password obfuscation

The same scheme is used in every RC build from 1.33 to 1.41, and it also hides the listserver host name inside RC 1.41 and the 2.05 client.

1. Build a 24-byte block: `len` (one byte), the password (at most 23 bytes), random padding up to 24 bytes.
2. Encrypt it as three 8-byte blocks with DES in ECB mode. The cipher is a d3des port whose key bit order is LSB-first, so it equals standard DES with each key byte bit-reversed.
3. Write each output byte as two characters, high nibble first, each nibble `+ 0x20`. The result is 48 printable characters.

The RC password key is the 8-byte string `\!x<|.ak`. Decoding is the reverse; a block whose length byte is 24 or more is rejected.

## Listserver login (new in 1.41) **[bin]**

- Host: stored as a 48-character ciphertext (scheme above, key bytes `2B 77 77 A7 B4 31 21 41`). It decodes to `listserver.graalonline.`, to which the code appends `com`. Port `14922`.
- Messages: id 0 `rc` (version string), then id 1 `str account`, `str password`.
- Replies handled: 0 (server list: `GCHAR count`, then per server `GCHAR field count` + that many `str` fields), 1 (one more server entry), 2 (end, disconnect), 4 (error text, disconnect).
- The server list shows name and player count. Connect uses the chosen server's ip and port.

The same key and nibble encoding hide the 2.05 client's list host, which the 2.05 notes left open: 2.05 rev 2 decodes to `www.graalonline.com`, port `14921`, version string `newmain`. **[bin]**
