# Packet-id cross-check — 1.39 vs v2.05

Date: 2026-10-14

## Sources
- 1.39: `shdecompiling/graal-139-dhrake/Graal 139.exe-2.c` (Dhrake)
- v2.05: `shdecompiling/graal-v205/DispatchGs1.txt` and `Graal.exe.c`

## Finding
`DispatchGs1.txt` is the GS1 interpreter, not the network packet dispatcher. It switches on script opcodes, not wire packet ids. A direct case-by-case packet-id diff against it is not meaningful.

## What the captures lock
| Logical | Wire | Role | Confidence |
|---------|------|------|------------|
| 0x02 | `"` (0x22) | walk / player update | high — clear sessions, research notes |
| — | (no type byte) | login line | high — prefix + GNW##### + length-biased fields |
| — | server→client | board modify | medium — PLO_BOARDMODIFY in GServer-v2 |

## Case-pattern notes
- 1.39 export uses `case 0xNN:` (586 hex cases). Includes `case 0x10:` in several switches; context is mixed (not all packet dispatch).
- v2.05 export uses `case (code)0xN:` inside `DispatchGs1` (script opcodes).

## Provisional ids still in Seihai
`PacketId::Login` (0x01), `LevelRequest` (0x10), `PlayerUpdate` (0x20) remain provisional. The classic login line and the walk frame do not use these ids; they use the shapes above.

## Next
Locate the actual receive switch in the 1.39 export (search for the session read loop, not `DispatchGs1`) and name the arms against the capture shapes.

## Update 2026-10-21 (resolved)

- The 2.05 network receive switch is now located. It is a jump table over `id = byte − 0x20` with bound 0xA8. Its arms match gs2lib `PLO_*` names for 0–25, 27–48, 75, 100, 150, 151, 153–156, 165, 166, and 168. 26 (`PLO_NPCACTION`) is not handled. **[2.05]**
- Client → server senders exist for ids 1–38 (except 6, 25, and 31), plus 80 and 81. Id 0 covers both the login line and `PLI_LEVELWARP`. **[2.05]**
- The provisional Seihai ids are retired. Login is client type 0, level request is `PLI_LEVELWARP` (0) or `PLI_ADJACENTLEVEL` (35), and the player update is `PLI_PLAYERPROPS` (2).
- The full table is in `packet-ids.md`. The 1.39 receive switch has not been redone yet. Expect the same ids with fewer arms.
