# Listserver login frames, real clients against Seihai (2026-10-25)

Derived note. Structure and sizes only. No account, password, key byte or raw login frame appears here; the account and password fields are described by length alone. Sources: lab captures of real clients against a private loopback listserver (2.05, 2.17.1, 2.22, 2.31), a lab capture of a real 2.00 (client side only), the public-listserver matrix run of 2026-10-25 22:43 JST (Seihai only, 38 runs), and Seihai `origin/main` 21a37a5 (`net/mod.rs` `login_listserver`, `protocol/chain.rs`).

## Question

Does every real Graal client version encode its listserver login differently (beyond a version tag), so that Seihai's one classic frame, sent for every profile from 1.41 to 2.17, looks fake to the public listserver on 14922 (silent) while 14923 answers?

## Short answer

No per-build difference exists in the real clients we could observe. The listserver login differs by client **generation**, in three shapes. Inside a generation every observed build sends the same bytes (2.22 and 2.31 send the same token and the same structure). Seihai's classic frame for 2.17 matches the real 2.17.1 frame in structure; what it does not match is the real 2.00/2.05 frame (id 0 only) and, apart from the two-byte zlib header, nothing else. For 2.1 to 2.16 no real client was ever observed, so no claim about "what a real one sends" can be made.

## The three real shapes

| Shape | Builds observed (real client) | Client to listserver | Notes |
|---|---|---|---|
| A: list name only | 2.00 (lab, client side), 2.05 (lab, 14921) | ONE plain zlib frame, 9 bytes decoded (id 0 + list name `newmain` + LF), 17 bytes on the wire. Nothing else. No account, password, token or key. Client then closes. | The 2.05 receive handler reads only ids 0 and 1; its send path is the base one (no cipher). |
| B: id 0 then id 1 | 2.17.1 (lab, 14922 from signed `arrays2.dat`) | ONE plain zlib frame holding two messages: id 0 `newmain`, id 1 (length-prefixed account, length-prefixed password), LF. No token, no key, no cipher. Reply: two plain zlib frames. | Built-in host list is `arrays2.dat` (host, port 14922, fallbacks). |
| C: id 7 + gen-5 | 2.22, 2.31 (lab, 14922) | Frame 1 plain zlib, 18 bytes decoded: id 7, one key byte, token `GNW30123`, `newmain`, LF (26 on the wire). Frame 2 gen-5, comp byte 0x02, then id 1 (account, password) XOR-ciphered with the key. | The same listserver token for 2.22 and 2.31. It is not the game build token (`GNW03014`, `GNW28015`). |

Per-build tokens (`GNW24011` for 2.00, `GNW03081` for 2.05, `GNW22122` for 2.17.1 ...) exist, but they go to the **game server** login, not to the listserver. Only shape C carries a token to the listserver, and it is one shared token.

Built-in listserver data from the binaries (no capture): 1.42 `<list-host-classic>:14921`, list name `newmain`; 2.00 to 2.05 the same, DES-hidden; the 2.1 test builds carry port 14922. 1.41: only a patched copy survives, original unknown.

## Real versus Seihai, per profile (Seihai main 21a37a5)

Seihai picks the shape by cipher generation: Gen5 gives C, everything else gives B (id 0 plus id 1). It never sends A.

| Profile | Real client login (evidence) | Seihai login | Same structure? |
|---|---|---|---|
| 1.33 to 1.39 | no listserver | fetches as 2.05 (B) | n/a |
| 1.41 | unknown (no binary with original host) | B | unknown |
| 1.42 | built-in host and list name known, wire frame never captured; expected A | B | probably not (extra id 1) |
| 2.00 | A (lab capture) | B | no: Seihai adds id 1 with account and password |
| 2.01, 2.02, 2.02 rev2, 2.03, 2.04 | no capture; same built-in list as 2.00/2.05, so expected A | B | probably not |
| 2.05 | A (lab capture) | B | no |
| 2.1 to 2.16 | no binary, no capture (2.1 test builds carry port 14922; wire frame never captured) | B | unknown; B is only a guess from 2.17 |
| 2.17 (2.17.1 binary) | B (lab capture) | B | yes, byte-for-byte after decompression; differs only in the zlib header (below) |
| 2.22 | C (lab capture) | C | yes (id 7 frame and the gen-5 id 1 frame decode to the same layout; sizes equal for the same account) |
| 2.3 | no binary; assumed C | C | assumed |
| 2.31 | C (lab capture) | C | yes |

### One byte-level difference that applies to every Seihai frame

The real clients compress with zlib at the best level: the stream starts `78 DA`. Seihai's zlib starts `78 9C` (default level). The deflate bodies and the checksum are identical for the same plaintext (checked on real 2.05, 2.17.1, 2.22, 2.31 frames against Seihai). The public service answers Seihai's gen-5 frames (2.22, 2.3, 2.31) with the `78 9C` header, so the header is not what makes the classic frame fail on 14922.

## What the matrix shows (public service, Seihai only)

- Every classic profile (1.41, 1.42, 2.00, 2.01, 2.02, 2.02 rev2, 2.03, 2.04, 2.1, 2.12 to 2.17; 15 profiles) sent the identical frame: one plain zlib frame, 34 bytes on the wire, 26 decoded: id 0 `newmain` (9 bytes) then id 1 with a 4-byte account and a 9-byte password field (account and password masked here). Build token, version and client type do not appear. A server cannot tell these profiles apart.
- 14922: connection accepted, no byte back, no close, 5 s read timeout, for all of them.
- 14923: one plain zlib frame back after about 0.4 to 0.6 s, id 0 only, no status, site or upgrade messages, no trailing NUL bytes. Two shapes appeared with the same request: 4 rows without type prefixes (1.42, 2.00 to 2.04, 2.12, 2.14 to 2.17, 2.22) and 2 rows with `P ` and `H ` type prefixes (1.41, 2.02 rev2, 2.1, 2.13). The shape does not follow the version (2.1 and 2.13 got the short one, 2.12 and 2.14 the long one) and does not follow the request (identical). It looks server-side (alternating or cached views). Nothing in the reply carries a version or acceptance line.
- Gen-5 profiles (2.22, 2.3, 2.31) got the modern list on both ports; on 14923 they also got the legacy list first (4 rows plain for 2.22, a gen-5 frame for 2.3 and 2.31, and a longer list, 17 rows total, for 2.31).

## Problem in the matrix data: the 2.05 rows are not a classic 2.05 login

The 2.05 runs sent shape C (id 7 with `GNW30123`, gen-5 second frame), and the public service answered it on both ports. Seihai main sends B for 2.05 (a unit test asserts it). The cause is in `bin/main.rs`: when the parsed version equals the default (2.05), the saved GUI version from the settings file replaces it, even when `--version 2.05` was given on the command line. The user's GUI had a gen-5 version saved, so every `--version 2.05` run ran as that profile. Consequences:

1. The matrix and the first user run have no real 2.05 data point. "2.05 got the modern list on 14922" is the saved profile's result.
2. The port rule "2.05 and later use 14922" rests on gen-5 logins only (2.22, 2.3, 2.31 and the masked 2.05 runs). A classic 2.05 (B) was never tried on the public service. Likely result on 14922: silent, like the other classic profiles.
3. The fix is one line: apply the saved version only when `--version` was not given (`version_given` is already tracked). Not done in this note's work.

## Does the evidence support "classic logins look fake"?

- For a version tag: there is none in classic frames at all, in the real clients as well as in Seihai. The real 2.17.1 frame has none either.
- For a per-version encoding: none exists inside a generation. 2.22 and 2.31 are identical on the wire; 2.00 and 2.05 are identical; the classic frame has no field that could carry a build.
- What the data does show: the public service answers gen-5 logins (shape C) on 14922 and ignores the 2.17-style frame (shape B) there. A real 2.17.1 sends shape B to 14922 (its signed `arrays2.dat` says so). Whether the public service answers a real 2.17.1 on 14922 was never observed; if it also ignores it, the real client falls back to the other hosts in `arrays2.dat`, or the service simply does not support classic logins on 14922 (consistent with 14923 being the legacy port).
- The only detectable differences between Seihai's B frame and the real 2.17.1 B frame are the two zlib header bytes (`9C` against `DA` as second byte, with the matching header check bits). The gen-5 evidence says the header is not checked, but it was not tested on a classic frame.

## What Seihai would change to look like the real clients

1. 2.00 to 2.05 (and 1.42, 2.01 to 2.04 as a best guess): send shape A, id 0 plus `newmain` only. This is a real, captured difference. Port 14923 would still be expected to answer (the legacy port answered B, and A is what the real clients send there).
2. All shapes: compress with the best zlib level (header `78 DA`) so the stream matches the real clients byte for byte. Cheap and risk-free.
3. 2.1 to 2.16: nothing to match against. Keep B (the 2.17 shape) or A and keep it marked inferred.
4. Fix the saved-version override so `--version 2.05` really runs 2.05.

## Confidence

- High: the three shapes; that 2.22 and 2.31 are identical to Seihai in structure; that 2.00/2.05 send id 0 only; that all 15 classic Seihai profiles send one identical frame; the zlib header difference; the matrix replies.
- Medium-high: the 2.05 override explanation (read from code and consistent with the gen-5 frames in the 2.05 runs; the user's saved version has not been inspected).
- Low: why 14922 stays silent for B (never tested with a real 2.17.1 or with a `78 DA` classic frame); whether 1.41, 1.42, 2.01 to 2.04 send A or something else; what 2.1 to 2.16 send.

## Captures that would settle it (all read-only list requests)

1. A real 2.17.1 client (`Graal_2171.exe`, pristine, its signed `arrays2.dat`) run on a machine that can reach the service, with a packet capture, started and closed at the list. Settles whether a real classic login also gets nothing on 14922, and what a real client does next (falls back, retries, or shows a list).
2. A real 2.00 or 2.05 client with its built-in host redirected to the public listserver on 14923 (hosts file), capturing the list exchange. Settles shape A on the real service.
3. Seihai, after the override fix: one list request each for the classic 2.05 profile on 14922 and 14923, plus a build with `78 DA` compression for 2.17 on 14922. If `78 DA` makes 14922 answer, the header is the tell; if not, 14922 simply does not serve classic logins.
