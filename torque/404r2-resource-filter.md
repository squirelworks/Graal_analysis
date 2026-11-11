# Windows 4.04r2 3D resource filtering and native mission path

This is the research owner's retained-code review of the original-carrier
4.04r2 plug-in captured by earlier load-only work. It is not the later
file-version 4.2.0.8 image. The publication editor reviewed the sanitized
fragment and source manifest, not raw code or captured binaries.

## Download filter

`[bin]` Short `.dso` and `.cs` literals exist in the captured plug-in but were
omitted from the earlier defined-string export. They are used by one resource-miss
download branch: normalize a filename, extract its extension, and request a
download only when it differs from `.dso`, `.cs` and `.ter`. Source:
`W404-E502-E503-20261109`.

`[bin]` This disproves the categorical absence of `.dso` literals in this
4.04r2 image. It establishes exclusion from that download branch, not an absence
of separate local readers, all possible file access, or a TorqueScript compiler.
The later 5.00r7 and 5.12 subjects are not re-evaluated by this finding.

## Positive native mission path

`[bin]` The mission-start handler dispatches three recognized phases to native
datablock, ghost and lighting routines. The ghost reader constructs network
classes and adds the resulting objects to the mission group; a separate path
handles deferred preloading. This positively identifies a network-populated
mission path. Source: `W404-E502-E503-20261109`.

`[bin]` Neither this path nor the extension filter rules out a separate local
mission-file loader or a reachable compiled-script reader. Indirect and GS2
file-access paths remain untraced. No new successful 3D session or local-file
trace was obtained, and no wire behavior was newly measured.

## Editorial disposition

- [x] ~~Recheck the claim that the 4.04r2 image has no script-extension literals.~~
  Retained code supplies the counterexample and its filter use.
- [x] ~~Identify positive native mission construction rather than arguing from string absence.~~
  The phase/ghost path above supplies that bounded result.
- [ ] Trace local mission/script readers and their reachability before closing E#502–503.
- [ ] Validate local-file access in an authorized isolated 3D session before claiming runtime behavior.

Evidence digests in [the source index](../docs/evidence-index.tsv) are
researcher-supplied. The captured image came from prior load-only work; this
static follow-up did not initialize a playable 3D world. Private mappings,
raw code and evidence records remain owner-held.
