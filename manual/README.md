# Graal Technical Reference Manual

Version 1.0, in progress. Specification: issue #191.

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
| 6b | Part II §2.7–2.10 | stub |
| 7, 8 | Part III | done (#197) |
| 9, 10 | Part IV | stub |
| 11 | Parts V to VII | stub |
| 12 | Part VIII | done (#196) |
| 13 | Parts IX, X | stub |
| 14 | Part XI + App. D, E | stub |
| 15 | audit and PDF build | not started |

## Checks

```
python tools/manual/check_manual.py
python -m pytest tools/manual -q
```

The PDF is built only when the owner asks for a build (work-plan PR 15). No tag or release is made from this folder without the owner's go-ahead.
