# v4 — PLI / PLO

Date: 2026-11-08 · Tags: **[bin]** · **[inf]**

## Model · **high**

| Concept | v4.2.0.8 |
|---|---|
| Wire id | `first_byte - 0x20` |
| Line framing | newline-delimited |
| FE remapper / `tclient_` | **Absent** |
| Send | `connection→vtable+8(opcode, payload)` |
| Recv (local) | line → dispatcher (`byte - 0x20`) |
| Other players | 2-byte GINT id prefix then property blob |

Names below are **functional** (from send wrappers / recv case bodies). Classic `PLI_*` / `PLO_*` enum labels are not stringified in this binary.

## PLI (client → server) · **high** (ids) · **medium** (names)

| id | wire | Role (evidence) |
|---|---|---|
| 1 | `!` | Board / tile modify (grid payload) |
| 2 | `"` | Player property blob send |
| 4 | `$` | Movement / position update (x,y + flags) |
| 5 | `%` | Action at coords (shoot-like) |
| 6 | `&` | Chat / text (length-prefixed) |
| 9 | `)` | Place / use at coords |
| 10 | `*` | Related action (packed flags) |
| 12 | `,` | Item / drop-style coords |
| 13 | `-` | Bomb / projectile coords |
| 18 | `2` | `client.*` var update (`name=value`) |
| 19 | `3` | `client.*` var update (name only path) |
| 20 | `4` | File / gani request style |
| 21 | `5` | Dual filename + coords |
| 26 | `:` | NPC-relative / distance gate |
| 28 | `<` | Mass PM (`PM sent to…`) |
| 34 | `B` | Request level file (+ 5×GCHAR mtime) |
| 46 | `N` | Short ping-like (`!` payload) |
| 47 | `O` | Request `.gupd` / `.gmap` (+ hash GCHARs) |
| 50 | `R` | Large buffer / upload size prelude |
| 152 | — | RC-ish |
| 154 | — | `sendServerText` / server-text bridge |
| 157 | — | `getgani` |
| 158 | — | `getweapon` |
| 161 | — | `getclass` |

Full numeric harvest (including thin wrappers): see repro `v4/pli.md` / `raw/pli_opcodes_from_vtable8.md`.

## PLO (server → client) · **high** (dispatch) · **medium** (case meaning)

Local-player dispatcher switches on wire byte (`0x20` = id 0, …):

| id | wire | Role (evidence) |
|---|---|---|
| 0 | ` ` | Login / session (`login` string path, timeout slot) |
| 1 | `!` | Flag / mode via vtable |
| 2–7 | | Coordinate / powerup / status deltas |
| 8–9 | | Length-prefixed skip / text-ish |
| 12 | `,` | Nickname / account string assign |
| 13 | `-` | Five small field writes |
| 14 | `.` | Numeric status + side effects |
| 15–16 | `/``0` | Relative X/Y adjust |
| 18 | `2` | Flag bits + obfuscated blob |
| 20 | `4` | Level / filename assign |
| 21–22 | `5``6` | Carry / mount object |
| 24 | `8` | Linked object id (3-byte GINT) |

Many higher wire bytes share a length-skip stub (payload length GCHAR then advance). Other-player add/update uses a **separate** path: 2-byte player id, then property applicator (sword/shield/head/chat events).

## Remapper · **high**

No 256-slot `0xFE` FE table.

## Diff vs v5 / v6 · **high**

| | v4 | Late v5 | v6.113 |
|---|---|---|---|
| `id+0x20` / newline | yes | yes | yes (+ FE after) |
| Named `tclient_*` / `onSend*` | no | no | **yes** |
| Numeric tables recoverable | **yes** (wrappers + switch) | harder without FE names | FE names |
