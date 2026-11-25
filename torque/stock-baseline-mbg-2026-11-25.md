# Stock TGE 1.1 baseline from the Marble Blast Gold demo

Date: 2026-11-25

Graal's 3.x–5.12 clients are built on TGE 1.x, and TGE 1.x source has no open licence (see [README.md](README.md#licences-which-torque-source-may-be-read)). Up to now, "stock" in these notes meant Torque2D or Torque3D, which are later code. This note uses a real TGE 1.x program instead: the free **Marble Blast Gold demo**, Linux build 1.4.1 (built May 2003, i386, stripped). It was read statically and run live, and each item was then read again in the Windows 4.04r2 and 5.12 `Graal3DEngine.dll`.

Marble Blast has no terrain, so nothing here covers `.ter` or `TerrainBlock`.

Tags as in [README.md](README.md), plus **[mbg]** read from the Marble Blast binary or its shipped scripts, and **[lab]** seen in the live run below. No decompiler text, binary addresses or game files are reproduced here.

## Engine version

| Build | `getVersionNumber` / string | DSO version | Game string | Protocol (current / minimum) |
|---|---|---|---|---|
| Marble Blast Gold demo 1.4.1 | 1101 / `1.101` | 33 | `Torque Game Engine Demo` | 9 / 9 |
| Graal 3.04 Linux (for reference, [engine-304.md](engine-304.md)) | 1100 / `1.100` | 33 | `Torque Game Engine Demo` | 9 / 9 |
| Graal 4.04r2 `Graal3DEngine.dll` | 1150 / `1.150` | – | `Graal3D` | 19 / 19 |
| Graal 5.12 `Graal3DEngine.dll` | not read | – | `Graal3D` | 24 / 24 |

**[mbg][bin]** All of them are on the TGE 1.1 line. The game string and protocol pair of an untouched TGE 1.1 build is `Torque Game Engine Demo`, 9 / 9, so Graal 3.04 still had stock values. The protocol check itself (reject below the minimum, reject above the current) is the same code in all three.

## Item by item

| Item | Stock TGE 1.1 (Marble Blast) | Graal 4.04r2 | Graal 5.12 | Verdict |
|---|---|---|---|---|
| DTS versions accepted | up to 24; no floor, older shapes go to the old reader | up to 24; no floor, below 19 goes to the old reader | **17 to 24**; below 17 rejected ("not supported anymore") | 5.12 adds a floor |
| `.dsq` sequence import | rejects only above 24 | 0 to 24, plus a read-failure check | 17 to 24, plus a read-failure check | Graal adds checks |
| DIF versions (`InteriorResource` / `Interior` / `ForceField`) | 44 / 0 / 0 | 44 / 0 / 0 | 44 / 0 / 0 | same |
| Out-of-band types handled | 26, 30, 32, 34, 36, 38 (28 is never handled) | same | same | same |
| Connect request order | u32 sequence, 4 × u32 digest, class name, u32 class group, u32 class CRC, game string, u32 current, u32 minimum, join password, argc and arguments | same | same | same |
| Class CRC | a static table `{0xFFFFFFFF, 0, 0, 0}`, never computed | same | same | **stock**, not a Graal change |
| Connect accept | u32 sequence, u32 protocol. No class table. **[lab]** | adds the class-name table | adds the class-name table | Graal-only |
| Data packet header | flag, int1, int9 sequence, int9 ack, int2 type, int3 ack bytes, ack mask | same | same | same |
| `PacketRateToServer` default / range | 32 / 8–32 | 32 / 8–32 | 32 / 8–32 | same |
| `PacketRateToClient` default / range | **10** / 1–32 | 32 / 1–32 | 32 / 1–32 | Graal raises the default |
| `PacketSize` default / range | **200** / 100–450 | **450** / 100–450 | **800** (clamped to 450) / 100–450 | defaults differ, clamp is stock; 5.12 has no `$pref::Net` names |
| Class id on the wire | per-group width computed from the class count | fixed 12 bits, server's numbering | fixed 12 bits, server's numbering | Graal-only |
| Ghost id bits (`GhostIdBitSize`) | **10** | 12 | 12 | Graal widens |
| Ghost index-width field | **3 bits, width − 3, minimum width 3** | **4 bits, raw width**, no − 3, no minimum | same as 4.04r2 | Graal-only (see below) |
| Class id on ghost updates | first update only | every update ([wire-by-build.md](wire-by-build.md)) | every update, live with the real client ([udp-session.md](udp-session.md)) | Graal-only (see open points) |
| Datablock id | 10 bits, id − 3 | 12 bits, id − 3 | no datablocks | Graal widens |
| Length prefix on events and ghost updates | none | int14 bit length on each | int14 bit length on each | Graal-only |
| Event framing | flag; guaranteed: flag next-in-sequence else int7 sequence; class id; payload | same, with 12-bit class id and the length prefix | same as 4.04r2 | same apart from width and prefix |
| `ConnectionMessageEvent` | u32 sequence, int3 message, int11 ghost count | identical | identical | same; the 11 bits are still 10 + 1 although Graal ghost ids are 12 bits |
| String buffer in game packets | attached at the start of read and write packet (with the compression point cleared), detached at the end | same | same | **stock** |
| First field of a server → client game packet | int32 last move ack, clamped against the move list | u32 at the same place, same clamp | – | same (see open points) |
| `MissionStartPhase` acks | carry the phase sequence (`%seq`); seq 1 on all three phases **[lab]** | no sequence | – (two phases) | Graal drops the sequence |
| Renderer | OpenGL through SDL 1.2; 17 GL extension names | OpenGL plus `D3DDevice` and Voodoo2 (Glide) device classes; 56 GL extension names (adds texture rectangle, vertex blend, PN triangles, two-sided stencil and others) | same as 4.04r2 | Graal adds devices and extensions |
| Registered classes | 143 (76 of them GUI or editor) | at least 102 | 28 | 16 shared by all three |

**[mbg][bin]**, with the **[lab]** rows confirmed on the wire as well.

### Corrections to earlier notes

- **Class CRC.** `{0xFFFFFFFF, 0, 0, 0}` is what TGE 1.1 itself does. It is not a Graal change ([wire-by-build.md](wire-by-build.md), [README.md](README.md#what-a-seihai-suite-would-need-in-order)).
- **Ghost index width.** [open-source-lineage.md](open-source-lineage.md) called Graal's 4-bit index-width field TGE-line behaviour, matching Torque2D's `GhostIndexBitSize = 4`. It is not. TGE 1.1 sends 3 bits holding width − 3 (minimum 3), Torque2D sends 4 bits holding width − 3, and Graal sends 4 bits holding the raw width. So [torque-engine-4x.md](../graal3d/torque-engine-4x.md)'s "sent as is" is right, and the field is a Graal change after all.
- **String buffer in protocol 19.** 4.04r2 attaches the buffer in both game-packet directions, as stock does. This settles the "test both forms" advice in [open-source-lineage.md](open-source-lineage.md) and agrees with [protocol19-server.md](protocol19-server.md).
- **4.04r2 `PacketSize` default.** The 2026-11-25 read gives 450, not 800 as in [torque-engine-4x.md](../graal3d/torque-engine-4x.md). The clamp to 450 makes the two the same in practice.
- **5.12 DTS bounds.** The two bounds left unread in [open-source-lineage.md](open-source-lineage.md#3d-formats) are 17 (minimum) and 24 (maximum).

## Live run

- **Setup.** The Linux build under Xvfb with software OpenGL (llvmpipe) in a headless Debian lab VM. The bundled SDL 1.2.5 deadlocks on a modern libX11. It runs with the distribution's i386 `sdl12-compat` and Ogg/Vorbis libraries in place of the bundled ones. **[lab]**
- **What ran.** One instance hosted a multiplayer game on the beginner `movement` mission (its DTS shapes and DIF interiors loaded without errors) and joined itself over real UDP through a user-space logging relay on the loopback address. 2,262 datagrams were logged. No pcap was taken (no root in the VM). **[lab]**
- **What the capture shows.**
  - Challenge request (26) and response (30) as in the table.
  - The connect request in the order above, with class CRC `0xFFFFFFFF` and protocol 9 / 9.
  - The connect accept is only the sequence and protocol 9. Stock TGE sends no class table.
  - Every data-packet header decodes with the stock layout.
  - The three `MissionStartPhase` acks each carry sequence 1.

  **[lab]**

## Test content for a renderer

The demo ships 12 `.dts` shapes, all version 24 (10 of them from exporter version 124), and 12 `.dif` interiors, all version 44. It also has 212 PNG and 79 JPEG textures, 6 `.ifl` texture-animation lists and no `.dsq` files. **[file]** These are the version numbers Graal 4.04r2 and 5.12 accept, so they are usable local test input for a DTS/DIF loader. They are third-party game files and stay out of every repo.

## Open points

- [ ] Whether 4.04r2's first u32 in a server → client game packet is only the stock move ack. If it is, the "u32 server time" after the dirty flag in [torque-engine-4x.md](../graal3d/torque-engine-4x.md#server--client-data-packet) needs a separate check against stock, which this pass did not decode.
- [ ] The 2026-11-25 static pass read the class id as first-update-only in the Graal DLLs too. That conflicts with the live 5.12 runs, where it comes with every update, so the live result stands; the 4.04r2 reading needs a recheck.
- [ ] Full `GameConnection` packet bodies (control object, camera, moves) in stock TGE 1.1, field by field.
- [ ] The 5.12 engine version number, and where its rate defaults come from (it has no `$pref::Net` names).
- [ ] The Graal class counts are lower bounds: the compiler folded identical functions, so some registrations are hidden.
- [ ] The Windows Marble Blast build was not unpacked or compared.
