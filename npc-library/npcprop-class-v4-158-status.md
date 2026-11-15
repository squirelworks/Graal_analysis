# `NPCPROP_CLASS` / empty line vs v4 `PLI_UPDATESCRIPT` (158) — status

Date: 2026-11-16

Research-list **#55** / comparison **B3**. Status only: what is settled from
existing notes, what Others Work claimed live, and what a loopback isolate
must still prove. No new lab this pass.

Tags: **[bin]** · **[srv]** · lead-only where marked.

## Settled **[bin]** **[srv]**

| Fact | Cite |
|---|---|
| 4.20r8 **does not** handle PLO **197** or **140** | `protocol/v4x-clients.md` |
| Working v4 weapon body path is **33 → 193 → (miss) 158 → 132** | `protocol/unknown-ids-2026-11-06.md`, class/weapon notes |
| Class ask/answer on v4 is **161 → 133**, not 197 | `protocol/class-bytecode-v4.md` |
| Packet-layout wording that “v4 and later” replace the script prop with **`NPCPROP_CLASS` + 197** describes **stock GServer-v2 habit**, not a verified 4.20r8 *client* requirement | `protocol/packet-layouts.md` **[srv]** |

So CLASS+197 cannot be how a pure 4.x client *receives* bytecode. The open
question is whether CLASS (or an empty line) on the **weapon-add prop stream**
stops the client from ever sending **158**.

## Others Work live claim (lead only)

On 4.20r8: weapon-add **with** `NPCPROP_CLASS` (and an extra empty line) →
client never asked 158; **without** → it did. They did **not** isolate CLASS
vs the empty line.

| Hypothesis | Status |
|---|---|
| CLASS alone suppresses 158 on stock 4.20r8 | **Open** |
| Empty line alone suppresses 158 | **Open** |
| Both required | **Open** |
| “v4+ ⇒ CLASS+197” as a *client* rule | **Over-broad** until isolate finishes |

## Method when run (loopback only)

1. Stock 4.20r8 (pairs with research **#3** unlock when available) + assets.
2. Controlled weapon-add fixtures: name only / +CLASS / +empty line / both.
3. Watch for **158** after a deliberate **193** miss (no matching `.code`).
4. Then check **5.00r7 / 5.12** (research **#5**): CLASS+197 vs still 193/132
   when both id families are accepted.

No public servers. Do not copy Others Work patches or prop tables.

## Implications

- Until isolate finishes, Seihai must not assume CLASS prevents 158 on v4.
- Keep correcting readers who treat the GServer “v4+” CLASS+197 line as a
  client requirement.
- Adjacent: research **#54** cache path must be right for a fair 193 hit/miss
  arm (`formats/weblevels-server-folders.md`, `formats/weblevels-code-residuals.md`).
