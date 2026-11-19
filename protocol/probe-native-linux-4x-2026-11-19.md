# Packet probe: native Linux 4.x clients

Date: 2026-11-19

This extends the 2026-11-18 probe pilot ([`probe-targets-2026-11-18.md`](probe-targets-2026-11-18.md),
[`probe-results.tsv`](probe-results.tsv)) to the **native Linux 3.x/4.x clients**. Before today the
harness could drive only the native Linux 6.03r7 client and the Windows 2.22/2.31/4.20r8/5.24r4
clients under Wine. The new run script is [`../tools/probe/lab/run4x.sh`](../tools/probe/lab/run4x.sh).

All runs were in the `debian-lab446` lab VM, between a real client and our own gserver-v2, inside a
loopback-only bwrap network namespace. Lab only; nothing here reaches a public server. Raw captures
(proxy logs, screenshots, client trees) stay off the repo per the standing rule; only this write-up
and the derived rows in `probe-results.tsv` are committed.

## What the 4.x client needs that 6.03r7 did not

The 3.x/4.x native clients use the same Torque-based engine, gen-5 login, and GUI login form. Four
things had to be added to drive them (all documented in the header of `run4x.sh`):

1. **i386 runtime.** The `graal` binary is a 32-bit ELF (unlike the x86-64 6.03r7). Needs the i386
   SDL 1.2 / libGL / mesa-dri (llvmpipe) / libX11 / libstdc++ stack, used under Xvfb with
   `LIBGL_ALWAYS_SOFTWARE=1`.
2. **`license/` subdir.** The autopackage extraction flattens it, but the client hard-exits at
   startup unless `license/{sig.graal,sig.license,license.graal}` exist. `license.graal` is the
   server config: for 4.x it names the official login-server host on port 14900, which the LD_PRELOAD
   `hostshim` maps to loopback — so no port remap is needed.
3. **An "arial" X font.** The client loads `arial` (fallback `helvetica`) as an X **core** font via
   `XLoadQueryFont("-*-arial-medium-r-*-*-SIZE-*...")`. A bare Xvfb has no fonts, which disables
   **all** text including the HUD digits. Fixed by registering Liberation Sans under the arial and
   helvetica family names on the Xvfb font path.
4. **A 32-bit `hostshim`.** `tools/hostshim.c` built for i386; the shipped `.so` is 64-bit.

The GUI login form is driven with xdotool (account / password / nickname, then the Start button);
the 6.03r7 lab client auto-logs-in, the 3.x/4.x clients do not.

## Canary

The reused world template has none of the 4.x gameplay/HUD assets (state.png etc.), so the on-screen
bomb-count canary is unreadable. Instead a **clientside GS1 NPC** copies the player's own
bomb/gralat/arrow counts into chat each 0.3 s; the client reports its chat to the server, so the
canary is read screen-free from the proxy log's `C>S id=2` lines. This is the pilot's chatback
method and is more robust here. Example, confirming a 3-byte rupee prop is read at width and the bomb
canary stays in step:

| injected (S→C id 9) | client chat reported back (C→S id 2) |
|---|---|
| `c:5 c:11` | `b11 r7` |
| `c:5 c:99` | `b99 r7` |
| `c:3 i3:4321` | `b99 r4321` (bombs unchanged → stream in step) |

## Results

Six native Linux 4.x builds were run through the full core plan
([`../tools/probe/lab/wine-core.plan`](../tools/probe/lab/wine-core.plan), `waitsession`/`sleep` in
place of the `wait s2c` the Wine run used): **4.03r1, 4.04r2, 4.10r2, 4.11, 4.20r6, 4.20r8**
(tokens G3D11125, G3D19026, G3D28076, G3D28076, G3D22126, G3D22126). Every build produced a
**byte-identical** canary pattern (29 of 34 shots land, client alive throughout, nothing lost), and
that pattern **matches the already-recorded Windows 4.20r8 run** on every probe.

Own-prop widths (S→C id 9 `PLO_PLAYERPROPS`), canary = whether the trailing `c:5 c:99` bomb set still
lands:

| prop | 1-byte value | 2-byte (`s:`) | 3-byte (`i3:`) | 5-byte (`i5:`) | reading |
|---|:-:|:-:|:-:|:-:|---|
| 3 (rupees) | — | — | **lands** (→4321) | — | 3-byte, as documented |
| 77 | lands | — | — | **loses** | read as 1 byte (not the 6.x 5-byte form) |
| 78 / 79 / 80 | — | **land** | — | — | 2-byte |
| 81 | lands | — | — | — | 1-byte |
| 82 (`str:x`) | — | — | — | — | **loses** — not a string prop here |
| 83 (gralat) | lands | — | — | **loses** | read as 1 byte (the 5-byte gralat form is 6.x-only) |
| 90 | lands | — | **loses** | — | 1-byte |

Unknown server→client PLO ids **60, 78, 81, 83, 110** (empty / `c:1` / text / binary bodies): the
client stays alive and the same-frame bomb canary lands for every variant → all ignored, no crash,
no desync.

### Reading

- The native Linux 4.x line is **uniform**: the earliest (4.03r1) and latest (4.20r8) builds, and
  everything between, handle these props and unknown PLOs identically.
- It is also **OS-independent** at this layer: native Linux 4.20r8 equals Windows 4.20r8 exactly.
- **prop 83 differs from 6.03r7.** On 6.x prop 83 is the five-byte gralat counter (pilot result); on
  4.x it is read as a single byte (a 5-byte value desyncs the message), so the wide gralat form
  post-dates the 4.x line. prop 77 behaves the same way.
- 4.03r1 sits below the lab server's default `modern` version floor (4.04r2); its login decodes as
  gen-5 fine, it was only refused by server policy, so the `modern` range in the world template's
  `allowedversions.txt` was widened to admit `G3D11125` for that run.

## 3.04 Linux

3.04 (the static `graalexe`, SDL/fmod bundled) uses the same Torque engine and **gen-5** login, but
a **listserver** flow rather than the 4.x login-server+serverwarp: its `license.graal` names the
official list-server host on port 14922; the client queries the listserver for a server list, then
connects to the chosen game server. [`../tools/probe/lab/run3x.sh`](../tools/probe/lab/run3x.sh)
runs one gserver that registers with `seihai-listserver`; hostshim maps the official host to
loopback and `GRAAL_PORTMAP` maps the client's 14922 to the listserver's client port. The game
connection (login token `G3D03014`, gen 5) goes through gen5probe exactly as 4.x does. 3.04 ships
its own HUD assets, so the on-screen bomb-count canary works (classified by `tools/probe/canary.py`,
box `324 46 354 66`); the chatback NPC is not used (3.04's clientside GS1 does not reflect
`setplayerprop #c`).

3.04 matches 4.x on most probes, with **one difference**:

| probe | 3.04 | 4.x | note |
|---|:-:|:-:|---|
| prop 77 (1-byte / 5-byte) | 1-byte lands, 5-byte loses | same | read as 1 byte |
| **prop 78 / 79 / 80 (2-byte `s:`)** | **lose** | **land** | **defined (2-byte) on 4.x, unknown (1-byte skip) on 3.04** |
| prop 81 (1-byte) | lands | lands | |
| prop 82 (`str:`) | loses | loses | |
| prop 83 (1-byte / 5-byte) | 1-byte lands, 5-byte loses | same | 1 byte (5-byte gralat is 6.x-only) |
| prop 90 (1-byte / 3-byte) | 1-byte lands, 3-byte loses | same | 1 byte |
| prop 3 (3-byte rupees) | lands | lands | |
| unknown PLO 60/78/81/83/110 | ignored, alive | ignored, alive | no crash/desync |

So **props 78–80 were added in the 4.x line**: on 3.04 they are unknown ids (skipped as one byte, so
a 2-byte value desyncs the message), whereas 4.x reads them as 2-byte props. Everything else is
identical to 4.x.

## Not yet covered (follow-ons)

- **3.0b / 3.01 / 3.151 Linux** (same engine/flow as 3.04; `run3x.sh` should take them directly).
- **6.015 Mac** in the Lion VM, and the **PPC Mac** 3.153/4.x/5.12 builds (need a Tiger/PPC
  environment, not the Intel Lion VM).
