# 08 Tampercheck (PLI 39) for 2.17+ and the process list

Snapshots read: Graal_analysis `8da6800` (`protocol/client-versions.md`, `version-profiles/2.22-2.31.md/.toml`), Seihai `06aacfd` (`protocol/profile.rs`), GServer-v2 (`TPlayer.cpp` `msgPLI_MAPINFO`, `msgPLI_PROCESSLIST`, `TPlayerLogin.cpp`), the public-server report.
Folded here: **PLO_LISTPROCESSES 182** and PLI 44/45 process list.

## Naming trap
GServer-v2's older header calls PLI 39 `PLI_MAPINFO` ("might be gmap related"). The Graal_analysis notes call it `PLI_TAMPERCHECK`. **Client to server 39** is not **server to client 39** (`PLO_LEVELMODTIME`, see 06). Never mix them.

## What it is **[bin][cap]**
- New in 2.17; absent in 2.05 and 1.x. Sent right after `PLI_LANGUAGE` (37) at login: it is the second message of the client's first gen-3/gen-5 frame, after `PLI 37` `English`.
- Payload: **10 raw bytes, not two GINT5 words** (corrected 2026-10-24 from real-client lab captures). Bytes below 0x20 occur in the 2.17 and 2.22 values, which a GINT5 byte can never be, and no value contains 0x0a, so it needs no escaping on the line-framed wire.
- It is a **per-build constant**: the same 10 bytes at every login, for different accounts and different login keys.

| Build | Token | 10 bytes (hex) | Re-sent |
|---|---|---|---|
| 2.17 | `GNW22122` | `2a7bad195e231243d82c` | no (once at login; nothing more in about 90 s) |
| 2.22 | `GNW03014` | `250e4d0f962b03ede631` | once per gmap edge crossing; no periodic send in about 100 s |
| 2.31 | `GNW28015` | `291655b7602e87c9eb82` | about every 3.2 s |

  The same table is in `version-profiles/tampercheck-values.tsv`. The 2.22 value matches the earlier TOML record, so that record is confirmed.
- 2.31 only: it also sends `PLI_SHOWIMGPLAYER` (24) with a 1-byte payload (value 9 seen) about every 5.1 s, and `PLI_ENTERLEVEL` (46, 1 byte, value 1) on every level entry (login and each gmap edge crossing; it does not come with a re-sent 39, which 2.31 sends on its 3.2 s timer only). Neither was in the profile notes; the meaning of the id 24 payload is unknown. (Lab batch c: 2.22 also sends 24 = 9 about every 5.1 s while another player is in its level, 2.31 always; 2.31 sends 46 on doors, links and server warps too and re-sends no 39 there. 2.22 sends no 46 but sends 39 in the same frame as each client-initiated level-link request, not after a server-side warp: `../decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md`.) (Id 46 is settled: see the settled index in `README.md` and `../decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`; door and warp entries untested.)
- **What the bytes are (decompile pass, 2026-10-24; all six lab values reproduced offline) [bin]:** two 32-bit words A then B, each written as 5 bytes in a form that is **not** GINT5 and **not masked**: byte 1 = `((v >> 28) & 0x0F) + 0x20`, bytes 2–4 = `((v >> 21) + 0x20) & 0xFF`, `((v >> 14) + 0x20) & 0xFF`, `((v >> 7) + 0x20) & 0xFF`, byte 5 = `(v & 0x7F) + 0x20`. Only bytes 1 and 5 are range-limited, which is why bytes below 0x20 occur. Both words are standard reflected CRC-32 (polynomial `0xEDB88320`, start `0xFFFFFFFF`) over the client's **own memory image** (the running exe), chained: the first call ends with the usual final inversion and its result seeds the next call, and the last call of each word skips the final inversion. Word A covers 8–9 contiguous ranges of the code section; word B covers one large code range plus one block of static data (a table of string pointers). Nothing depends on the login key, account, level or time, so the result is a per-build constant that changes only if the exe bytes change. Words per build: `version-profiles/tampercheck-words.tsv`; full write-up: `client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md`.
- **2.31 re-send timing [bin]:** a 50 ms main-form timer keeps a counter modulo 64 (the length of the 64-character alphabet string it uses), so one cycle is 64 × 50 ms = 3.2 s. Phases: 1 anti-debug probe and a 5000 ms timer is armed; 10 recompute word A; 20 scan top-level windows against an obfuscated blacklist (not decoded); 30 recompute word B; 31 send PLI 39. The 5.1 s PLI 24 cadence fits the 5000 ms timer (inference). 2.17.1 has no such timer and 2.22 re-sends only from its level-change routine. See `client-internals/decomp-findings-2026-10-24-b/03-periodic-ids-2.31.md`.

## Exact server behaviour **[srv]**
`TPlayer::msgPLI_MAPINFO` (id 39) reads the rest of the packet and returns. **GServer-v2 does not validate it.** The lab therefore cannot tell you whether a different value would be rejected. Real servers may check; unknown.
Process list: the server sends `PLO_LISTPROCESSES` (182) once during login (2.17+). The client can answer `PLI_PROCESSLIST` (44) with a list of running programs (inferred from the names and the server's parse, not captured); `msgPLI_PROCESSLIST` parses it into a vector and ignores it. A later copy of the server also has 45 (process running). Anti-cheat only.
Also relevant: `msgPLI_NULL` counts unknown ids and disconnects after more than 5, so never send ids that are not in the client's profile `pli` set.

## Public servers
The 2026-10-24 run logged in to 4 public servers with 2.22 and **no id 39**; none disconnected within 20 s. That shows presence is not enforced at login on those four, not that it is never enforced. A real 2.31 client resends it every ~3.2 s, so a periodic check is plausible there, but no server behaviour has been observed.

## Seihai today
- Profile flag `tampercheck` exists. `send_post_login` sends LANGUAGE only (no id 39), per the report. In the lab (2026-10-24) the merged Seihai logged in as 2.17, 2.22 and 2.31 without sending it, and GServer-v2 accepted that.
- 182 and 44 are not handled.

## Steps for Claude
0. The bytes are a constant per unmodified build, so replay the table values; do not try to recompute them at run time.
1. In the 2.17/2.22/2.31 profiles add `tampercheck_bytes: Option<[u8;10]>` from the table above; send `PLI 39` right after LANGUAGE when the profile has `Some`. Version-specific re-sends (2.22 on each gmap edge crossing, 2.31 about every 3.2 s) only matter if a server is seen to enforce it.
2. Make it opt-in at first (`--send-tampercheck`) so the public-server default stays "same as the 4 servers that accepted us".
3. Handle 182 by sending nothing (or an empty `PLI_PROCESSLIST` if a server complains); log it.
4. Add a test asserting that the message after LANGUAGE in the first post-login frame is id 39 followed by exactly the 10 raw profile bytes.

## How to test
- Lab with GServer-v2: confirm the extra packet causes no error and no invalid-packet counter increase (the handler exists). Compare Seihai's frames with the 2.22 capture frame by frame (`examples/lab_replay`).
- Cannot test enforcement locally.

## NEEDS
- ~~For enforcement only: the 2.22 id-39 value builder~~ Done 2026-10-24: the decompile shows how the bytes are built (above). Computing them for a patched exe needs that exe's own code ranges, which are inside each client binary; replaying the per-build constant is enough for an unpatched client.
- The decompiles only show the sender. There is no check on the client's receive side, so whether any server enforces the value is still unknown.
- ~~For 2.17 and 2.31 values~~ Done 2026-10-24: captured from the real clients under Wine in the loopback lab (table above).
