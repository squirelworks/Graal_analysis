# 3D client conformance suite

Date: 2026-11-26. Small worlds and GS2 probe scripts that each exercise one
thing the [3D capability board](../3d-capability-board.md) has found, with the
expected result for each client build, and a runner that plays them on the
real clients in lab VMs and writes a derived results table.

The board says what each build does. The suite turns those answers into runs
that can be repeated: after a gserver change, on another build, or to turn a
`?` into a board answer. A case whose observed result differs from its
expectation is either a regression in our server or a board row to revisit.

| File | What |
|---|---|
| [`cases/*.toml`](cases/) | one case each: a world, optional probe script, checks, expectations per build |
| [`scripts/*.gs2`](scripts/) | the GS2 probes (`weapon3d`), compiled at link time by seihai-gserver with seihai-core's compiler |
| [`EXPECTED.md`](EXPECTED.md) | every case's expected result per build (generated) |
| [`results.tsv`](results.tsv) | one line per lab run, appended by the runner (derived data only) |
| [`RESULTS.md`](RESULTS.md) | the latest verdict per case and build (generated) |
| [`tools/conformance/`](../../tools/conformance/) | the content generator, the judge, the VM runner and their tests |

Builds: **3.153, 4.04r2, 4.20r8, 5.12, 6.037** (the 6.03r7 retail client, which
the board reads as a 2D-only Quattro build, T3D-121, so its cases check that it
does *not* link). A case may add another build as its own column; the first
batch adds `4.20r6L`, the Linux 4.20 (`G3D22126`) most single-client board labs
ran on.

## A case

```toml
id = "C005"
slug = "cube-red"
title = "A .3ds cube with one red material at the spawn is fetched and drawn"
rows = ["T3D-032", "T3D-106", "T3D-011"]   # board rows it exercises
priority = 1                               # 1 runs first

[world]                                    # config/graal3dworld.txt (seihai-gserver docs/GRAAL3D.md)
lines = """
object ConfCube conf_red.3ds 0 0 1
...
"""
files = ["conf_red.3ds", "conf_sky*"]      # generated content to serve (gen_content.py)
                                           # "served=generated" serves a file under another name
scripts = []                               # probes, sent as weapon3d ConfProbe
grid = []                                  # [{name, shape, nx, ny, step, z}]: nx x ny object lines

[server]                                   # optional
kind = "seihai"                            # or "v2": run on seihai-gserver-v2 (see below)
options = []                               # extra server.txt lines (serveroptions.txt for v2)
flags = []                                 # config/serverflags.txt lines
lobby_name = "3 Conformance"               # the name the lobby warps to

[run]
seconds = 60                               # per session
sessions = 1                               # >1: relaunch the client on the same server run
keep_cache = false                         # true: keep the client's download cache between sessions
between = []                               # [{swap, with}]: served files swapped before each later session
mid_action = ""                            # or "stop-server" / "inject-junk" / "inject-flood" half way

[[check]]
id = "red_drawn"
kind = "pixel"                             # see below
colour = [220, 0, 0]
min_fraction = 0.002

[expect."5.12"]
red_drawn = true                           # true, false, or "?" (record, do not judge)
source = "[lab] T3D-032 ..."               # where the expectation comes from
```

Check kinds, each reading one artefact of the run:

| Kind | Reads | True when |
|---|---|---|
| `trace` | the gserver's `graal3d_trace` file | `pattern` (a regex) matches |
| `server` | the gserver log (`--verbose`: logins, file requests, control object) | `pattern` matches |
| `probe` | the gserver log: a probe's `triggerserver("gui", "ConfProbe", "cf", key, value)` arrives as `trigger ignored (...)`, or on seihai-gserver #214 and later, which routes it to the server weapon, as `trigger sent (...)` (any `trigger <word> (...)` line with the arguments is read) | some report of `key` matches `value` |
| `console` | the client's console log(s) | `pattern` matches |
| `files` | a listing of the client folder after the run | `pattern` matches |
| `inject` | the output of the case's `inject-junk` or `inject-flood` mid action (`guest/junk.py` in the server VM) | `pattern` matches |
| `alive` | the guest's process list just before the client is closed | the client's exe is still running (no crash) |
| `pixel` | the last screenshot | at least `min_fraction` of the screen is within `tol` of `colour` |
| `blobs` | the last screenshot | at least `count` separate regions of `colour`, each of `min_pixels` or more (e.g. two players' cubes) |

A text check (`trace`, `server`, `console`, `files`, `inject`) with `count = N`
is true when the pattern matches at least N times. In a multi-session case the
last session's client artefacts are judged (earlier ones stay in `s1`, `s2`,
...), and the server log and trace span every session.

A check with `client = 2` reads the second client's artefacts in a two-client
case (`[run] clients = 2`); the server log and trace are shared.

Pixel checks count a colour over the whole screen rather than at a position,
so they hold for a windowed client wherever its window sits. The generated
content uses colours that nothing else on a lab desktop has.

A run is **PASS** when every judged check matches, **FAIL** with the checks
that did not, **ERROR** when an artefact a judged check needs is missing
(for example no screenshot), and `?` checks are recorded in `results.tsv`
either way. Every probe case also checks that seihai-core compiled the probe
(`compiled = false` everywhere: the gserver logs `not compiled` otherwise).

## Content

Everything a world names is generated by
[`gen_content.py`](../../tools/conformance/gen_content.py): `.3ds` cubes (one
with a red material, one with none, one textured), solid-colour sky faces as
PNG and GIF, an overlay image, `.cs`/`.ter` markers, and a flat 256 x 256
streamed terrain (`[world] terrain = ["conf_ter"]`: 256 chunk files in the
client's own cache format, `torque/terrain-512.md`) with its `heights.info`
and one texture. No client asset is needed and nothing generated is
committed.

Cases that need held content name a pack in `needs` and take copies from it
with `derive` (the first file matching `pick`, its version word set to
`version`): the `.dts`/`.dif` version-bound cases (C016, C017) take one held
version-24 `.dts` and one version-44 `.dif`. The runner runs them only when the
lab config's `[packs]` names that pack, and the derived files stay in the work
folder like every other world.

## The runner

[`run.py`](../../tools/conformance/run.py) runs on a lab host, never in the
cloud, against a lab config that stays on that host
([`lab.example.toml`](../../tools/conformance/lab.example.toml) is the
template):

- **Two VMs, one VM-only link.** The server VM (a Linux lab VM) runs
  seihai-gserver with the case's world, the conformance lobby
  (`guest/lobby.py`), DHCP and DNS for the link (`guest/labnet.py`) and an
  artefact receiver. The client VM runs one real client. They are joined by a
  QEMU `dgram` link over two Unix sockets in the work folder: no host address
  and no outside network. The server VM's only other NIC is restricted user
  networking (`restrict=on`) with one SSH forward on the host loopback, the
  runner's management channel. A Windows client VM has nothing but the lab
  link and is driven over QMP (keys, mouse, screendump). The server VM answers
  on the addresses the client images already dial (they were set up on QEMU
  user networking), so the images need no change.
- **Two clients.** A two-client case runs the build in two client VMs: the
  second (`slot = 2` in the lab config) is on a second dgram link to a second
  NIC of the server VM, the two NICs bridged inside it, and `labnet.py` gives
  it its own address by MAC. Only builds whose lab config names a `pair_vm`
  run these cases.
- **Overlays only.** Both VMs run on throw-away qcow2 overlays; base images are
  only read. A run that fails or leaves no console log restarts its client VM
  on a fresh overlay.
- **Per run:** overlay the case's world on the base world in the server VM,
  start the lobby and gserver, launch the client, wait, take the case's mid
  action, screenshot, record the process list, close the client, collect its
  console log and file listing, pull the server log and trace, judge.
- **Output:** verdicts and captures under the lab host's work folder. With
  `--record` one line per run is appended to [`results.tsv`](results.tsv) and
  [`RESULTS.md`](RESULTS.md) is rewritten. Screenshots, logs, pcaps and client
  files never leave the lab host.

- **seihai-gserver-v2.** A case with `[server] kind = "v2"` runs on
  seihai-gserver-v2 instead. The lab config names a v2 server folder
  (`base_world_v2`: a copy of `bin/servers/default` with the lab accounts)
  and the `gs2emu` binary. `guest/case.sh v2up` copies the folder, merges the
  case's options into `config/serveroptions.txt` (the case's keys replace the
  folder's, and the port and lab address are set), puts the files in
  `world/3d/` and starts `gs2emu` in the folder. v2 cases take no terrain or
  scripts yet. Their results go into `results.tsv` under `server_label_v2`.

```
python3 tools/conformance/run.py --lab <lab.toml> --dry-run        # the plan
python3 tools/conformance/run.py --lab <lab.toml> --build 5.12 --case C001,C005 --record
python3 tools/conformance/conformance.py expected --write          # after editing a case
python3 -m pytest tools/conformance -q
```

The board's lab threads keep their own rows and harnesses; the suite runs on
its own VM overlays and work folder, so it can share a lab host with them. A
new board answer becomes a case (or a changed expectation) in a PR here; a
case that turns up something new becomes a board row.

## Cases so far

Single-client cases on the rows our server and renderer rely on: entry and
the UDP link (C001, C002), Sky (C003, C004), shapes and textures (C005, C006),
what is never fetched (C007), and the GS2 surface in 3D through probes
(C008 to C014), plus a server drop (C015). Second batch: the `.dts` and `.dif`
version bounds from a content pack (C016, C017), a flat streamed terrain
(C018) and water (C019), and the first two-client case (C020). Third batch,
from the T3D-142 to T3D-156 round: broken world lines (C021) and
out-of-range objects (C022, T3D-154/146), 256 and 1024 objects (C023, C024,
T3D-153/147), junk datagrams and connections on the 3D ports mid-session
(C025, T3D-144/142), a 10-second junk flood at the 3D port (C027, T3D-143) and a slice of the typed GS2 member table on a live
object (C026, T3D-150/125). Multi-session cases: a shape changed on the
server between two visits with the cache kept (C028, T3D-155), and five
visits in a row on one server run (C029, T3D-145). Ground cover (T3D-048,
needs seihai-gserver #214 or later): the origin-cell dead spot (C031), cover
around an avatar away from the replicator (C032), and an avatar outside the
cover box at radius 3 and 1 (C033, C034). Grass (T3D-048, needs
seihai-gserver #218): a radius-4 grass line still draws, since the server
sends grass at radius 8 or more (C035), while the same grass object sent
directly as a `rawobject` at radius 4 draws none (C036) and at radius 8 draws
(C037, the control that shows the raw encoding is right). The raw line comes
from `gen_content.grass_rawobject`, checked bit for bit against the server's
own replicator encoder. seihai-gserver-v2's 3D defences (`[server] kind =
"v2"`): junk on the 3D ports (C038, T3D-142/144), a flood cut by the
per-address budget (C039, T3D-143), five visits in a row (C040, T3D-145) and
a texture claiming 100000 x 100000 refused at start-up (C041, T3D-119).
Impossible positions (NaN or huge coordinates, T3D-146) need a client that
sends them and are not covered yet. C030 records the
defaults and value formats of the core GameObject and SceneObject members
(position, scale, transform, rotation, vectors, boxes, velocity, the
player's own object), which graal-client-repro needs to build its GS2 3D
objects. Their client-side answers are `?` until a lab
run records them. See [`EXPECTED.md`](EXPECTED.md).

Next: terrain extent ramps (T3D-148), malformed shapes from the graal-client-repro fuzz sets (T3D-038), the
camera and movetype (T3D-023, T3D-055), mixed-build pairs and a 2D client
beside a 3D one (T3D-071 to T3D-073), and a runner backend for the Windows
lab host's VMs.
