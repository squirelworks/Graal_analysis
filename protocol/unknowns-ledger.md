# Unknowns ledger: packets, props and fields

Date: 2026-11-18

This is the running tally for the probe work (`../tools/probe/`). It lists every packet id,
prop and field that our notes mark as unknown, unnamed, untraced or not checked on a real
client, with the status of each. Lab rows are in [`probe-results.tsv`](probe-results.tsv), and
the write-up is [`probe-targets-2026-11-18.md`](probe-targets-2026-11-18.md).

Status words:

| Status | Meaning |
|---|---|
| **resolved** | Checked on a real client or on our server in the lab. The result agrees with, or corrects, the static reading. |
| **open** | Not checked yet, but reachable with the clients and servers we have. |
| **blocked** | No client or server we can run reaches it yet. The reason is in the row. |

## Tally (2026-11-19, round 3)

| Group | Resolved | Open | Blocked |
|---|---:|---:|---:|
| Own player props on real clients (77–83, unknown ids, widths 0–90) | 8 | 1 | 0 |
| Server→client ids (60, 78, 81, 83, 110 unhandled; 156; 195 LOADGANI list) | 7 | 0 | 0 |
| Client→server ids at our server (0–223) | 1 | 1 | 0 |
| Wire bytes (NUL and high bytes inside a message) | 2 | 0 | 0 |
| Baddy types | 1 | 0 | 0 |
| Other streams and clients (other-player, injected player, NPC, baddy props, 2.00–2.17; 6.1.1.3, 6.037, 2.19–2.21, mobile) | 5 | 0 | 4 |
| Early clients, gen 1 relay and gen 2 GSERV/GNW (1st Graal to 1.39) | 8 | 5 | 0 |
| **Total** | **32** | **7** | **4** |

**Early clients (2026-11-19, [`early-clients-probe-2026-11-19.md`](early-clients-probe-2026-11-19.md)):** gen-2 parse rules, `PLI_PACKETCOUNT` cadence, prop 31 as the UDP port, own-prop widths per build, and the relay join, pairing, `I` and line-length rules on 18 betas.

**New this round (resolved):**
- 2.00–2.17 can now be probed (gen 3 in the proxy; 2.05 and 2.17.1 run).
- The other-player stream on 6.03r7.
- What makes 6.03r7 draw an injected player.
- The 2.31 / PLO 110 case.

## Own player props (`PLO_PLAYERPROPS`)

| Id | Name | Question | 6.03r7 Linux | 5.24r4 Win | 4.20r8 Win | 2.31 / 2.22 Win | Status |
|---:|---|---|---|---|---|---|---|
| 83 | (unnamed) | meaning, width, range | gralat count, 5 bytes. Values up to 999,999,999 are stored (script read-back); larger ones are ignored. Same counter as prop 3. The HUD draws the low 7 digits | no case: skipped as 1 byte | no case: skipped as 1 byte | ends the message | resolved |
| 77 | ONLINESECS2 | width, effect | 5 bytes, no visible effect | skipped as 1 byte | skipped as 1 byte | ends the message | resolved |
| 78–80 | X2 / Y2 / Z2 | width, effect | 2 bytes: local x, y, height; low bit = sign | 2 bytes | 2 bytes | 2.31: 2 bytes; 2.22: ends the message | resolved |
| 81 | PLAYERLISTCATEGORY | width | 1 byte | 1 byte | 1 byte | ends the message | resolved (effect on the player list: open) |
| 82 | COMMUNITYNAME | width | string | string | skipped as 1 byte | ends the message | resolved |
| 84–90 | (none) | how an unknown id is skipped | id + 1 byte; a longer value loses the rest of that message only | the same | the same | ends the message | resolved |
| 0–76 | (named) | do the documented widths hold? | yes, for every id with a case; 33, 50, 51, 53, 75 and 76 have no case and are skipped as 1 byte | yes; no case for 33, 50, 51, 53, 75, 76, 77, 83 | yes; no case for those and 82 | — | resolved |
| 81 | PLAYERLISTCATEGORY | what it changes | — | — | — | — | open: needs the player-list window opened on a client that has a second player |

## Server→client ids that no client handles

| Id | gs2lib name | Result on 2.22, 2.31, 4.20r8, 5.24r4 and 6.03r7 | Status |
|---:|---|---|---|
| 60 | `PLO_UNKNOWN60` | Ignored with an empty, one-byte or text body; no reply, no crash | resolved |
| 78 | `PLO_NC_CONTROL` | The same | resolved |
| 81 | `PLO_UNKNOWN81` | The same | resolved |
| 83 | `PLO_UNKNOWN83` | The same | resolved |
| 110 | `PLO_UNKNOWN110` | The same | resolved |
| 195 | `PLO_LOADGANI` list | resolved for 4.20r8, 5.24r4, 6.03r7: gani header lines (`SETBACKTO`, `LOOP`) that override the file for the named gani, newest wins, lost if sent before the gani loads; redundant for file ganis. Round 2: `CONTINUOUS`, `SINGLEDIRECTION` and `LOOP` taken too; `DEFAULT*` no effect seen; a 195 or a forged `PLO_GANISCRIPT` for an unloaded gani makes the client load it; names are case-insensitive; other players and 5.12 match. 2.22 and 2.31 ignore 195 (lab). `DEFAULT*` lines (head, body, attr1–3, shield, sword, horse, param1) change nothing for the player's own character on 6.03r7 and 4.20r8, and no named file is fetched ([fuzz](../live-runs/fuzz-2026-11-19/README.md)). Open: `DEFAULT*` on an NPC with no head of its own, 6.1.1.3, 6.037 | resolved |
| 156 | `PLO_SETACTIVELEVEL` | The extra step in 2.31 | resolved: sends pending `graal://` start parameters once as a `serverstartparams` trigger action; confirmed on 2.31 under Wine ([note](plo-156-setactivelevel-231.md), [lab](lab-baddyprops-ganiscript-156-2026-11-19.md)). Fuzz on 2.22 and 2.31: no screen change for the current, neighbour, empty or unknown name, and later board and prop updates still land; a gmap name makes both ask for the gmap file (`PLI_UPDATEFILE`) ([fuzz](../live-runs/fuzz-2026-11-19/README.md)) |

## Client→server ids at our server

| Item | Result | Status |
|---|---|---|
| Every id 0–223 with an empty body, sent to our GServer-v2 build | Handled set measured. Three unknown ids disconnect the client. Unchecked bodies: 17 (makes a type-224 baddy that crashes 6.03r7), 31, 41 and 130. 39 (tamper check) gets no reply. seihai-gserver-v2#103 | resolved |
| The same sweep against seihai-gserver (Rust) | A 6.x-capable seihai-gserver world in the lab | open |

## Wire bytes

| Item | Result | Status |
|---|---|---|
| A NUL byte inside a message on 2.22 and 2.31 | Loses the rest of the frame on both; `ff`, `80` and `1f` are harmless; 4.20r8 is unaffected | resolved |
| 2.31: why `ff 00 ff 00` lost the next packet after ids 60, 78, 81 and 83, but not after 110 | The canary after 110 went out in a frame of its own (0.2 s later), so it never met the NUL byte. 2.31 behaves like 2.05, 2.17.1 and 2.22. The proxy now takes `s2c A \| B` for one frame | resolved |

## Other streams and clients

| Item | Status | Why |
|---|---|---|
| Other-player props 77 and 83 (`PLO_OTHERPLPROPS`), 6.03r7 | resolved | 77 and 83 (and 90) have no case: the rest of the message is dropped; 81 is 1 byte, 82 a string, 78 2 bytes (run `opp-a`) |
| Does an injected player need the server or UDP? | resolved | Neither. The server's own other-player message, replayed under an unknown id, draws a new player; 6.03r7 draws a player only once it has prop 10 (`GANI`) (runs `tc-c`, `opv-a`) |
| NPC props 48–52, 74–78 (6.03r7) | resolved | 48–52 and 78+ drop the rest of the message; 75–77 are two bytes; a CLASS the client lacks stops the NPC script. 4.20r8 and 5.24r4: the same widths; 74 ends the message there ([fuzz](../live-runs/fuzz-2026-11-19/README.md)). 2.22 and 2.31 not run yet |
| Baddy type range a client accepts | resolved | 6.03r7 survives 0–24 and quits on 25 and 31; 4.20r8 and 2.22 survive every type up to 223 |
| Baddy props 11 and up | resolved | 6.03r7 has cases for 0–10 only; any id of 11 or more ends the message, so later props are lost (static read, then a mode-9 kill canary, run `kc`; [lab](lab-baddyprops-ganiscript-156-2026-11-19.md)). 4.20r8 and 2.22 are the same: ids 11–30, as a byte or a string, lose the rest of the message (silent mode-10 baddy, mode 0 as the canary, `PLI_BADDYPROPS` as the observer; [fuzz](../live-runs/fuzz-2026-11-19/README.md)) |
| 6.1.1.3 | blocked | RC4 after a server-sent connector script; no loopback login yet (`v6113-status.md`) |
| Windows 6.037 | blocked | runs only in the Win10 lab VM (8 GB); booting it on Mirae now would leave about 3 GB free, under the host-stability rule. The host side is ready: the proxy runs on Windows with a TCP control port (`tcp:PORT`) |
| 2.00 to 2.17 (gen 3) | resolved | the proxy speaks gen 3; real 2.05 rev 2 and 2.17.1 probed (runs `w205-b`, `w217-b`) |
| 2.19 to 2.21 (gen 4) | blocked | the proxy has gen 4 from server source, but no 2.19–2.21 binary is held |
| Mobile clients | blocked | iPhone codec now known: Classic+ 1.13 is desktop gen 5 with round-down for compressed bodies, which the proxy already speaks ([note](ios-classic-plus-113-framing.md)). Still blocked on running it: no 32-bit iOS device or emulator, no Android package on the lab hosts, no KVM in the Linux VM |

## Early clients (gen 1 relay, gen 2 GSERV/GNW)

From [`early-clients-probe-2026-11-19.md`](early-clients-probe-2026-11-19.md); rows `w1xx-*` and `w<beta>-*` in `probe-results.tsv`.

| Item | Status | Why |
|---|---|---|
| How 1.28b2–1.39 parse an unknown own prop, a NUL, an empty line, unknown PLO ids | resolved | unknown prop ends the message (no skip); NUL or an empty line drops the rest of the frame; unknown PLO with a text body is ignored; same on all 11 builds |
| Own-prop widths 0–40, 1.28b2 to 1.39 | resolved | width sweep with a white-digit bomb canary; table in the note |
| C>S `PLI_PACKETCOUNT` (31) | resolved | every 10.2 s with a GSHORT count, 1.33 to 1.39 only; the GSERV builds never send it |
| C>S own prop 31 at login | resolved | the client's own UDP port as GINT3 (matched the bound socket); 1.32+ add props 18 and 33 |
| Relay join and rooms, 1st Graal to 1.1.9 | resolved | 1st–5th join the level room directly; 6th on join `G<n>`, leave, re-join `G<n>onlinestart.graal`; fixed rooms `Zelda2`, `Graal`, `Graal2`…`Graal8` |
| Relay pairing and state push | resolved | `+` answered with `P` only when unpartnered; the server's `P` triggers a `D` push whose types grow by build (`Y` from 4th alpha, `7` from 10th) |
| Relay `I` (own id) | resolved | 8 decimal digits; shorter ignored; sender id = id mod 16384 |
| Relay line length | resolved | 10th–15th and 1.1 reset the connection on a 1104-byte line; 1st–9th and 1.1.9 keep it |
| `PLO_OTHERPLPROPS` player-id width on 1.35 vs 1.36 | open | neither id form drew a player on 1.34–1.37; needs a second real client |
| Own props with no simple layout (23 on 1.34–1.39, and the `—` cells) | open | sweep two-field layouts (byte + byte, byte + GSHORT) |
| 1.1.9 state push to a fake peer | open | answers the join `+` with `P` but pushes nothing and ignores later lobby lines; a real second 1.1.9 does get a push |
| 1.21 | open | different start form; tree prepared (1.28b2 image folders), login not attempted |
| 5th Graal alpha, 9th Graal alpha | open | never reached the relay in two tries each (9th alpha needed `commands.rtf` first) |
