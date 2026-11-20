<!-- manual: kind=front status=complete -->
# Appendix F. Source map

The source map ties every note in the repository to the manual. It lives in `manual/sources.tsv`, one row per note, so the map is checked by machine rather than kept by hand here. This appendix says what the map holds, what each status means and how the checks use it. The citation form that links a manual line to a note is fixed in → §0.3, and the checks themselves in → §0.11.

## F.1 Columns

Each row of `manual/sources.tsv` has five tab-separated columns.

| Column | Holds |
| --- | --- |
| `path` | the note's path from the repository root; every `.md`, `.tsv`, `.toml` and `.txt` note outside `manual/` has exactly one row |
| `status` | `cited`, `excluded` or `pending` (F.2) |
| `sections` | the manual files that cite the note, by their number: a Part (`5`), a chapter (`4.12`) or an appendix letter (`E`), separated by `;` |
| `planned` | the sections the note was expected to feed when its row was written |
| `reason` | for an excluded note, why the manual leaves it out; for a cited note, where its facts went when the carry rule (F.3) would otherwise flag it |

## F.2 Statuses

| Status | Meaning |
| --- | --- |
| `cited` | at least one manual line cites the note with a `[tag] (path)` source, and its `sections` column lists every manual file that does |
| `excluded` | the manual does not cite the note, and the `reason` column says why |
| `pending` | the note is not carried yet; allowed only between releases, since `check_manual.py --final` fails on any pending row |

The usual reasons for an exclusion are these:

| Kind of note | Why it is excluded |
| --- | --- |
| reimplementation plans and design (Seihai and its tools) | the manual covers Graal, not a reimplementation (→ §0.1) |
| table or index forms of another note | the note they index is cited instead |
| raw lab tables (probe results, per-key sweep tables) | the lab write-up that derives them is cited |
| working drafts, binders and earlier book editions | draft inputs, superseded by the notes they were built from |
| repository tooling, procedures and release notes | not about Graal |
| per-sample notes on trainers and hacks | out of scope except where they document the client's integrity checks (→ §4.10.1) |
| inventories of owner-held material | they describe what is held, not how Graal behaves |

## F.3 How the checks use the map

| Check | Rule |
| --- | --- |
| `tools/manual/check_manual.py` | every note has a row; every cited path exists; a file that cites a note must be listed in that note's `sections`; a `cited` row lists at least one section; an `excluded` row has a reason; with `--final`, no row is `pending` |
| `tools/manual/check_carry.py` | for a `cited` row with no reason, every `planned` section must be among those that cite it, and enough of the note's distinctive terms (message names, constants, magics) must appear in the manual; a note that fails needs a reason |
| `tools/manual/coverage.py` | a report, not a gate: the distinctive terms of each cited note that the manual does not contain, per Part |

In the PDF, each citation becomes a numbered note, and the cited notes are listed in a closing Sources chapter that links to the repository (→ §0.11).
