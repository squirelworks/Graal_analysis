# Mac PowerPC clients: graphics setup, transport, events and resources

This note gathers the findings of a broad static pass over the four distinct Mac
OS X PowerPC executables. The pass is dated 2026-11-09. Two topics from the same pass
have their own notes:
- start-up and input: [Mac start-up and input](mac-ppc-startup-input-2026-11-09.md);
- receive framing: [PowerPC receive framing](../protocol/macos-ppc-receive-framing.md).

The pass also produced [the decompression note](../protocol/macos-ppc-receive-decompression.md)
and [the gmap reader note](../formats/gmap-heights-mac-ppc.md).

**How the findings were made.**
- Each finding comes from function bodies that were opened in that build and checked against the assembly.
- No client, guest or server was run for this note.
- Every build had a cap on how many functions could be selected, so the coverage is partial. This is not a full teardown.

| Archive group | Copies with the same main executable |
| --- | --- |
| Shared v3 (labels 3.04 and 3.15r2) | 2 |
| Label 4.04r2 | 1 |
| Label 4.20r6 | 1 |
| Shared v5 (one copy labelled 5.12) | 5 |

Matching bytes do not authenticate a release label. Executable digests are owner-held.

## Graphics context setup

[bin] All four builds have the same two setup helpers, opened separately in each build.

**The window helper.**
- Its attribute list is `4, 5, 73, 72, 12, D, 0`. `D` is 16 when the requested depth is below 17, and 32 otherwise.
- It chooses a pixel format, creates a context, attaches the drawable and makes the context current, in that order. Each step runs only if the one before it succeeded.
- If no pixel format is found, it logs `Could not find valid pixel format` and returns zero.
- If context creation fails, it logs `Could not create context`.
- If making the context current fails, the drawable is detached.

**The fullscreen helper.**
- Its attribute list is `4, 5, 73, 72, 12, D, 54, 50, P, 0`, where `P` is the depth that was originally requested.
- It first tries fullscreen with a refresh rate read from a global. If that fails, it logs `SetFullScreen(0Hz) failed`, sets the refresh globals to 60 and retries at 60.
- A second failure logs `SetFullScreen(60Hz) failed` and returns zero.
- The first log line says 0 Hz, but the global's value at the first call was not established.

[bin] Neither helper retries the pixel-format choice with fewer attributes. This is a negative result for these two bodies only. A fallback in a caller or another helper is not ruled out.

[inf] Apple's public `agl.h` gives these numbers the following names:

| Value | Name |
| --- | --- |
| 4 | `AGL_RGBA` |
| 5 | `AGL_DOUBLEBUFFER` |
| 12 | `AGL_DEPTH_SIZE` |
| 50 | `AGL_PIXEL_SIZE` |
| 54 | `AGL_FULLSCREEN` |
| 72 | `AGL_NO_RECOVERY` |
| 73 | `AGL_ACCELERATED` |

The binaries do not carry these names; they were matched from the header.

[inf] If those names are right, both helpers ask for an accelerated renderer with no software fallback. A machine with no hardware OpenGL renderer would then find no pixel format. That would fit the black window seen when an unmodified client ran under emulation. It also fits the earlier lab run, which needed a software-renderer shim; see [the October 2026 Mac lab run](../version-profiles/lab-mac-tiger-2026-10-31.md). This is a lead, not a measured cause: no unmodified run has been seen to reach these helpers.

[bin] **4.20r6.** A capability routine does the following:
- scans the OpenGL extension string;
- reads selected limits;
- sets capability globals and publishes the result as support variables.

If paletted textures are not supported and the forced-paletted preference is on, it turns that preference off and turns forced 16-bit textures on.

[bin] **v5.** Two more helpers were opened:
- One creates a CoreFoundation bundle for the system OpenGL framework on first use, then looks up a function pointer by name.
- One walks the texture objects, tries to rebuild each eligible one, and logs textures that are missing or were replaced unexpectedly.

[file] **v3.** A packaged v3 preference script sets the following:
- display device `OpenGL`;
- windowed mode;
- 800 × 600;
- a profiled-renderer string naming a PC graphics card.

These are packaged defaults. They say nothing about the hardware of any guest.

## Transport wrappers

[bin] **4.04r2.** These are socket wrappers, not the Graal frame parser.

- **Connect.** It opens an IPv4 stream socket. It tries to parse the host as a numeric address, then falls back to a host name lookup. It then connects and sets descriptor flags. On failure it can close and clear the descriptor.
- **Receive.**
  - It polls with a zero-timeout `select`.
  - It reads at most 8192 bytes per call, using the stream or datagram call according to a mode flag.
  - It appends what it reads to a buffer and counts the bytes.
  - On end-of-stream it closes the stream.
- **Send.**
  - It polls for writability with a zero-timeout `select`, sends once and returns the byte count from the system.
  - It has no loop that guarantees the whole buffer is sent. Whether callers handle partial writes was not traced.
- **Journal.** A separate send wrapper reads from a journal instead of sending when in replay mode. In recording mode it records the send status. Journal modes are not wire traffic.

[bin] **4.20r6.** It has the same 8192-byte buffered receive. Its send and connect wrappers include journal branches.

[bin] **v5.**
- The connector sets descriptor flags before connecting.
- It retries on one numeric error code and stays pending on another.
- The send helper needs a ready state, polls for writability and sends once, again with no whole-buffer loop.
- The symbolic names of these flags and error codes were not checked.

## Machine identity

[bin] **What the helper does.** In 4.04r2, 4.20r6 and v5, one helper does the following:
- gets the I/O Kit master port;
- builds matching criteria for `IOEthernetInterface`, with an `IOPrimaryInterface` property match;
- asks for the matching services.

[inf] This is presumably where the MAC address comes from for the hash sent at login. It does not explain why that field was empty in the emulated 4.20r6 run; see [the lab note](../version-profiles/lab-mac-tiger-2026-10-31.md). The routine that reads the property and the routine that hashes it were not opened.

## 3D mission stages in Mac 4.04r2

[bin] The opened mission-stage bodies call `onGraal3DLoginStep` with these values:

| Value | When it is called |
| --- | --- |
| 1 | When the datablock download starts |
| 2 | During the ghost-object download |
| 3 | After a lighting-start request, if a condition holds |
| 4 | When lighting is complete |
| 5 | After the initial control object's GUI is set up |

**The step 5 path.** It looks up `GUIContainer3D` and attaches it if a condition holds, then runs the callback.

**Acknowledgements.** The bodies for stage 1, stage 2 and lighting complete each build matching acknowledgement work when a condition holds.

[bin] Until now this 1-to-5 numbering was documented only from the Windows plug-in; see [the Windows 4.x 3D notes](../graal3d/torque-engine-4x.md#mission-start). The Mac executable matches it.

[inf] The construction and queue helpers were not followed to bytes on the wire. These callback values are not packet ids, and this is not the classic 2D login.

## v5 event-name bridge

[bin] **v5 event names.** One v5 helper maps numbers to event names:

| Number | Event name |
| --- | --- |
| 1 and 10 | `onCreated` |
| 2 | `onEnterFrame` |
| 4 | `onMouseMove` |
| 5 | `onMouseDown` |
| 6 | `onMouseUp` |
| 7 | `onKeyDown` |
| 8 | `onKeyUp` |

Any other number takes a default path that builds a string.

**[bin] How the records are built.** A second helper:
- walks the input records and names each one with the same mapping;
- creates an output object when it first needs one;
- appends typed records. In the opened branch their tags are 1, 23, 51, 10 and 9;
- calls a payload processor;
- patches an earlier record with the collection size;
- finalizes the object.

**[bin] v3.** A static initializer builds the scripting event-name strings and collections, including the player, mouse and keyboard event names.

[inf] These numbers belong to the helper. They are not published script event ids or wire codes.

**[inf] What is not known.**
- The record layout and what the tags mean.
- Whether the records come from GS1, GS2 or Flash. The executable has both `TGraalScript` and `TFlash` type names, and that is only a lead.
- Whether any of this runs.

## Where resources go

[bin] **v3: 3D files by extension.** A helper builds paths under `levels3d` and chooses a subfolder from the file extension:

| Extension | Subfolder |
| --- | --- |
| `.dts` | `shapes` |
| `.dsq` | `anis` |
| `.map`, `.dif`, `.ml`, `.lm` | `interior` |
| `.ter`, `.hfl` | `heights` |
| `.help` | `help` |
| `.gani` | `ganis` |

For other extensions:
- A file name containing `gui` goes to `gui`.
- If the name has a qualifying underscore, its prefix becomes the subfolder.
- Otherwise the file goes to `images`.

The helper only builds the path. It does not open the file.

[bin] **v3 terrain.**
- A terrain routine has two branches, one labelled "terrain file" and one labelled "terrain chunk".
- It builds paths under `levels3d/heights`, including `heights.info` and `heightsX-Y.dat`.
- It loops over a 16 × 16 grid.
- A related helper builds a collection of 32 terrain fields.

The I/O helpers were not opened. So the file format, and whether these routines read or write, are not established.

[bin] **4.20r6 destinations.** A download helper chooses folders by extension, by name tests and by globals:

| Extension or kind | Folder |
| --- | --- |
| `.gupd` | `updatepackages` |
| `.wav` | `sounds` |
| `.gmap` | `maps` |
| `.gani` | `levels/ganis` |
| `.ttf` | `levels/fonts` |
| vector formats | `levels/vector` |
| audio formats | `levels/music` |
| video formats | `levels/videos` |

The final write, decryption and package-install helpers were not opened.

[bin] **v5.** The same helper keeps most of those branches. It also has branches that the opened 4.20r6 helper lacks:

| Extension or name test | Folder |
| --- | --- |
| `.ft` | `levels3d/trees` |
| `.po` | `levels/translations` |
| `.wba` | `levels/guistyles` |
| names containing `smilie` or `newsmilie` | `smilies` |

This is a difference between two helpers. It does not show which version first added these branches.

[bin] **What happens when a resource changes.** Both 4.20r6 and v5 have a change dispatcher. It has:
- its own paths for `.gani`, `.wav` and `.swf`;
- in v5 only, a path for `.po`;
- a refresh for objects tied to a player, with `onPlayerChanges` callback work;
- a `.gmap` branch that refreshes the map and level;
- a pass over the collections that depend on the resource.

In 4.20r6, `.gani` setters split the name into a basename and a suffix after empty and comma checks. A helper walks eight entries and re-applies matching `.gani` state.

In v5, the GANI lookup does the following:
- normalizes the name and checks for an existing object;
- appends `.gani` before fetching the content;
- can create a placeholder when a provider exists.

## Packaged resources

[file] This survey was read-only. Every file was checked against the existing manifest.

**Shared v3.**
- 718 files, including 44 compiled `.dso` scripts, 13 plain `.cs` scripts, 83 `.gani` files and a single `.gmap`.
- All 44 `.dso` files are container version 33. Each one parses to the end with no bytes left over, and every patch index is in range. This uses the container description in [the Torque scripting note](../torque/scripting.md).
- That checks the container only. It does not check the opcode map or show the scripts loading at run time.
- `main.cs` runs only `main2D.cs`.

**4.04r2 and 4.20r6.**
- The two packages differ only in their executables, `Info.plist`, `.DS_Store` files, `license/sig.graal`, and an added `levels/fonts/arial.ttf` in 4.20r6.
- Each ships nine plain `.cs` files and no `.dso`.

**Shared v5.** It ships six `.po` GUI translation files (German, English and French, for the GUI and for GUI windows), each with between 129 and 164 entries.

**All builds.** `CFBundleVersion` is the generic `0.6.1d1` in every build checked. It is not a release id.

## Limits

- The selected script function timed out in shared v3 and in both 4.x builds. No interpreter behaviour was recovered from those bodies.
- Call-graph links can miss indirect calls and callbacks. A link in the graph is not proof that the code runs.
- No rendering, gameplay, login or reply from a public service was observed. No timing was measured.

## Remaining work

- [ ] Open the callers of the context helpers and record the real arguments, including the first refresh value.
- [ ] Trace how callers handle a partial send, and how mission acknowledgements reach the wire.
- [ ] Open the record constructor and payload processor behind the v5 event-name bridge.
- [ ] Open the routines that read and hash the machine-identity property.

## Evidence

These are sanitized static summaries held by the researcher. They are registered in
[the evidence index](../docs/evidence-index.tsv). Raw exports, function lists and
digests are owner-held.

- `MAC-PPC-V3-BROAD-STATIC-20261109-R1`
- `MAC-PPC-404-BROAD-STATIC-20261109-R1`
- `MAC-PPC-420-BROAD-STATIC-20261109-R1`
- `MAC-PPC-V5-BROAD-STATIC-20261109-R1`
- `MAC-PPC-RESOURCES-BROAD-20261109-R1`
