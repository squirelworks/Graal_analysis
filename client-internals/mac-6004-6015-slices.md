# Mac 6.004 and 6.015: selected architecture and declared linkage

Date: 2026-11-15. Static comparison of retained architecture/header and
per-architecture dependency reports for two owner-held Mac executables. Evidence
ID `MAC-6004-6015-SLICES-20261115` in the
[evidence index](../docs/evidence-index.tsv). Nothing was run for this study.
Tags: **[bin]** for report observations, **[inf]** for comparison limits.

## What the reports establish

The inspected bundles identify themselves as 6.004 and 6.015. Each executable
contains three architecture slices: PowerPC 7400, 32-bit Intel (`i386`) and
64-bit Intel (`x86_64`). The all-architecture Mach headers identify each slice
as an executable. The architecture-list report and headers agree. **[bin]**

The per-architecture dependency reports declare OpenGL, OpenAL and AppKit for
each of the three slices of both builds. This is a statement about declared
framework dependencies, not an observed call to a renderer, audio device or
window initializer. It does not identify which framework paths a session
actually uses. **[bin]**

## What must stay architecture-specific

The [token catalogue](version-token-catalogue.md#g3d-era-30603) records the
6.004 and 6.015 Mac login-token observations as reads of their `x86_64`
connect routines. The three-slice container does not upgrade those observations
to PowerPC or `i386` evidence. A matching framework declaration likewise does
not establish matching code paths, packet layouts or script behavior. **[inf]**

These reports do not establish that every slice starts on a particular macOS
release. Successful framework loading, application/window initialization,
graphics-context creation and a first rendered frame require separate evidence.
No minimum supported OS or playable-client result is inferred here. **[inf]**

The Mac container also does not settle the Windows launcher/module boundary
for a similarly numbered build. An original startup trace must bind the exact
platform, build and selected architecture, then connect entry, initialization,
window creation and the game loop. The presence of three Mac slices supplies
none of those crosscalls for Windows. **[inf]**

## Open points

- [x] ~~Compare architecture lists, executable headers and declared OpenGL,
  OpenAL and AppKit dependencies for the inspected Mac 6.004 and 6.015 inputs.~~
  [Report observations](#what-the-reports-establish).
- [ ] Trace one selected slice from entry through application/window
  initialization to the game loop, retaining the exact-build evidence.
- [ ] Observe compatible-guest initialization and a first frame separately
  from the static trace; a first frame alone does not establish playable
  login, level drawing or input handling.
