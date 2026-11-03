# Graal Analysis 0.0.3 — assignment

This file is the scaffold for revision 0.0.3. It is the brief another model (Claude) implements later. The manual is not written here. No chapter, no bible PDF, and no tag belong with this scaffold.

## What already exists

**0.0.1 is the notes binder.** Path: `release/0.0.1/`. It is on `main` via PR 187 (merged). The research notes are stitched into the PDFs listed in `release/0.0.1/README.md` (18 PDFs, 868 pages, with the source file behind each PDF). Call it the binder. Leave those PDFs where they are.

**0.0.2 is the summary.** Paths: `docs/book/00-how-to-read.md` through `docs/book/04-where-the-notes-disagree.md`, and the PDFs in `book/0.0.2/`. It is on `main` via PR 189 (merged 2026-11-03, merge `aaccd17`). Five short chapters, 45 pages: how to read, a level and a session, the player, the machines, where the notes disagree. Call it the summary. Leave those chapters and PDFs where they are.

Checked with `gh pr view` on 2026-11-03. PR 187 and PR 189 are both `MERGED` into `main`. 0.0.2 is not an open pull request.

## The job

Write a complete technical reference manual, in the spirit of Gekkio's Game Boy complete technical reference. Systematic. Exhaustive. One subsystem at a time. Every behaviour specified in plain language with its source tag, intelligible from page one.

Write it from the note tree. The binder is the evidence pile: `release/0.0.1/README.md` is the inventory of notes already gathered, and the note files are the evidence. The summary is the map of disagreements: `docs/book/04-where-the-notes-disagree.md` names the pairs and where they disagree. Do not stitch files. Do not stop at the 45-page summary.

The manual is new prose. It is not a paste of the binder and not a retelling of the summary. Put it in `docs/reference/`, one markdown file per section below. Keep this assignment. Keep the 0.0.2 chapters, the 0.0.2 PDFs, and the 0.0.1 PDFs as they are.

A section is finished when the behaviours in its source folders are specified. The titles below are the reading order, not a page budget. A behaviour those titles do not name is still specified, under its own title, in that section.

## Table of contents

Empty titles only. No section bodies in this file. A reader follows this order: how to read a claim, the level, the session, the player, the machines, the tools, open disagreements.

### How to read a claim

Source: `AGENTS.md`, the tag table in `docs/book/00-how-to-read.md`, `tools/release/how-to-read.md`.

- What a claim is
- Source tags
- Unmeasured builds
- Inferences
- A disagreement is a pair
- What this manual leaves out

### The level

Source folders: `formats/`, `tools/level-convert/`, `archive/` (level and world inventories), `graal3d/` (level files).

- Level file families
- Board, links, and arrivals
- Tiles and passage
- Signs
- Objects, chests, and bushes
- Animations
- Overworld maps
- Save games
- Graal3D level files

### The session

Source folders: `protocol/`, `version-profiles/`, `live-runs/`.

- Framing and the codec
- Login
- The walk packet
- Player properties
- Entering and leaving a level
- File transfer
- Chat, private messages, and remote control
- NPC control
- List traffic
- Peer messages
- Clients 3.x through 6.x
- The 1998 relay and the 1999 login

### The player

Source folders: `client-internals/`, `version-profiles/`, `archival/`.

- The body and the step
- Sword, hurt, and knockback
- Death and return
- Carry, hide, and the glove
- Water, lava, and animations
- Ledges, push, and pull
- Status
- Speech and the sign panel
- Items
- Differences by build

### The machines

Source folders: `server-notes/`, `ash/`, `graal3d/`, `torque/`, `tools/lab-servers/`, `npc-library/` (commands the host runs). List behaviour also uses the listserver notes in `protocol/`.

- The list
- HQ level 0 on a list
- The game server
- The script host
- Graal3D
- Torque

### The tools

Source folders: `tools/`, `recovered-drive-tools/`, `recovered-hacks/`, `archive/`, `npc-library/` (the script corpus).

- Editors
- Generators and converters
- Classic list and stat tools
- Recovered programs
- Trainers
- The script corpus
- Asset inventories

### Open disagreements

Map: `docs/book/04-where-the-notes-disagree.md`. Evidence is the notes that map cites. Pair titles already on that map:

- Bushes, walls, and the passable lists
- Knockback in 1.39
- Listserver shapes
- How many bits a Z3 code uses
- Whole tiles and fractions
- Where a sign list ends
- An offset after playerx
- What GENERATED names, and where HEIGHTS lives
- Which board GraalEditor writes
- A sketch that still prints another frame

## Rules

- Source tags stay on the claim they belong to. `AGENTS.md` names `[2.05]`, `[bin]`, `[lab]`, `[cap]`, `[srv]`, `[doc]`, `[inf]`. A tag the notes already add stays when that note uses it, including `[file]`, `[live]`, `[wire]`, `[run]`, `[shot]`, `[test]`, `[src]`, `[GE]`, `[checked]`, and a build tag such as `[2.22]`.
- Unmeasured builds stay unmeasured. A figure from one build stays on that build.
- Disagreements stay as pairs. Both claims, both tags. The manual does not pick a winner and does not fold two figures into one.
- No invented numbers. A number in the manual comes from a note.
- Leak rules: no dotted IPs, no `FUN_` or `DAT_` names, no `0x` offsets, no official hostnames, no Drive URLs. Community handles that the notes already use may stay.
- No tag unless Chiaki is told to cut `v0.0.3`. This scaffold does not tag, merge, or push `main`.

## How to check the result

A new reader can answer each of these from the manual alone. The citation is still on the sentence:

- what a walk packet contains
- when a bush returns
- what HQ level 0 does on a list

The answer is the specified behaviour. The citation is the note path and the source tag. The reader does not have to open a second file to learn the fact.

The same check applies to any other behaviour the source folders record. A section that only points at the binder, or that ends where the 45-page summary ends, is not finished.

## The notes viewer

The notes viewer on `main` is the browser for the notes, not a substitute for the bible. From a checkout: `python3 tools/navigator/navigator.py`, loopback port 8765. `tools/navigator/README.md` describes the map. `tools/navigator/` is not a section of the manual.
