# Stock TGE 1.1 reference: the Marble Blast Gold demo

Date: 2026-11-25

> **Reference only. Nothing in the Marble Blast columns is evidence about Graal.**
> Marble Blast Gold is a separate GarageGames game on stock TGE 1.1. It shows what *stock* Torque does, so that a value read from a Graal client can be labelled "same as stock" or "changed". Every Graal value in this note comes from a Graal client (a read of a Graal DLL or a Graal lab), and its source is given beside it. Where only the Marble Blast side was read, the Graal cell says so and no Graal claim is made.

## Why a reference program

Graal's 3.x–5.12 clients are built on TGE 1.x, and TGE 1.x source has no open licence (see [README.md](README.md#licences-which-torque-source-may-be-read)). Until now, "stock" in these notes meant Torque2D or Torque3D, which are later code with some different constants ([open-source-lineage.md](open-source-lineage.md)). A shipped TGE 1.x program is a closer reference. The free Marble Blast Gold demo, Linux build 1.4.1 (built May 2003, i386, stripped), was read statically and run live for this.

Marble Blast has no terrain, so this reference says nothing about `.ter` or `TerrainBlock`.

## Sources and tags

| Tag | Meaning |
|---|---|
| **[ref]** | Read from the Marble Blast binary or its shipped scripts. Stock TGE 1.1 reference, not Graal. |
| **[ref-lab]** | Seen in the Marble Blast live run below. Stock TGE 1.1 reference, not Graal. |
| **[bin 4.04r2]**, **[bin 5.12]** | 2026-11-25 static read of that client's `Graal3DEngine.dll`, done for this comparison. |
| note link | A Graal value taken from an earlier Graal note, with that note's own evidence. |

No decompiler text, binary addresses or game files are reproduced here.

## Engine version

| Program | `getVersionNumber` / string | Game string | Protocol (current / minimum) | Source |
|---|---|---|---|---|
| Marble Blast Gold demo 1.4.1 (reference) | 1101 / `1.101`, DSO 33 | `Torque Game Engine Demo` | 9 / 9 | **[ref]** |
| Graal 3.04 Linux | 1100 / `1.100`, DSO 33 | `Torque Game Engine Demo` | 9 / 9 | [README.md](README.md#lineage-at-a-glance) |
| Graal 4.04r2 | 1150 / `1.150` | `Graal3D` | 19 / 19 | **[bin 4.04r2]**; protocol also [torque-engine-4x.md](../graal3d/torque-engine-4x.md) |
| Graal 5.12 | not read | `Graal3D` | 24 / 24 | [network.md](network.md) (live) |

The reference and all three Graal builds use the TGE 1.1 version numbering. Graal 3.04's game string and protocol equal the reference's.

## Item by item

The **Graal reading** column is the comparison of the Graal value with the reference. Only the Graal cells are evidence about Graal.

| Item | Stock reference (Marble Blast) | Graal 4.04r2 (source) | Graal 5.12 (source) | Graal reading |
|---|---|---|---|---|
| DTS versions accepted | up to 24, no floor **[ref]** | up to 24, no floor, below 19 to the old reader **[bin 4.04r2]** | 17 to 24; below 17 "not supported anymore" **[bin 5.12]** | 5.12 adds a floor |
| `.dsq` import | rejects only above 24 **[ref]** | 0 to 24 plus a read-failure check **[bin 4.04r2]** | 17 to 24 plus a read-failure check **[bin 5.12]** | Graal adds checks |
| DIF versions (`InteriorResource` / `Interior` / `ForceField`) | 44 / 0 / 0 **[ref]** | 44 / 0 / 0 **[bin 4.04r2]** | 44 / 0 / 0 **[bin 5.12]** | as stock |
| Out-of-band types handled | 26, 30, 32, 34, 36, 38 **[ref]** | same **[bin 4.04r2]** | same, live in [network.md](network.md) | as stock |
| Connect request order | sequence, digest, class name, class group, class CRC, game, current, minimum, password, arguments **[ref][ref-lab]** | same **[bin 4.04r2]** | same, live in [network.md](network.md) | as stock |
| Class CRC | static `{0xFFFFFFFF, 0, 0, 0}`, never computed **[ref][ref-lab]** | same **[bin 4.04r2]** | same, [wire-by-build.md](wire-by-build.md) | as stock (see below) |
| Connect accept | sequence and protocol only, no class table **[ref-lab]** | class-name table **[bin 4.04r2]**, [wire-by-build.md](wire-by-build.md) | class-name table, live in [network.md](network.md) | changed |
| Data packet header | flag, int1, int9, int9, int2, int3, ack mask **[ref][ref-lab]** | same **[bin 4.04r2]** | same, live in [udp-session.md](udp-session.md) | as stock |
| `PacketRateToServer` default / range | 32 / 8–32 **[ref]** | 32 / 8–32 **[bin 4.04r2]** | 32 / 8–32 **[bin 5.12]** | as stock |
| `PacketRateToClient` default / range | 10 / 1–32 **[ref]** | 32 / 1–32 **[bin 4.04r2]** | 32 / 1–32 **[bin 5.12]** | default changed |
| `PacketSize` default / range | 200 / 100–450 **[ref]** | 450 / 100–450 **[bin 4.04r2]** | 800, clamped to 450 **[bin 5.12]**; no `$pref::Net` names | default changed |
| Class id on the wire | width computed from the class count **[ref]** | fixed 12 bits **[bin 4.04r2]**, [wire-by-build.md](wire-by-build.md) | fixed 12 bits, live in [network.md](network.md) | changed |
| Ghost id bits | 10 **[ref]** | 12 **[bin 4.04r2]**, [torque-engine-4x.md](../graal3d/torque-engine-4x.md) | 12, live in [udp-session.md](udp-session.md) | changed |
| Ghost index-width field | 3 bits, width − 3, minimum 3 **[ref]** | 4 bits, raw width **[bin 4.04r2]**, [torque-engine-4x.md](../graal3d/torque-engine-4x.md) | 4 bits, raw width **[bin 5.12]**, [wire-by-build.md](wire-by-build.md) | changed |
| Class id on ghost updates | first update only **[ref]** | every update, [wire-by-build.md](wire-by-build.md) | every update, live in [udp-session.md](udp-session.md) | changed (see open points) |
| Datablock id | 10 bits, id − 3 **[ref]** | 12 bits, id − 3 **[bin 4.04r2]**, [torque-engine-4x.md](../graal3d/torque-engine-4x.md) | no datablocks, [engine-and-formats.md](engine-and-formats.md) | changed |
| Length prefix on events and ghost updates | none **[ref]** | int14 on each **[bin 4.04r2]** | int14 on each, live in [udp-session.md](udp-session.md) | changed |
| `ConnectionMessageEvent` | u32 sequence, int3 message, int11 ghost count **[ref]** | same **[bin 4.04r2]** | same **[bin 5.12]** | as stock; 11 bits although Graal ghost ids are 12 |
| String buffer in game packets | attached at the start of read and write, detached at the end **[ref]** | attached in both directions **[bin 4.04r2]** | attached, live in [udp-session.md](udp-session.md#2-bit-stream-conventions) | as stock |
| First field of a server → client game packet | int32 last move ack, clamped to the move list **[ref]** | u32 at the same place, same clamp **[bin 4.04r2]** | not compared | as stock (see open points) |
| `MissionStartPhase` acks | carry the phase sequence; 1 on all three **[ref][ref-lab]** | no sequence, [torque-engine-4x.md](../graal3d/torque-engine-4x.md#mission-start) | two phases, [5007-g3d.md](5007-g3d.md) | changed |
| Renderer | OpenGL through SDL 1.2, 17 GL extension names **[ref]** | OpenGL plus `D3DDevice` and Voodoo2 (Glide) devices, 56 GL extension names **[bin 4.04r2]** | same as 4.04r2 **[bin 5.12]** | Graal adds devices and extensions |
| Registered classes | 143, 76 of them GUI or editor **[ref]** | at least 102 **[bin 4.04r2]** | 28 **[bin 5.12]** | 16 names shared by all three |

## What the comparison changes in Graal notes

For the first two items Graal's behaviour is unchanged and only the attribution moves (stock versus Graal change). The last three are new or corrected Graal facts, and each comes from the Graal DLL read, not from the reference.

- **Class CRC.** The static `{0xFFFFFFFF, 0, 0, 0}` table was already read in Graal ([wire-by-build.md](wire-by-build.md)). The reference has the same table, so it should not be listed as a Graal change.
- **Ghost index width.** Graal writes the raw width in 4 bits (**[bin 4.04r2]**, **[bin 5.12]**, and [torque-engine-4x.md](../graal3d/torque-engine-4x.md)). [open-source-lineage.md](open-source-lineage.md) had matched it to Torque2D, which writes width − 3. That match is withdrawn, and the field is listed as a Graal change.
- **Protocol-19 string buffer.** The 4.04r2 read **[bin 4.04r2]** finds the buffer attached in both directions. That settles the "test both forms" advice in [open-source-lineage.md](open-source-lineage.md).
- **4.04r2 `PacketSize` default.** The 4.04r2 read **[bin 4.04r2]** gives 450, not 800 as in [torque-engine-4x.md](../graal3d/torque-engine-4x.md). The clamp to 450 gives the same packets either way.
- **5.12 DTS bounds.** The 5.12 read **[bin 5.12]** gives 17 and 24, the two bounds [open-source-lineage.md](open-source-lineage.md#3d-formats) left unread.

## Reference live run (Marble Blast, not Graal)

- **Setup.** Linux build under Xvfb with software OpenGL (llvmpipe) in a headless Debian lab VM. The bundled SDL 1.2.5 deadlocks on a modern libX11, so the distribution's i386 `sdl12-compat` and Ogg/Vorbis libraries were used. **[ref-lab]**
- **What ran.** One instance hosted a multiplayer game on the beginner `movement` mission and joined itself over UDP through a user-space logging relay on the loopback address. Its DTS shapes and DIF interiors loaded. 2,262 datagrams were logged. No pcap was taken. **[ref-lab]**
- **What the log shows.** Challenge request and response; a connect request in the order above with class CRC `0xFFFFFFFF` and protocol 9 / 9; an accept with only the sequence and protocol 9; stock data headers throughout; the three `MissionStartPhase` acks each carrying sequence 1. **[ref-lab]**

No Graal client was run for this note.

## Reference content for local loader tests

The demo ships 12 `.dts` shapes (all version 24) and 12 `.dif` interiors (all version 44), with 212 PNG and 79 JPEG textures, 6 `.ifl` lists and no `.dsq`. **[ref]** These versions are inside what the 4.04r2 and 5.12 readers accept (table above), so they can exercise a loader locally. They are third-party files, are not Graal content, and stay out of every repo.

## Open points

- [ ] The first u32 of a 4.04r2 server → client game packet sits where the reference has its move ack. Whether the "u32 server time" after the dirty flag in [torque-engine-4x.md](../graal3d/torque-engine-4x.md#server--client-data-packet) is a separate Graal field needs a field-by-field read of the reference's control-object section. That section was not decoded here.
- [ ] The 2026-11-25 static pass also read the class id as first-update-only in both Graal DLLs. That conflicts with the live 5.12 runs, where it comes with every update. The live Graal result stands, and the 4.04r2 reading needs a recheck.
- [ ] Full `GameConnection` packet bodies in the reference, field by field.
- [ ] The 5.12 engine version number, and where its rate defaults come from.
- [ ] The Graal class counts are lower bounds: the compiler folded identical functions, so some registrations are hidden.
- [ ] The Windows Marble Blast build was not compared.
