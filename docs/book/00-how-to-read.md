# How to read this book

Graal Analysis, revision 0.0.2.

This repository holds cleaned notes on Graal: how a level is stored, how a client talks to a server, how the player moves and dies, and how the programs around that session behave. The notes stay in their folders. This book is a reading of them, written so a new reader can start here.

Revision 0.0.1, printed under `release/0.0.1/`, is those notes in repository order, with appendices. Chiaki tags `v0.0.1`. This revision is the reading in `docs/book/`. The 0.0.1 files stay where they are.

## What this project is

A fact in these notes is a piece of behaviour, written in plain language, with a mark for where it came from. The working notes live beside the code and the captures they describe. This book cites them by path. It does not reprint them.

The observations were made on the loopback address, in a lab this project ran, or by reading a program or a file the archive already held. Public servers are outside that work. `AGENTS.md` is the rule for what may be written down.

Two uses of the word generation are easy to mix. One is the family of the level file: Z3-V1, GR-V1, GLEVNW01, then a gmap that names levels. The other is the family of the connection: the 1998 text relay, the 1999 compressed login, and the later ciphers. They changed on different calendars. Chapter 1 keeps them apart.

## What a source tag means

A tag in square brackets belongs to the claim it sits on.

| Tag | Where the claim came from |
| --- | --- |
| `[2.05]`, `[2.22]`, `[2.31]` | A read of that client |
| `[bin]` | A static read of a program |
| `[file]` | A shipped file |
| `[doc]` | A readme, a manual, or a release note |
| `[srv]`, `[src]` | Server source |
| `[lab]`, `[live]` | A client this project ran |
| `[cap]`, `[wire]`, `[run]` | A capture or a loopback session |
| `[shot]` | A still from a run |
| `[test]` | A check against real files |
| `[inf]` | An inference the note marked as one |
| `[GE]` | The GraalEditor notes |
| `[checked]` | A search of named builds for a script word |

`AGENTS.md` names the set `[2.05]`, `[bin]`, `[lab]`, `[cap]`, `[srv]`, `[doc]`, `[inf]`. The other tags are the ones the working notes add when a claim is a file, a still, a server tree, or a search. A sentence in this book with no tag is the arrangement of tagged claims. A number in this book comes from a note. Nothing here adds a measurement.

## What is not claimed

A build that was never opened for a rule stays unmeasured. A neighbour's number is not copied across to fill the gap. Chapter 2 says so each time a year was timed for the step and not read for the sword or the death clock.

An inference stays an inference. A string found in a program, with no caller found, is a string in a program.

Where two notes do not say the same thing, chapter 4 quotes both. This book does not choose between them, and it does not fold two figures into one.

Decompiled listings, binary addresses, and disassembler names are not in this book. People already named in the notes stay named.

## How the chapters sit

1. **A level and a session.** The file under the player's feet, then the bytes of one login, one board, and one walk.
2. **The player.** The body, in time order, from September 1998 through the later Windows builds.
3. **The machines.** The directory, the game server, the script host, the staff window, the offline tools, the 3D servers, and the trainers.
4. **Where the notes disagree.** The pairs the notes leave open, and what would settle each pair.

The walk message is explained in chapter 1. Later chapters use it. Each death clock is told in the era that has it. A bush growing back is the server's timer; the rectangle on the wire is told once, with the waits that belong to each lab.

The notes viewer is already on `main`. From a checkout of this repository:

```
python3 tools/navigator/navigator.py
```

It listens on the loopback address, port 8765. `tools/navigator/README.md` describes the map. The program stays in the source tree.
