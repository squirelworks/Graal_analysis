# Graal Analysis

Field notes on how the Graal Online client and servers actually work: the
network protocol, file formats, NPC scripting, level design and the way each
client version behaves. The work started with a close study of the Windows
client 2.05 rev 2 and has since grown to cover Graal from the 1998 betas through
the 6.x clients, the classic game servers, the listserver, the RC and NC staff
tools, Graal3D and the Torque-era clients.

The notes are written as plain behaviour, with a tag saying where each fact came
from. They are the research base for [Seihai](https://github.com/squirelworks/seihai),
an open Graal client and server suite written from scratch.

## Start here

- **The Graal Technical Reference Manual.** The notes, organised by subject into
  one book. The latest edition is
  [0.0.7](https://github.com/squirelworks/Graal_analysis/releases/tag/v0.0.7)
  (394 pages): download `graal-trm-0.0.7.pdf` from the release, or the A4 print
  set and A3 insert next to it. Every release keeps its section numbers for good,
  so "manual §4.12 (0.0.7)" always means the same text. The Markdown source is in
  [`manual/`](manual/README.md).
- **The [notes index](INDEX.md).** Every individual note, with a one-line summary.
  Notes are often more detailed than the manual and carry the raw tables.
- **The [version token map](VERSION-TOKENS.md).** If you have a client and want to
  know which build it is, or which login token a build sends, start here.

## What is in the repository

| Folder | What it holds |
| --- | --- |
| [`manual/`](manual/README.md) | The reference manual source, its figures and the release PDFs (`manual/pdf/`) |
| [`protocol/`](protocol/) | The wire protocol: framing, ciphers, login, packets, props, file transfer, lab runs against real clients |
| [`formats/`](formats/) | Levels (`.nw`, `.graal`, `.zelda`), gmaps, ganis, tiles, saves and caches |
| [`client-internals/`](client-internals/) | How the clients behave inside: input, rendering, combat, the GS2 virtual machine, per-version differences |
| [`version-profiles/`](version-profiles/) | Build-by-build profiles and the version matrix |
| [`npc-library/`](npc-library/README.md) | GS1 and GS2 scripting: commands by version, compiler behaviour, and original example scripts |
| [`server-notes/`](server-notes/README.md) | The classic game servers and how they differ from GServer-v2 |
| [`graal3d/`](graal3d/README.md), [`torque/`](torque/README.md) | Graal3D (2000) and the Torque Game Engine era (3.x to 5.12) |
| [`tools/`](tools/README.md) | Decoders, converters, fuzzers, lab servers, the manual builder and notes on the classic Graal tools |
| [`docs/`](docs/) | Release notes, the research plan, the evidence index and the citable data files |
| `live-runs/`, `recovered-*`, `archive/`, `archival/`, `ash/`, `book/`, `release/` | Lab run records, notes on recovered tools and hacks, earlier editions and archived material |

## How to read a note

Each finding carries a source tag: `[bin]` read from a client binary, `[lab]`
seen in a lab run, `[cap]` from a packet capture, `[srv]` from server source,
`[doc]` from a readme or other document, and `[inf]` for a step the note marks
as an inference. A build tag such as `[2.05]` or `[5.12]` means the fact was read
from that client build. Appendix G of the manual has the full legend. Open
questions are kept as task lists in each note and gathered in Appendix E.

## What is not here

This is a public repository, so some things never go in it:

- no raw decompiles, disassembly, binary addresses or tool-generated function names;
- no client binaries, game assets, packet captures or raw lab logs;
- no real server addresses or hostnames (lab notes use the loopback address and
  placeholders);
- no script text copied from the original game levels.

## Building and checking

The tools are Python 3.12. CI runs the leak checks and the tool tests on Linux,
Windows and macOS (see [`.github/workflows/checks.yml`](.github/workflows/checks.yml)).
To run the same tests locally:

```
python -m pip install pytest
python -m pytest tools/navigator tools/file-formats tools/level-convert -q
```

To build the manual PDF yourself you also need pandoc and the `playwright` and
`pypdf` Python packages:

```
python tools/manual/build_manual.py --version 0.0.7
```

`python3 tools/navigator/navigator.py` starts a small local viewer for browsing
the notes in a browser.

## Contributing

Contributions go through pull requests. Before opening one, read
[`AGENTS.md`](AGENTS.md) for the house rules: no addresses or hosts, how labs are
run, and the leak checks to run on your diff. Add any new note to the
[notes index](INDEX.md) in the same pull request. Releases follow
[`VERSIONING.md`](VERSIONING.md).

## Status

The manual is at 0.0.7 and still well short of 1.0.0. The roadmap is in
[#191](https://github.com/squirelworks/Graal_analysis/issues/191) and the research
toward it in [#370](https://github.com/squirelworks/Graal_analysis/issues/370).
The largest open areas are GS2 syntax and its built-in library, and exactly what
a public 5.x or 6.x login server sends.

## Licence

- **Notes, tables, figures and books** (the Markdown, TSV, SVG and PDF files):
  [Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0). Share
  and adapt them freely; credit "Graal_analysis by squirelworks" with a link
  back here.
- **Scripts and tools** (Python, shell and other source files): [Apache License
  2.0](LICENSE-CODE), the same as the Seihai server stack.
- **Patches against GPL servers** in `tools/lab-servers/` are GPL-3.0, like the
  code they patch.

This is an independent fan project. It is not affiliated with, endorsed by, or
connected to GraalOnline. "Graal" is used only to identify the software these
notes describe.
