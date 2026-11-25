# 3D fuzz targets by build: every input that takes server-sent bytes

Plan for the fuzz strand of the client-mapping phase (T3D-114). It lists each
place where a 3D client reads bytes a server controls, ranked by how easy the
input is to reach. Fuzzing runs only against the real client in a lab VM,
served from our own gserver, never against a third party's server. A finding
is an accepted or rejected case with the bytes that caused it. **[plan]**

Reach: **A** = every session reaches it; **B** = reached when the server sends
that object or file; **C** = needs a script or a rare path.

## Files the client downloads and loads

| Target | Builds | Reach | Known checks | What to vary | Board |
|---|---|---|---|---|---|
| `.3ds` mesh | 512W, 420r8W, 500r7W | B | none known; our own reader survives 200k mutations | chunk lengths, counts, nested chunk depth, face indices past the vertex count, material names | T3D-038 |
| Shape and sky textures (PNG, JPEG, GIF, BMP, TGA, DDS) | all | A (sky) / B | decoded by content, not extension | header sizes, bit depth, huge width/height, truncation, palette length | T3D-077 |
| `.dts` shape | 404W, 512W | B | version 17 to 24 in 5.12; below 19 to the old reader | version word, mesh and node counts, string table, sequence data, each version 16 to 25 | T3D-029, T3D-038 |
| `.dsq` sequence | 404W, 512W | C | version range plus a read check | same as `.dts` | T3D-035 |
| `.dif` interior | 404W, 512W | B | InteriorResource 44, Interior 0, ForceField 0 | version fields, then truncation at each section | T3D-030, T3D-087 |
| `heights.info` and the heights cache | 3153M, 512W | B (TerrainBlock) | terrain textures 256x256x24 | texture names, counts, missing files, bit depth | T3D-040, T3D-044 |
| Weapon scripts for 3D (GS2) | 512W | A | CRLF files are not compiled | line ends, size, nesting | T3D-021 |
| Served file names | all | A | extension stripped from texture names; lower-cased | `../`, absolute paths, device names, long names, odd characters | T3D-112 |

## Network input (UDP, Torque)

| Target | Builds | Reach | Known layout | What to vary | Board |
|---|---|---|---|---|---|
| Connect accept | all | A | sequence, class table, protocol | class table length and names, protocol number (19, 21, 24, others) | T3D-072, T3D-080 |
| Event section | all | A | flag, 12-bit class id, int14 bit length, payload | unknown class ids, length longer or shorter than the payload | T3D-097 |
| Ghost section | all | A | ghost index width sent raw in 4 bits | index width, unknown class, update for a ghost never created, delete twice | T3D-105 |
| Control object | all | A | int12 ghost index of a GameObject, Camera or Player | index of the wrong class, of a deleted ghost | T3D-082 |
| `TerrainChunkEvent` | 512W | B | see terrain-512.md section 2 | chunk position out of range, inflated size, compressed stream damage | T3D-040 |
| `TerrainBlock` / `WaterBlock` / `Sky` / `Sun` ghosts | all | A or B | per-class fields | scale (zero, negative, huge), coordinates far out, texture counts | T3D-091 |
| `GameObject` ghost fields | 512W | A | shape, nickname, movetype, attached object | long strings, missing shapes, self-attachment | T3D-015 |
| Mission phase commands | 3153M, 404W | A | three phases | phases out of order, repeated, missing | T3D-022 |
| clientCmd remote commands | 3153M | A | 12 handlers | argument count and length | T3D-009 |

## Order of work

1. The A-reach network targets, because every session hits them: connect
   accept, the event and ghost sections, and the control object.
2. The sky textures and served names, which every session also touches.
3. `.3ds` and `.dts`, using the renderer lab's one-change sets.
4. The terrain path on 5.12, with the terrain lab's harness.
5. `.dif`, then the rarer paths.

Each target needs a baseline that loads cleanly before any mutation. The
gserver's seeded FZ worlds and the renderer lab's g3d-fuzzcases are the
starting sets.
