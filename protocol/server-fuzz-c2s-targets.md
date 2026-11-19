# Client→server fuzzing of the original servers — targets and status

Date: 2026-11-19

The 2026-11-19 packet-fuzz coverage audit found that **no original official server has
ever been client→server packet-fuzzed**: GServer13 (1999), the 1.21/1.25/1.27/1.28b2
GServers, the Linux `gserver13` and `GServer-NW`, and ListServer 2.37.2.59 (2003) are all
"run live, capture only" or untouched. The only C→S server fuzzing done so far is the empty
id sweep 0–223 against our own GServer-v2, plus 3 rows into gs2emu. This note tracks a
standalone harness for the gap and its run status.

Harness: [`../tools/srvfuzz/`](../tools/srvfuzz/) (`[lab]`, loopback only). Unlike the
proxy in `../tools/probe/`, it needs no real client and no captured key, because the
original servers are **cipher-free**:

- GServer13 / 1.2x: encryption generation 2 — `u16be len` + zlib, no cipher; login is
  `type` + `GSERVnnn` + account + password ([`gserv-1999.md`](gserv-1999.md)).
- ListServer 2.37 pre-2.2 link: plain `u16be len` + zlib, no cipher; login is id 0
  `newmain` then id 1 account+password ([`listserver.md`](listserver.md)).

So the harness speaks the wire directly and can fuzz the **frame** reader and the
**login/handshake** (pre-auth) as well as post-login packets — surface the proxy cannot
reach. It runs one case per fresh connection and, after each, checks a clean guest login
still answers (the **canary**); a case that drops the canary is the culprit.

## What the harness sends

Full taxonomy in [`../tools/srvfuzz/README.md`](../tools/srvfuzz/README.md). In brief:
malformed framing (bad `u16` length, non-zlib, truncated, max-`u16`, an 8 MiB-inflate
ratio DoS probe, empty-packet flood); malformed gen-2 login (bad/short/oversized token,
wrong type incl. type 1 = RC, length-prefix overruns, truncated, double login); the empty
id sweep 0–223; malformed bodies for the ids that parse one (`LEVELWARP`/`BOARDMODIFY`/
`PLAYERPROPS`/`NPCPROPS`/`WANTFILE` with **path traversal**/`OPENCHEST`/`LANGUAGE`, RC ops
as a player, in-frame floods); and the listserver equivalents. 292 gen-2 cases, 43
listserver cases as of this note.

## Validation

Self-tested on cloud loopback against mock gen-2 and listserver targets
(`../tools/srvfuzz/selftest.py`, 3/3): login+canary works, the whole case list runs
without throwing, the capped inflate survives the ratio case, and a planted crash is
detected by the canary. **No real binary has been run yet** — that is lab work.

## Run status (lab, opportunistic)

Real-binary runs go in a lab VM on the loopback address (lab ports 14804 game, 14921
list), per `AGENTS.md`; archived Windows binaries under Wine+Xvfb in the sandbox only
(`ListServer.exe` phones home). Only redacted derived results return to the repo.

- [ ] GServer13 (1.28b2 / 1.3 test, `GSERV013`/`GSERV014`) — gen2 sweep
- [ ] GServer 1.21 (`GSERV007`) — gen2 sweep (packs reply into one frame; watch framing)
- [ ] GServer 1.25 (`GSERV009`) — gen2 sweep
- [ ] GServer 1.27 (`GSERV011`) — gen2 sweep
- [ ] Linux `gserver13` — gen2 sweep
- [ ] `GServer-NW` — gen2 sweep (GNW token; confirm it is still cipher-free)
- [ ] ListServer 2.37.2.59 — listserver sweep (pre-2.2 link)

When a run lands, record it as a plain-behaviour `[lab]` note (server build + commit,
before/after, the `results.tsv`/`crash-*` names), redacted per `AGENTS.md`, and tick the
box above with a link. File server bugs as issues/PRs in the matching repo.
