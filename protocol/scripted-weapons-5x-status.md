# Scripted weapons / NPC GS2 on 5.00r7 and 5.12 — status

Date: 2026-11-16. Research-list rank **#5** (focus 5.007, 5.120; adjacent 4.208). Consolidates packet-guard and unknown-id notes; **no new handler read or weapon fixture** this pass.

Tags: **[bin]** receive sets; **[srv]** server habits as contrast; **[inf]** open path choice.

## Settled: which messages can carry scripts

| Era | Builds | Weapon / class delivery ids | Ask ids |
|---|---|---|---|
| **Classic** | 3.153–**5.12** (incl. **5.00r7**, **4.208**) | **193** hash → **132** weapon body / **133** class body (behind RAWDATA) | **158** weapons / **161** classes |
| **Modern** | **5.00r7** onward (incl. **5.12**, 5.24+, 6.x) | **197** load descriptor → **140** weapon/script body (`GRESCR01` when cached) | **158** on miss |

Hard gates (do not send ids the client dropped or never had):

- Never **132 / 133 / 193** → 5.24+ (incl. 6.037).
- Never **197 / 140** → pure 4.x (through 4.208).

Canonical tables: `script-packet-guards.md`, `class-bytecode-v4.md`, `unknown-ids-2026-11-06.md`. **[bin]**

## Transitional focus: 5.00r7 and 5.12

Both builds **handle classic and modern** sets. Seihai-gserver’s profile gate prefers **classic while 193/132/133 are still present**. That is a **server policy**, not a proof that stock worlds never use 197/140 on these clients. **[bin][inf]**

| Open question | Why it matters | Next method |
|---|---|---|
| Which path a **stock** 5.00r7 / 5.12 world needs for scripted weapons | CLASS prop / empty line / 158 ask vs 197+140 | **L** weapon fixture (+ optional **S** of ask sites) — research **#55** / **#54** |
| Empty GS2 from GS1-only under “modern” compile (C6) | v4/v5 may get no script without GS1 fallback | Server compile lab; tag **#16** |
| Offline / local-game skip on 132/193 | Third-party lead | Unproven on our side |

## 4.208 reminder

Pure 4.x takes **classic only**. Answering a class ask with 197/140 is the wrong path (`class-bytecode-v4.md`). CLASS vs empty-line suppression of 158 is **#55**, not closed here.

## Open checklist

- [x] Loopback weapon fixture on 5.12: which ask/body ids fire for a GS2 weapon ([below](#lab-gs2-weapon-fixture-on-512-g307-2026-11-25)).
- [ ] The same fixture on 5.00r7 (the lab install still stalls before connecting).
- [x] Same fixture with CLASS prop / empty line variants (#55), on 5.12: the empty line does not suppress 158; classes arrive on 133 or 140 after a 161, and prop 74 also triggers 161 ([class delivery](#lab-class-delivery-on-512-g307-follow-up-2026-11-25)).
- [ ] Static read of the leading byte that 5.12 skips in prop 74, and whether a prop-74 NPC runs the class once answered.
- [ ] Confirm C6 empty-program threshold if a modern compile oracle is available.

## Lab: GS2 weapon fixture on 5.12 (G307, 2026-11-25)

Windows 5.12 (packed `Graal.exe`) under Wine in the loopback-only lab VM,
against the lab GS2Emu (`generation = modern`, `serverside = false`) behind the
probe proxy. Rows are in `probe-results.tsv` under runs `wpn512-b` to `wpn512-h`.
5.00r7 was tried and still stalls before it connects, so this covers 5.12 only.

**Fixture.** A weapon `GS2Fix` on the default account whose clientside
`onCreated` sets `player.chat = "wpn ok"` and starts a one-second timer that
reports `wpn t1`, `wpn t2` and so on. The client reports its own chat in prop
12, so "the weapon runs" is read from the wire. The compiled body is 187 bytes.
This server needs a `//#GS2` line: without it the weapon is lexed as GS1 and the
server sends only the 33 with no script. The client keeps weapon code under
`weblevels/weapons/<server>/<weapon>.code` with the server name escaped (space as
`%032`). "Cold" means that folder was removed first.

**Both paths run the weapon on 5.12.**

| path | sequence | weapon runs |
|---|---|---|
| modern (server default) | 33 → 197 → client 158 (0.08 s later) → 100 + 140 | 0.04 s after the 140 |
| classic (forced at the proxy) | 33 → 193 (CRC-32 of the bytecode + name) → client 158 (1 ms later) → 100 + 132 with the same 187 bytes | 0.036 s after the 132 |

The lab server never sends 193, 132 or 133 to 5.12; it always picks 197/140. The
classic case was forced by dropping the server's 197s and the client's 158s at
the proxy and injecting 193 and 132.

**Cache.** With a warm cache the client skips the ask on either path: 197 alone
or 193 alone is enough, and the weapon runs from the cached file (a later 132
re-runs `onCreated`). The two paths write different files (195 bytes after a
140, 204 bytes after a 132), and a file written by one path counts as a miss for
the other path's check: the client asks 158 again in both directions. So the
cache format or the hash basis differs between 193 and 197 [inf on which].

**#55 variants.**

- A weapon whose clientside part is empty (`//#GS2` and `//#CLIENTSIDE` only)
  still gets a 197 and still causes a 158 on a cold cache; the server answers a
  71-byte 140 holding an empty program. An empty script line does not suppress
  the ask.
- A level NPC whose clientside GS2 joins a class makes 5.12 ask **161** (body:
  GINT5 0 + class name) 64 ms after the level arrives. The lab server never
  answers it (no 133, no class 140 or 197), so the class does not run and the
  client asks again on every login. The follow-up below answers 161 by
  injection.

## Lab: class delivery on 5.12 (G307 follow-up, 2026-11-25)

Same lab and client as above; rows under runs `cls512-a` to `cls512-h`. A level
NPC's clientside GS2 joins class `g307cls`, whose timer reports `cls ok N` in the
player's chat. The class body is the lab server's own compile, taken from a run
where the same script was briefly delivered as a weapon. The client's 161 was
dropped at the proxy so the server stayed out of it, and answers were injected.

| answer to 161 | runs the class? | cache |
|---|---|---|
| 100 + **133**: GCHAR name length, name, bytecode (no hash, no header) | yes, 0.05 s after the 133 | none written |
| **197** `class,<name>,1,<hash>,"<5 bytes>"` alone | no, and no further ask in 8 s | none |
| 197, then 100 + **140**: GSHORT header length, `class,<name>,1,<hash>`, bytecode | yes, 0.043 s after the 140 | `weblevels/classes/<server>/<name>.code` |

The 133 layout matches [class-bytecode-v4.md](class-bytecode-v4.md); the class
140 is the weapon 140 with `class` as the type. Whether a 140 works without a
preceding 197 was not tested.

**161 on every login.** The 161 body is GINT5 + class name. With no cached class
(including after a 133 delivery) the GINT5 is 0. After a 140 delivery it is the
second, 5-byte field of the 197 descriptor that came with the body, not the
CRC-32 of the bytecode. The client asks even with the class cached, and the
cached class does not run until the server answers. How short a server may
answer a matching hash (a 197 alone?) is open.

**CLASS prop 74.** An NPC with no `join` whose prop 74 is set by PLO 3 also
makes 5.12 ask 161, about 50 ms later. The client skips the first byte of the
value: `g307cls` gives an ask for `307cls`, and `_g307xyz` gives `g307xyz`. So a
server must put one leading byte before the class name [wire only; what that
byte means is open]. Whether such an NPC then runs the class was not tested.
