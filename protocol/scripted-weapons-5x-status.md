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
- [x] The same fixture on 5.00r7 ([below](#lab-gs2-weapon-fixture-on-500r7-g307-2026-11-25)).
- [x] Why a weapon whose 33 carried source text ignores later bytecode on 5.00r7 (static): the 33 text marks the weapon as a GS1 object, and event dispatch then goes only to GS1 ([5.00r7 section](#lab-gs2-weapon-fixture-on-500r7-g307-2026-11-25)).
- [x] Same fixture with CLASS prop / empty line variants (#55), on 5.12: the empty line does not suppress 158; classes arrive on 133 or 140 after a 161, and prop 74 also triggers 161 ([class delivery](#lab-class-delivery-on-512-g307-follow-up-2026-11-25)).
- [x] Static read of the leading byte that 5.12 skips in prop 74: there is no skipped byte. Prop 74 has a GSHORT length, and the lab runs sent a GCHAR length ([CLASS prop 74](#lab-class-delivery-on-512-g307-follow-up-2026-11-25)).
- [ ] Lab: a prop-74 NPC sent with a GSHORT length, and whether it runs the class once 161 is answered.
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
makes 5.12 ask 161, about 50 ms later. Prop 74 is a string with a two-byte
GSHORT length, (b1 − 32) × 128 + (b2 − 32), not a GCHAR length. The client hands
the string to the object's script space as its class list (5.12, 4.20r8 and
6.037 read it the same way) [static]. The lab runs sent a GCHAR length and then
the name, so the client took the length byte and the first letter as the two
length bytes. The length came out too long and was clamped to the end of the
message, which is why the ask looked as if one byte had been skipped (`g307cls`
gave `307cls`) [lab, re-read 2026-11-25]. A malformed prop 74 like that also
swallows every prop after it in the same message. If the object had no script
before, the parser then fires `created` [static].

**Server rule:** prop id 74, a GSHORT length, then the class name(s). Whether
such an NPC runs the class once 161 is answered has not been run.

## Lab: GS2 weapon fixture on 5.00r7 (G307, 2026-11-25)

Windows 5.00r7 (unpacked `Graal.exe`, the lab's licence-check-patched engine)
under Wine in the same loopback-only lab, with the same `GS2Fix` weapon as the
5.12 runs. Rows are under `wpn500-a` to `wpn500-e`.

**Lab note: why 5.00r7 had stalled.** The client needs its signed licence files
(`license/license.graal` and `license/sig.license`); without them it never dials.
With them it dials the login host and port 14900 named in the signed licence,
which does not exist in a closed lab. The licence cannot be edited, so the lab
redirects that one connect to the local login server with a preloaded connect
shim. Under Wine 10 the shim must also load into wineserver, which is the process
that performs the connect. **[lab]**

**What the lab server sends.** To 5.00r7 the lab GS2Emu sends each weapon's
script as **source text inside 33**, with no 197, 193, 140 or 132, and the client
asks nothing (no 158). GS1 weapons sent that way run. The GS2 weapon does not
run, on a cold or warm login, and no cache file is written. (To 5.12 the same
server sends a bare 33 and then 197/140.)

**Bytecode paths, injected.**

| what was sent | ask | runs? |
|---|---|---|
| server's source-text 33, then 197 | 158; server answers 100 + 140; 195-byte cache file | **no** |
| server's source-text 33, then 193, then 100 + 132 | 158; 204-byte cache file | **no** |
| **bare** 33 (image only), then 100 + 132 | — | yes, 0.004 s after the 132 |
| **bare** 33, then 100 + 140 | — | yes, 0.97 s after the 140 |

So 5.00r7 handles 197 → 158 → 140 and 193 → 158 → 132 like 5.12 (same ask id,
same cache sizes), and both bodies run GS2 bytecode, but only for a weapon whose
33 carried no script text. A weapon first created from source text ignores
bytecode that arrives later on either path [lab].

The block is in event dispatch, not in the 132/140 handlers. On 4.20r8 and
5.00r7, a weapon whose 33 carried script text counts as a GS1 object, so every
event goes to the GS1 interpreter and never reaches the bytecode loaded later
[static]. The 4.20r8 text-prop parser also stores script text only while the
GS1 slot is empty [static]. 5.12 has no GS1 branch, so the same 33 should not
block it there [inferred; not run].

**Server rule for 5.00r7:** send a bare 33 and then 197/140 or 193/132. Do not
send GS2 as source text in 33.
