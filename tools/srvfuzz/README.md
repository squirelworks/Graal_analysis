# C→S server fuzzer (`srvfuzz`)

Date: 2026-11-19

A lab-only client→server packet fuzzer for the **original** Graal servers, the ones the
packet probe (`../probe/`) cannot drive: GServer13 and the 1.2x GServers (1999–2000) and
ListServer 2.37.2.59 (2003). None of these had been packet-fuzzed before (see
`../../protocol/server-fuzz-c2s-targets.md` and the 2026-11-19 coverage audit).

**Lab only.** Point it at a server **you** started on the loopback address, inside a
container or a lab VM. It is never pointed at a public server, and nothing here helps
reach one. Follow `../../AGENTS.md`: loopback address or the lab ports (14804, 14900,
14921–14923) only, no real hosts or IPs in any note or log.

## Why a standalone client, not the proxy

`../probe/gen5probe.py` is a *proxy*: it needs a live real client to drive it, and its
codec reads a key byte after the login type, so it assumes a GNW / gen-3-or-later login.
The first central servers predate all of that and are **cipher-free**:

| Target | Codec | Framing | Login |
|---|---|---|---|
| GServer13, 1.2x GServers | gen 2, no cipher | `u16be len` + zlib | `type` + `GSERVnnn` + account + password |
| ListServer 2.37 (pre-2.2 link) | no cipher | `u16be len` + zlib | id 0 `newmain`, then id 1 account+password |

Because there is no cipher and no captured key, a standalone client can speak either
target directly — no real game client needed. Speaking the wire directly also reaches
the surface a proxy cannot: malformed **frames** and malformed **login** bytes, i.e. the
pre-authentication attack surface, which is the most interesting part of an old server.

Protocol sources: `../../protocol/gserv-1999.md`, `../../protocol/listserver.md`,
`../../protocol/codec-and-framing.md`, `../../protocol/OPCODE-SUMMARY.md`.

## Parts

| File | Role |
|---|---|
| `srvfuzz.py` | The driver. Opens a fresh connection per case, (optionally) logs in, sends the case bytes, reads the reply, then runs a **canary** on a *new* connection — a clean guest login that must still answer. A case that drops the canary is the culprit. Writes `results.tsv` and `srvfuzz.log`; dumps `crash-<n>-<cat>.txt` on a canary drop. |
| `cases.py` | Fuzz-case generators (below). `python3 cases.py gen2` / `list` prints the plan without sending anything. Reuses the probe's packet spec language (`c:` `s:` `i3:` `b:` `t:` `str:` `hex:`). |
| `mockgen2.py` | A faithful-enough gen-2 gserver for self-testing on loopback (framing + login + an id-9/id-6 reply). Not GServer13. |
| `mocklist.py` | A pre-2.2 listserver stand-in for self-testing. |
| `selftest.py` | Drives `srvfuzz` against both mocks: login+canary works, the whole case list runs without throwing, and a planted crash is detected. `python3 selftest.py` or `python3 -m pytest tools/srvfuzz`. |
| `lab/run-srvfuzz.sh` | Lab-VM template: start the target on a loopback lab port, run a sweep, collect output, relaunch-on-crash. |

## Case categories

`srvfuzz --only CAT` runs one category.

| Category | Mode | What it sends |
|---|---|---|
| `frame` | gen2 | Malformed `u16`/zlib framing on a fresh pre-auth socket: zero length, length over/under-run, non-zlib body, header-only, truncated stream, max-`u16` valid frame, an 8 MiB-inflate ratio case (bounded; tests an uncapped-inflate DoS), a giant no-newline line, a frame of thousands of empty packets, two frames in one send. |
| `login` | gen2 | Malformed gen-2 login: bad/empty/oversized/short token, wrong type bytes (1 = RC path, and undefined ones), account/password length-prefix overruns, empty and 250-byte fields, NUL/high bytes, type-only and truncated lines, a double login, and a non-login first packet. |
| `idsweep` | gen2 | Every client→server id 0..223 with an empty body, after a clean login. |
| `body` | gen2 | Well-known ids with malformed bodies: `LEVELWARP`/`LEVELWARPMOD` name overruns and traversal, `BOARDMODIFY` out-of-range geometry, `PLAYERPROPS` out-of-range prop ids / width truncation / GSTRING overrun / 250-byte nick / 400-byte prop run, `NPCPROPS` truncated id, **`WANTFILE` path traversal** (`../`, Windows `..\`, absolute, NUL-embedded, 250-byte), `OPENCHEST`/`LANGUAGE` edges, RC ops 51–87 as a player, embedded newlines/CR, and a 500-packet in-frame flood. |
| `listlogin` | list | Pre-2.2 listserver: valid id0/id1 variants, oversized/empty version, SERVERLIST account overruns, unknown and out-of-range ids, a gen-5 `V2ENCRYPTKEYCL` sent to a pre-2.2 server, `GRSECURELOGIN` blob, an empty-id sweep, and all the frame-level cases. |

## Running it

Self-test (cloud, loopback, no real binary):

```sh
python3 tools/srvfuzz/selftest.py
# or, fast:
SRVFUZZ_RECV_TIMEOUT=0.3 SRVFUZZ_CANARY_TIMEOUT=0.6 python3 tools/srvfuzz/selftest.py
```

Against a real server in a lab VM (loopback only), e.g. GServer13 on lab port 14804.
Build the loopback address rather than writing it (the repo bars dotted-IP literals):

```sh
LB=$(printf '%d.%d.%d.%d' 127 0 0 1)
# 1.2x / 1.3 GServers accept GSERV007..GSERV014; match the --token to the build
python3 tools/srvfuzz/srvfuzz.py gen2 "$LB" 14804 --token GSERV014 --out out/gserver13
python3 tools/srvfuzz/srvfuzz.py list "$LB" 14921 --out out/listserver237
```

Because a crash kills the whole server, pass `--stop-on-crash` to halt at the culprit, or
`--relaunch 'CMD'` to have the driver restart the target and resume at the next case. Use
`--resume N` to continue a stopped run, and `--only CAT` to focus one category.

## Reading the results

`results.tsv` columns: `n category name sent_len reply closed decode_err canary canary_note rtt_ms`.
The interesting rows are `canary == down` (the server stopped answering a clean login
after that case) and sudden `rtt_ms` growth (the server slowed — watch the inflate-ratio
and flood cases). `reply` shows the packet ids the server sent back to the case itself; an
unexpected reply to a malformed packet is worth a look even when the canary stays up.

**The goal is protocol learning, not only crash hunting.** `replies.tsv` is the capture for
that: one row per S→C packet the server sent back to each probe —
`n category name reply_id reply_len body_hex` (body capped at 128 bytes). It answers which
C→S ids the server acts on, what it replies with, and how it rejects bad input (e.g. id 16
`DISCMESSAGE` on a bad login, id 30 `FILESENDFAILED` on a refused file). `srvfuzz.log` keeps
the same timeline in prose. Fold the confirmed per-id behaviour into the protocol notes
(`../../protocol/gserv-1999.md` for gen-2, `listserver.md` for the list link).

Turn confirmed findings into a plain-behaviour note under `../../protocol/` with a `[lab]`
tag and the server build + commit, per `AGENTS.md` — never a host, IP, or binary address.
File server bugs as issues/PRs in the matching repo.

## Limits

- Cipher-free targets only (gen 2 and the pre-2.2 list link). The gen-5 servers
  (GServer-v2, seihai-gserver) are reached through the proxy's `c2s` instead; their empty
  id sweep is already done against GServer-v2.
- The canary is a *liveness* check (does a clean login still answer), so it catches
  crashes, hangs and the server dropping new logins. It does not by itself catch silent
  state corruption that still lets logins through; for that, read the `reply` column and
  the server's own console log.
- One case per fresh connection, so cases do not poison each other — but a case that
  corrupts shared server state (not the connection) can still affect later cases until the
  server is relaunched. Use `--relaunch` for a clean run when that matters.
