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
detected by the canary. The 2026-11-19 GServer 1.28b2 run (below) corrected one harness
fact: the gen-2 login line must end in `\n`, or a real 1.x GServer reads the bytes and
never replies; the mock now only acts on newline-terminated lines so the self-test guards it.

## Run status (lab, opportunistic)

Real-binary runs go in a lab VM on the loopback address (lab ports 14804 game, 14921
list), per `AGENTS.md`; archived Windows binaries under Wine+Xvfb in the sandbox only
(`ListServer.exe` phones home). Only redacted derived results return to the repo.

- [x] **GServer 1.28 beta 2 (`GSERV013`) — gen2 sweep. 2026-11-19, no crashes.** See below.
- [x] **GServer 1.3 test (`GSERV014`) — gen2 sweep. 2026-11-20, 292 cases, no crash.** Folded into [`gserv-1999.md`](gserv-1999.md#clientserver-packet-fuzz-lab).
- [ ] GServer 1.21 (`GSERV007`) — gen2 sweep (packs reply into one frame; watch framing). First run invalid (host load caused false canary timeouts); redo pending a quiet host.
- [x] **GServer 1.25 (`GSERV009`) — gen2 sweep. 2026-11-20, 292 cases, no crash.** Folded into [`gserv-1999.md`](gserv-1999.md#clientserver-packet-fuzz-lab).
- [x] **GServer 1.27 (`GSERV011`) — gen2 sweep. 2026-11-20, 292 cases, no crash.** Folded into [`gserv-1999.md`](gserv-1999.md#clientserver-packet-fuzz-lab).
- [ ] Linux `gserver13` — gen2 sweep
- [ ] `GServer-NW` — gen2 sweep (GNW token; confirm it is still cipher-free)
- [~] ListServer 2.37.2.59 — **not fuzzable with the held binary**: `ListServer.exe` is the owner registration GUI (phones home to a hardcoded external tracker URL, binds no listening socket), so `list` mode has no target. Recorded in [`listserver.md`](listserver.md#clientserver-fuzz-of-the-pre-22-link-lab). The real pre-2.2 query daemon is not held as a runnable loopback binary.
- [x] **seihai-listserver 0.1.1 (our clean-room Rust list daemon) — `list` sweep. 2026-11-20, cloud loopback, 43 cases, no crash.** Covers the pre-2.2 link gap. Folded into [`listserver.md`](listserver.md#clientserver-fuzz-of-the-pre-22-link-lab).

When a run lands, record it as a plain-behaviour `[lab]` note (server build + commit,
before/after, the `results.tsv`/`crash-*` names), redacted per `AGENTS.md`, and tick the
box above with a link. File server bugs as issues/PRs in the matching repo.

## GServer 1.28 beta 2 — gen2 sweep (2026-11-19) **[lab]**

Target: the original **GServer 1.28 beta 2** (`GServerv.exe`, token `GSERV013`), the same
binary as the earlier 1.28 control lab. Run under Wine in the Debian lab VM, in a private
network namespace on the loopback address, port 14804, with a private copy of the server
folder and a `guest`/`guest` account for the canary. Lowest priority (`nice 19`) on a busy
VM; nobody else's work touched. Harness: `srvfuzz gen2`, 292 cases (frame 12, login 22,
idsweep 224, body 34), `--relaunch` armed. Owner-held capture: `results.tsv` + `srvfuzz.log`.

**No crash, no hang, no canary drop in any of the 292 cases.** `--relaunch` never fired;
no `crash-*` dumps. The server kept accepting clean logins throughout. The slowest canary
was 959 ms (right after the `frame/all-empty-packets` frame); every other case canary came
back under 460 ms, so the `inflate-ratio-8mb` and 500-packet flood cases caused no
slowdown — 1.28b2 does not inflate unboundedly or choke on a packed frame. This is the
first original official server to be client→server packet-fuzzed.

Behaviours seen (canary up throughout; all **[lab]**, 1.28b2 only):

- **Login refusals are clean.** Bad token, empty account/password, and 250-byte account or
  password each get id 16 (`DISCMESSAGE`) then a close — the documented refusal path.
- **No file-path traversal.** `WANTFILE` (id 23) with `../`, `..\`, an absolute path, an
  empty name, and a 250-byte name each returned id 30 (`FILESENDFAILED`); no file contents
  came back. The empty-body id-23 in the sweep also got id 30.
- **id sweep:** ids 40 and 222 drew a `9,33,14` burst; every other id (bar 23) drew no
  reply. Empty id 17 (`BADDYADD`) did **not** crash the server — note it crashes the
  6.03r7 *client*, which is the opposite direction.
- **Odd login types:** type 1 (RC) and a non-login first packet closed the socket with no
  reply; types 2, 5, 64 and 127 were left open with no reply.
- **Half-open on double login:** two valid login lines in one frame left the connection
  neither logged in nor disconnected — a half-open socket. Worth a closer look.
- **Unauthenticated id 8 — canary artifact (confirmed 2026-11-24):** pre-auth frame and
  malformed-login cases in the canary harness saw an S→C id 8 (`OTHERPLPROPS`) on sockets
  that had not logged in. A solo re-run on the same 1.28b2 build with **no canary and no
  other guest** (one fresh socket per case, idle-accept first) produced **zero** id 8 across
  idle-accept plus all 34 frame/login cases. The same build with the normal canary harness
  reproduced id 8 on **every** frame case, always body `0x21 0x53` (player index 1 + one
  prop byte). So the unauthenticated id 8 is leave/other props from the harness guest, not
  a reply to the malformed pre-auth input.
- **Server state persisted across cases:** from the id-40 case onward every canary login
  also received id 33 (`NPCWEAPONADD`) — a fuzz case granted the shared `guest` account a
  weapon that stuck server-side. So the post-login (idsweep/body) results reflect
  cumulative state on one account, not clean per-case state.

Follow-ups:

- [x] Confirm or explain the unauthenticated id 8 — re-run on a single connection with no
  concurrent canary so a broadcast can't be the cause. **Done 2026-11-24:** solo (no canary)
  → no id 8; canary harness → id 8 on every frame case (body `0x21 0x53`). Canary artifact.
- [ ] Re-run the post-login cases with a per-case `guest` account reset, to separate each
  case's effect from cumulative state.
- [ ] Narrow which case grants `NPCWEAPONADD` (id 33 first appears from the id-40 case).
- [ ] The half-open double-login socket: does it leak a slot / persist?

## GServer 1.3 test, 1.25, 1.27 — gen2 sweeps (2026-11-20) **[lab]**

Three more original GServers (`GServerv.exe`, tokens `GSERV014`/`GSERV009`/`GSERV011`), each
under Wine in the lab VM on a loopback lab port with a private server folder and a
`guest`/`guest` canary account. Harness `srvfuzz gen2`, 292 cases, `--relaunch` armed.
**No crash, hang or canary drop on any build.** The per-build login contracts and the
pre-auth findings are folded into [`gserv-1999.md`](gserv-1999.md#clientserver-packet-fuzz-lab);
in brief:

- Version-gate refusal text confirmed live and per-build (1.25 "1.2 rev1", 1.27 "1.27",
  1.3 "1.3"); empty/oversized creds → id 16 "doesn't exist", close.
- **Double login differs by build:** 1.25/1.27/1.3 honour the second login; 1.28b2 half-opens.
- No `WANTFILE` traversal on any build (id 30 FILESENDFAILED, no bytes).
- The 1.2x servers stream the whole start level on login (9,14,100,board,6,1,[5],10); the
  harness drain-to-idle fix (commit in this session) keeps that stream out of post-login
  reply capture. Post-login, id 23 → id 30 is the only reliable dedicated reply.

One harness correction came out of these runs: the gen-2 login line must end in `\n` or a
real 1.x GServer reads the bytes and never replies; fixed, and the self-test mock now guards
it. A loaded VM also produced false canary timeouts (the deferred 1.21 run), so these were
run on a quiet host and re-checked.

### GServer13: second, independent run (2026-11-20) **[lab]**

A second gen-2 sweep of GServer13 from the early-client probe campaign
([`early-clients-probe-2026-11-19.md`](early-clients-probe-2026-11-19.md)), in its own network
namespace and Wine prefix, the same 292 cases: again no crash, hang or canary drop, and the same
login and `WANTFILE` behaviour as above. It adds three details:

- **Warp to a level the server does not have** (`PLI_LEVELWARP` 0 or `LEVELWARPMOD` with a
  250-byte or `../` name) gets `PLO_WARPFAILED` (15), a warp (14) back, the board as
  `PLO_LEVELBOARD` (0) rather than the 100/101 raw-data pair, and `PLO_ISLEADER` (10). A name
  with a NUL gets no reply.
- **Two frames in one TCP send close the socket**, and so does a single 65535-byte frame; every
  other malformed frame (zero length, over- and under-runs, non-zlib or truncated zlib, an 8 MB
  inflate ratio, a giant line with no newline, a frame of empty packets) is ignored with the
  socket left open.
- The pre-auth id 8 appeared on every fresh socket here too.

## seihai-listserver 0.1.1 — `list` sweep (2026-11-20) **[lab]**

Our own clean-room Rust list daemon (`squirelworks/seihai-listserver`, v0.1.1), fuzzed on
cloud loopback instead of a lab VM (own code, cipher-free pre-2.2 link, avoids lab disk
pressure). Started with `login_fail_limit = 0` so the built-in login-failure rate cap
(default 30/60s/addr) does not false-flag the canary; log confirmed "login failures: no cap"
and a single verified instance answered. Harness `srvfuzz list`, 43 cases.

**No panic, crash or hang; canary up on all 43.** Unknown/out-of-range ids are logged and
ignored (no reply, no close); malformed frames draw no reply and leave the socket open; the
capped inflate-ratio probe caused no slowdown. Two behaviours differ from the 1.x gen-2
gserver: no newline is required to terminate a login line, and two logins in one frame are
both processed. No server bug to file. Detail in
[`listserver.md`](listserver.md#clientserver-fuzz-of-the-pre-22-link-lab).
