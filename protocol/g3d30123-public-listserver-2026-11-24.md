# Public listserver: `G3D30123` one-frame login (2026-11-24)

Derived note. One list-only check on the owner's machine (Asia/Tokyo afternoon): the 3.x listserver hello (`G3D30123` + `newmain`) against `<list-host-reborn>` on port **14922**, then **14923**, with a generous pause between the two sessions. No game-server login, no chat, no warp, no retries. The account name is masked; login-frame bytes, credentials and keys stay private. Closes the open point in [`login-tokens-3x-7x.md`](login-tokens-3x-7x.md) (line 98) and the "assumed" port status for 3.04 / 3.153 in [`list-ports.md`](../client-internals/version-profiles/list-ports.md).

## Login sent

One plain zlib frame (default level, wire header `78 9C`), holding both messages, matching the real 3.04 lab shape (**[cap]** `version-profiles/lab-304-linux-2026-10-30.md`):

- id 7: key byte + `G3D30123` + `newmain` + LF
- id 1: account + password (GSTRINGs) + LF

Wire length was 44 bytes (34 clear). This is Seihai's `Gen5OneFrame` shape, not the two-frame 2.22/2.31 gen-5 login (`GNW30123` handshake then a separate gen-5 id 1).

## Result

| port | connect | reply | shape (decoded) |
|---|---|---|---|
| 14922 | accepted | **modern list** | two gen-5 zlib frames (ctype 4): id 0 list (**10** rows), then ids 2, 3, 5 and 6 (status / site / upgrade / one extra id) |
| 14923 | accepted | **legacy list then modern list** | three gen-5 zlib frames (ctype 4): id 0 (**6** rows), id 0 (**10** rows), then the same status frame as 14922 |

So a `G3D30123` login is answered on both ports, in the same reply family as the 2026-10-25 gen-5 (`GNW30123`) matrix in [`listserver-login-type-matrix-2026-10-25.md`](listserver-login-type-matrix-2026-10-25.md). The token prefix alone does not change the public service's port rule for gen-5-shaped list logins.

- No refuse, reset, rate-limit or ban text was seen.
- Row counts (6 / 10) are that afternoon's list size; they are not a protocol constant.
- Id **6** on the status frame was present on both ports; its layout was not traced this run (earlier public notes listed 2, 3 and 5 only).

Correction (2026-11-25): on 14923 the first (legacy) frame is plain zlib, not gen 5. A stock 3.04 client disconnects on it; see [`g428-stock-304-public-list-2026-11-25.md`](g428-stock-304-public-list-2026-11-25.md).

## Defaults that follow

`3.04` and `3.153` keep default port **14922** (`supported` / gen-5 family). `port_status` moves from **assumed** to **confirmed** for both: Seihai's own 3.x list login got a list on that port. A real 3.04 / 3.153 client was not captured against the public service in this run.

## What this does not show

- A stock 3.04 Linux or 3.153 Mac client was not used; only the documented one-frame wire shape.
- No game-server login followed the list.
- Id 6 on the status frame is observed only; content and meaning stay open.
