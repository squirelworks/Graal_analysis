# Archival notes — local research workspace decommissioned

**Date:** 2026-10-28

The local Graal research workspace (gserver dumps, Phoenix binary package, Ash Python rewrite, Ember architecture atlas, and the 39-chapter GServerStory narrative) has been decommissioned.

The full contents were archived as a single zip:

- **Google Drive:** `/[Grok/[Projects/Graal gServers.zip`
- **Direct link:** https://drive.google.com/file/d/1XtT0MEltbmApGG5_cL_TmR8QnvgPYsAS/view?usp=drivesdk
- **File ID:** `1XtT0MEltbmApGG5_cL_TmR8QnvgPYsAS`
- **Size:** ~27 MB

That archive contains the original source dumps (`graal gservers/`), the Reborn 2.4.0 Phoenix package, the Ash Python reference server, the Ember atlas (markdown + ATLAS.html), the complete GServerStory, and supporting files.

## What is already in this repository

This repo (`Graal_analysis`) holds the cleaned client-focused notes, protocol tables, format documentation, version profiles, and decompile findings derived from public sources and observed behavior. It deliberately excludes raw decompile material.

## What was added from the local workspace

Under `server-notes/` you will find high-value extracts from the Ember atlas and related materials that document the *server* side of the same protocol surface:

- Lineage of the dumps (1.3.x monolith → gs2emu → Phoenix → Ash)
- Protocol framing, G-integers, login, props, file send, listserver IDs
- Algorithms and pseudocode (LCG, gen-3 dummy byte, gen-4/5 XOR stream, login, warp, baddies, trigger hacks, RC file browser, etc.)
- Architecture and on-disk blueprints (see the original Ember files in the Drive archive for the full set)

These notes are faithful to the dumps and the Ash rewrite; nothing was invented about the protocol. They complement the client-centric material already in this repository.

## Ash as a readable reference

The Ash Python server (included in the Drive archive) is a deliberate cut-down rewrite of the gs2emu protocol surface. It implements gens 3–5, GRACC001 accounts, GLEVNW01 levels, listserver register/ping, RC, gmaps, baddies, and trigger-action hacks. It is useful as a readable companion to the C++ dumps when implementing a server.

## Prior attempts

The local workspace also contained earlier attempts to map the environment:

- Phoenix: packaged Reborn 2.4.0 binary (port 14802) with a named world
- Ash: the Python rewrite described above (port 14812, offline login)
- Ember: the architecture atlas that walks the dumps
- GServerStory: a narrative walk through the engines in learning order (chapters 1–39 + command index)

All of those materials remain available in the Drive zip for anyone who needs the original trees or the full narrative.

---

*This file was added when the local research project was decommissioned. The Drive archive is the authoritative source for the original dumps and the complete Ember / GServerStory materials.*
