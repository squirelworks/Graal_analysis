# Batch Linux 3.0beta / 3.01 / 3.151 clean installers

Date: 2026-11-16

Three Makeself Linux installers from the 2026-11-14 web-discovered batch were unpacked on a lab host (`upx -d` after extracting the Makeself payload). This note records what that closed, and what it does not. Tags: **[bin]** · **[file]** · **[inf]**. Evidence ids: `BATCH1-LINUX3-20261116`, `BATCH1-LINUX3151-CLEAN-20261116`.

## Builds

| Label | Installer `version=` | Token (catalogue grade B) | Role vs existing profiles |
|---|---|---|---|
| 3.0beta | `3.0` | `G3D16053` | Early Torque monolith; listed as client type 4 / gen 4 on the server side |
| 3.01 | `3.0` (component still `3.0`) | `G3D27063` | Same era as 3.0beta; still type 4 / gen 4 in server tables |
| 3.151 | product `3.15`, component `3.151` | `G3D27015` | Layout matches the Mac 3.153 tree (`languages3D`, `levels3d`, `scripts*`) |

Tokens are **not** contiguous ASCII in the UPX-unpacked `graalexe`. That matches the connect-routine one-character append method already documented for 3.x. The values above are the catalogue reads from 2026-11-13, not a new wire capture. **[bin]**

The literal `GSERVL01` is present in all three unpacked executables (text-parser / web-cache family marker already noted for 3.04). **[bin]**

## Clean 3.151 (closes the damaged-upload gap)

Earlier notes described a 3.151 Linux Makeself whose gzip payload had lost every CR LF pair (ASCII-mode transfer), so only installer metadata survived and the game binary was unusable (`protocol/v3x-clients.md`, open item in `version-profiles/3.04-3.153.md`).

The batch copy unpacks to a normal ELF: UPX decompresses cleanly, the release tree carries the 3.153-style folders, and `setup.xml` names component version `3.151`. Treat that damaged upload as superseded for binary work. **[file][bin]**

## Behaviour deltas visible without a live run

- **3.0beta → 3.01:** almost the same string surface; 3.01 adds a direct-connect preference string (`serverDirectConnect`). **[bin]**
- **3.0beta → 3.151:** large jump toward the 3.153 feature set already profiled: PM / player-list GUI class names, `TServerWeapon` / class-script related type names, `addweapon`, 3D GUI controls, and prefs such as `dontsavepasswords` / `nomassmessages`. Home-folder change to `~/.graal` is already recorded for 3.151 in the Torque notes. **[bin]**

Installer `setup.xml` for 3.0beta and 3.01 still points `update_url` at the historical Linux updates feed under the old product path; do not fetch it from a lab without a sandbox. **[file]**

## Open (still)

1. **Gen-4 wire capture** of 3.0beta or 3.01 against a lab gserver. Server tables and an invented seihai/repro link exist; no observed type-4 login or bz2 frame is held yet (`protocol/codec-and-framing.md`).
2. Full PLI/PLO tables for 3.151 Linux comparable to the 3.04 / 3.153 profiles (static send/receive pass, then a loopback lab).
3. Confirm whether 3.151 Linux speaks the same gen-5 / 2.31-shaped login as Mac 3.153 on the wire (expected **[inf]**, not yet captured).
