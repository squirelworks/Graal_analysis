# Graal's Torque against the open Torque code bases

Date: 2026-11-11. Tags as in `README.md`, plus **[doc]** for a public source code base. Static comparison only; nothing was run.

Graal's 3.x–5.12 clients are built on TGE 1.1–1.3-era code (`engine-and-formats.md`). TGE 1.x itself was never published under an open licence. These public code bases come from the same line and can be read and reused under their own licences:

| Code base | Licence | How close to Graal's Torque | Use it for |
|---|---|---|---|
| [Torque2D](https://github.com/TorqueGameEngines/Torque2D) (`engine/source/network`, `engine/source/io/bitStream.cc`) | MIT | Closest open net layer. Same TGE-line constants as Graal (below). No `GameConnection`, no 3D. | The base for a server's `BitStream`, notify protocol, events and ghosting |
| [Torque3D](https://github.com/TorqueGameEngines/Torque3D) (`Engine/source/sim`, `core/stream`, `math`, `ts`, `terrain`, `T3D/gameBase`) | MIT | Several generations later. Same packet types, header and Huffman table, but some constants and behaviour changed (below). | Math I/O, DTS reading (versions 19+), the legacy `.ter` loader, the stock `GameConnection` shape for protocol 19 |
| [dso-sharp](https://github.com/Elletra/dso-sharp) | BSD-3-Clause | Has the TGE 1.0–1.3 `.dso` v33 opcode table | Checking `scripting.md`'s table, and a second decompiler |
| [Marble Blast web port](https://github.com/Vanilagy/MarbleBlast) (`src/ts/parsing/`) | MIT | Reads TGE-era DTS and DIF (Marble Blast Gold is a TGE 1.x game) | DTS/DIF parsing for 3D content tools |

Repositories that carry the TGE 1.x or Tribes 2 sources themselves have no open licence. They are not used here.

## What matches

**Packet types and header.** The out-of-band types 26 (`0x1A`) to 38 (`0x26`) in `network.md`, and the data header (connect-sequence bit, 9-bit sequence, 9-bit ack, 2-bit type, 3-bit ack byte count, ack mask), are Torque2D's and Torque3D's `NetInterface` and `ConnectionProtocol`, unchanged. **[doc][bin]**

**Huffman strings.** The character-frequency table in `tools/tbits.py` already came from Torque3D's `bitStream.cpp`. Torque2D has the same table. **[doc]**

**Ghost index widths.** Graal's 12-bit ghost index (control object, camera) and the 4-bit "index width" field before each ghost block are Torque2D's `GhostIdBitSize = 12` and `GhostIndexBitSize = 4` (the bit count is sent as width − 3). So the "raw index width" that `graal3d/torque-engine-4x.md` lists among Graal's changes is TGE-line behaviour. Torque3D raised `GhostIdBitSize` to 18, so a server that copies Torque3D's constants writes every ghost index 6 bits too wide. **[doc][bin]**

**Connection messages.** Ghosting starts and stops through `ConnectionMessageEvent` (registered in every Graal build) with the stock message enum: `GhostAlwaysDone`, `ReadyForNormalGhosts`, `EndGhosting`, `GhostAlwaysStarting`, `SendNextDownloadRequest`, `FileDownloadSizeMessage`. Torque2D's `activateGhosting` shows the server's order. **[doc][inf]**

**TorqueScript opcodes.** `scripting.md` and manual §10.4.3 said Graal's numbering "differs from stock TGE 1.x". It does not. It differs only from TGE 1.4. dso-sharp's table for "Torque Game Engine 1.0–1.3" (DSO version 33) is the same 83 opcodes in the same order as Graal's, with the same three unused slots at 2, 3 and 72. TGE 1.4 (DSO version 36) dropped those three slots, which is where the renumbering comes from. dso-sharp also marks 2, 3 and 72 as unused, so what they once were is still unknown. **[doc][file]**

**First-person flag.** The first bit of the 5.12 client → server game packet (`wire-by-build.md`) is stock `GameConnection`'s first-person flag: it is set when the connection's camera-position value is 0. The same field drives `GameObject::isFirstPerson`, which matches stock `ShapeBase::isFirstPerson`: not a ghost → true; otherwise true only when this object is the connection's control object and the camera position is 0. **[bin][doc]**

## What this closes

**`GameObject` update, section 5 (dirty bit `0x20`).** The write is Torque's `mathWrite` of a position and an `AngAxisF`:

| Field | Bits |
|---|---|
| position x, y, z | 3 × F32 |
| rotation axis x, y, z | 3 × F32 |
| rotation angle, radians | F32 |

The writer takes the object's transform, builds a quaternion from it (Torque's `QuatF::set(MatrixF)`), then the axis and angle (`AngAxisF::set(QuatF)`: angle = 2·acos(w), axis = xyz / sqrt(1 − w²), or (1, 0, 0) when that is 0). The reader reads the same seven floats and rebuilds the matrix from the axis and angle, then sets the position. The "then 32 bits" in `wire-by-build.md` is the angle. Scale is not sent. **[bin][doc]**

**Strings in data packets (protocol 24).** TGE's `BitStream::readString` has a prefix-reuse mode: when a string buffer is attached, each string starts with a flag and, if set, an 8-bit count of characters taken from the previous string. The 5.12 reader still contains that branch. No code in the 5.12 decompile attaches a buffer, so for 5.12 every string is a plain Huffman string, as `tools/tq.py` sends it. Torque3D stubs the buffer out altogether. **[bin][doc]** Not checked for protocol 19: 4.04r2 still has the stock TGE `GameConnection`, and stock TGE attaches the buffer at the start of each game packet. A protocol-19 server should test both forms against the client.

## What stays Graal's own

None of the open code bases has these. They still come only from the client binaries and lab runs:

- the class-name table in the connect accept, with fixed 12-bit class ids in the server's numbering (`network.md`);
- the 14-bit length prefix on every event and ghost update;
- the server time in the server → client game packet, and the 5.12 packet shapes (client-reported position, no moves);
- `BigDataStartEvent` / `BigDataChunkEvent`, `TerrainChunkEvent` / `TerrainRequestUpdatesEvent`, `DynamicGrass…`;
- `GameObject` and its movement and shape sub-objects, apart from section 5 above;
- GS2 in place of TorqueScript from 4.x on.

## 3D formats

- **DTS.** Torque3D's `TSShape::read` loads versions 19 to 28; TGE wrote 24. 5.12 checks a minimum and a maximum version (the "not supported anymore" and "can only load version %i and before" messages) and still keeps a reader for versions below 19. The two bounds are data values that were not read. Torque3D and the Marble Blast parser can both read version-24 shapes for content tools. **[doc][bin]**
- **DIF.** Torque3D no longer has interiors. The Marble Blast parser reads TGE-era DIF, and `io_dif` (Blender) writes it. 5.12 rejects an incompatible `Interior`, `InteriorResource` or `ForceField` version. **[doc][bin]**
- **TER.** Torque3D's `TerrainFile` still loads the old TGE `.ter` layout (`_loadLegacy`, versions below 7). 3.x and 4.04r2 read `.ter`; 5.12 streams terrain chunks instead (`engine-and-formats.md`). **[doc][bin]**

## Porting notes for a Seihai Torque side

- Start from Torque2D's net layer, not Torque3D's: the ghost id widths match, and its `BitStream` still has the string buffer for a protocol-19 test.
- Take from Torque3D only what Torque2D lacks: `GameConnection` (protocol 19's stock packet shape), `mathRead`/`mathWrite`, DTS, legacy `.ter`.
- Add Graal's changes from the list above.
- MIT code can be reused in any of the Seihai repos if its copyright notice is kept. This is separate from the decompile rule in `AGENTS.md`: this note's Graal findings still stay out of the clean-room repos.
