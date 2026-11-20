# How the Graal3D client copes with malformed `.x` levels (2026-11-20)

Date: 2026-11-20. Evidence: **[lab]**. The February 2000 `Graal3D.exe`, unchanged, run on real
Windows 10 with Microsoft's Windows XP `d3drm.dll` placed beside the executable (Windows 10 ships
none). Levels were mutated copies of the shipped scene, loaded from the client folder. An earlier
400-mutant pass ran under Wine; its extra faults turned out to be Wine's Retained Mode stubs, not
the client.

## Result

- **One client bug.** A level mesh whose face count is inflated (for example 65536), or whose
  face indices are partly out of range, leaves the client with no collision object for the level.
  The next step reads through that empty object. Delphi's exception handler catches the fault and
  shows its access-violation error box (a read of a null pointer in `Graal3D.exe`),
  and the window then stays black.
- It is a handled exception, not a crash of the process, and the client does nothing beyond the
  read. Because the server sends levels as text in id 0 (→ manual §9.3), a server that sends such a
  level puts every client entering it into that error state.
- **Everything else loaded cleanly:** malformed structure, unknown or missing texture names,
  special float values (NaN, infinities, huge values) and out-of-range indices in other parts of
  the mesh. Across 11 Windows 10 runs there were no unhandled crashes.

## For a replacement client or server

- Check a level's face count against the faces actually present, and every face index against the
  vertex count, before building collision from it.
- A server that hosts user-made levels can apply the same check before sending one.
