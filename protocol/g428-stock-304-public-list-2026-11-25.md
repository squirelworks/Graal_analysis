# Public listserver: stock 3.04 Linux list login (2026-11-25)

Derived note that answers gap G428 and partly answers G427. It repeats the
[2026-11-24 `G3D30123` check](g3d30123-public-listserver-2026-11-24.md) with a
real client in place of the synthetic one-frame login.

## Setup

- **Client:** stock Graal 3.04 Linux, the shipped packed executable. An unpacked copy
  fails the client's own signature check and exits silently, so it cannot be used.
- **Where:** the Debian Linux VM on lab host B, headless under Xvfb, in a private network
  namespace. Every official host name the client's licence names resolves to the loopback
  address. A one-host bridge carries the client's single connection to the community
  listserver and refuses every other host. The official listserver was never contacted.
- **Approval:** Squirrel's written OK for the community listserver only (2026-11-25).
- **Account:** the owner's community account, typed by the owner. Login bytes,
  credentials and keys stay private.
- **Done:** one list-only login per port, no game-server login, no chat, no retries.
- **Captures:** a pcap and bridge log per port, held on the lab host. They are not in
  this repo.

A dry run against a fake gen-5 listserver inside the VM came first and sent nothing
outside the VM.

## Login sent [lab]

One plain zlib frame (wire header `78 9C`). Nothing follows it on the wire.

- id 7: key byte + `G3D30123` + `newmain`
- id 1: account + password (GSTRINGs)

The key byte changes on each run. On this run it was 52 bytes on the wire, 42 after
inflation, for a 10-character account and a 10-character password. This is the same
one-frame shape as the 2026-11-24 synthetic login, so **a stock 3.04 sends the
`Gen5OneFrame` login.**

## Result, port 14922 [lab]

The connection was accepted and the reply came about 0.5 s after the login. It was
610 bytes in two gen-5 frames (compression type 4):

| frame | wire | inflated | ids |
|---|---|---|---|
| 1 | 491 | 1067 | id 0: server list, 9 rows, 8 fields per row |
| 2 | 119 | 128 | ids 2, 3, 5, 6 |

- Server-name prefixes in the list: none, `3 `, `H `, `P ` and `U `. The client drew the
  list with Gold, Classic, Graal 3D and Hosted tabs.
- **id 2** (67 bytes): a welcome line naming the account, then
  "There are 10 server(s) online." The named account shows the login was accepted.
- **id 3** (20 bytes): the community site's URL.
- **id 5** (30 bytes): a charity donation URL.
- **id 6** (3 bytes): ASCII `000` (`30 30 30`).

There was no refusal, reset, rate-limit or ban text.

This is the same reply family as the 2026-11-24 synthetic result for 14922: the id 0 list
first, then ids 2, 3, 5 and 6 in a second frame.

## Result, port 14923 [lab]

The first 14923 attempt never left the VM: the lab VM was powered off from outside during the
pause, and the next attempt collided with a local test holding the bridge port. The third
attempt reached public 14923. The stock client always dials 14922, the port fixed in its
signed licence, so the bridge carried that connection to public 14923 with the client's bytes
unchanged.

The login had the same shape as on 14922: one plain zlib frame, 52 bytes on the wire, 42
inflated. The server sent three frames, 960 bytes, all within about 0.5 s:

| frame | wire | inflated | framing | ids |
|---|---|---|---|---|
| 1 | 350 | 582 | **plain zlib** (no compression byte, no cipher) | id 0: legacy list, 5 rows, 8 fields, no category prefixes |
| 2 | 491 | 1067 | gen 5, type 4 | id 0: modern list, 9 rows, the same size as on 14922 |
| 3 | 119 | 128 | gen 5, type 4 | ids 2, 3, 5, 6, the same as on 14922 (id 6 = `000`) |

The gen-5 cipher state starts fresh at frame 2. The plain frame does not advance it.

**The stock 3.04 cannot use 14923.** It sent FIN 17 ms after the plain legacy frame,
answered the modern list with RST, and showed an "Error / Disconnected" box on its login
screen. It never read frames 2 and 3. The client expects gen-5 frames after its login, so a
plain-zlib frame ends the session. On 14922, where the first frame is already gen 5, the client
drew the list normally.

This corrects the [2026-11-24 note](g3d30123-public-listserver-2026-11-24.md), which recorded
all three 14923 frames as gen 5. Frame 1 is plain zlib, matching the classic three-frame
reply. The row counts (5 and 9 here, 6 and 10 then) are that hour's list size.

## What this shows and does not show

- The stock 3.04 login is byte-shape identical to the synthetic one.
- **14922:** the stock client gets and draws the list. Its `confirmed` status now rests on a
  real client.
- **14923:** the server answers, but its plain-zlib legacy frame comes first and the stock
  client disconnects. The port is not usable by a stock 3.04 client.
- **G427 (id 6):** on both ports, for this account, id 6 is the 3-byte text `000`. Its meaning
  (a counter, flags or a status code) and whether it varies by account or time are not
  known. No client handler or lab listserver has been read for it yet.
- The list held 9 rows while id 2 said 10 servers were online. Row counts are that hour's
  list size, not a protocol constant. Whether the gap is a filtered server or a stale count
  is not known.
- A 3.153 Mac client was not run. It probably behaves the same, but that is untested.
