# Probe targets: unknown packets and props

Date: 2026-11-18

This note lists the ids and props that our notes still mark as unknown, unnamed or "not
traced", and how the probe harness (`../tools/probe/`) can test each one on a real client.
Results go in [`probe-results.tsv`](probe-results.tsv). Sources: [`packet-ids.md`](packet-ids.md),
[`player-props.md`](player-props.md), [`v5-props.md`](v5-props.md),
[`unknown-ids-2026-11-06.md`](unknown-ids-2026-11-06.md), `../manual/app-b-props.md`.

Clients the harness can drive:

- **Now:** the native Linux 6.03r7 client (`tools/probe/lab/run603.sh`), and Windows 2.22, 2.31,
  4.20r8 and 5.24r4 under Wine (`tools/probe/lab/runwine.sh`). All of them use gen 5.
- **Need a gen-2/3/4 codec in the proxy:** 2.00 to 2.21.
- **Need the Win10 VM:** Windows 6.037, which is packed and does not run under Wine.
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

- **The built-in HUD draws only the low seven digits, but the client stores all nine.**
  In run `cb83-d`, a level script copied `playerrupees` into the player's chat, and the client
  reported that chat to the server. After 83 = 123,456,789 the script read 123456789. After
  999,999,999 it read 999999999, and after 1,000,000,000 the value stayed 999999999. **[lab]**

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

## Self-prop widths 0–90 on 6.03r7 (run `cwid-b`)

Each own prop 0–90 was sent at the width that [`player-props.md`](player-props.md) gives it,
followed by the bomb canary. The canary was read from the client's own report:
`CHATBACK=1` adds a level script that copies the bomb count into the player's chat (see
`tools/probe/chatcanary.py`). This avoids the black-screen problem. **[lab]**

- **Every id with a case reads at its documented width.** That is 0–32, 34–49, 52, 54–74 and
  77–83, including the risky ids 14 (`ID`) and 20 (`CURLEVEL`). The client stayed up
  throughout.
- **The ids with no case** are 33, 50, 51, 53, 75 and 76, the 6.x self parser's no-case set.
  Each one is skipped as one byte:
  - 51 (sent with no value) and 76 (sent as three bytes) lost the canary.
  - 33, 50 and 53 (sent as one byte) kept it.
  - 75 kept it only by chance, because the bytes of the string `linux` parse as other props.
- **84–90** are skipped as one byte.

**Caveat and re-check.** In `widths.plan`, the multi-byte ids 24, 27–31, 36, 42 and 77 were
sent as all-zero values. An all-zero tail can line up again by chance, because `0x20 0x20`
reads as an empty prop 0. So `widths-fix.plan` sent those ids again with values whose
too-short read leaves `0x20 0x9f` behind, and that swallows the canary. **[lab]**

- On 6.03r7 (`wf603-a`), all of them hold.
- On 4.20r8 (`wf420-a`) and 5.24r4 (`wf524-a`), all of them hold except 77, which has no case
  there.

**4.20r8 and 5.24r4.** The same plan ran on both (`w420-wid`, `w524-wid`). **[lab]**

- Every id with a case reads at its documented width.
- The ids with no case:
  - 4.20r8: 33, 50, 51, 53, 75, 76, 77, 82 and 83
  - 5.24r4: the same set without 82

  Each one is skipped as one byte.

This closes the per-id width item in `v5-props.md` for 4.20r8, 5.24r4 and 6.03r7.

## The same probes on Windows clients (2026-11-18)

The runs were `w222-a`, `w231-a`, `w420-c` and `w524-b`, all using plan `tools/probe/lab/wine-core.plan`.
Before each test the bomb count was reset to 1, and the canary set it to 99. The canary column
of [`probe-results.tsv`](probe-results.tsv) is read with `tools/probe/canary.py`.

| Probe | 2.22 | 2.31 | 4.20r8 | 5.24r4 | 6.03r7 |
|---|---|---|---|---|---|
| Prop 3 (`i3`) | read | read | read | read | read |
| Prop 77 | ends the message | ends the message | skipped as 1 byte | skipped as 1 byte | 5 bytes |
| Props 78–80 (`s`) | end the message | 2 bytes | 2 bytes | 2 bytes | 2 bytes |
| Prop 81 (`c`) | ends the message | ends the message | 1 byte | 1 byte | 1 byte |
| Prop 82 (string) | ends the message | ends the message | skipped as 1 byte | string | string |
| Prop 83 | ends the message | ends the message | skipped as 1 byte | skipped as 1 byte | 5 bytes, gralat count |
| Unknown own id 90 | ends the message | ends the message | skipped as 1 byte | skipped as 1 byte | skipped as 1 byte |
| PLO 60, 78, 81, 83, 110 (text bodies) | ignored | ignored | ignored | ignored | ignored |
| PLO 60, 78, 81, 83 (body `ff 00 ff 00`) | **next packet in the frame lost** | **next packet in the frame lost** (110: kept) | ignored | ignored | ignored |

**What this shows**

- **2.22 and 2.31 stop at any prop id they have no case for.** 2.31 has cases up to 80 and
  2.22 stops before 78. **[lab]** This matches the 2.x rows of [`player-props.md`](player-props.md).
- **4.20r8 and 5.24r4 skip an id they have no case for as one byte,** like 6.03r7.
  - **5.24r4** reads 82 as a string, but has no case for 77 or 83. **[lab]**
  - **4.20r8** has no case for 82 either. **[lab]**
- **2.22 and 2.31 stop reading a frame at a NUL byte.** The byte-by-byte runs (`b222-a`, `b231-a`,
  `b420-a`, plan `bytes2x.plan`) settle this:
  - On 2.22 and 2.31, a message with a `00` byte anywhere in it loses every packet after it in
    the same frame. This holds for an unknown id and for a chat prop alike.
  - On both, `ff`, `80` and `1f` bytes are harmless.
  - 4.20r8 keeps the rest of the frame in every case.
  - 2.31 lost the next packet after `ff 00 ff 00` on ids 60, 78, 81 and 83, but not on 110.
    That one case is not explained yet.

  **[lab]** So a server should never put a `00` byte in a message for a 2.x client. File
  bodies sent behind `PLO_RAWDATA` hold such bytes and still arrive, so the raw-data path is
  probably exempt. **[inf]**
- No inject crashed any of the Windows clients.


## Server side: every client→server id at our GServer-v2 build

The sweep sent each id 0–223 with an empty body from a live 6.03r7 session. The target was our
seihai-gserver-v2 build (`GS2Emu 4.0.0-beta`, built 2026-11-11). The runs were `pli-a`, `pli-b`
(ids 0–17) and `pli-c` (18–223), using the plans `pli-sweep*.plan`. **[lab][srv]**

**Ids the build handles.** It handles 0–41, 44, 46–48, 50, 80, 81, 130, 152, 154, 157–159, 161
and 223. Every other id from 18 to 223 is unknown to it (168 ids). The ids it does not handle
include:

| Id | Name |
|---:|---|
| 42 | |
| 43 | `PLI_MUTEPLAYER` |
| 45 | `PLI_PROCESSRUNNING` |
| 49 | |
| 51–79 | the RC range |
| 82–129 | |
| 131–151 | |
| 153, 155, 156, 160 | |
| 162–222 | |

**What an unknown id does.** The server logs `Unknown Player Packet: N` and counts it. After
three unknown packets it sends `PLO_DISCMESSAGE` ("Disconnected for sending invalid packets.")
and drops the client. 6.03r7 then logs in again by itself, which is why the sweep could keep
going.

**Handled ids that do not check an empty body:**

| Id | Name | What happened |
|---:|---|---|
| 17 | `PLI_BADDYADD` | The missing fields read as `0 − 32`, which made a type-224 baddy at tile 112,112. The server sent it to the level, and the 6.03r7 client asked for `crush.wav` and quit. This ended the session in both runs (`pli-a`, `pli-b`). The sweep's later plans skip 17. |
| 31 | `PLI_PACKETCOUNT` | Logged "invalid packet count" and kept the client. |
| 41 | `PLI_SERVERWARP` | Logged a serverwarp request to an empty server name. |
| 130 | `PLI_REQUESTUPDATEBOARD` | Logged an empty level with x, y, w and h of −4128 and a junk modtime. |

**Replies.** 34 (`PLI_UPDATEFILE`) got `PLO_FILEUPTODATE`, and 159 (`PLI_UPDATEPACKAGEREQUESTFILE`)
got 105 and 106. 39 (`PLI_TAMPERCHECK`) got no reply and no log line, so this build does not act
on the tamper check (E#320).

**Which baddy types a client survives.** A follow-up sent `PLO_BADDYPROPS` with one new baddy
per type, using plans `baddytypes*.plan`. **[lab]**

| Client | Survives | Quits |
|---|---|---|
| 6.03r7 (`bt603-a`, `bt603-b`) | types 0–24 | type 25 and type 31; 26–30 not tried |
| 4.20r8 (`bt420-a`) | every type sent, 223 included | — |
| 2.22 (`bt222-a`) | every type sent, 223 included | — |

So a server should never send a baddy type above 24 to a 6.x client, and should keep to 0–9
(the named types) for any client.

**What follows from this.**
- A server should check each body's length before reading it, and should check the baddy type
  before adding a baddy.
- A 6.03r7 client cannot survive a baddy whose type is out of range.

## Recommended next batches

1. ~~**Self-prop width table for 0–90 on 6.03r7.**~~ Done in run `cwid-b`. Next, run the same
   plan on 4.20r8 and 5.24r4. Their HUD canary works because those runs draw the screen.
2. **The same tests on Windows 4.20r8, 5.24r4 and 6.037 under Wine:** prop 83, prop 77,
   unknown ids and PLO 60/78/81/83/110. These clients already run in the VM (`~/sl13`), so
   this needs only a runner. 4.x and 5.x have no case for 83, so the probe shows how they
   skip it.
3. ~~**A script read-back of prop 83.**~~ Done in run `cb83-d`: all nine digits are stored.
4. **Other-player and NPC streams.** Test other-player props 77 and 83 (expected to end the
   stream) and NPC props 48–52. A second lab client in the level acts as the observer.
5. **Server side.** Send unknown PLI ids with `c2s` to our GServer-v2 build and to
   seihai-gserver. Record what each server does: ignore the packet, log it, or drop the
   client.
6. **2.x clients**, after a gen-2/3 codec is added to the proxy. This also covers the extra
   step that 2.31 runs on `SETACTIVELEVEL`.
7. **6.1.1.3**, once a loopback connector harness exists.
