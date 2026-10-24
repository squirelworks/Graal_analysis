# Lab findings: PLI 46, PLO 186 trailer, 2.00 listserver handshake (batch b2, 2026-10-24)

Derived facts only. Lab-only runs (loopback network, private display, placeholder accounts). No public server was contacted. Tables are under `version-profiles/`:

| Table | Content |
|---|---|
| `lab-enterlevel-231.tsv` | the seven PLI 46 sends of one 2.31 run, with the props that follow |
| `lab-boardmodify2-186-trailer.tsv` | the six `PLO_BOARDMODIFY2` test cases on 2.22 and 2.31 |
| `lab-200-listserver-handshake.tsv` | the 2.00 listserver and gserver handshake, step by step, with provenance |

## How to read the provenance
- **Observed** means a real client talking to the stock lab servers, with nothing in between that changed the traffic.
- **Synthetic** means the lab needed a lab-only helper in the path. Two results rest on one:
  - The **2.00 listserver reply** was not sent by a real listserver. The lab listserver only answers a 2.17-style request, so a forwarder added such a request upstream after the client's frame. What 2.00 accepts is confirmed; what a real 2.00-era listserver sends is **unobserved**.
  - The **id 186 frames** were injected by a re-encoding proxy. Stock GServer-v2 defines the id only as an unknown packet and never sends it, and its scripting has no raw-packet send. So the client reactions below are real, but no server of any kind has been seen sending 186.

## PLI_ENTERLEVEL (46), real 2.31 client [observed]
- Payload is always one byte, `GCHAR 1`. It is **not** a login one-shot: it is sent on every level entry. One run produced 7 sends: login plus six gmap edge crossings (east, west, east, west, south, north). Table: `version-profiles/lab-enterlevel-231.tsv`.
- Order inside the client's frame: 46 first, then the props message that carries the cell prop (43 for a horizontal crossing, 44 for a vertical one) and the wrapped local coordinate. At login it is the first message of the second client frame, before PLI 35 (adjacent levels) and PLI 44.
- It is client-initiated and does not wait for the server. The server's answer to a crossing is the same as for 2.22 (level name, mod time, board, gmap name, 174, 10, 42, 156).
- **2.31 does not re-send the tamper check (id 39) at a crossing.** Its 39 stays on the 3.2 s timer, and 24 stays about every 5.1 s. 2.22 is the build that re-sends 39 at a crossing.
- Not tested: a level change that is not a gmap edge crossing (door, warp). The "every level entry" wording rests on the gmap crossings plus login.
- Not sent by 2.17 or 2.22 (client id sets in `version-profiles/2.22-2.31.md`).
- Emulation rule for a 2.31 profile: send PLI 46 = `GCHAR 1` at login and on each level change, just before the props message that changes the cell prop.

## PLO_BOARDMODIFY2 (186), 2.22 and 2.31 [client reaction observed, frames synthetic]
Layout: `GCHAR mapX, mapY, x, y, w, h`, then `w*h` GSHORT tiles. Results, identical on 2.22 and 2.31 (`version-profiles/lab-boardmodify2-186-trailer.tsv`):
- The handler's length check is "at least `6 + 2*w*h`". Bytes after the tiles are **unread padding**.
- A trailer of arbitrary bytes has no effect and does not disconnect.
- A complete second record placed in the trailer is **not applied**.
- One byte short of `6 + 2*w*h` is rejected silently: nothing is drawn and the client stays connected. A payload that is much shorter behaves the same.
- A block that runs past board column 63 is **clipped**, not rejected: only the columns inside the board are drawn.
- Not tested: `mapX`/`mapY` other than the current cell, or out of range.

## 2.00 listserver handshake [client side observed, list reply synthetic]
Setup: the 2.00 exe run beside a copy of the 2.22 data folder, plus `objects.dat`, which 2.00 needs and the 2.22 folder does not contain (it came from a NewMain 26 folder). The hidden list host resolved through a per-namespace hosts file, so the exe was not patched. Table: `version-profiles/lab-200-listserver-handshake.tsv`.
- **Observed:** the client sends **one** plain zlib frame: `GCHAR 0` + `newmain` + LF, then half-closes. No account, password, token or key. This differs from 2.17, whose first frame also carries `GCHAR 1 account password`.
- **Synthetic:** the list reply (two plain zlib frames: id 0 list; ids 2, 3, 5) came from the lab listserver after a forwarder injected a 2.17-style request. 2.00 parsed and drew it, so the 2.17-style reply format is **accepted** by 2.00. What a real 2.00-era listserver replies to the bare `newmain` request is **still unobserved**.
- **Observed:** pressing Connect opens no second listserver connection. The client goes straight to the gserver with type 0, key byte, `GNW24011`, `GCHAR len + account`, `GCHAR len + password`, then gen-3 framing (junk-byte rule, 0 mismatches). The lab server's allowed-versions entry for `GNW24011` was enough; no patch.
- **Observed:** first client ids after login: 34, 23, 18 (twice, the gr.x and gr.y flags), 2. None of 37, 39, 46, 24 or 44 appear. The server's 168, 190, 194, 47 and 182 are ignored without a disconnect.
- **Data-file caveat:** the 2.22 data folder alone is not enough for 2.00; `objects.dat` is missing there.
