# Graal Technical Reference Manual

Version 0.0.5. The target is 1.0.0; the specification and the roadmap to it are in issue #191.

This folder is the reference manual for Graal itself: clients, wire protocol, file formats, servers, listserver, RC and NC, NPC scripting, Graal3D, the Torque-era clients and tools. It is organised by subject, not by note. Start with `00-conventions.md`, which fixes scope, numbering, citation and notation.

## Layout

| File | Part |
| --- | --- |
| `00-conventions.md` | 0 Front matter and conventions |
| `01-builds.md` | I Client generations and builds |
| `02-protocol/` | II Wire protocol (§2.1 to §2.10) |
| `03-formats/` | III File formats (§3.1 to §3.10) |
| `04-behaviour/` | IV Client behaviour by version (§4.1 to §4.10) |
| `05-servers.md` | V Game servers |
| `06-listserver.md` | VI Listserver |
| `07-rc-nc.md` | VII RC and NC |
| `08-scripting/` | VIII NPC scripting (§8.1 to §8.4) |
| `09-graal3d.md` | IX Graal3D (2000) |
| `10-torque.md` | X Torque-era 3D |
| `11-tools.md` | XI Tools and the formats they define |
| `app-a-messages.md` … `app-g-tags.md` | Appendices A to G |
| `sources.tsv` | the source map: every note, `pending`, `cited` or `excluded` |

## Status

| Work-plan PR | Content | State |
| --- | --- | --- |
| 1 | skeleton, conventions, tag legend, source map, checker, CI | done |
| 2 | Part I + App. C | done |
| 3 | Part II §2.1–2.3 | done |
| 4 | Part II §2.4 + App. A | done |
| 5 | Part II §2.5 | done |
| 6 | Part II §2.6 + App. B | done |
| 6b | Part II §2.7–2.10 | done |
| 7, 8 | Part III | done (#197) |
| 9, 10 | Part IV | done (#207, #209, #210, #211) |
| 11 | Parts V to VII | done (#204) |
| 12 | Part VIII | done (#196) |
| 13 | Parts IX, X | done (#205) |
| 14 | Part XI + App. D, E | done |
| 15 | audit and PDF build | done: `check_manual.py --final` passes; `manual/pdf/graal-trm-0.0.3.pdf` built with `build_manual.py` from commit b8643ec, 347 pages A4 |
| 16 | coverage audit and 0.0.4 | done: every flagged note carried or given a reason, `check_carry.py` in CI; `manual/pdf/graal-trm-0.0.4.pdf` built with `build_manual.py --version 0.0.4` from commit 3a700ad, 377 pages A4 |
| 17 | research publication and 0.0.5 | done: the 0.0.5 research merged (#372), reading syntheses for Parts I, II, IV, VIII and X, `coverage.py` as a report; `manual/pdf/graal-trm-0.0.5.pdf` built with `build_manual.py --version 0.0.5` from commit 8559449, 306 pages (A4, with nine A4 landscape pages for six wide tables), with bookmarks, footnoted sources and a reading paragraph before every table |

## Checks

```
python tools/manual/check_manual.py
python tools/manual/check_carry.py
python tools/manual/coverage.py --notes
python -m pytest tools/manual -q
```

`coverage.py` lists every distinctive term of a cited note that the manual does not contain, per Part. It is a report, not a gate, until the 0.0.6 coverage passes have carried each miss or explained it in `manual/coverage-explained.tsv` (issue #191).

`python tools/manual/build_manual.py` builds the PDF on Linux, macOS or Windows: pandoc turns the chapters into one HTML page, then Chromium (through the `playwright` package) prints it to A4 at `manual/pdf/graal-trm.pdf`, and `pypdf` adds the bookmarks (Parts, chapters and sections) from the headings. In the PDF, each citation becomes a numbered superscript and the cited notes are listed in a closing Sources chapter that links to the repository; tables lose their Source column. Before printing, the build measures every table: one that cannot fit a portrait A4 page without overflowing, or that has six or more columns and would be squashed below two thirds of its natural width, is printed with its heading and reading paragraph on an A4 landscape page, and on A3 landscape if even that is too narrow; the build fails if any table is still wider than its page. The Markdown here keeps every citation on its own line. `--version X` puts the version on the title page and names the file `graal-trm-X.pdf`; `--out` writes it elsewhere. It needs pandoc (or `pip install pypandoc_binary`), `pip install playwright pypdf`, and `python -m playwright install chromium`. CI builds the PDF on all three systems in the `manual-pdf` job and keeps the Linux copy as a workflow artifact. The PDF is committed to `manual/pdf/` only when the owner asks for a build (work-plan PR 15). No tag or release is made from this folder without the owner's go-ahead.
