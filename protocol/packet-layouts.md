# Additional protocol layouts

Date: 2026-10-14

## Board modify (`TLevelBoardChange::getBoardStr`)
```
x:u8  y:u8  width:u8  height:u8  tiles:raw
```
- `tiles` is the raw tile data for the rectangle (same 2-byte codes as the board).
- Used by both `PLO_LEVELBOARD` and `PLO_BOARDMODIFY`.

## Player property encoding (selected, from `TPlayerProps.cpp`)

| Prop | Encoding |
|------|----------|
| `PLPROP_X` / `Y` | `(char)(pos * 2)` |
| `PLPROP_Z` | `(char)((z + 0.5) + 50)` |
| `PLPROP_X2` / `Y2` / `Z2` | `u16`: `abs(pos * 16) << 1`, low bit = sign |
| `PLPROP_GANI` | length-prefixed string |
| `PLPROP_HEADGIF` / `BODYIMG` | length-prefixed string |
| `PLPROP_COLORS` | 5 bytes |
| `PLPROP_ID` | `short` |
| `PLPROP_CURLEVEL` | length-prefixed level name (or map name) |
| `PLPROP_NICKNAME` | length-prefixed |
| `PLPROP_ALIGNMENT` | `char` |
| `PLPROP_RUPEESCOUNT` etc. | various ints/chars |

Props are sent as a sequence of `(propId:u8 + payload)` until the buffer is exhausted.

## GANI format (from `walk.gani`)
Text file:
```
SPRITE id  SET  x y w h  description
...
ANI
...
```
- `SPRITE` lines define source rectangles from named sheets (`HEAD`, `BODY`, `SHIELD`, `ATTR1`, …).
- Later sections define animation frames (not fully parsed yet).
- Standard sheets: body, head, shield, sword, hat, etc.

## NPC props
Similar pattern to player props (`NPCPROP_IMAGE`, `NPCPROP_X`, `NPCPROP_Y`, `NPCPROP_GANI`, `NPCPROP_SCRIPT`, …).  
`PLO_NPCPROPS` is `id:int + prop stream`.

## Implications for Seihai
- Board updates are simple rectangles of raw tile shorts.
- Position on the wire is usually `pos * 2` as a byte (or the higher-precision `*16` form).
- GANI is a text format we can parse independently of the network.
- Player/NPC state is a flat list of tagged properties — easy to model as an enum + payload in Rust.
