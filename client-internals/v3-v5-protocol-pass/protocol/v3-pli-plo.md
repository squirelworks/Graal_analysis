# v3 — PLI / PLO

Date: 2026-11-08 · Tags: **[bin]** · **[inf]**

## Model · **high**

Graal payloads are classic **GCHAR**: wire byte = `id + 0x20`. No FE remapper, no `tclient_` names. The binary is stripped, so names below are **functional**, not enum labels from the image.

A full client→server opcode harvest like v4’s send-wrapper table was **not** recovered (no equivalent vtable slot list). What is solid is the inbound/property side.

## Inbound (server → client), partial · **high** (these ids) · **medium** (meaning)

Applied when a buffer is matched to a player and switched on the wire byte:

| id | wire | Notes |
|---|---|---|
| 0 | `0x20` | present; body not named |
| 11–29 | `0x2b`–`0x3d` | consecutive cases (status / string / coord style updates) |

Ids 1–10 and the high band (30+) are **not** in this switch. v4’s local-player dispatcher is larger; treat this v3 table as a **subset**, not the whole PLO map.

## Properties as packets · **high**

A 0…76 property codec (gaps at 25, 27–30, 34, 36, 50–51) reads and writes GCHAR fields. Sword/shield image names are normalized inside ids 8 and 9. That codec is the v3 stand-in for “player props on the wire.” See the properties note.

## Outbound (client → server) · **low** (numeric table)

GCHAR writers exist (including the `.code` saver and the property codec). Individual PLI ids for move/chat/bomb/file were **not** enumerated to the same confidence as v4. Do not copy the v4 id table onto 3.0.4 without a capture.

## Remapper · **high**

None.

## Diff vs v4

v4 proves newline records plus a large PLI wrapper list and a local PLO switch. v3 shares the GCHAR rule and a smaller observed switch, and puts its block cipher on `.code` rather than on voice.
