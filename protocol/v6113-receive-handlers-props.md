# 6.113 receive handlers and prop parsers (joined)

Date: 2026-11-16. Own-words join of three notes that were already on main.
No new decompile. Tags stay with the source notes: **[bin]** unpacked
6.1.1.3 / 6.0.3.7 · **[lab]** Mac 6.111 live id tables.

| Source | What it already settled |
| --- | --- |
| [`v6113-handlers.md`](v6113-handlers.md) | How `setindatahandlers` installs wire→slot pairs; 95 native slots; named `tclient_*` indices |
| [`v6-props.md`](v6-props.md) | The four `tclient_set*props` methods call the same native parsers 4.x/5.x/6.037 use |
| [`v611-id-tables.md`](v611-id-tables.md) | Live Mac 6.111 incoming map: which wire ids land on which slots under the new-protocol set |

Status hub: [`v6113-status.md`](v6113-status.md). This page answers “which
wire id hits which prop parser on the connector path?” without re-opening
the cipher.

## Install path (connector era)

Until a connector script calls `setindatahandlers`, no wire id has a
handler. Pairs are `(wire_id, handler_byte)`:

- handler byte **&lt; 95** → native function at that index;
- **255** clears; **254** “do not call”; **253** / **252** special
  (bundle / enc-key wiring — see `connector-script.md` §5 and
  `v611-id-tables.md`).

6.037 has no copy of this installer: it keeps a fixed incoming switch.
**[bin]** (`v6113-handlers.md`)

The live Mac 6.111 table that was in use matched the script’s
**new-protocol** incoming set (96 pairs: drops wire 100, adds 252→252 and
253→253). Slot names were joined from the Windows 6.1.1.3 native index
table; empty slot 90 and several length checks match across those two
images. **[lab][bin]**

## Prop-related incoming rows (new-protocol set)

From the live Mac table, joined to the Windows native index and gs2lib
names by wire id only:

| Wire id | Native slot | Slot / method name | gs2lib name |
| ---: | ---: | --- | --- |
| 9 | 1 | `tclient_setplayerprops` | `PLO_PLAYERPROPS` |
| 8 | 35 | (unnamed slot; other-player props by role) | `PLO_OTHERPLPROPS` |
| 3 | 57 | (unnamed slot; NPC props by role) | `PLO_NPCPROPS` |
| 2 | 88 | (unnamed slot; baddy props by role) | `PLO_BADDYPROPS` |

**[lab]** (`v611-id-tables.md`) · **[bin]** (`v6113-handlers.md`)

Self props are the clean join: wire **9** → slot **1** →
`tclient_setplayerprops` → native self-player parser. **[bin][lab]**

NPC / baddy / other-player props land on **unnamed** native slots in the
95-wide table. Separately, the image still has script methods
`tclient_setnpcprops`, `tclient_setbaddyprops` and
`tclient_setotherplayerprops`. Those three are **not** entries 0–94; they
are the same family of one-string methods that call the native parsers.
**[bin]** (`v6113-handlers.md`, `v6-props.md`)

So: the connector maps wires 2 / 3 / 8 onto native slots by number; the
named `tclient_set*props` trio for NPC / baddy / other-player remains a
script-facing entry that shares the parsers, not a fourth copy of the
install table. Field-byte layouts inside the parsers were not re-read for
this join. **[bin][inf]**

## What the prop methods do once called

Each of the four named methods takes **one string** and does not switch
on property ids itself. Each calls the matching native parser (self, NPC,
baddy, other-player). 6.037 reaches those same parsers from its packet
switch instead of from `tclient_set*`. **[bin]** (`v6-props.md`,
`v5-props.md`)

Encoder side (client→server): both 6.037 and 6.113 walk player ids 0–83
with the same case list (twelve ids in the loop have no case). Baddy
encoders cover 0–10 with matching cases. There is no third client→server
NPC encoder loop of that shape. **[bin]** (`v6-props.md`)

## Outgoing prop wires (for labs)

Under the same live Mac outgoing table, internal send slots map to:

| Internal slot | Wire id | Event / role | gs2lib |
| ---: | ---: | --- | --- |
| 44 | 2 | `onSendPlayerProperties` | `PLI_PLAYERPROPS` |
| 45 | 3 | `onSendNPCProperties` | `PLI_NPCPROPS` |
| 23 | 15 | `onSendBaddyProperties` | `PLI_BADDYPROPS` |

**[lab]** (`v611-id-tables.md`)

A Gen5-only sink that never installs connector id tables will not see
this routing. A connector-era lab that answers after RC4 must expect
wire 9 (and 2 / 3 / 8) on the decrypted server stream for props.
**[inf]**

## Still open after this join

1. Per-id field widths inside the native parsers on 6.113 (bytes stored
   for each player id) — not recovered in `v6-props.md`.
2. Exact body of unnamed slots 35 / 57 / 88 beyond “props by role” —
   shape only in `v6113-handlers.md`.
3. Whether a live Windows 6.113 connector script uses the same
   new-protocol pair list as Mac 6.111 — Mac is the only live table held;
   Windows string-table reads did not recover the pair lists
   (`connector-script.md` §7).
4. Post-decrypt Login prop burst on a Windows 6.113 loopback harness —
   still open (`v6113-live-connector-2026-11-16.md`).

## Non-goals

- No addresses, digests, key material or third-party decomp text.
- No claim that 6.037’s fixed switch is bit-identical to the connector
  slot bodies — only that the prop **parsers** are the shared native
  ones. **[bin]**
