# Public listserver, first observed results (2026-10-25)

Derived note. Everything here comes from the program output and one packet capture of two runs of the read-only list check, made on the user's own Linux machine on 2026-10-25 (11:50 and 11:53 JST). The account name is masked, and no game-server address or name is recorded; rows are described by type tag, field lengths and counts only. The raw capture holds login frames and is kept private. No login frame bytes, credentials, or keys appear here.

Both runs fetched the list only: no game-server login, no chat, no warp.

## What the runs settle

| question | answer |
|---|---|
| Which listserver ports answer | 14922 and 14923 accept connections. 14921 is dead: the connection is refused at once (TCP reset to the first SYN), for any client version. |
| Port for classic (plain-frame) logins | 14923. A classic login (one plain zlib frame holding id 0 `newmain` and the id 1 account/password message, 34 bytes on the wire) got a reply there and nothing on 14922. |
| Port for the gen-5 login (2.22, 2.31) | 14922 and 14923 both answer. |
| 14922 and a classic login (the 2.17 profile) | The server accepts the connection and sends nothing at all, and it does not close; the client gave up after its 5 s read timeout (twice in two runs, same result). Whether a real 2.17 client sends something else is not known. |
| Real 2.00-era listserver reply (overnight item 13) | Observed (14923, classic login): ONE plain zlib frame, id 0 only, 4 rows of 8 fields each, no status/site/upgrade messages, no trailing NULs. The server then waits. |
| Shape of the 14922 reply | Two gen-5 zlib frames (comp byte 0x04): frame 1 = id 0 list; frame 2 = id 2 status, id 3 site URL, id 5 upgrade URL. See the layout below. |
| Shape of the 14923 reply to a gen-5 login | Three gen-5 zlib frames: the legacy list (4 rows) first, then the same two frames as 14922. The legacy list is sent straight after the id 7 handshake frame, before the client has sent its login message. |
| "9 server(s) online" against 8 rows | Nothing is dropped. The id 0 count byte was 8 and 8 complete rows followed (every row 8 fields, the payload consumed exactly). The number in the status text is the server's own text and does not match the row count (it still said 9 over 12 rows on 14923). |
| The host with missing leading characters | The server sent it that way. The host field is 15 bytes, starts with `.`, then groups of 3, 3 and 2 digits (`.ddd.ddd.ddd.dd`). The same bytes are in the legacy list and the current list. It is not a parse error. |
| The name that shows `???` | The name field carries three literal `0x3F` bytes. The `?` is on the wire, not an output artifact. (A three-byte character replaced one byte for one byte is the likely cause; that part is an inference.) |

## Frame and field layout (derived)

Client to server, gen-5 login (2.22, 2.31, and the 2.05 profile of the user's binary): two frames.
- Frame 1: plain zlib (first payload byte 0x78), 26 bytes on the wire, 18 bytes decoded: id 7, key byte, 8-byte token, list name (7 letters), LF.
- Frame 2: gen-5 frame with comp byte 0x02 (no compression), 18 bytes on the wire: the id 1 message.

Client to server, classic login (2.17 and 2.00 profiles): one plain zlib frame, 34 bytes on the wire, 26 decoded: an 8-byte id 0 message (list name) and a 16-byte id 1 message (account and password, each a length-prefixed string).

Server to client, id 0 list (decoded body): `id byte`, `count byte` (GCHAR), then per row a field-count byte (always 8 here) and 8 length-prefixed strings:
1. type prefix `X ` plus name (`P`, `U`, `H`, or no prefix for silver), 2. language (7 bytes, English), 3. description, 4. URL, 5. version text, 6. players (1 byte, `0`), 7. host, 8. port (5 digits). LF after the last row. Gen-5 frames have two 0x00 bytes after the final LF; the plain legacy frame does not.

Server to client, status frame (decoded, 118 bytes): id 2 status text of 60 bytes (two lines joined by CR: a welcome line and the "N server(s) online" line), id 3 site URL (20 bytes), id 5 upgrade URL (30 bytes), LF after each, two trailing 0x00 bytes.

Row counts on the wire: 14922 gen-5 list: 8 rows (count byte 8, decoded 933 bytes; wire 455). Legacy list: 4 rows (count byte 4; gen-5 wire 309 / decoded 458, or plain wire 306 / decoded 456). Status frame wire 113.

The legacy rows are the same fields in the same layout, all untagged (silver). Three of the four rows also appear in the current list, one does not; for the shared ones the host, port and version text are byte for byte equal. All other fields in legacy rows use the same language and player count values as the current list.

## Timing (user's link, round trip about 0.2 s)

- 14922: the reply arrives about 0.4 s after the client's second frame, both frames at once.
- 14923, gen-5 login: the legacy list arrives within a few ms of the handshake being acknowledged (before the client sends its login frame); the two current frames arrive about 0.35 s after the client's login frame. A reader that stops waiting 0.5 s after the first list leaves very little margin.
- 14923, classic login: the single reply frame arrives about 0.2 s after the login.
- 14922, classic login: no bytes for the whole 5 s, until the client closed.

## Open

- An earlier run of the 2.05 profile on 14923 failed once with "unknown gen-5 compression byte 0x78" (a plain zlib frame read by a gen-5 reader). The second run of the same command succeeded, and the capture holds only the successful one, so the frame that failed was never captured. The cause is not known.
- The binary that made the runs sent the gen-5 login for the 2.05 profile; the current main sends the classic one. So the classic login on 14923 has been observed with the 2.00 and 2.17 profiles (identical frame), and the classic 2.05 login on 14923 and 14922 follows from that, but was not run.
- A real 2.17 client's list login is unobserved; what the server wants on 14922 from 2.17 is open. A classic login to 14923 with the 2.17 profile was not tried.
- A real 2.00 client sends only id 0 and the list name (no account); Seihai's 2.00 profile sends the account too. Whether the legacy list needs the account is untested.
- Why the host has lost its leading characters, and why the status number is 9, only the server's operator can say.
- No game-server login has been made, so nothing is known yet about login frames, file requests or the tamper check from a public game server.

## Applied to the version profiles

Every profile now defaults to `listserver.graal.in` on the port that gets a list: legacy profiles (1.41 to 2.04) on 14923 and supported profiles (2.05 and later) on 14922. 14921 is dead and is not a default anywhere. The port and host the build itself carries stay in the profile as `built_in_port` and `built_in_host`. Each profile also says whether its port is `confirmed` by a public check or `assumed` from the rule: only 2.00, 2.22 and 2.31 are confirmed. The table and the reasons are in `client-internals/version-profiles/list-ports.md`.

Two cases the rule does not settle: 2.17 (a classic login on 14922 got no reply, so 14922 is the rule's port, not one a 2.17 login is known to use) and 2.05 (14922 answered the user's gen-5 2.05 binary, but a classic 2.05 login was not run).
