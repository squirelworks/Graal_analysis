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
| `gen5probe.py` | Gen-5 proxy. Decrypts and logs both directions, re-encrypts with its own cipher state, and takes commands on a unix socket: `s2c SPEC`, `c2s SPEC`, `after s2c ID SPEC`, `drop s2c ID`, `seen s2c ID`, `mark TEXT`, `status`. |
| `probectl.py` | Sends one command, or runs a plan file step by step (`waitsession`, `wait s2c ID`, `sleep`, `shot NAME`, `sh CMD`, and any proxy command). Every step is also written to the proxy log as a `MARK`, so one log holds the whole timeline. |
| `selftest.py` | A fake gen-5 client and server around the proxy. It checks relaying, injection both ways, `after`, `drop`, and that the cipher stays in step afterwards. Run `python3 selftest.py` (Linux). |
| `lab/run603.sh` | One run of the native Linux 6.03r7 client: login gserver that serverwarps to a world gserver behind `gen5probe.py`, own Xvfb, no window manager, everything in `bwrap --unshare-net --unshare-pid`. Screenshots go through the plan's `shot` steps. |
| `lab/*.plan` | Probe plans. `prop83.plan` is the pilot. |
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
The client, gserver build and world come from the existing lab copies in the VM
(`/opt/graal-lab/work`, `~/seihai-lab/world`, `~/issho-lab/world`); a tile sheet is
copied in so the screen repaints between shots.

## Limits

- Gen-5 only (2.x clients with the gen-2/3 codecs and 6.1.1.3's RC4 stream are not covered).
  6.1.1.3 needs a loopback connector harness first (`../../protocol/v6113-status.md`).
- Injected packets go out as their own frame, at a packet boundary, so they never split
  a server packet. A server `PLO_RAWDATA` body that spans frames delays the inject until it ends.
- `drop` removes whole packets only.
