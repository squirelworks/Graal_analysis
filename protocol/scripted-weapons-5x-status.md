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

- [ ] Loopback weapon fixture on 5.00r7 and 5.12: which ask/body ids fire for a GS2 weapon.
- [ ] Same fixture with CLASS prop / empty line variants (#55).
- [ ] Confirm C6 empty-program threshold if a modern compile oracle is available.
