# v7 Graal3DEngine: discovery rollup

Date: 2026-11-08

Index of cleaned notes for WorldsSetup64-614 (and sibling builds where noted). **[bin]** unless marked.

---

## Notes map

| Topic | File |
|---|---|
| Identity / token / six builds | `v7-graal3d-identity-and-builds.md` |
| Framing / ciphers / remapper model | `v7-graal3d-framing-and-packet-tables.md` |
| PLI + PLO (`tclient_*`) tables | `v7-graal3d-pli-plo-tables.md` |
| Property streams | `v7-graal3d-property-streams.md` |
| Script property registry (95 names) | `v7-graal3d-player-properties.md` |
| GS2 / GRESCR | `v7-graal3d-gs2-and-scripts.md` |
| Files / packages | `v7-graal3d-file-and-packages.md` |
| Chat / board / warp / UDP | `v7-graal3d-chat-world-udp.md` |
| Unity bridge | `../client-internals/v7-graal3d-unity-bridge.md` |

Work JSON (addresses OK): `Graal_analysis/_work/ghidra_v7_614/`.

---

## Status

| Item | Status |
|---|---|
| PLI gaps + ispker | **done** (shared remapper cells) |
| PLO `tclient_*` list + payloads | **done** (92 names); native slot order open |
| PLPROP / NPCPROP | **done**; BDPROP walk thin |
| GRESCR DES + key contract | **done** |
| GS2 opcode map | **open** (needs decrypted body) |
| Wire-id maps | **not claimed** (runtime remapper) |
| Login token cleartext | **absent** |
| Package filenames | `basepackage.gupd` + paths; full package_* list script-side |
| UDP peer | codec fields only; socket path unproven |
| Unity exports | **done** |
| Six-build diff | Flavor0 rename on 71243; same Quattro/crypto set |

---

## Still open (honest gaps)

1. Live remapper dump → real wire ids.  
2. GS2 opcode switch from a decrypted GRESCR.  
3. Native slot 0…94 ↔ `tclient_*` ordered table.  
4. Baddy encode/decode case walk.  
5. Exact upload/download numeric caps.  
6. Whether production Worlds calls `setprotocol` after connect.
