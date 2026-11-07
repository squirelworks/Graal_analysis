# Graal2001 NPC server: notes from the 2001 design document

Source: `NPC Server Document Graal2001.rar`, which holds one file,
`npcserverdoc_Graal2001.txt` (13,520 bytes, sha256 `59edd6c1…57fd0dc`).
It is byte-identical to `npcserverdoc.txt` in the
NPCControl1.3 archive. Everything below
is paraphrased; nothing here comes from a binary unless marked **[checked]**.

## 1. What the NPC server is

- A separate program that **logs into the GServer like an ordinary player** and
  owns the NPCs of a configured set of levels.
- Main loop, every **0.1 s**: read from GServer, run all NPC scripts, push changed
  NPC attributes to players, push changed player attributes to GServer and
  players, then sleep out the rest of the tick. So 0.1 s is the smallest useful
  `timeout` / `sleep` on the server side.
- Startup order: load options, connect to GServer, then (only if connected) load
  the level list, then load NPCs from its database.
- Data it receives from GServer: player attributes; temporary level state (bombs,
  explosions, bush removal, dropped items and the like); PMs; game time;
  levels to update or reload; `server.` flags being added or removed.
- Only some of what the NPC server computes is forwarded to clients; GServer
  decides.

### Implied GServer link (inference, needs a capture to confirm)

| Direction | Content named in the doc |
|---|---|
| GServer → NPC server | player props, level temp objects, PMs, time, level reload, server-flag add/del |
| NPC server → GServer | NPC props, player props (when scripts change a player), PM replies, weapon grants (`addweapon`/`toweapons`), warps (`setlevel2`) |

The doc does not give packet ids or a port. From other threads: NPC Control
1.3 talks of port **14950** on the NewWorld host and admin level ≥ 4, and RC 1.41
logs into the NPC server with `NCL11012` on default the loopback address on **14804**.
**[checked]** `RemoteControl.exe` contains `NCL11012`, `14804`,
`Connected to NPC-Server`, and UI strings `Add NPC`, `Add Class`, `Classes`,
`NPC List`, `NPC Level List`, `Script from Class`. These match the PM commands in
section 5 one for one, which suggests RC 1.41 moved the 2001 PM interface onto its
own connection. That last step is an inference.

## 2. Server-side scripting model

- Scripts run on the server by default. A line `//#CLIENTSIDE` splits the script:
  everything after it is shipped to clients. Clients only read NPC attributes and
  never propagate their own changes, so the client half is for visuals and sound.
- Server-only events: `created` (first run), `initialized` (reloaded, such as after
  an NPC-server restart), `playerenters`, `playerleaves` (not on disconnect),
  `playertouchsme` (needs `setshape`), `playerchats`, `npcwarped`, `exploded`.

## 3. Commands

Flow and core: `destroy`, `if`, `while`, `for`, `break`, `continue`, `sleep`,
`set`, `unset`, `setstring`, `message`.

NPC appearance and state: `setgif`/`setimg`, `setgifpart`/`setimgpart`,
`setshape`, `drawoverplayer`, `drawunderplayer`, `dontblock`, `blockagain`,
`show`, `hide`, `noplayeronwall`, `showcharacter`, `setcharprop`, `setcharani`,
`setchargender`, `putbomb`, `putexplosion`, `putexplosion2`, `setarray`.

Server-side additions: `canwarp`, `canwarp2`, `cannotwarp`, `callnpc`,
`with (players[i])`, `with (getplayer(acct))`, `with (npcs[i])`,
`with (getnpcs(name))`, `join`, `warpto`, `tokenize`, `tokenize2`.

Acting on the current player: `setplayerprop`, `setani`, `setgender`, `say`,
`enableweapons`, `disableweapons`, `toweapons`, `addweapon`, `removeweapon`,
`setlevel2`, `freezeplayer2`, `unfreezeplayer`.

Behaviour worth recording:

- `setshape 1,w,h`: the server never loads images, so it needs a rectangle to
  detect touches. Type 0 ("use the image") was planned, not built.
- `noplayeronwall`: `onwall`/`onwall2` stop counting players (the doc's example
  is the Elephant, which always has players on it).
- `canwarp` / `canwarp2`: database NPCs only. `canwarp` warps exactly as a
  player would (used with recorded waytracker paths for police NPCs). `canwarp2`
  is for wandering overworld NPCs: normal links, checks `onwall` at the
  destination, refuses small links such as house doors.
- `with`: temporarily swaps the current player or NPC. Commands inside are
  skipped if the target does not exist. Local variables still resolve to the
  caller, and the code still runs from the calling NPC's script. `sleep`,
  `break` and `continue` inside `with` leave the swapped context in place (a
  documented hazard).
- `join class`: loads `class.txt` from the scripts folder. Each NPC holds a
  list of script objects (its own first, then each joined class). A class
  already loaded by another NPC is shared, not copied, so updating a class
  updates every member. Later scripts can override functions.
- `warpto`: moves the NPC to another level; database NPCs only.
- `addweapon`: like `toweapons`, but takes the weapon script from the database
  (the weapon must already exist). Used by the Graal2001 trading house.
- String helpers: `strlen`, `startswith(part,str)`, `indexof(part,str)` (−1 if
  absent), `#e(start,len,str)`, `#T(str)` trim, `tokenscount`, `#t(i)`.
  `tokenize` splits on spaces and commas; `tokenize2` adds extra delimiters.

## 4. Variables and flags

| Kind | Scope | Persisted |
|---|---|---|
| `name` | current script or class | no |
| `this.name` | current NPC | yes, for database NPCs |
| `level.name` | the NPC's level | no |
| `server.name` (number) | this NPC server only | no |
| object attributes | as in the client, plus `playerlastdead` (last death or login time; Graal2001 only) | — |
| flags | current player | yes, in the account |
| `client.` flags | current player, also sent to the client, and the client can change them | yes |
| `this.` flags | current NPC | yes, for database NPCs |
| `server.` flags | world-wide, shared with other NPC servers of the same world, never sent to players | yes |

So `server.` *numbers* are local to one NPC server, while `server.` *flags*
are shared across the world.

## 5. Admin interface (PM based)

Admins control the NPC server by sending PMs to its player login. Only senders
whose nickname carries the `(NPC Admin)` tag are answered. An unknown command
such as `help` returns the command list. Multi-line commands put their payload
on the lines after the first.

| Command | Payload and effect |
|---|---|
| `add npc <name>` | next lines: id, type (≤6 chars), scripter, level, x, y. Ids must be unique and ≥1000 for database NPCs (built-ins such as gralats sit below). The level and x,y become the reset position. |
| `reset npc <name>` | resets every attribute except the script and returns the NPC to its start (the name is case-sensitive) |
| `update script <name>` | the following lines replace the script. A running `sleep` is cut, so a `reset npc` is often needed afterwards. |
| `get script <name>` | returns an NPC's or a class's script |
| `update class <name>` | replaces a class script, saved to the scripts folder; members pick it up at once |
| `get npc list` | lists database NPCs (id ≥1000) with positions |
| `dump vars` / `dump vars <name>` | dumps the level's or an NPC's variables |
| `reload level list` | rereads the configured text file of levels this server handles |

## 6. Message codes

- `#F`: the current *player's* level name. It can differ from `#L` (the NPC's
  level), for example in `playerleaves` or inside `with (getplayer(...))`.
- `#a(i)` and similar: an index suffix addresses the i-th player in the level.
- `#e`, `#T`, `#t`: see the string helpers above.

## 7. Cross-check against the v2.05 client [checked]

Mostly a plain string search of the client executables. The second bullet comes
from the 2.05 script command table.

- `Graal_v2.05_rev2.exe` already contains most server-side names:
  `setshape`, `canwarp`, `canwarp2`, `callnpc`, `join`, `tokenize`,
  `tokenize2`, `tokenscount`, `setplayerprop`, `setgender`, `setchargender`,
  `toweapons`, `setlevel2`, `freezeplayer2`, `unfreezeplayer`, `putexplosion2`,
  `setarray`, `startswith`, `indexof`, `//#CLIENTSIDE`, and the events
  `playerenters`, `playertouchsme`, `playerchats`, `exploded`, `initialized`.
  The string `warpto` is also in the file, but it is not a script command
  there.
- How 2.05 handles them, from its script command table:
  - In the table but with no handler, so parsed and ignored:
    `canwarp`, `canwarp2`, `join`, `freezeplayer2`, `unfreezeplayer`.
  - In the table with a handler, so they run on the client:
    `setshape`, `callnpc`, `tokenize`, `tokenize2`, `setplayerprop`,
    `setgender`, `setchargender`, `toweapons`, `setlevel2`, `putexplosion2`,
    `setarray`.
  - Not script commands at all: `warpto`, `noplayeronwall`, `cannotwarp`,
    `addweapon`, `removeweapon`.
  So in 2.05 the first group does nothing whatever the server says; it does
  not depend on server packet 44 (which tells the client an NPC server is
  present). A server freezes a 2.05 player with server packets 154 and 155
  instead of the script commands.
- Not found in any client build checked (2.05, 2.171, 2.22): `playerleaves`,
  `npcwarped`, `noplayeronwall`, `cannotwarp`, `addweapon`, `removeweapon`,
  `playerlastdead`, `level.`. These look server-only.
- `getplayer`/`getnpc` appear in 2.171 and 2.22 but not in 2.05.

## Open questions

1. Packet ids and port for the NPC-server ↔ GServer link (needs a 2001-era
   GServer or NPC server binary, or a capture). The RC 1.41 (2002) side of
   NPC Control is now mapped in `tools/npc-control.md`. It shows the PM
   commands above became packet ids one for one: `add npc` is NC id 111 with
   the same seven fields (name, id, type, scripter, level, x, y), and type is
   one of OBJECT, ANIMAL, POLICE, HORSE, BOAT or HOUSEC. The RC finds the NPC
   server as the player whose nick contains `(Server)` rather than
   `(NPC Admin)`. There is still nothing on the GServer-side link itself.
2. Where the NPC database and the level-list file live, and their formats.
