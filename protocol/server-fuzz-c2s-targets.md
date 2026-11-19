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
- [ ] GServer 1.3 test (`GSERV014`) — gen2 sweep
- [ ] GServer 1.21 (`GSERV007`) — gen2 sweep (packs reply into one frame; watch framing)
- [ ] GServer 1.25 (`GSERV009`) — gen2 sweep
- [ ] GServer 1.27 (`GSERV011`) — gen2 sweep
- [ ] Linux `gserver13` — gen2 sweep
- [ ] `GServer-NW` — gen2 sweep (GNW token; confirm it is still cipher-free)
- [ ] ListServer 2.37.2.59 — listserver sweep (pre-2.2 link)

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
- **Unauthenticated id 8 (unconfirmed):** pre-auth frame and malformed-login cases saw an
  S→C id 8 (`OTHERPLPROPS`) on a socket that had not logged in. This may just be the prior
  canary guest's leave props being broadcast to the freshly-accepted socket; the cause is
  not confirmed.
- **Server state persisted across cases:** from the id-40 case onward every canary login
  also received id 33 (`NPCWEAPONADD`) — a fuzz case granted the shared `guest` account a
  weapon that stuck server-side. So the post-login (idsweep/body) results reflect
  cumulative state on one account, not clean per-case state.

Follow-ups:

- [ ] Confirm or explain the unauthenticated id 8 — re-run on a single connection with no
  concurrent canary so a broadcast can't be the cause.
- [ ] Re-run the post-login cases with a per-case `guest` account reset, to separate each
  case's effect from cumulative state.
- [ ] Narrow which case grants `NPCWEAPONADD` (id 33 first appears from the id-40 case).
- [ ] The half-open double-login socket: does it leak a slot / persist?
