<!-- manual: kind=reference status=draft -->
# 7 RC and NC

RemoteControl (RC) is the staff client for a game server; NPC Control (NC) is its connection to the NPC server (→ §5.5). Both are Delphi programs that reuse the game client's connection class [bin] (tools/npc-control.md#program-shape-bin). The game-server login types are in → §2.3.6.1, framing in → §2.1.4 and ciphers in → §2.2. Staff ids that game clients also handle are in → §2.4.10 and → §2.5.9.

> Status: draft. Every layout here is a static read of the RC binaries, except those in → §7.1.8, which one capture of the 2004 RC against a GServer-v2 fork shows. The checks that would settle the rest are listed in the protocol note's loopback list.

## 7.1 RC login and commands

### 7.1.1 Builds

RemoteControl went through many builds. Each row gives one archive, its date, its login token, its number of forms and what it added [bin] (tools/remotecontrol-lineage.md#builds).

| Archive | Title date | Login token | Forms | Adds | Source |
| --- | --- | --- | ---: | --- | --- |
| rc133 | none | `GSERV014` | 7 | accounts, players, send, update levels | [bin] (tools/remotecontrol-lineage.md#builds) |
| rc139rev2 | 2000/8/19 | `GSERV019` | 15 | chat window, flag lists, toalls, SQL account list, options, warp | [bin] (tools/remotecontrol-lineage.md#builds) |
| rc1025 | 2000/10/25 | `GSERV020` | 15 | same forms | [bin] (tools/remotecontrol-lineage.md#builds) |
| rc62101 | 2001/01/27 | `GSERV021` | 15 | same forms | [bin] (tools/remotecontrol-lineage.md#builds) |
| rc8212001 | 2001/08/20 | `GSERV022` | 18 | rights, comments, local ban; server options leave the start dialog | [bin] (tools/remotecontrol-lineage.md#builds) |
| rc201 | 2002/01/04 | `GSERV022` | 18 | new main window layout | [bin] (tools/remotecontrol-lineage.md#builds) |
| (2002 RC) | 2002/01/11 | `GSERV023` | 27 | NPC Control, server list, file browser and short message already present | [bin] (server-notes/original-server-builds-1999-2007.md#npc-control-and-remotecontrol-20012002-bin) |
| rc141 | 2002/05/02 | `GSERV023` | 26 | NPC Control, server list, file browser, short message popup | [bin] (tools/remotecontrol-lineage.md#builds); [bin] (tools/npc-control.md#program-shape-bin) |
| RemoteControl in the Graal Reborn folder (2004) | n/a | `GSERV024` | 25 | RC and NC in one program, file browser, server list | [bin] (tools/remotecontrol.md) |

The archive names do not sort by date: rc141 is the newest of the 2000–2002 set [bin] (tools/remotecontrol-lineage.md). RemoteControl builds of 1999 log in with `GSERV007` (shipped with 1.21) and `GSERV011` (shipped with 1.28 and 1.3) [bin] (protocol/gserv-1999.md#login). A GServer-v2 also knows `GSERV025` (→ App. E#405).

### 7.1.2 Login

The RC login changed in 2004. Each row gives a group of builds, the first message and the framing during and after login [bin] (tools/remotecontrol-lineage.md#what-stays-the-same-bin).

| Builds | First message | Mode during login | Mode after | Source |
| --- | --- | --- | --- | --- |
| 1999 to rc141 (2002) | type 1, token, `str account`, `str password`; no key byte | `u16be` length + zlib, no cipher, no type byte | unchanged | [bin] (tools/remotecontrol-lineage.md#what-stays-the-same-bin); [bin] (tools/npc-control.md#logins-bin) |
| 2004 | type 6, `c key` (`rand & 0x7F`), `GSERV024`, `str account`, `str password` | `u16be` length + zlib, no cipher, no type byte | generation 5 (type byte + partial XOR) | [bin] (tools/remotecontrol.md#logins-bin) |

The rules below explain the RC2 name, how the tokens are stored and the defaults in the connect dialog [bin][srv] (tools/remotecontrol.md#logins-bin).

| Rule | Source |
| --- | --- |
| Type 6 is what the server calls RC2; the 2004 Delphi RC already uses it, so "RC2" in server tables means the generation-5 RC login, not the later GTK program | [bin][srv] (tools/remotecontrol.md#logins-bin) |
| The 2004 tokens are plain string constants, unlike the game clients' tokens built one character at a time | [bin] (tools/remotecontrol.md#logins-bin) |
| The connect dialog of every build has a built-in default account; the start dialog up to 2001/01/27 defaults to the loopback address and port 14804 | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |
| From 2002/05/02 the address fields are gone and the server is picked from the listserver (→ §6.1.1) | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |
| In the 39ster 2.1 remake an RC connection (type 1) skips the per-line descramble (→ §5.2.2) | [src] (ash/ARCHITECTURE.md#1-system-context) |
| A GServer-v2 refuses an RC whose account is not on the staff list | [src] (server-notes/04-algorithms.md#5-login) |

Right after login the RC sends one `PLI_PLAYERPROPS` (2):

| Builds | Props | Source |
| --- | --- | --- |
| 2000/8/19 on | 0 (NICKNAME) = the nickname from the options; closing the player list with "Go in away mode" sends it again with ` - away` appended | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |
| rc141 (2002) | 33 (ADDITFLAGS) = 1 only when "Ignore mass messages" is ticked; 0 (NICKNAME); 53 (PSTATUSMSG) = the selected status index | [bin] (tools/npc-control.md#logins-bin) |
| 2004 | a short message whose prop list is not traced | [bin] (tools/remotecontrol.md#logins-bin) |

### 7.1.3 Framing

RC framing is the game framing without the cipher. Each row gives a group of builds and its rule [bin] (tools/remotecontrol.md#codec).

| Builds | Rule | Source |
| --- | --- | --- |
| all | messages are `c id` + payload + `\n`, G-integers + `0x20`, batched and flushed at 0x1000 bytes | [bin] (tools/remotecontrol.md#codec); [bin] (tools/npc-control.md#framing-both-sockets-bin) |
| 2000 to 2002 | `u16be` length + zlib (zlib 1.1.2); no cipher, type byte, key byte or per-message insertion | [bin] (tools/remotecontrol-lineage.md#what-stays-the-same-bin) |
| 2002 | large uploads: id 50 (`PLI_RAWDATA`) with an `i3` length, a flush, then one frame of `c id` + header + raw bytes with no `\n`; receiving id 100 switches the reader to raw mode for that many bytes | [bin] (tools/npc-control.md#framing-both-sockets-bin) |
| 2002 | more than 256 KB queued unsent drops the socket | [bin] (tools/npc-control.md#framing-both-sockets-bin) |
| 2004, RC socket | client-side generation 5: each flush picks raw, zlib or bz2 by size, writes a type byte, and XORs the first 12 or 4 dwords with the `0x04A80B38`-seeded LCG plus the key, one step per 4-byte group present; send and receive keep separate iterators with the same key (→ §2.2.3) | [bin] (tools/remotecontrol.md#codec) |

### 7.1.4 Start dialog and server timers

Up to 2001/01/27 the start dialog asks for four server timers, each with a "don't change" box; each value goes out after login as an `i4`, only when its box is unticked [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin):

| Field | Default | Id | Name | Source |
| --- | ---: | ---: | --- | --- |
| Respawn time (bushes etc.) in sec | 10 | 55 | RC_RESPAWNSET | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |
| Horse lifetime in sec | 10 | 56 | RC_HORSELIFESET | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |
| Alignment increment time in sec | 1200 | 57 | RC_APINCREMENTSET | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |
| Baddies respawn time in sec | 60 | 58 | RC_BADDYRESPAWNSET | [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin) |

These are GServer13's four timer options (→ §5.1.1). From 2001/08/20 the timers are gone from the dialog and 55 to 58 are no longer sent [bin] (tools/remotecontrol-lineage.md#start-dialog-and-the-old-option-packets-bin).

### 7.1.5 Client → server ids by build

Constant ids at the RC socket's send call sites; ids sent through a computed value are not included, so each row is a floor [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin); [bin] (tools/remotecontrol.md#ids).

| Build | Ids | Source |
| --- | --- | --- |
| rc133 | 1, 51–64 | [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin) |
| 2000/8/19, 2000/10/25 | 1, 2, 6, 28, 55–58, 61–64, 67–79, 82 | [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin) |
| 2001/01/27 | 1, 2, 6, 28, 55–58, 61–64, 68, 70–74, 76–79, 82 | [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin) |
| 2001/08/20 | 1, 2, 6, 28, 61–64, 68, 70–79, 82–88 | [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin) |
| 2002/01/04 | 1, 2, 6, 28, 61–64, 68–79, 82–88 | [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin) |
| 2002/05/02 | 1, 2, 6, 28, 51–54, 61–64, 68–79, 82–92, 94, 96–98, plus the NC ids (→ §7.3.2) | [bin] (tools/remotecontrol-lineage.md#client--server-ids-per-build-bin) |
| 2004 | 2, 6, 28, 51–54, 61–64, 68–76, 78, 79, 82, 84, 86, 88–92, 94, 96–98 | [bin] (tools/remotecontrol.md#ids) |
| 2004, on the wire | also 83, 85 and 87 (rights, comments and ban get), with 73 and 76; the static row is a floor | [cap] (protocol/rc-capture-2026-11-04.md#ids-against-the-static-read) |

The later names cover server options, folder config, player props get and set, accounts, bans, rights, comments and the file browser [srv] (protocol/chat-pm-rc.md#admin-and-staff). Ids 51 to 54 changed meaning:

| Id | rc133 use | Later name | Source |
| ---: | --- | --- | --- |
| 51 | account list: Edit (get account) | RC_SERVEROPTIONSGET | [bin] (tools/remotecontrol-lineage.md#ids-5154-changed-meaning-bin) |
| 52, 53 | edit account: Apply | RC_SERVEROPTIONSSET, RC_FOLDERCONFIGGET | [bin] (tools/remotecontrol-lineage.md#ids-5154-changed-meaning-bin) |
| 54 | account list: Delete | RC_FOLDERCONFIGSET | [bin] (tools/remotecontrol-lineage.md#ids-5154-changed-meaning-bin) |
| 59 | player list: Edit (get player props) | RC_PLAYERPROPSGET | [bin] (tools/remotecontrol-lineage.md#ids-5154-changed-meaning-bin) |
| 60 | edit player: Apply | RC_PLAYERPROPSSET | [bin] (tools/remotecontrol-lineage.md#ids-5154-changed-meaning-bin) |

From 2000/8/19 accounts move to 70 to 78, and 51 to 54 are unused until 2002/05/02 brings them back as server options and folder config; a server that talks to rc133 cannot use the later names for 51 to 54 [bin][inf] (tools/remotecontrol-lineage.md#ids-5154-changed-meaning-bin).

| 2004 file operation | Rule | Source |
| --- | --- | --- |
| folder change | id 0x5a | [bin] (tools/remotecontrol.md#file-and-account-operations) |
| upload | framed by ids 0x9b, 0x5d, 0x9c | [bin] (tools/remotecontrol.md#file-and-account-operations) |
| delete | needs the rights string to contain `w` | [bin] (tools/remotecontrol.md#file-and-account-operations) |

### 7.1.6 Server → RC ids

The 2004 RC handles a fixed set of ids from the server. The row lists them [bin] (tools/remotecontrol.md#ids).

| Builds | Ids handled on the RC socket | Source |
| --- | --- | --- |
| 2004 | 13, 16, 30, 35, 37, 55–59, 61–70, 72–74, 76, 77, 79, 100, 103, 180 | [bin] (tools/remotecontrol.md#ids) |

The table gives each server-to-RC id with its name and layout [srv][2.05] (protocol/chat-pm-rc.md#toall).

| Id | Name | Layout | Source |
| ---: | --- | --- | --- |
| 13 | TOALL | `s player id`, `str message` (→ §2.8) | [srv][2.05] (protocol/chat-pm-rc.md#toall) |
| 16 | DISCMESSAGE | `rest` = text; a disconnect box | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 35 | RC_ADMINMESSAGE | `rest` = `Admin <account>:\xa7<text>` | [srv][2.05] (protocol/chat-pm-rc.md#admin-and-staff) |
| 37 | PRIVATEMESSAGE | `s from id`, then a quoted, comma-separated type label and message (→ §2.8) | [srv][2.05] (protocol/chat-pm-rc.md#private-messages) |
| 47 | STAFFGUILDS | `"guild",` repeated, sent at login | [srv][2.05] (protocol/chat-pm-rc.md#admin-and-staff) |
| 0x37 | (player list) | creates or updates a player row: a 14-bit id, then a prop stream (the note gives the id in hex only); defaults are 3 hearts, `sword1.gif`, `body.png`, `onlinestartlocal.graal` | [bin] (tools/remotecontrol.md#player-list) |
| 74 | RC_CHAT | an RC console line | [srv] (protocol/chat-pm-rc.md#admin-and-staff) |
| 79 | NPCSERVERADDR | `s player id`, then `ip,port` (→ §7.2.2) | [bin] (tools/npc-control.md#finding-the-npc-server-bin) |

Players in jail can PM only RCs [srv] (protocol/chat-pm-rc.md#private-messages). The layouts of the other RC ids are unmeasured in the notes [bin] (tools/remotecontrol.md#ids), except those seen on the wire in → §7.1.8 [cap] (protocol/rc-capture-2026-11-04.md#player-props).

### 7.1.7 Features and local settings

RC features were added build by build. Each row gives a build and what it added [bin] (tools/remotecontrol-lineage.md#feature-timeline-from-forms-bin).

| Build | Feature | Source |
| --- | --- | --- |
| rc133 | player list (nickname, account, level, head, id), disconnect, edit player, message, message to all, account list (add, delete, edit), update levels; the account form already carries rights (Load only, Graalian Police, Trusted Admin, Administrator, No rights, Blocked), look, position, items, weapons, opened chests, NPC flags, MP, AP, spin attack | [bin] (tools/remotecontrol-lineage.md#feature-timeline-from-forms-bin) |
| 2000/8/19 | chat window (RTF), server flags, toalls, SQL account list with a filter, message editor, options (ignore mass messages, no HTML in PMs, no images in PMs, away on close), warp player | [bin] (tools/remotecontrol-lineage.md#feature-timeline-from-forms-bin) |
| 2001/08/20 | edit rights, edit comments, local ban | [bin] (tools/remotecontrol-lineage.md#feature-timeline-from-forms-bin) |
| 2002/05/02 | NPC Control (NPC list, add NPC, local NPCs, classes, weapons, level list), listserver login and server list, file browser with drag and drop, short message popup | [bin] (tools/remotecontrol-lineage.md#feature-timeline-from-forms-bin) |

RC keeps its settings in two places. Each row gives a setting and where it is stored [bin] (tools/npc-control.md#local-settings-bin).

| Setting | Where | Source |
| --- | --- | --- |
| options: `nickname=`, `nomassmessages=`, `nohtmlinpms=`, `nohtmlimages=`, `attachaway=` | `controlconfig.txt` beside the exe; the later GTK RC2 uses `control2config.txt` | [bin] (tools/npc-control.md#local-settings-bin); [bin] (tools/remotecontrol.md#file-and-account-operations) |
| account (plain) and password (DES-obfuscated, 48 printable characters) | registry `HKCU\Software\Graal\RemoteControl` | [bin] (tools/npc-control.md#local-settings-bin); [bin] (tools/remotecontrol-lineage.md#what-stays-the-same-bin) |

The password scheme is a 24-byte block (length byte, up to 23 bytes of text, random padding), encrypted as three DES ECB blocks with an LSB-first key, each output byte written as two nibbles + `0x20` [bin] (tools/npc-control.md#password-obfuscation). The same scheme, with other keys, hides the RC 1.41 and 2.05 list hosts and the 1.1 guild files [bin] (tools/npc-control.md#password-obfuscation); [bin] (tools/server-tools-2001.md#graal-11-guildmaker-1999-bin).

### 7.1.8 Player admin on the wire (2004)

One session of the 2004 RC against a GServer-v2 fork, with one 2.22 player online; each row is a single observation [cap] (protocol/rc-capture-2026-11-04.md#setup). Notation as in → §2.1.

| Step | Rule | Source |
| --- | --- | --- |
| after login | server → RC in this order: 25, 194, 74 three times, 190 (empty), 47, 180, 103, one 55 per player online, then 74 `Currently online: ...` | [cap] (protocol/rc-capture-2026-11-04.md#after-the-rc-login) |
| after login | the RC then sends 2 PLAYERPROPS twice and the server answers with 9 | [cap] (protocol/rc-capture-2026-11-04.md#after-the-rc-login) |

Player administration was captured on the wire from a 2004 RC. Each row gives a direction, an id and its layout [cap] (protocol/rc-capture-2026-11-04.md#after-the-rc-login).

| Dir | Id | Layout | Source |
| --- | ---: | --- | --- |
| S→RC | 103 RC_MAXUPLOADFILESIZE | `i5` bytes; 20971520 seen | [cap] (protocol/rc-capture-2026-11-04.md#after-the-rc-login) |
| S→RC | 55 ADDPLAYER | `s player id`, `str account`, then props as id + value | [cap] (protocol/rc-capture-2026-11-04.md#after-the-rc-login) |
| RC→S | 73 RC_PLAYERPROPSGET2 | `s player id` | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| S→RC | 72 RC_PLAYERPROPSGET | `s player id`, `str account`, `str world`, `c n`, n bytes of props, tail | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| RC→S | 76 RC_PLAYERPROPSSET2 | `str account`, `str world`, `c n`, n bytes of props, tail, then one more byte (0 seen; → App. E#421) | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| both | props tail | `s`, `s` (flag and chest counts, order unseen → App. E#420), `c weapon count`, `str` per weapon | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| RC→S | 83 RC_PLAYERRIGHTSGET | account as `rest` | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| S→RC | 62 RC_PLAYERRIGHTSGET | `str account`, `i5 rights`, `str IP range`, `s n` + n bytes of folder rights | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| RC→S | 84 RC_PLAYERRIGHTSSET | same layout as 62; folder lines as CSV (→ App. E#422) | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| RC→S | 85 RC_PLAYERCOMMENTSGET | account as `rest` | [cap] (protocol/rc-capture-2026-11-04.md#comments) |
| S→RC | 63 RC_PLAYERCOMMENTSGET | `str account`, comments as CSV (`rest`), one item per text box line | [cap] (protocol/rc-capture-2026-11-04.md#comments) |
| RC→S | 86 RC_PLAYERCOMMENTSSET | `str account`, comments as CSV (`rest`) | [cap] (protocol/rc-capture-2026-11-04.md#comments) |
| RC→S | 87 RC_PLAYERBANGET | account as `rest` | [cap] (protocol/rc-capture-2026-11-04.md#ban) |
| S→RC | 64 RC_PLAYERBANGET | `str account`, `c banned`, reason (`rest`) | [cap] (protocol/rc-capture-2026-11-04.md#ban) |
| RC→S | 88 RC_PLAYERBANSET | `str account`, `c banned`, reason as CSV (`rest`) | [cap] (protocol/rc-capture-2026-11-04.md#ban) |

The rules below record what the capture showed: which props the RC sends back, how rights map to bits, and what the ban menu offers [cap] (protocol/rc-capture-2026-11-04.md#player-props).

| Observation | Rule | Source |
| --- | --- | --- |
| props sent back | the RC's 76 leaves out props 0, 30, 34 and 36, adds 21, 22 and 23 as one zero byte each, and sends 29 as 0 | [cap] (protocol/rc-capture-2026-11-04.md#player-props) |
| rights bits | the dialog's check boxes map to bits from bit 0; "Warpto x y" and "Admin message" gave 513 (bits 0 and 9) | [cap] (protocol/rc-capture-2026-11-04.md#rights) |
| ban menu | the player menu has Edit Ban only: the account ban, with no IP or computer id ban | [cap] (protocol/rc-capture-2026-11-04.md#ban) |

## 7.2 NC login

### 7.2.1 Login and framing

NPC Control logs in on its own socket. The rules below give its first message and framing [bin] (tools/npc-control.md#logins-bin).

| Rule | Source |
| --- | --- |
| The NC socket's first message is type 3, `NCL11012`, `str account`, `str password`, with no key byte, sent right after the socket connects | [bin] (tools/npc-control.md#logins-bin); [bin] (protocol/npc-control.md#login) |
| The NC socket stays in fixed zlib framing (`u16be` length + zlib) for the whole session: no type byte, no cipher | [bin] (tools/remotecontrol.md#logins-bin); [bin] (protocol/npc-control.md#login) |
| The NC login did not change between rc141 (2002) and the 2004 RC | [bin] (protocol/npc-control.md#login) |
| A GServer-v2 also knows the NC token `NCL21075` (→ §2.3.6.1) | [srv] (protocol/login-and-walk.md#how-the-server-parses-it-srv) |
| Status bar text after login: "Connected to NPC-Server" | [bin] (tools/npc-control.md#finding-the-npc-server-bin) |

### 7.2.2 Finding the NPC server

The RC never asks for an NC address [bin] (tools/npc-control.md#finding-the-npc-server-bin):

| Step | Rule | Source |
| ---: | --- | --- |
| 1 | any player whose nickname contains `(Server)` is treated as an NPC-server player | [bin] (tools/npc-control.md#finding-the-npc-server-bin) |
| 2 | for each, the RC sends id 94 (`PLI_NPCSERVERQUERY`): `s player id` + the text `location`, when the player appears and again whenever the NC socket drops | [bin] (tools/npc-control.md#finding-the-npc-server-bin) |
| 3 | the server answers id 79 (`PLO_NPCSERVERADDR`): `s player id`, then `ip,port` | [bin] (tools/npc-control.md#finding-the-npc-server-bin) |
| 4 | the RC opens the NC socket only if it is not already open and that player's nickname still contains `(Server)`, then sends the NC login | [bin] (tools/npc-control.md#finding-the-npc-server-bin) |

The rules below give how NPC Control finds the NPC server and what the 2001 texts say about it [bin][inf] (tools/npc-control.md#finding-the-npc-server-bin).

| Rule | Source |
| --- | --- |
| The binary's default NC fields (the loopback address and 14804) are leftovers of the old start dialog and unused once discovery works | [bin][inf] (tools/npc-control.md#finding-the-npc-server-bin); [bin] (protocol/npc-control.md#finding-the-npc-server-bin) |
| The 2001 NPC Control text says the NewWorld game server exposed NC on port 14950; NewWorld accounts could connect, main-server accounts needed admin level 4 or higher | [doc] (tools/npc-control.md#what-the-npccontrol-13-bundle-is-doc) |
| The 2001 bundle says adding, viewing and changing classes did not work yet | [doc] (tools/npc-control.md#what-the-npccontrol-13-bundle-is-doc) |

## 7.3 NPC, class and weapon messages

On the NC socket, received ids 33, 80, 157 to 164 and 167 go to the NC handler; everything else, 16 included, goes to the RC handler [bin] (tools/npc-control.md#routing-on-the-nc-socket-bin).

### 7.3.1 NC → client

These are the ids NPC Control receives. Each row gives the id, its name, its layout and what it opens [bin] (tools/npc-control.md#nc--client-ids-handled).

| Id | Name | Layout | Effect | Source |
| ---: | --- | --- | --- | --- |
| 16 | DISCMESSAGE | `rest` = text | disconnect box | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 33 | NPCWEAPONADD | `str name`, `str image`, `s len`, `len` bytes of script | weapon script editor | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 80 | NC_LEVELLIST | `rest` = level list, one per line | level list editor | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 157 | NC_NPCATTRIBUTES | `rest` = attribute text, one per line | attribute viewer (view only) | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 158 | NC_NPCADD | `i3 id`, then props in any order and any subset: `c 50` + `str name`, `c 51` + `str type`, `c 52` + `str level` | adds or updates an NPC list row | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 159 | NC_NPCDELETE | `i3 id` | removes the row | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 160 | NC_NPCSCRIPT | `i3 id`, `rest` = script | script editor | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 161 | NC_NPCFLAGS | `i3 id`, `rest` = flags, one per line | flag editor | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 162 | NC_CLASSGET | `str name`, `rest` = script | class editor | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 163 | NC_CLASSADD | `rest` = class name | adds to the class list | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 164 | NC_LEVELDUMP | `rest` = text | dump viewer (view only) | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 167 | NC_WEAPONLISTGET | repeated `str name` | weapon list | [bin] (tools/npc-control.md#nc--client-ids-handled) |
| 188 | NC_CLASSDELETE | class name, form unmeasured | handled from 2004, not in 2002 | [bin][inf] (protocol/npc-control.md#nc--client-server-ids) |

### 7.3.2 Client → NC

These are the ids NPC Control sends. Each row gives the id, the action that sends it and its payload [bin] (tools/npc-control.md#client--nc-ids-sent).

| Id | Name | From | Payload | Source |
| ---: | --- | --- | --- | --- |
| 3 | (login) | connect | → §7.2.1 | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 79 | RC_CHAT | a console line typed in NC mode | text | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 103 | NC_NPCGET | NPC list: open, Enter, Attributes | `i3 id` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 104 | NC_NPCDELETE | NPC list: Delete, after a confirm | `i3 id` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 105 | NC_NPCRESET | NPC list: Reset | `i3 id` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 106 | NC_NPCSCRIPTGET | NPC list: Script | `i3 id` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 107 | NC_NPCWARP | Quick warp or the warp dialog | `i3 id`, `c x×2`, `c y×2`, level | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 108 | NC_NPCFLAGSGET | NPC list: Edit flags | `i3 id` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 109 | NC_NPCSCRIPTSET | script editor: Save | `i3 id`, script | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 110 | NC_NPCFLAGSSET | flag editor: Save | `i3 id`, flags | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 111 | NC_NPCADD | Add NPC dialog | comma text: name, id, type, scripter, start level, x, y; type is one of `OBJECT`, `ANIMAL`, `POLICE`, `HORSE`, `BOAT`, `HOUSEC` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 112 | NC_CLASSEDIT | class list: open | class name | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 113 | NC_CLASSADD | class editor: Save | `str name`, `rest` = script | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 114 | NC_LOCALNPCSGET | Local NPCs dialog | level name | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 115 | NC_WEAPONLISTGET | console button | empty | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 116 | NC_WEAPONGET | weapon list: open | weapon name | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 117 | NC_WEAPONADD | weapon editor: Save | `str name`, `str image`, `rest` = script | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 118 | NC_WEAPONDELETE | weapon list: Delete | weapon name | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 119 | NC_CLASSDELETE | class delete; sent from 2004, no button in 2002 | class name | [bin] (protocol/npc-control.md#client--nc-client-ids) |
| 150 | NC_LEVELLISTGET | console button | empty | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| 151 | NC_LEVELLISTSET | level list editor: Save | level list | [bin] (tools/npc-control.md#client--nc-ids-sent) |

The rules below give how NC saves its texts and which reply layouts are still unmeasured [bin] (tools/npc-control.md#client--nc-ids-sent).

| Rule | Source |
| --- | --- |
| All NC texts open in one shared editor window with a mode; Save sends 109, 110, 113, 117 or 151 by mode; attributes (157) and dumps (164) can only be saved locally as `.rtf` | [bin] (tools/npc-control.md#client--nc-ids-sent) |
| The reply id and layout after id 114 (local NPCs) are unmeasured | [inf] (protocol/npc-control.md#check-on-loopback-inf) |
| Whether 33 carries the script length as `s` or `i3` for large scripts, and whether big set messages go through the raw-data path, is unmeasured | [inf] (protocol/npc-control.md#check-on-loopback-inf) |

### 7.3.3 The 2001 PM admin interface

Before the NC socket, admins controlled the 2001 NPC server by PMs to its player login; only senders whose nickname carries `(NPC Admin)` were answered, and an unknown command such as `help` returned the command list [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based). Multi-line commands put their payload on the lines after the first [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based).

| Command | Payload and effect | Source |
| --- | --- | --- |
| `add npc <name>` | next lines: id, type (up to 6 characters), scripter, level, x, y; database NPC ids are unique and at least 1000; level and x, y become the reset position | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `reset npc <name>` | resets every attribute but the script and returns the NPC to its start; the name is case-sensitive | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `update script <name>` | the following lines replace the script; a running `sleep` is cut | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `get script <name>` | returns an NPC's or a class's script | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `update class <name>` | replaces a class script, saved to the scripts folder; members pick it up at once | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `get npc list` | lists database NPCs (id ≥ 1000) with positions | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `dump vars`, `dump vars <name>` | dumps the level's or an NPC's variables | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |
| `reload level list` | rereads the text file of levels this server handles | [doc] (tools/npcserver-2001.md#5-admin-interface-pm-based) |

The NC Add NPC dialog has the same seven fields as `add npc`, so id 111 is most likely that command moved onto its own message [inf][doc] (protocol/npc-control.md#client--nc-client-ids). The RC finds the NPC server by `(Server)` in the nickname rather than `(NPC Admin)` [bin] (tools/npcserver-2001.md#open-questions).
