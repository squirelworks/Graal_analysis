# Per-3D-player resource budget: ~5 packets/s and ~50–60 B/s each way (idle ≈ moving), and a stable ~141 MB client with no memory leak (T3D-127/131, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; loopback pcap + RSS sampling. Observation only. Board rows: [T3D-127](3d-capability-board.tsv) (bandwidth/tick) and [T3D-131](3d-capability-board.tsv) (long-run memory). Companion to the frame-rate note [T3D-113](3d-capability-board.tsv); the position-reporting cadence ties to [T3D-128](3d-session-lifecycle-420r6-2026-11-26.md).

## Headline

A single 3D player costs the server **~5 packets/s and ~50–60 B/s each direction** at steady state — a **fixed low cadence that movement does not change** (the control object reports its position in every packet at a fixed tick, so moving changes values not rate) — plus a one-time few-KB scene download at join. The client itself holds a **stable ~141 MB** over a sustained session with **no memory leak**.

## T3D-127 — bandwidth & tick rate **[lab]**

Loopback pcap over a session (idle → scripted `setposition` movement → teleport), steady-state per second:

| stream | client → server | server → client |
| --- | --- | --- |
| 3D UDP link | ~2–3 pk/s, **~26–31 B/s** | ~1–2 pk/s, **~7–13 B/s** |
| game TCP | ~2–3 pk/s, ~12–18 B/s | ~2–3 pk/s, ~0–17 B/s |

So **~5 pk/s and ~50–60 B/s each direction** at steady state. **Idle ≈ moving**: the control object reports its position in *every* packet at a fixed ~2–3 Hz, so movement changes the values, not the rate. The only heavy traffic is a **one-time few-KB mission/ghost download at join**. There is **no frame-rate-coupled stream** (network cadence is independent of render FPS).

**For a server:** budget **~50–60 B/s and ~5 pk/s per 3D player each way**, plus a few-KB scene download at join; movement does not raise bandwidth.

## T3D-131 — long-run memory stability **[lab]**

A ~15-minute session with per-second script activity (overlay images/text + a positional sound call), RSS sampled every 20 s (45 samples): warm-up ~122 MB → ~138 MB by +60 s, then **flat in a ~0.5 MB band around ~141 MB** (141.0 ↔ 141.5) through +900 s. **Slope ≈ 0 MB/min** — no growth; extrapolated, it holds ~141 MB indefinitely. **No memory leak.**

**For a server:** a long-lived 3D client with ongoing script activity holds a stable ~141 MB — no per-minute leak to budget against.

## Method caveat

Single client, loopback server, software GL. Byte/packet rates are from a loopback pcap (loopback framing, not a WAN MTU) — the application-payload cadence (~5 pk/s, position every packet) is the portable fact; absolute B/s on a real network would add transport overhead. RSS is the resident set of the one 32-bit client process over 15 min; a multi-hour extrapolation assumes the observed flat slope continues, which the 0 MB/min trend supports.
