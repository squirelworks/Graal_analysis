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
