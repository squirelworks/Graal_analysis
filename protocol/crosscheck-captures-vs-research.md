# Cross-check: captures vs other-project research

Date: 2026-10-14

## Codec (confirmed)
From `graalcodec.txt` / `PROTOCOL.md` and the gserver-research README:

```
wire_byte = logical_id + 0x20
length_byte = nbytes + 0x20
```

14-bit: `(b0-0x20)*0x80 + (b1-0x20)`  
21-bit: `(b0-0x20)*0x4000 + (b1-0x20)*0x80 + (b2-0x20)`

Line: `(type+0x20) + payload + "\n"`  
First line of a session inserts one extra LCG byte.

Framing: 16-bit big-endian length + zlib (or raw, or encrypted). Matches the pcaps.

## Login (confirmed)
v2.05 shape from the research:

```
Chr((rand & 0x7F) + 0x20) + GNW##### + length-biased account/password
```

Pcap matches (credentials redacted):
- `GNW28015` (session 01)
- `GNW22122` (session 03)
- `GNW03014` (session 04)
- `GNW07080` (session 11)

The leading garbage byte is the random prefix. Account and password follow as length-biased fields.

## Movement (now identified)
Short client frames in the clear sessions start with `"` (0x22).  
`0x22 - 0x20 = 0x02`.

Research notes: after login, short frames headed `02` / `04` / `06` are walk and session.  
So the `"1-\n` / `"/[\n` packets are **logical type 0x02** (walk), character-encoded, newline-terminated.

Payload after the type byte is still to be split (x/y/dir). The classic/precise position codecs remain property helpers, not this packet.

## Encryption
Even modes XOR with the Borland LCG:

```
state = state * 0x08088405 + increment
dword ^= state
```

Initial state `0x04A80B38`. Explains why 14801 sessions stop decompressing after the first frame.

## Scripting references promoted
- `commands.rtf` — classic GS1 command surface (control flow, NPC/player verbs, item indices, directions, baddy names, message codes).
- `Graal_Reborn_Scripting_Guide.rtf` — 2008 forum guide; same language plus extras (setbow, mouse flags, showtext, tiledef split).

Direction note from the rtf: 0–3, with `up/left/down/right`. The earlier client note used 0 south / 1 west / 2 east / 3 north. Treat the rtf order as the script-facing names; confirm the numeric mapping against a named decompile before locking Seihai.

## Files
- `/shworkingpapers/protocol/from-other-projects/` — PROTOCOL.md, graalcodec.txt, players.md, flows.md, gserver-research README
- `/shworkingpapers/scripting/commands.rtf`
- `/shworkingpapers/scripting/Graal_Reborn_Scripting_Guide.rtf`

## Update 2026-10-21

- "Even modes XOR with the Borland LCG" describes gs2lib gen 4/5 (2.19+ clients), keyed by the login key, and XORs only the first 4 or 12 dwords. 2.05 is gen 3 (single-byte insertion). See `codec-and-framing.md`.
- Direction numbering is settled: 0 up, 1 left, 2 down, 3 right (2.22 `commands.rtf`, GServer).
- The movement frame is `PLI_PLAYERPROPS`. See `login-and-walk.md`.
