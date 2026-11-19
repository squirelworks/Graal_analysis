# Packet probe harness

Date: 2026-11-18

A lab tool for sending chosen packets to a real Graal client (or to our own gserver)
in the middle of a live session, and recording what the client does. It answers the
questions static reading leaves open: what an unnamed prop sets, which value range a
client accepts, whether a stream stays in step after an odd value, and whether an
unknown packet id is ignored, crashes the client, or gets a reply.

**Lab only.** It runs between a real client and our own lab gserver, inside a
private network namespace with loopback only. It is never pointed at a public
GraalOnline server, and nothing here helps reach one.

## Parts

| File | Role |
|---|---|
| `gen5probe.py` | Proxy for encryption generations 2–5 (picked from the login line). Decrypts and logs both directions, re-encrypts with its own cipher state, and takes commands on a unix socket: `s2c SPEC`, `c2s SPEC`, `after s2c ID SPEC`, `drop s2c ID`, `seen s2c ID`, `mark TEXT`, `status`. |
| `probectl.py` | Sends one command, or runs a plan file step by step (`waitsession`, `wait s2c ID`, `sleep`, `shot NAME`, `sh CMD`, and any proxy command). Every step is also written to the proxy log as a `MARK`, so one log holds the whole timeline. |
| `selftest.py` | A fake gen-5 client and server around the proxy. It checks relaying, injection both ways, `after`, `drop`, and that the cipher stays in step afterwards. Run `python3 selftest.py` (Linux). |
| `lab/run603.sh` | One run of the native Linux 6.03r7 client: login gserver that serverwarps to a world gserver behind `gen5probe.py`, own Xvfb, no window manager, everything in `bwrap --unshare-net --unshare-pid`. Screenshots go through the plan's `shot` steps. |
| `lab/runwine.sh` | One run of a Windows client under Wine in the same VM: 2.05 rev 2 and 2.17.1 (gen 3), 2.22, 2.31 (gen 5, login form and server list), 4.20r8 (clock held at 2007-07-01, login form) or 5.24r4. It reuses the gs1 lab tree (Wine prefix, clients, worlds and its own network namespace). |
| `lab/*.plan` | Probe plans. `prop83.plan` is the pilot. `wine-core.plan` runs the same core probes on every client. `widths.plan` checks each self prop 0–90 at its documented width. `pli-sweep*.plan` sends every client→server id to our gserver. `bytes2x.plan` tests raw bytes inside a message. `readback83.plan` reads prop 83 back through a level script. |
| `lab/keysweep.sh`, `lab/keysweep.py`, `lab/keysweep.keys` | The key and mouse sweep (see below): presses every key of the list on one client, one at a time, and records windows, screen change, packets and what a key-logging script saw. `keysweep_tsv.py` turns the raw rows into the derived table. |
| `lab/keylog-gs1.npc`, `lab/keylog.gs2`, `lab/keylog-gs2.bc.hex`, `lab/keylog-stub.npc` | The sweep's key loggers: a GS1 level NPC for 2.x, and for 4.x–6.x a GS2 `onKeyPressed` script compiled to bytecode by Seihai's own compiler, delivered over a stub NPC through the proxy. |
| `canary.py` | Classifies each shot's bomb count against two reference shots (canary lost: count 1; canary landed: count 99). Pass the bomb-count box for the client's HUD. |
| `xwd2png.py` | Converts the `xwd` screenshots. |

## Packet spec

A spec is the packet id followed by typed fields. The newline is added.

| Field | Bytes |
|---|---|
| `c:N` | GCHAR, N + 32 |
| `s:N` | GSHORT, two 7-bit groups + 32 |
| `i3:N`, `i4:N`, `i5:N` | three, four or five 7-bit groups + 32 |
| `b:N` | one raw byte, for out-of-range bytes |
| `t:TEXT` | raw text (quote it if it has spaces) |
| `str:TEXT` | GCHAR length + text |
| `hex:HEX` | raw bytes |

`9 c:83 i5:1234 c:5 c:11` is a `PLO_PLAYERPROPS` with prop 83 = 1234 followed by
prop 5 (bombs) = 11. Putting a prop with a visible effect after the one under test
(a "canary") shows whether the client read the test prop at the width we gave it:
if the canary lands, the stream stayed in step.

## How a probe is observed

| Evidence | Source |
|---|---|
| What was sent, when | `proxy.log` `INJECT` and `MARK` lines (monotonic seconds) |
| Client replies | `proxy.log` `C>S` lines after the inject |
| Screen state | `shot` steps (HUD, chat, level) |
| Client alive | each `shot` records whether the window still exists |
| Client log | `game_console.log`, `client.log` |
| Server side | the gserver console logs |

The results table is `../../protocol/probe-results.tsv`; the target list is
`../../protocol/probe-targets-2026-11-18.md`.

## Running the pilot

In the Debian lab VM, with the lab tree as `~/probelab/tools`:

```sh
sh tools/run603.sh tools/prop83.plan p83-b      # output in ~/probelab/out/p83-b
```

`DISP=NN` picks another Xvfb display; the script refuses a display that is in use.
The client, gserver build, world template, tile sheet and DNS responder are named in
`~/probelab/lab.env` on the lab VM (see the header of `run603.sh`); they are lab copies and
are not in this repo. The tile sheet is copied into both servers and the client cache.

## Two clients, and Windows hosts

`CLIENTS=2 sh run603.sh ...` starts a second real 6.03r7 client in the same namespace, and shots
then cover the whole screen. The probe acts on the client that logged in last. `PROBE_FULLHEX=8,9`
logs those ids' whole bodies. On a Windows host, where Python has no unix sockets, give the
proxy and `probectl.py` the control address `tcp:PORT`.

## The black-screen retry (6.03r7)

On some runs the 6.03r7 client never draws the tile layer, and the screen stays black. HUD
digits then draw over each other, which breaks the canary. `run603.sh` waits until the
session is up, checks a shot of the game area, and starts the whole run again if it is black
(up to four tries, recorded in `tries.txt`). `NOBLACK=0` turns this off.

## Key and mouse sweep

`lab/keysweep.sh CLIENT SWEEP` runs every entry of `lab/keysweep.keys` (F1–F12, Escape, the number
row, every letter and punctuation key, Return, Space, the modifiers alone, the edit block, arrows,
keypad, lock keys, Ctrl+letters, Alt+digits, Alt+Return, Shift/Ctrl+arrows, mouse buttons and double
clicks on the player, the ground, an NPC and the HUD, the wheel, and Alt+F4 last) on one client. For
each one `keysweep.py` records the visible windows and a root screen grab, marks the proxy log, sends
the key to the game window with `xdotool`, waits 1.5 s, and records windows, screen difference
(changed pixels and bounding box), whether the client is alive and still in its session, and the
client→server packets between the marks. It then resets: new windows get Escape, then `n`; pause,
item-list, map, chat and lock keys are pressed again; arrows are undone with the opposite arrow. When
the client died, lost its session or kept a window open, the next run logs in again and goes on from
the next key (a key that fails three runs in a row is skipped).

`KEYLOG=1` adds a key logger that copies each key event and the `keydown(0..10)` bits into the
player's chat, so they arrive in the proxy log as chat props. 2.x clients take the GS1 text NPC
`keylog-gs1.npc` (`keypressed`, `#p(0..2)`). 4.x–6.x clients take bytecode, and the lab gserver's
GS1 lowering has no `keypressed`, so `keylog-stub.npc` goes in the level and `keysweep.py
--bytecode` replaces its script through the proxy (PLO_RAWDATA + PLO_NPCBYTECODE) with
`keylog-gs2.bc.hex`, which is `keylog.gs2` compiled by seihai-core's GS2 compiler. Run each client
once with and once without the logger (`KEYLOG=0`); `keysweep_tsv.py ROWS --clean ROWS2` takes the
screen and window effects from the clean run, so the logger's chat bubble does not count as an effect.

Lab inputs: `PROBE_ROOT` names the lab folder (default `$HOME/probelab`), so a sweep can run in its own
folder next to other probe runs; `DISP` picks the display. For the Wine clients `WINELAB` must be a
private copy of the Wine lab tree (marked with a `.keysweep-ok` file), because the sweep rewrites its
start levels before each run. Raw rows, logs and screen grabs stay in `$PROBE_ROOT/out/keysweep-*`;
only the derived tables go in the repo (`protocol/keysweep/`).

## Limits

- Generations 2, 3 and 5 are tested (gen 3 on real 2.05 and 2.17.1, gen 5 on 2.22 and later). Gen 4 (2.19–2.21) follows the server source and is untested. 6.1.1.3's RC4 stream is not covered.
  6.1.1.3 needs a loopback connector harness first (`../../protocol/v6113-status.md`).
- Injected packets go out as their own frame, at a packet boundary, so they never split
  a server packet. A server `PLO_RAWDATA` body that spans frames delays the inject until it ends.
- `drop` removes whole packets only.
