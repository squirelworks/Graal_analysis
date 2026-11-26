# Closing the partly answered 3D board rows: gap and method per row (2026-11-26)

Date: 2026-11-26. Triage of every row on the [3D capability board](3d-capability-board.md) that
is partly answered on `main` at 4c35484: the 38 rows whose status starts `partial`, plus
T3D-026, which is `assigned` but already carries partial lab results (39 rows). For each row: what
is still missing, the cheapest method that closes it, and the batch that runs it. This is a
planning table; it changes no row status. Rows close in the TSV only when the note that settles
them lands.

## Method classes

| Class | Meaning |
|---|---|
| `static` | A read of the binary (or of a note that already exists) settles the rest. No client run. |
| `lab-1` | One client against our own server on loopback inside one lab VM. |
| `lab-N` | Two or more clients in one world, all inside one lab VM on loopback. |
| `fidelity` | The same scene on a real client and on our renderer (g3d-replay), compared per feature. |
| `missing build` | Needs a build we do not hold. **No row needs one**: every gap below can be closed with builds already in the lab. |

## Batches and lab VM allocation

Two lab batches run at the same time, so each owns its own VMs and never touches the other's.

| Batch | Runs in | Rows | Expected to close |
|---|---|---|---|
| S: static reads | no VM | T3D-014, 015, 016, 021, 031, 057, 096 | 7 |
| A: single-client (5.12-class via Linux 4.20r6, and 4.04r2) | Linux lab VM only | T3D-010, 011, 020, 022, 024, 026, 034, 035, 036, 042, 045, 047, 048, 050, 052, 053, 078, 100 | 18 |
| A+: in flight, closes on merge | none | T3D-062 (closed by T3D-123, PR #945) | 1 |
| F: fidelity (after batch A) | Linux lab VM only | T3D-105 | 1 |
| W: multi-client, Windows builds, 3.153 | Windows 10 lab VM and Tiger VM only | T3D-006, 030, 051, 059, 066, 067, 070, 072, 074, 087, 089, 116 | 12 |
| | | **Total** | **39** |

Batch W already holds the Windows 10 and Tiger VMs and is running T3D-030/087 now; T3D-026 moves
from its queue to batch A because it needs the Linux 4.20r6 client, which lives in the Linux VM.
Multi-client pairs stay inside one VM (all clients and the server on loopback), so no row needs
two VMs to talk to each other. Mixed-protocol pairs for T3D-072 use the Windows 4.04r2 (19),
Windows 4.11 (21) and 5.12 (24) clients in the same Windows 10 VM (4.11 is a single packed
client; if it will not run there, the 21 leg uses Linux 4.11 in batch A's VM after batch A ends).

## Per-row plan

| Row | What is still missing | Method | Batch |
|---|---|---|---|
| T3D-006 | 3.153 has a compiler but no run has shown it executing a served or local `.cs`/`.dso`; 4.20r6 marker run not done | lab-1 (3.153 marker `.cs` beside the client and served over TCP, file trace) | W (Tiger) |
| T3D-010 | Marker `.mis` beside a 4.20r6/5.12-class client with a file trace | lab-1 | A |
| T3D-011 | Live per-extension run: serve one missing resource per extension, watch which the client asks the gserver for | lab-1 | A |
| T3D-014 | 5.12 `Sky`/`Sun` GS2 property and function names | static (likely closed by T3D-096's typed surface, PR #941) | S |
| T3D-015 | Wire mapping for `movetype`, `solid`, `collision`, `shadow`, `alpha`, `liquid*` | static (the property dispatcher), one probe only if a field stays ambiguous | S |
| T3D-016 | Why a script-made GameObject is created and fetched but never drawn (missing scene add, ghost-only draw list, or a flag) | static (the creation path); the lab half is done | S |
| T3D-020 | Opening WorldEditor / EditManager live and what it can save | lab-1 (GS2 probe opens each; file trace for saves) | A |
| T3D-021 | Receivers other than `onGraal3DLoginStep`: collisions, text, RPG message, player-enter style events | static (event-name dispatch list), confirm with the existing logging weapon in batch A if needed | S |
| T3D-022 | Both routes on our own gserver (mission phases and the phase-free route), login steps and GUI attach recorded | lab-1 | A |
| T3D-024 | Server time field: jumping time vs animations, `timevar3`, day/night | lab-1 | A |
| T3D-026 | Same world to Linux 4.20r6 and 5.12: GameObject section order and class-set diff | lab-1 on 4.20r6, compared with the 5.12 runs already written up | A |
| T3D-030 | Portals/zones (needs an enclosed interior and a player-carried camera) and collision under any client-driven movement | lab-1 (running now) | W |
| T3D-031 | How 4.04r2 picks an MD3 animation (4.04r2 cannot draw a GameObject on protocol 19, so a lab cannot show it) | static (the 4.04r2 MD3 loader and its frame selection) | S |
| T3D-034 | `.ifl` and `.dml` on a 5.12-class client (static says 4.04r2 only) | lab-1 (one shape with an `.ifl`, one with a `.dml`; expect ignored) | A |
| T3D-035 | `.dsq` on a 5.12-class client: listed but is it loaded and applied | lab-1 (shape plus `.dsq`) | A |
| T3D-036 | `.gft` fonts; a `GameShapeFT` label drawn with a valid `.ttf` (now that `.ft` is known to be a text label) | lab-1 | A |
| T3D-042 | gmap with `HEIGHTS` on a 3D server: does any terrain appear (static says no path) | lab-1 | A |
| T3D-045 | WaterBlock fog and surface look; `liquidtype`/`liquidheight` on a GameObject | lab-1 | A |
| T3D-047 | fxSunLight flag-bit count (14 or 16, two reads disagree) and which bit crashes | lab-1 (bisect the flag bits one at a time) | A |
| T3D-048 | Replicators in a world **with** a ghosted TerrainBlock: do grass and shapes scatter | lab-1 | A |
| T3D-050 | Does `setTerrain` write a heights cache; the 4.04r2 half | lab-1 (5.12-class with a file diff, then 4.04r2) | A |
| T3D-051 | Which renderer the client picks live and what each of the 8 video prefs changes | lab-1 on Windows (the D3D wrapper path needs real Windows) | W |
| T3D-052 | What lighting computes and caches; the disk-cache half is already in [lightScene caching](3d-lightscene-cache-2026-11-25.md) (T3D-092); missing: 4.04r2 vs 5.12 timing with many objects | lab-1 (timing run) plus a link to T3D-092 | A |
| T3D-053 | Files written in a 3D session (screenshots, caches) | lab-1 (one file diff of a full session with a screenshot key press; shares the run with T3D-100) | A |
| T3D-057 | The full key bind list the client handles itself | static (the default bind table; input path already in T3D-102) | S |
| T3D-059 | Missing-DLL behaviour, and the `3 ` prefix on 4.20r8 and 5.00r7 | lab-1 on Windows (remove the DLL; one entry per build) | W |
| T3D-062 | Live confirmation of the sound formats | done by T3D-123 (PR #945); closes on merge | A+ |
| T3D-066 | 4.04r2 draws no ground and no other Player, so nothing is visible | lab-N (two 4.04r2 clients in a world with a TerrainBlock and a PlayerData shape, both in its protocol-19 ghost table) | W |
| T3D-067 | Other players on 3.153 untested; 3.153 draws nothing past loading | lab-N (two 3.153 clients after T3D-089 finds a world 3.153 draws) | W (Tiger) |
| T3D-070 | Files, attachments, PMs, weapons and NPC objects between clients | lab-N | W |
| T3D-072 | Mixed-protocol pairs live (19+24, 21+24, 19+21) | lab-N | W |
| T3D-074 | Interaction where a drawable world exists: collision, mounting, `attachedtoobject`, triggers | lab-N (two 5.12 clients with GameObjects) | W |
| T3D-078 | Heightmap formats and sizes on 4.04r2 and 4.20r8 (5.12 done) | lab-1 on 4.04r2; the 4.20r8 half waits on T3D-079 (4.20r8 crashes on any TerrainBlock) and may close as "crashes first" | A |
| T3D-087 | Portals/zones and the malformed-v44 matrix; same run as T3D-030 | lab-1 (running now) | W |
| T3D-089 | Datablocks, the 12 `clientCmd` handlers and missions one type per run on 3.153 | lab-1 | W (Tiger) |
| T3D-096 | Argument ranges and GS2 reachability for every registered name | static (PR #941, in review) | S |
| T3D-100 | Files the DLL writes by itself, confirmed by a session file diff | lab-1 (same run as T3D-053) | A |
| T3D-105 | The fidelity comparison itself: fov, near/far, fog curve, lighting, filtering, mips, alpha sorting against g3d-replay (the current status text is fuzz results, not fidelity) | fidelity | F |
| T3D-116 | 3D chat seen on the 2D client; PMs and flags in both directions | lab-N (one 2D and one 3D client) | W |

## Order inside each batch

- **S**: T3D-014 and T3D-096 first (they likely close when PR #941 merges), then 015, 021, 016, 057, 031.
- **A**: one file-diff session first (closes 010, 053, 100 and feeds 052), then content formats (034, 035, 036, 011), then terrain, water and sun (042, 045, 047, 048, 050, 078), then script and session (020, 022, 024, 026), then the fidelity batch F.
- **W**: finish the running interiors work (030, 087), then 5.12 pairs (074, 070, 116), mixed protocols (072), 4.04r2 pair (066), then Windows single-client (051, 059), then the Tiger VM (089, 006, 067).

Rows that can only close with a negative ("the client never does this") still close: the note
records the run that shows it, and the status becomes `answered`.
