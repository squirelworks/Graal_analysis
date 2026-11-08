# Windows 4.04r2 gmap height blocks

This note restates the research owner's sanitized `W404-E606-20261109` finding.
The publication editor did not open recovered code or the archived game asset.
Windows reader observations and the Mac file fixture are separate evidence scopes.
The indexed Windows digest identifies the researcher's derived core-analysis
carrier; the fixture digest identifies the archived Mac file. Both are
researcher-supplied. The fixture check was reported by that researcher, not rerun
by the publication editor.

## Reader support

`[bin]` The Windows 4.04r2 `GRMAP001` reader has separate branches for a coarse
`HEIGHTMAP` and named per-level `HEIGHTS` blocks. The named branch normalizes a
level filename, looks it up in the map and stores samples in that level's height
record. The reported grid capacity is nine by nine. This is reader support,
not a claim that every writer emits both forms or every server accepts them.

`[bin]` For a matching level and the required map state, the branch stores up to
nine input rows and nine float values per row, using a fixed nine-value row
stride. It does not reject a block merely for containing fewer than 81 supplied
values; excess rows or values are not stored by this branch. Missing-cell
defaults and numeric-error handling remain unmeasured. No new rendering
experiment is reported.

## File fixture

`[file]` A preserved archive-labelled Mac 4.04r2 tutorial gmap contains both a
four-by-four coarse grid and nine named per-level nine-by-nine grids. The
researcher's read-only fixture checker passed the block-structure check.
No fixture bytes, proprietary level contents or private location are published.

`[file]` This demonstrates one matching-era file structure. It does not prove
that the original Windows package shipped that file, that Windows rendered it,
or that a server processed those blocks. No client or server run was added by
this fixture check or by publication.

## Correction and limits

The earlier exclusive claim that `HEIGHTS` belongs only inside level files is
too broad. Level files can carry their own height data, and this client reader
also supports named height blocks in the gmap itself. The documented generator
and server descriptions retain their own writer/build scope.

- [x] ~~Check whether named per-level height blocks can occur inside a gmap.~~
  Reader support and the file fixture supply a bounded positive result.
- [ ] Establish rendering, server handling and any broader writer coverage separately.
- [ ] Measure missing-name and malformed-grid behavior before specifying rejection rules.

See [the source index](../workingpapers/sources.tsv) and
[the existing gmap reader note](gmap.md). This narrows Appendix E#606; it does
not authenticate the historical salvage author's intended meaning.
