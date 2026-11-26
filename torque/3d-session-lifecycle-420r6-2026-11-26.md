# The 5.12-class 3D session lifecycle: gen-5 account login → a `3 `-prefixed 178 warp → a dual TCP+UDP link; position is client-authoritative; a drop is a 30 s timeout with no resume (T3D-130/128/129, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; loopback gserver, link trace + GS2 probes. Observation only. Board rows: [T3D-130](3d-capability-board.tsv) (login path), [T3D-128](3d-capability-board.tsv) (position trust), [T3D-129](3d-capability-board.tsv) (reconnect/persistence). Extends [T3D-111](3d-capability-board.tsv) (position relay), [T3D-059](3d-capability-board.tsv) (entry), [T3D-108](3d-capability-board.tsv)/[T3D-027](3d-capability-board.tsv) (link teardown); dual-link shape per [live-512-third-party-session](live-512-third-party-session-2026-11-24.md).

## Headline

A 3D session is reached by an **ordinary gen-5 account login**, then a **`3 `-prefixed list entry via a `PLO_SERVERWARP` (178)**, then a **dual TCP+UDP link**. Once in, the server treats the control-object position as **client-authoritative** (no validation — teleports accepted), and a dropped link is a plain **30 s timeout with no resume**: a rejoin is a fresh session rebuilt from the world.

## T3D-130 — login path into 3D **[lab]**

1. The client connects to the **login server** and sends its **account login** — the gen-5 mode-3 frame (zlib, key byte, account/password).
2. The login/list server answers with a **`PLO_SERVERWARP` (178)** to a list entry **whose name starts with `3 `** (the 3D marker, e.g. `3 Lab 3D`), carrying host:port.
3. The client opens the 3D session on the listed port: a **TCP login** plus a **UDP 3D link** (the dual-link entry). The **UDP link is not re-authenticated** — it is opened only for an account already logged in over TCP.

**For a server:** 3D entry = an ordinary account login + server list, a `3 `-prefixed entry reached by a 178 warp, then a TCP login + a UDP link on the listed port; authenticate on the **TCP** side (the UDP link rides the authenticated TCP session).

## T3D-128 — position trust: client-authoritative, no anti-cheat **[lab]**

The gserver stores the control object **as its updates describe it**; the client reports its position in **every** packet, and there is **no speed/delta/teleport check**. A scripted teleport (an impossible delta) was **not rejected** — the server kept the self-reported position. Position is trusted end to end (extends [T3D-111](3d-capability-board.tsv)).

**For a server:** do **not** trust a 3D client's position — the path accepts arbitrary teleports. Add position/speed sanity checks server-side if you need anti-cheat.

## T3D-129 — reconnect & state persistence: none **[lab]**

The 3D link times out after **30 s** of silence (`TIMEOUT_MS = 30000`) and tears down; there is **no reconnect/resume handshake**. Per-session state (control object, ghosts) is tied to the connection — a rejoin re-enters via login + warp and **rebuilds from the world** (ghosts re-sent, control object re-created, 3D state reset). The server keeps nothing session-specific across the gap.

**For a server:** there is **no transport-level 3D session persistence** across a reconnect — implement any "resume where you were" at the world/script layer, not the link.

## Method caveat

Single client, loopback gserver, software GL. The login steps and position acceptance are from the live link trace + a scripted teleport. The reconnect verdict is read from the gserver timeout/teardown path (`TIMEOUT_MS`) and the login+warp rebuild — the harness runs one session per launch, so a live mid-session drop-and-rejoin was not orchestrated; the "fresh session, no resume" conclusion rests on there being no resume handshake in the entry path.
