# Gmap file before every pre-3.0 PLAYERWARP2

Date: 2026-11-16

Why a server must put the `.gmap` file on the wire **before** each
`PLO_PLAYERWARP2` (49) for clients older than GServer's `CLVER_3` (3.0),
and why "send once per session" is not enough. Focus build: **2.22**.

Tags: **[bin]** client binary · **[cap]** loopback lab · **[srv]** open
server source as behaviour only · **[inf]** inferred from those.

## Verdict

| Claim | Result | Evidence |
|---|---|---|
| 49 with a `.gmap` name needs `LEVELNAMES` already loaded | Confirmed | [bin] |
| `LEVELNAMES` comes from the `.gmap` file on disk | Confirmed | [bin] |
| Missing file when 49 arrives → loading-screen hang | Confirmed | [bin] |
| Downloaded files are written only when `saveimages` is on | Confirmed | [bin][cap] |
| 2.22 saves a downloaded gmap under `maps/` when it writes | Confirmed | [cap] |
| "Send once per session" fails when the client did not keep the file | Confirmed as server risk | [srv] + [bin] |
| A later WANTFILE answer re-runs 49 | Not shown; treat as unsafe | open (lab) |

## What 49 does with a `.gmap` name **[bin]**

From the 2.22 (and 2.17.1 / 2.31) read in
[`gmap-adjacent-level-target.md`](gmap-adjacent-level-target.md):

- If the gmap's `LEVELNAMES` is loaded, the client clamps the cell bytes,
  swaps the gmap name for that cell's level, and **finishes the warp at
  once** (no board wait).
- If the `.gmap` is **not on disk** when 49 arrives, the load has no
  `LEVELNAMES`. The handler stops and leaves the warp waiting under the
  gmap name — the loading-screen hang.

So the file must be present as a disk file the gmap loader can open
**before** 49 is processed. That is stronger than "the client has seen
this name on the wire this session."

## Why once-per-session is wrong **[bin][cap]**

A received file is held in memory and **written to disk only when
`saveimages` is on** (default on; a missing or false key reads as off).
[`client-internals/decomp-findings-2026-10-25-e/02-save-rules.md`](../client-internals/decomp-findings-2026-10-25-e/02-save-rules.md).
**[bin]**

Lab: a 2.22 download of a `.gmap` was saved as `maps/<name>` when writing
was on. **[cap]**

A server that marks the gmap "already sent" after the first push (GServer-v2
`hasSeenFile` / known-files set) will skip the file on a later gmap warp.
If the client never wrote `maps/<name>` (`saveimages=false`, wiped
`maps/`, or a clean install), the next 49 hits the hang path above.

## What a cold 2.22 login looks like **[cap]**

On a 2×2 gmap lab (2026-10-24), the server sent 49 with the gmap name,
then level framing; the client **asked** for the `.gmap` as a file
transfer and sent `PLI_ADJACENTLEVEL` (35) for the neighbours
([`feature-specs/06-gmap-overworld.md`](../client-internals/feature-specs/06-gmap-overworld.md)).
That run had a working install; it does **not** prove that a file answer
arriving *after* 49 re-drives the warp. The static hang rule still
requires the file on disk when 49 is handled. **[bin][cap]**

## Server rule

For every client older than **3.0** (`CLVER_3` in GServer-v2 / seihai-gs2lib:
token era `G3D16053` and later):

1. On each gmap warp (login into a gmap cell, link/server warp onto a
   `.gmap`, or any other path that emits 49 with a `.gmap` name),
2. send the `.gmap` file **first** (normal / file queue, then compress),
3. then send 49.

From 3.0 on, sending once per session when the name is new remains
acceptable until a later build is shown to share the disk-only rule.

## Seihai stack check (2026-11-16)

| Repo | Hole? | Notes |
|---|---|---|
| `seihai-gserver-v2` | **Yes** | `PlayerClient::warp` only `sendFile`s when `!hasSeenFile` |
| `seihai-gserver` (Rust) | **Yes** | login burst and `warp_to` emit 49 / level framing without pushing the `.gmap` file; the client must WANTFILE |
| `seihai` client | No change needed for this lead | Clean-room client fetches the gmap into its session grid; not the production 2.22 path |

Primary production / mixed-lab host for classic 2.22 remains
**seihai-gserver-v2**; Rust seihai-gserver is the contrast server and needs
the same push-before-49 rule for pre-3.0 builds.

## Limits

- No new binary pass in this note: confirmation is from existing
  Graal_analysis reads and the 2026-10-24 2.22 gmap lab. **[bin][cap]**
- Whether a WANTFILE answer alone finishes a warp that already hung on 49
  was not re-labbed here; the safe server rule does not depend on it.
- 3.0+ gmap load paths were not re-read for this note.
