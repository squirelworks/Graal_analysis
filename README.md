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
  [0.0.9](https://github.com/squirelworks/Graal_analysis/releases/tag/v0.0.9)
  (415 pages): download `graal-trm-0.0.9.pdf` from the release, or the A4 print
  set and A3 insert next to it. Every release keeps its section numbers for good,
  so "manual §4.12 (0.0.9)" always means the same text. The Markdown source is in
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

## Getting started

Most people only need the manual PDF from the release. To work with the notes
and tools, you need Git and Python 3.12 or later; the tools below use
only the standard library unless their row says otherwise.

```
git clone https://github.com/squirelworks/Graal_analysis
cd Graal_analysis
python3 tools/navigator/navigator.py      # then open http://localhost:8765
```

The navigator is a small local viewer for the notes. It only listens on the
loopback address and fetches nothing from the internet.

## Running the tools

There is nothing to build: every tool is a script you run with `python3`.
Each folder under [`tools/`](tools/README.md) has its own README; the ones
you are most likely to use are below. Scripts with `-h` print their options.

| Command | Arguments |
| --- | --- |
| `tools/navigator/navigator.py` | `--port PORT` (default 8765), `--host HOST` (loopback only; anything else is refused), `--repo DIR` (default: this checkout). |
| `tools/manual/build_manual.py` | `--version LABEL` (shown on the title page and in the file name), `--out PDF` (default `manual/pdf/graal-trm[-VERSION].pdf`), `--html FILE` to keep the HTML too, `--chromium PATH` to use your own Chromium, `--root DIR`. Needs pandoc and the `playwright` and `pypdf` packages. |
| `tools/level-convert/convert.py SRC DST` | Converts between `.zelda`, `.graal`, `.nw`, `.gmap` and `.seihai`; the suffixes choose the formats. Exit code 1 for a truncated file, 2 for any other refusal. |
| `tools/gs1-lint/gs1lint.py PATH...` | Checks GS1 NPC scripts against the 2.05 command table; `-q` prints errors only. |
| `tools/leak-check/check_addresses.py [ROOT]` | The address and disassembler-name check CI runs; run it before you open a pull request. |
| `tools/lab-servers/listserver.py [LOGFILE]` | The lab listserver, on the loopback address. `--accounts FILE` (lines of `account password`; only those may log in), `--name TEXT`, `--greet-delay S` (default 1.5). `run-lab.sh` starts it with a GServer-v2 build, `run-lab.sh stop` stops both; see its README. |

To run the same tests CI runs, on Linux, Windows or macOS:

```
python3 -m pip install pytest
python3 -m pytest tools/navigator tools/file-formats tools/level-convert -q
```

To build the current manual yourself:

```
python3 -m pip install playwright pypdf     # and install pandoc
python3 -m playwright install chromium     # or pass --chromium PATH
python3 tools/manual/build_manual.py --version 0.0.9
```

## Contributing

Contributions go through pull requests. Before opening one, read
[`AGENTS.md`](AGENTS.md) for the house rules: no addresses or hosts, how labs are
run, and the leak checks to run on your diff. Add any new note to the
[notes index](INDEX.md) in the same pull request. Releases follow
[`VERSIONING.md`](VERSIONING.md).

## Status

The manual is at 0.0.9 and still well short of 1.0.0. The roadmap is in
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
