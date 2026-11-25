# TorqueScript and the terrain tools, build by build (3.153, 4.04r2, 5.12)

Date: 2026-11-25. Static reads of the Mac 3.153 client, the Windows 4.04r2 `Graal3DEngine.dll` and
the Windows 5.12 `Graal3DEngine.dll`. Behaviour only; no decompiled text, no addresses. Answers or
narrows board rows T3D-006, T3D-007, T3D-008, T3D-019 and T3D-041
([board](3d-capability-board.md)). Tags: **[bin]** static read, **[lab]** earlier lab run,
**[inf]** inference.

## Does the client take and run Torque files?

| | 3.153 Mac | 4.04r2 Win plug-in | 5.12 Win engine |
|---|---|---|---|
| TorqueScript compiler messages (`%s Line: %d - Syntax error.`, `Compiling %s...`) | present | absent | absent |
| `exec`, `compile` console names | present | absent | absent |
| `eval` console name | present | present | absent |
| `schedule`, `dumpConsoleFunctions` | present | present | absent |
| `.dso` extension literal | present | present (download filter) | present (download filter list) |
| Ships TorqueScript | yes (`main3D.cs` and `.dso` files) | no | no |

**[bin]**

- **3.153** is a full TGE client: it compiles and executes TorqueScript, and its 3D side is driven
  by the shipped `main3D.cs` scripts (see [`scripting.md`](scripting.md)). **[bin][file]**
- **4.04r2** has lost the compiler. The console still registers `eval`, `schedule` and the dump
  functions, so a part of the console survives, but with no compiler messages and no `exec` it has no
  visible way to turn text into code. The earlier lab run found that it opens no `.cs`, `.dso` or
  `.mis` beside it in a normal 3D session ([manual §10.6](../manual/10-torque.md), formerly E#502 and
  E#503). What `eval` does when called is still open (T3D-008). **[bin][lab]**
- **5.12** has no compiler, no `exec`, `eval` or `compile`, and no `schedule`. Its `.cs` literal is
  one entry of a list of file extensions that also holds `.txt`, `.nw`, `.gani`, `.gmap`, `.png` and
  others, next to the folder list `levels/`, `levels3d/`, `translations/`, `offline/`,
  `tileobjects/`, `updatepackages/` and `scriptfiles/`. That reads like a script file-access allow
  list, not a TorqueScript loader (T3D-013). **[bin][inf]**

So the answer for the 4.x and 5.x clients is no: they keep Torque's engine, file readers and
network layer, but GS2 replaced TorqueScript, and the TorqueScript compiler is gone. Only 3.153 (and
the stock 3.04 TGE base) runs Torque scripts. **[bin]**

## The terrain tools inside the client

Torque ships two terrain tools as engine classes: `Terraformer`, a procedural height-field generator,
and `TerrainEditor`, the in-mission brush editor. Both survive in all three builds, cut down
differently. **[bin]**

| | 3.153 | 4.04r2 | 5.12 |
|---|---|---|---|
| `Terraformer` generator operations (`rigidMultiFractal`, `turbulence`, `erodeHydraulic`, `erodeThermal`, `smoothRidges`, `generateSeed`, `previewScaled`, `terrainData`) | present | absent | absent |
| `Terraformer` functions kept | full stock set | `loadGrayscale`, `loadGreyscale`, `saveGreyscale`, `setTerrain` | the same four |
| How `Terraformer` is exposed | TorqueScript console class | registered as a Graal script object with those four functions | the same, as a subclass of Graal's script variable object |
| `TerrainEditor` | stock | stock function and field set (brush, selection, `setHeightVal`, `adjustHeightVal`, `smoothFactor`, `paintMaterial`, `attachTerrain`, `get/setTerrainMaterials`, `mirrorTerrain`, `processAction`, …) registered as script properties | the same set, as a GUI control |
| Local `.ter` load message (`Loaded terrain from terrain file.`) | present | present | absent |
| Chunk load message (`Loading terrain from terrain chunks.`) | present | present | present |

**[bin]**

What follows from this:

- The 4.x and 5.x clients cannot generate terrain procedurally any more. What they keep is the
  import, export and apply path: read a greyscale image as heights, save heights as a greyscale image,
  and apply the result to a `TerrainBlock`. **[bin][inf]**
- Both tools are registered in Graal's script object-creator registry, so GS2 can name them in
  `new` ([gs2-3d-objects-404r2-512.md](gs2-3d-objects-404r2-512.md)). `setTerrain` applies the
  register to the client's current `TerrainBlock` and relights it, with no cache write seen. A live
  call is still open (T3D-019, T3D-050). **[bin][inf]**
- 4.04r2 still has the local `.ter` file path beside the streamed chunks; 5.12 only builds terrain
  from chunks (see the terrain notes for the chunk layout). **[bin]**

## The original TerrainGenerator is a different tool

The 2001-2003 `TerrainGenerator.exe` from the New World and 2.22 tool sets is a 2D world tool: it
writes a `GRMAP001` gmap with `HEIGHTMAP` and `RANDOMSEEDS` and `GLEVNW01` levels with a 9 by 9
`HEIGHTS` block ([`tools/generators-222/README.md`](../tools/generators-222/README.md),
[stock LCG note](../tools/generators-222/gmap-terrain-stock-2026-11-16.md)). It does not write Torque
terrain. Whether a Torque-era client turns those 2D heights into 3D terrain is open (T3D-042); a lab
run of the original tool against `seihai-servertools gen terrain` is under way (T3D-043). **[bin][inf]**

## Open

- [ ] T3D-008: what `eval` does on 4.04r2 and whether any input reaches it.
- [ ] T3D-019 / T3D-050: create `Terraformer` and `TerrainEditor` from GS2; what `setTerrain` writes.
- [ ] T3D-041: when 4.04r2 takes the local `.ter` path over the chunk path.
- [ ] T3D-013: confirm the 5.12 extension list is GS2 file access.
