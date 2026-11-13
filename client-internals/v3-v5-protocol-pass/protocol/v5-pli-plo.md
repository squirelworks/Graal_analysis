# v5 — PLI / PLO

Date: 2026-11-08 · Tags: **[bin][ghidra]**

Primary image: unpacked **5.314** (`5.31r4`). **5.303** matches the same marker strings (illegal-data wording, `onPlayerLogin` / `onPlayerLogout`, `sword1.`, `GRESCR01`, no `onSend`). Its switch was not decompiled again. **5.0.0.7** is a different binary shape (see the end).

## Model · **high**

| Concept | Late 5 (5.314) |
|---|---|
| Wire id | byte minus `0x20` (same GCHAR family as the framing note) |
| FE remapper / `onSend*` / `tclient_` | **Absent** |
| Inbound local switch | Partial. Cases are the wire bytes below, not a full 0–255 table |
| Other players | Separate path: two-byte id, then the property applicator |
| Properties | Large switch on the same GCHAR byte (see `v5-properties.md`) |
| Outbound PLI ids | **Not recovered** as a numeric table |

## PLO (server → client) · **high** (which ids exist) · **low** (most meanings)

Local dispatcher switches on the wire byte. Id = byte − `0x20`.

| id | Named evidence | Confidence |
|---|---|---|
| 0 | Length check, then writes a reply byte (`value + 0x20`) from a runtime table | low |
| 11, 12, 13 | Dedicated handlers, no nearby string | low |
| 15 | String copy into a level-like object | low |
| 16, 17, 18 | Dedicated handlers, no string | low |
| 19 | Handler references the words `sword` and `shield` | medium |
| 20 | Plays `extra.wav` | medium |
| 21, 22 | Dedicated handlers | low |
| 23 | Calls the property applicator | **high** |
| 24 | Two-byte read, then a short follow-up | low |
| 25 | Same helper as id 21 | low |
| 26 | String `clientside` | medium |
| 27 | Builds a reply the same way id 0 does | low |
| 28, 30 | Dedicated handlers | low |

Ids not in that set are not in this switch. That is a real gap, not a claim that those packets do not exist.

### Other-player path · **high** (events) · **medium** (split)

One function reads two bytes into a player id (first byte scaled by 128), runs the property applicator, then:

| Branch | String |
|---|---|
| New player | `onPlayerLogin` |
| Existing player leaving | `onPlayerLogout` |
| Non-empty text on that path | prefixed `"Mass message:"` |

## PLI (client → server) · **open**

The send routine takes an opcode and rejects a newline in the body (`Illegal characters in the outgoing data`), except internal opcodes `0x5D` and `0xA3`. Call sites do not pass a fixed opcode immediate. The reply-id tables used by PLO ids 0 and 27 are zero in the file (filled at runtime).

No `onSend*` name table exists to harvest. Numeric PLI ids stay open. Confidence: high on that absence.

## 5.0.0.7 · **medium** (family) · **open** (numbers)

`Graal 5.0.0.7.exe` plus `GraalEngine.dll` carry `graal://`, `graal3://`, and `setGraalProtocol`, plus `Illegal characters` / `Received illegal data`. No `onSend*`. No baked `loginserver` / `14900`. UDP prefs `fixedudpport` and `noudp` are present; the exe contains `14899`.

This pass did not re-walk the 5.0.0.7 send wrappers. Treat its numeric PLI/PLO as the v4-style gap, not as the late-5 switch above.

## Remapper · **high**

No 256-slot `0xFE` table in 5.314, 5.303, or the 5.0.0.7 engine.
