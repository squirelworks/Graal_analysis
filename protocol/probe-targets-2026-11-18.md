# Probe targets: unknown packets and props

Date: 2026-11-18

This note lists the ids and props that our notes still mark as unknown, unnamed or "not
traced", and how the probe harness (`../tools/probe/`) can test each one on a real client.
Results go in [`probe-results.tsv`](probe-results.tsv). Sources: [`packet-ids.md`](packet-ids.md),
[`player-props.md`](player-props.md), [`v5-props.md`](v5-props.md),
[`unknown-ids-2026-11-06.md`](unknown-ids-2026-11-06.md), `../manual/app-b-props.md`.

Clients the harness can drive:

- **Now:** the native Linux 6.03r7 client (gen 5), through `tools/probe/lab/run603.sh`.
- **Need only a runner:** Windows 4.20r8, 5.12, 5.24r4 and 6.037 (all gen 5). They already run under Wine in the same VM.
- **Need a gen-2/3 codec in the proxy:** the 2.x clients.
- **Out of reach:** 6.1.1.3, until a loopback connector harness exists ([`v6113-status.md`](v6113-status.md)).

## Priorities

| Pri | Target | Direction | Question | What static reading says | Probe |
|:-:|---|---|---|---|---|
| 1 | Player prop 83 | S→C self | What it sets, value range, width | 6.0.3.7 and 6.1.1.3: five-byte number, applied when ≤ 999,999,999 **[bin]** | **Done on 6.03r7** |
| 1 | Unknown own prop id with a long value | S→C self | Does the rest of the message desync? | 4.x–6.x skip an unknown id as one byte **[bin][inf]** | **Done on 6.03r7** |
| 1 | Player prop 77 (`ONLINESECS2`) | S→C self | Does 6.x read five bytes and store nothing? | five-byte skip in 6.x; ends the stream in 2.x **[bin]** | **Done on 6.03r7** |
| 2 | Player props 78–82 on 6.x | S→C self, other | Value widths and effect per id | cases exist; widths not listed **[bin]** | **Self stream done on 6.03r7**; other-player stream open |
| 2 | Self-prop width table 0–90 on 5.x/6.x | S→C self | Per-id value width | open item in `v5-props.md` | width sweep with a canary for every id |
| 2 | NPC props 48–52 | S→C NPC | Is the rest of the message dropped? | no case **[bin]** | NPC prop message with 48, then a visible prop |
| 3 | PLO 60, 78, 81, 83, 110 | S→C | Ignored, crash or reply? | no handler in any client checked **[bin]** | **Done on 6.03r7** |
| 3 | PLO 156 `SETACTIVELEVEL` | S→C | What the extra step in 2.31 does | unknown **[bin]** | needs 2.31 (gen-2/3 codec) |
| 3 | Other-player prop 77 | S→C other | Does it end the stream in 5.x/6.x? | no case **[bin]** | other-player message with 77, then a visible prop |
| 4 | Unknown PLI ids sent to our servers | C→S | What GServer-v2 and seihai-gserver do (ignore, log, drop the client) | handler tables **[srv]** | `c2s` from a live client session, on our own servers only |
| 4 | PLO 132/133 bytecode installs on 6.x | S→C | Still handled after 5.12? | gone after 5.12 **[bin]** | send a known-good body, then check the weapon or class |

## Pilot on 6.03r7 (2026-11-18)

The pilot used five runs: `p83-d`, `p83r-a`, `plo-a`, `w78-a` and `w78-c`. Each ran the
Linux 6.03r7 client against our gs2emu world behind `gen5probe.py`, using the plans in
`tools/probe/lab/`.

Each inject was one packet. Most were `PLO_PLAYERPROPS` messages with the bomb count
(prop 5, one byte) after the tested prop as a canary. Every row is in
[`probe-results.tsv`](probe-results.tsv).

### What the runs show

- **Prop 83 is the gralat (rupee) count, five bytes wide.** `83 = 1234` puts 1234 in
  the HUD counter, and the bomb canary after it lands, so the client read exactly five
  bytes. Prop 3 (`RUPEESCOUNT`, three bytes) writes the same counter. Sending 83, then 3,
  then 83 replaces the shown value each time. 83 is the wider form, for counts up to
  999,999,999. **[lab]**
- **Values over 999,999,999 are ignored, not clamped.** Each over-limit value left the
  shown value unchanged, and the rest of the message was still read. This matches the
  static `≤ 999,999,999` check. **[lab][bin]**

  | Shown before | Sent as 83 | Shown after |
  |---|---|---|
  | 1234 | 1,000,000,000 | 1234 |
  | 999,999,999 | 1,000,000,001 | unchanged |
  | any | 2^35 − 1 (largest five-byte value) | unchanged |

- **The built-in HUD draws only the low seven digits.** Whether the client stores all
  nine digits is not visible on the HUD. A GS2 read of `player.rupees` would settle it
  (next batches, item 3). **[lab]**

  | Value | HUD shows |
  |---|---|
  | 999,999,999 | 9999999 |
  | 123,456,789 | 3456789 |
  | 12,345,678 | 2345678 |
  | 10,000,000 | 0 |

- **Prop 77 is read as five bytes and has no visible effect**, as `v5-props.md` says
  for 6.x. **[lab]**
- **An unknown own prop id is skipped as one byte.** This closes the open item in
  `v5-props.md` for 6.03r7. **[lab]**
  - With a one-byte value, the canary lands.
  - With a three-byte value, the canary is lost and nothing else on screen changes.
  - The next message parses normally, so the desync ends with the message.
- **Props 78, 79 and 80 are `X2`, `Y2` and `Z2`: two-byte pixel positions of the local
  player.** **[lab]**
  - Each value is GSHORT = pixels × 2, and the low bit is the sign (`961` puts x at −480 px).
  - Z2 lifts the player sprite and leaves its shadow on the ground.
  - With two-byte values the canary lands. Values of 1, 3 or 5 bytes lose it.
  - This confirms the `78–80` row of [`player-props.md`](player-props.md) on a real client.
- **Prop 81 (`PLAYERLISTCATEGORY`) is one byte** with no visible effect on the local player. **Prop 82 is a length-prefixed string.** **[lab]**
- **PLO 60, 78, 81, 83 and 110 are ignored.** Each was sent with four bodies: empty, one
  byte, 60 bytes of text and four binary bytes. The client sent no packet in reply and
  did not crash, and the bomb canary after each one landed. **[lab]**
- No inject in any run crashed the client or made it send anything back.

Lab notes: the lab world sometimes shows a black screen. This happens when the login
server's warp arrives before the tile sheet. The HUD digits then draw over each other, so
those runs were read by comparing the newly drawn pixels between shots.

## Recommended next batches

1. **Self-prop width table for ids 0–90 on 6.03r7.** Run one group of ids at a time, with
   values of 1, 2, 3 and 5 bytes and a canary after each. This closes the per-id width item
   in `v5-props.md`. graal-client-repro's prop parser and the seihai-gserver encoder can
   then be tested against the table.
2. **The same tests on Windows 4.20r8, 5.24r4 and 6.037 under Wine:** prop 83, prop 77,
   unknown ids and PLO 60/78/81/83/110. These clients already run in the VM (`~/sl13`), so
   this needs only a runner. 4.x and 5.x have no case for 83, so the probe shows how they
   skip it.
3. **A GS2 read-back of prop 83.** Push a weapon that echoes `player.rupees` to chat, using
   the `gen5swap` bytecode route. This shows whether all nine digits are stored.
4. **Other-player and NPC streams.** Test other-player props 77 and 83 (expected to end the
   stream) and NPC props 48–52. A second lab client in the level acts as the observer.
5. **Server side.** Send unknown PLI ids with `c2s` to our GServer-v2 build and to
   seihai-gserver. Record what each server does: ignore the packet, log it, or drop the
   client.
6. **2.x clients**, after a gen-2/3 codec is added to the proxy. This also covers the extra
   step that 2.31 runs on `SETACTIVELEVEL`.
7. **6.1.1.3**, once a loopback connector harness exists.
