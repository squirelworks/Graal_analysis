# How to read these notes

Graal Analysis 0.0.1 is a document set of the notes in this repository.
The chapter PDFs follow the contents list in `README.md`. Chiaki tags `v0.0.1`.

## Boundary

`README.md` and `AGENTS.md` in this volume state the boundary. The notes
are cleaned observations. Raw decompiles stay out of the repository. A
fact is written as plain behaviour and carries a source tag.

## Source tags

`AGENTS.md` names these tags: `[2.05]`, `[bin]`, `[lab]`, `[cap]`, `[srv]`,
`[doc]`, `[inf]`.

The gap-fill section of `README.md` glosses `[2.05]` as confirmed in 2.05,
`[srv]` as server source only, `[doc]` as the 2.22 docs, `[cap]` as
captures, and `[inf]` as inferred.

`version-profiles/matrix/README.md` (in the client-internals volume)
glosses `[bin]` as read from the client binary, `[file]` as shipped files,
`[live]` as seen in a running client, `[cap]` as a packet capture, `[srv]`
as server source, `[doc]` as release notes, and `[inf]` as inferred.

## Notes viewer

After `git pull` of the tagged source, run:

```
python3 tools/navigator/navigator.py
```

The viewer listens on loopback port **8765**. No virtualenv is required.
`tools/navigator/README.md` describes the map UI. The program stays in the
source tree and is not reprinted as a PDF.

## Left in the source tree

NPC script bodies stay in `npc-library/` as `page.json` files. The
script-name appendix lists each script's image name, genre, and topic.

Machine-readable `.toml` and `.tsv` tables stay next to the notes that
describe them.

Drive links in three source notes are omitted from these PDFs.
