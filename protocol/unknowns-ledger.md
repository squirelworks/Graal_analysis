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

## Tally (2026-11-18)

| Group | Resolved | Open | Blocked |
|---|---:|---:|---:|
| Own player props on a real client (77–83, unknown ids, 0–76 widths) | 8 | 2 | 1 |
| Server→client ids no client handles (60, 78, 81, 83, 110, 156) | 5 | 0 | 1 |
| Client→server ids at our server (0–223) | 1 | 1 | 0 |
| Wire bytes (NUL and high bytes inside a message) | 1 | 1 | 0 |
| Other streams and clients | 0 | 3 | 4 |
| **Total** | **15** | **7** | **6** |

## Own player props (`PLO_PLAYERPROPS`)

| Id | Name | Question | 6.03r7 Linux | 5.24r4 Win | 4.20r8 Win | 2.31 / 2.22 Win | Status |
|---:|---|---|---|---|---|---|---|
| 83 | (unnamed) | meaning, width, range | gralat count, 5 bytes. Values up to 999,999,999 are stored (script read-back); larger ones are ignored. Same counter as prop 3. The HUD draws the low 7 digits | no case: skipped as 1 byte | no case: skipped as 1 byte | ends the message | resolved |
| 77 | ONLINESECS2 | width, effect | 5 bytes, no visible effect | skipped as 1 byte | skipped as 1 byte | ends the message | resolved |
| 78–80 | X2 / Y2 / Z2 | width, effect | 2 bytes: local x, y, height; low bit = sign | 2 bytes | 2 bytes | 2.31: 2 bytes; 2.22: ends the message | resolved |
| 81 | PLAYERLISTCATEGORY | width | 1 byte | 1 byte | 1 byte | ends the message | resolved (effect on the player list: open) |
| 82 | COMMUNITYNAME | width | string | string | skipped as 1 byte | ends the message | resolved |
| 84–90 | (none) | how an unknown id is skipped | id + 1 byte; a longer value loses the rest of that message only | the same | the same | ends the message | resolved |
| 0–76 | (named) | do the documented widths hold? | yes, for every id with a case; 33, 50, 51, 53, 75 and 76 have no case and are skipped as 1 byte | open (`widths.plan`) | open (`widths.plan`) | — | resolved for 6.03r7 |
| 81 | PLAYERLISTCATEGORY | what it changes | — | — | — | — | open: needs a second client looking at the player list |
| any | — | Windows 6.037 | — | — | — | — | blocked: runs only in the Win10 VM |

## Server→client ids that no client handles

| Id | gs2lib name | Result on 2.22, 2.31, 4.20r8, 5.24r4 and 6.03r7 | Status |
|---:|---|---|---|
| 60 | `PLO_UNKNOWN60` | Ignored with an empty, one-byte or text body; no reply, no crash | resolved |
| 78 | `PLO_NC_CONTROL` | The same | resolved |
| 81 | `PLO_UNKNOWN81` | The same | resolved |
| 83 | `PLO_UNKNOWN83` | The same | resolved |
| 110 | `PLO_UNKNOWN110` | The same | resolved |
| 156 | `PLO_SETACTIVELEVEL` | The extra step in 2.31 | blocked: needs a visible effect to look for; static reading first |

## Client→server ids at our server

| Item | Result | Status |
|---|---|---|
| Every id 0–223 with an empty body, sent to our GServer-v2 build | Handled set measured. Three unknown ids disconnect the client. Unchecked bodies: 17 (makes a type-224 baddy that crashes 6.03r7), 31, 41 and 130. 39 (tamper check) gets no reply. seihai-gserver-v2#103 | resolved |
| The same sweep against seihai-gserver (Rust) | A 6.x-capable seihai-gserver world in the lab | open |

## Wire bytes

| Item | Result | Status |
|---|---|---|
| A NUL byte inside a message on 2.22 | Loses the rest of the frame; `ff`, `80` and `1f` are harmless; 4.20r8 is unaffected | resolved |
| 2.31: why `ff 00 ff 00` lost the next packet after ids 60, 78, 81 and 83, but not after 110 | Run `bytes2x.plan` on 2.31 | open |

## Other streams and clients

| Item | Status | Why |
|---|---|---|
| Other-player props 77 and 83 (`PLO_OTHERPLPROPS`) | open | needs a second lab client in the level as the observer |
| NPC props 48–52 | open | needs a level NPC with a visible prop after the tested one |
| Baddy props 11 and up, and the baddy type range a client accepts | open | type 224 crashes 6.03r7; the valid range is not measured |
| 6.1.1.3 | blocked | RC4 after a server-sent connector script; no loopback login yet (`v6113-status.md`) |
| Windows 6.037 | blocked | runs only in the Win10 VM (packed, clock-gated) |
| 2.00 to 2.21 (gen 2, 3, 4) | blocked | the proxy speaks gen 5 only |
| Mobile clients | blocked | no lab path to a mobile client yet |
