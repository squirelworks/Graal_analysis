# Ash — 39ster 2.1 GServer architecture pack

Source of truth (do not edit the museum):

`39sters-2.1-Gserver/39ster's 2.1 Gserver/win32Gserver/`

This folder is a reverse-engineered blueprint of that 2006 tree: modules, wire format, packet tables, level codec, and the algorithms the server actually runs. Comments in the original headers lie in a few places (opcode numbers after 83). The `msgFuncs[89]` table and the C enums (which increment by one) are authoritative.

| File | What it is |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System view, process model, class graph, data stores |
| [BLUEPRINT.md](BLUEPRINT.md) | File-by-file ownership, runtime layout, wire frames, known holes |
| [FLOWCHARTS.md](FLOWCHARTS.md) | Mermaid flowcharts: boot, tick, login, warp, animate, files |
| [ALGORITHMS.md](ALGORITHMS.md) | Pseudocode for scramble, zlib frames, GCHAR, GR-V1 tiles, IDs |
| [OPCODE-MAP.md](OPCODE-MAP.md) | Client / server / prop / baddy / NPC tables (already present in repo) |
| [diagrams.html](diagrams.html) | Same mermaid diagrams in a browser-renderable page |

Phoenix rebuild notes lived separately. Ash describes the **2006 server as written**, not the rewrite.

Default listen port: **14822**. Start map used by the stub account loader: **level13.graal**.

This archival copy was added from the decommissioned Graal 39sters gServer analysis project (October 2026).
