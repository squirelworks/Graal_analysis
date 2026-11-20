# Early clients on the probe proxy: gen 1 (1998 relay) and gen 2 (GSERV/GNW), 2026-11-19

Date: 2026-11-19

Real Windows clients from the 1998 betas to 1.39 were run under Wine behind the probe proxy
(`../tools/probe/`), and server-to-client traffic was injected row by row. The aim was to learn
the protocol these builds actually speak: which ids and props each build reads, field widths
and terminators, how a parser recovers from an unknown id or a bad byte, and the lobby and
pairing state machine of the relay builds. Crashes were checked along the way: no build
crashed or hung on any row. Rows are in [`probe-results.tsv`](probe-results.tsv) (run tags
`w1xx-row`, `w1xx-sweep` for gen 2; `w<beta>-row`, `w<beta>-lobby` for gen 1). Open items are in
[`unknowns-ledger.md`](unknowns-ledger.md). The protocol references these results extend are
[`gserv-1999.md`](gserv-1999.md) (gen 2) and [`relay-1998.md`](relay-1998.md) (gen 1).

Tags: **[lab]** seen in these runs. **[srv]**, **[bin]**, **[cap]**, **[inf]** as elsewhere.

## Setup

| | Gen 2 (1.28b2, 1.3 test, 1.31–1.39) | Gen 1 (1st Graal to 1.1.9) |
|---|---|---|
| Server | seihai-gserver `3f8d35b`, `rules = 1999`, accounts made on first login | `relay98.py`, a stand-in for the 1.1.9 relay lobby (`NR`, `NL`, `I`, `+`/`P` pairing, `D` relay); `--fakepeer=9900` announces one fake peer in every room a client joins |
| Proxy | `gen5probe.py`, gen 2 picked from the token (no key byte) | `gen5probe.py`, gen 1 picked from the first line (`N...` rather than a u16 length): plain LF lines, injected lines land between whole lines |
| Observer | HUD bomb count as canary: each row resets bombs to 1, sends bombs = 99 behind the row (same message, or its own message in the same frame), then again in a frame of its own ("post"). Only white digit pixels are compared, so a changed background does not count | The client's own lines (the sender id inside its `D` lines, `P` answers, state pushes) and its connections. There is no in-band canary (see below) |
| Driver | `lab/run12.sh`, `login1x.sh` (start form), `camp12.sh` (fresh login after a crash), `waitload.sh` (load guard) | the same |

Everything ran on the probe lab VM in a private network namespace with loopback only, under
Wine 9 with the GDI renderer, one client per namespace.

### Wine interventions (none touch the client files)

- **3rd to 5th Graal:** the start form's server box is greyed out and holds a fixed historical
  relay address. An `LD_PRELOAD` that sends `connect()` for that address to loopback brought
  them to the lab relay. The address lives only in the lab VM's `lab.env`.
- **6th to 13th Graal:** the greyed box holds the historical relay host name. These clients
  resolve it with `WSAAsyncGetHostByName` and a window handle of 0 **[lab]** (Wine `+winsock`
  trace). Wine posts the reply to that handle, so it never arrives, and the form hangs after
  Start with no connect. A patched copy of the exe refuses to run ("This program has been
  modified either by a virus or by a transfer problem", then "The Graal execution file is
  corrupted") **[lab]**, so the betas check their own file. `lab/sethost.pas`, a 30-line Win32
  helper built with FPC, finds the edit control holding the host name, enables it and sets the
  loopback address with `WM_SETTEXT` before Start.
- **Incomplete archives (follow-up, 2026-11-20).** The 5th Graal alpha archive has no `levels`
  folder, and the 9th Graal and 9th Graal alpha archives have no `levels` and (alpha) no graphics
  or `commands.rtf`. The missing data files were copied from the nearest numbered build (5th,
  8th, 9th); the exes were not touched. Without its start level the **5th alpha opens both relay
  sockets and closes them about 10 ms later without sending a line**, then plays offline **[lab]**
  (Wine `+winsock` trace: `connect` returns would-block on the async sockets, then
  `closesocket` on both).
- **1.21** (follow-up, 2026-11-20): it uses the combo start form of the 14th Graal–1.1.9
  layout with nickname, server (an editable list), port, account and password, and needs the
  1.28 beta 2 head, sword, shield, weapon and baddy image folders beside it
  (`../client-internals/early-clients.md`) or its character list is empty and Start fails with
  "List index out of bounds". It logs in with `GSERV007`.

## Gen 2: message and prop parsing

The results below were identical on every gen-2 build that logged in: 1.21 (`GSERV007`, added in
the follow-up), 1.28 beta 2 (`GSERV013`),
1.3 test (`GSERV014`), 1.31 (`GSERV016`), 1.32 (`GSERV018`), 1.33 (`GNW20020`), 1.34
(`GNW22030`), 1.35 (`GNW13040`), 1.36 (`GNW10050`), 1.37 (`GNW21050`), 1.38 (`GNW22060`) and
1.39 (`GNW07080`) **[lab]**. seihai-gserver accepted the 1.31 and 1.32 tokens, which GServer13
refuses ([`gserv-1999.md`](gserv-1999.md#what-the-gservers-accept)).

| Input | What the client did **[lab]** |
|---|---|
| An own prop the build does not know (40, 50, 83, 90), with any value | Stops reading the message. Props after it in the same message are lost; the next message is read normally. There is no one-byte skip as in 4.x–6.x ([`probe-targets-2026-11-18.md`](probe-targets-2026-11-18.md)). |
| A NUL byte anywhere in a message (inside a string, as a prop value, as the id byte) | Drops the rest of the **frame**, not just the message. The next frame is read normally. |
| An empty line (a lone LF) | Also drops the rest of the frame. |
| An unknown PLO id (42, 60, 110; and 30, which these builds read as "file not sent") with an empty, one-byte or text body | Ignored; the next message in the same frame is read. |
| The same ids with the binary body `ff 00 ff 00` | Rest of the frame dropped, because of the NUL. |
| Id bytes `0x1F`, `0x7F`, `0xFF` (ids −1, 95, 223) with a text body | Ignored like any unknown id. |
| `0xFF` inside the nickname, or as all three rupee bytes | Read as data; the rupee count shows the decoded number. |
| A CR (`0x0D`) after the last prop of a message | No effect. |
| A 223-byte nickname (length byte `0xFF`) | Read whole; the props after it land. |
| A prop id with no value at the end of a message | No effect on the next message. |

So a gen-2 client treats NUL and an empty line as "end of this frame". A server must not put
NUL inside a gen-2 message, and a newline-only message is not a no-op.

### Own-prop widths (PLO_PLAYERPROPS, self)

Each prop 0–40 (except 5, the canary) was sent with six layouts: one byte (`c`), GSHORT (`s`),
GINT3 (`i3`), five 7-bit bytes (`i5`), a 6-character string (`str`, 7 bytes) and a byte plus a
string (`cstr`), each followed by bombs = 99. The values were chosen so that any wrong reading
puts an unknown id (90, 65 or 66) next, which ends the message, and every layout has its own
length; so the canary lands only for the layout the client reads **[lab]**.

| Prop | 1.21 | 1.28b2 | 1.3 test | 1.31 | 1.32 | 1.33 | 1.34–1.35 | 1.36–1.38 | 1.39 |
|---:|---|---|---|---|---|---|---|---|---|
| 0 | string | string | string | string | string | string | string | string | string |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 |
| 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 7 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 8 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 9 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 10 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 11 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 12 | string | string | string | string | string | string | string | string | string |
| 13 | 5 bytes | — | — | — | — | 5 bytes | 5 bytes | 5 bytes | 5 bytes |
| 14 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | GSHORT | GSHORT |
| 15 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 16 | n/a | n/a | n/a | n/a | n/a | n/a | 1 | 1 | 1 |
| 17 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 19 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 20 | string | string | string | string | string | string | string | string | string |
| 21 | string | string | string | string | string | string | string | string | string |
| 22 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 23 | — | — | — | — | — | — | — | — | — |
| 24 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 |
| 25 | — | GSHORT | GSHORT | GSHORT | GSHORT | GSHORT | GSHORT | GSHORT | GSHORT |
| 26 | — | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 27 | — | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 |
| 28 | — | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 |
| 29 | — | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 |
| 30 | — | 5 bytes | 5 bytes | 5 bytes | 5 bytes | 5 bytes | 5 bytes | 5 bytes | 5 bytes |
| 31 | — | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 | GINT3 |
| 32 | — | — | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 33 | — | — | — | — | 1 | 1 | 1 | 1 | 1 |
| 34 | — | — | — | — | — | — | — | — | string |
| 35 | — | — | — | — | — | — | — | — | — |
| 36 | — | — | — | — | — | — | — | — | — |
| 37 | — | — | — | — | — | — | — | — | — |
| 38 | — | — | — | — | — | — | — | — | — |
| 39 | — | — | — | — | — | — | — | — | — |
| 40 | — | — | — | — | — | — | — | — | — |

`—` means no layout landed: the prop is compound (more than one field), longer than five
bytes and not a plain string, or past the build's last prop (the message ends there). `n/a`
means the canary could not be read (see below). Builds that share a column gave the same answer
on every prop.
Prop 2 (current hearts) can only be read where the value does not kill the player; the GSHORT
test value decodes as 0 hearts and opened the death menu on 1.28b2–1.33, so those builds were
swept again from prop 3 on with a fresh login. On the same builds a small X (prop 15) scrolls the
view so that the HUD digits sit over bright tiles, so prop 16 could not be read there and props
17–40 were swept a third time, again with a fresh login.

Against [`player-props.md`](player-props.md) and the static table in
[`gserv-1999.md`](gserv-1999.md#props-by-build) **[lab]**:

- **Last prop read:** 24 on 1.21, 31 on 1.28b2, 32 on 1.3 test and 1.31, 33 on 1.32: the same as
  the static table. 1.33 to 1.38 also stop at 33, and 1.39 adds 34 as a string. A higher id ends the message.
- **Prop 14 (player id) is one byte on 1.21 to 1.35 and a GSHORT from 1.36.** This is the same
  build boundary as the static one-byte vs two-byte player id in `PLO_OTHERPLPROPS`
  ([`player-props.md`](player-props.md)), now measured on the self stream.
- **Prop 13 (colours) is five bytes on every build.** The targeted rows below (five small colour
  indexes) landed on 1.21, 1.28b2, 1.3, 1.32, 1.35, 1.36 and 1.39, and three or four bytes did
  not. The sweep's five-byte test value used colour index 90: 1.21 and 1.33 and later read it,
  while **1.28b2 to 1.32 stop reading the message at an out-of-range colour index**.
- **Prop 23** has no single-field layout on any build; see the compound rows below.
- Props 30 (five bytes, the IP address) and 31 (GINT3, the UDP port) have the widths the server
  source gives, on every build.
- Props 8 to 11 read as one byte with the small test value 3; with larger values they carry an
  image, see below.

### Compound own props (follow-up, 2026-11-20) **[lab]**

Fifteen targeted rows from the server-source encodings, each followed by the bombs canary, on
1.21, 1.28b2, 1.3 test, 1.32, 1.35, 1.36 and 1.39. Every build gave the same answer:

| Prop | Layout the client reads |
|---|---|
| 8 (sword) | one byte; when it is 30 or more (power + 30) a length-prefixed image name follows. `c:31` alone (no image) desynchronises. |
| 9 (shield) | one byte; when it is 10 or more (power + 10) a length-prefixed image name follows. |
| 10 (bow) | one byte; below 10 it is the bow power alone; at 10 or more, (value − 10) raw image bytes follow (no length prefix of their own). |
| 11 (head) | one byte; below 100 it is a head number alone; at 100 or more, (value − 100) raw image bytes follow. |
| 13 (colours) | five bytes (three or four bytes desynchronise). |
| 23 (effect colours) | one byte; 0 stands alone, and any nonzero value is followed by four more bytes (the value is not a count: 9 + four bytes lands, 1 + one byte and 2 + two bytes do not). Checked on 1.21 and 1.39. |

### What the clients send unprompted

- **`PLI_PACKETCOUNT` (31)** every 10.2 s (±0.1 s) with a GSHORT count: 3 the first time, then 1
  each time while idle. 1.33 to 1.39 send it. 1.28 beta 2 to 1.32, the builds with GSERV
  tokens, never do **[lab]**.
- **Login props.** The first `PLI_PLAYERPROPS` (2) of every build carries nickname (0), head (11),
  colours (13, five bytes) and **prop 31: the client's own UDP port as a GINT3**. The value
  matched the port of the UDP socket the client process had bound (`ss -uanp` inside the
  namespace: 36729 = `22 3e 99`) **[lab]**. 1.32 and later also send prop 18 (status, 16) and
  prop 33 (0). The second message is prop 12 (chat) with an empty string. This is the client
  half of the peer-UDP endpoint question in [`gserv-1999.md`](gserv-1999.md#udp-128-beta-2-on):
  the server learns each client's UDP port from prop 31, and can pass it on with the address in
  other-player props 30 and 31, as GServer 1.28 sends them **[lab][inf]**.

### `PLO_OTHERPLPROPS` player-id width (1.35 vs 1.36): settled

[`player-props.md`](player-props.md) reads (statically) a one-GCHAR player id in 1.35 and a
GSHORT from 1.36. A first try with nickname, X, Y and sprite drew no player on 1.34–1.37 in
either form. **The missing piece is the other player's level, prop 20:** with
`20 = <the client's current level>` added (plus colours and head), the clients draw the player
**[lab]**:

| Injected `8` | 1.28b2 | 1.35 | 1.36 | 1.39 |
|---|---|---|---|---|
| one-byte id 7, then nick, level, X, Y, sprite, colours, head | not drawn | **drawn** ("one") | not drawn | not drawn |
| two-byte id 9, same props | not drawn | not drawn | **drawn** ("two") | **drawn** |
| two-byte id 11, level first, then the rest | not drawn | not drawn | **drawn** | **drawn** |

So 1.35 reads a one-byte player id and 1.36 and later a GSHORT, as the static read says, and an
other-player message is drawn only when it carries the viewer's own level. Prop order does not
matter.

**1.28b2 adds an other player on prop 50 ("joined the level") instead** (second follow-up,
2026-11-20) **[lab]**. Nothing was drawn with the level and full look, with the peer address and
UDP port (props 30 and 31) added, or with peer UDP id-0 movement datagrams sent from that port
to the client's own UDP port (which it reports as prop 31 at login). With `50 = 1` first in the
message:

| Injected `8` on 1.28b2 | Drawn |
|---|---|
| one-byte id 7, `50 = 1`, nick, level, X, Y, sprite | yes ("one") |
| two-byte id 9, the same props | no |
| one-byte id 12, `50 = 1`, nick, X, Y, sprite, **no level** | yes ("three") |

So 1.28b2 reads a one-byte player id, like 1.35, and creates the player when it sees the join
flag, whatever the level; 1.35 and later draw a player whose level matches the viewer's.

## Gen 1: the relay protocol on real clients

### Join and rooms **[lab]**

| Builds | Fixed room | Level connection |
|---|---|---|
| 1st, 2nd | `Zelda2` | joins `Zhouse12` directly |
| 3rd, 4th | `Graal` | joins `Ghouse1.graal` directly |
| 4th alpha | `Graal2` | joins `G2level13.graal` directly |
| 5th | `Graal3` | joins `G3level13.graal` directly |
| 6th to 1.1.9 | `Graal4` … `Graal8` | joins `G<n>` with no level, sends `-` and `C`, then joins `G<n>onlinestart.graal` |

Every build opens both connections at once and waits for `I<id>` on each; neither depends on
`NL` (1st to 13th got no `NL` and joined the same rooms).

### Pairing and the state push **[lab]**

A client answers `+<id>def` with `P<id>` only when it has no partner on that connection: right
after joining a room, or after the server has sent `-<partner>`. While it has a partner, a
second `+` gets no answer. When the server then sends `P<id>`, the client pushes its state to
the new partner as `D` lines carrying its own sender id:

| Builds | Level connection push | Fixed-room push |
|---|---|---|
| 1st to 4th | `T P C N S` | `L P N` |
| 4th alpha, 5th alpha (follow-up), 5th to 7th | `T P Y C N S` | `L P N` |
| 8th | `T P Y N S C` | `L P N` |
| 9th alpha (follow-up, with levels) | `T P Y N S` | none seen |
| 9th | none: it joins `G5` and `Graal5`, then sends nothing more (no move to the level room, no `P`), also with levels supplied; its start level is fetched from the historical web host, which the lab does not serve, so its rows show only that it stayed up | none |
| 10th, 11th | `T P Y N S 7` | none seen (no `P` answer on the fixed room) |
| 12th to 15th, 1.1 | `T P Y N S 7 C` | `L P N S 7` |
| 1.1.9 | none to the fake peer | none |

`T` = login time, `P` = position, `Y` = sword and shield, `C` = chat, `N` = nickname, `S` =
colours, `L` = level, `7` = a pose flag (`relay-1998.md`). 1.1.9 answered the join-time `+` with `P`
on its level connection, but sent no push and reacted to no later lobby line on an established
connection. In a two-client run (two real 1.1.9 clients on the same relay) the newly joined
client did push `T P Y N S 7` after its `P` **[lab]**. Follow-up (2026-11-20): a fake peer
announced 2, 5 or 10 s after the join got no answer at all, while the 15th Graal control
answered on both connections and pushed; sending `C<id>` before `+<id>`, as the real server
does for room members, made no difference (answer `P` only when announced at the join, never
a push). So 1.1.9 answers a peer only in a short window after joining a room, and its state
push needs something only a real peer connection provides (not identified) **[lab]**.

The 10th to 15th betas and 1.1 send `D` type `A` (arrow) lines steadily on their start level
(two level NPCs shoot), which makes their own id visible in every line.

### Own id (`I`) **[lab]**

Read from the sender id in the 10th–15th and 1.1 clients' own `D` lines:

| Line from the server | Own id afterwards |
|---|---|
| `I12345678` (8 digits) | 12345678; the two-character sender id is its low 14 bits (8526) |
| `I` + 40 nines | 99999999 (the first 8 digits); sender id = low 14 bits (8447) |
| `I123456789` (9 digits) | unchanged by the extra digit (the first 8 are the same as before) |
| `I1234567` (7 digits), `I12` | unchanged: shorter ids are ignored |
| `I1234567x` | the client stops sending its arrow lines until it is paired again |
| `I00000001` after that | the push to the next partner uses id 1 again |

So `I` is read as 8 decimal digits after the letter: a shorter id is ignored, further digits are
ignored, and the wire sender id is the id modulo 16384 (two 7-bit characters). A non-digit inside
the 8 is not ignored: it upsets the client's own arrow sending.

### Line handling **[lab]**

- No row crashed or hung any build. Lobby lines the client has no use for (bare `C`, `-` or `P`
  for unknown ids, `NR`, `NX`, an unknown letter, `D` with no sid or an unknown type, truncated
  `D` payloads, NUL or CR inside a line, an empty line) produced no reply and left both
  connections up.
- **Line length.** A 1104-byte `D` line made the 10th to 15th betas and 1.1 reset their level
  connection at once (TCP reset from the client); the fixed-room connection closed about
  3 s later. The 1st to 9th betas and 1.1.9 kept the connection. This matches the 1 KB read
  buffer in `relay-1998.md`: the later betas abort on a line that does not fit, the earlier ones
  and 1.1.9 do not.

### No in-band canary for gen 1

An idle 1998 client sends nothing on its own (except the arrow lines above) and does not redraw
under Wine, and its only answers are to `+` (when unpartnered) and `P`. So a `D` row shows only
whether the client answered, kept its connections and kept running; it cannot tell "applied"
from "ignored". The lobby probes (`w<beta>-lobby`) are the rows that carry protocol meaning.

## Open questions left

Settled in the follow-up (2026-11-20): 1.21 login and its tables; 5th and 9th Graal alpha
(missing archive data); the 1.35 vs 1.36 `PLO_OTHERPLPROPS` id width (and that an other-player
message needs the viewer's level); prop 13 (five bytes everywhere) and props 8–11 and 23.

- 9th Graal never leaves the bare `G5` room. Its online start level is not a file or a web
  download: the 9th (like the 8th, 9th alpha and 10th) loads `onlinestart.graal` from an
  embedded `ONLINESTARTLEVEL` resource **[bin]**. Serving the historical web start level over
  loopback HTTP, supplying a levels folder, or sending `NL` changed nothing, and the 9th made no
  HTTP or other connection beyond its two relay sockets (Wine `+winsock`) **[lab]**. What keeps it
  in `G5` is open.
- 1.1.9's state push needs something a real peer connection gives that a fake peer does not.
- Which gen-2 build first accepts colour index 90: 1.28b2 to 1.32 stop reading there, 1.21 and
  1.33+ do not.
