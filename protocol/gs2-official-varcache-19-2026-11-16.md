# Official GS2 bodies: variable-cache opcodes on the full 19 (6.113)

Date: 2026-11-16. Tags: **[cap]** for the offline walk of held official bodies; **[inf]** where bytecode cannot recover source predicates.

Leads-only confirm against a third-party claim. No third-party code. Bodies, keys, script names and server names stay out of this repository — counts and structure only.

Extends the partial seven-body walk in [gs2-official-varcache-functable-partial-2026-11-16.md](gs2-official-varcache-functable-partial-2026-11-16.md) to the full **19** official 6.113-era bodies (six class + thirteen login-weapon) from [gs2-official-bytecode-6113.md](gs2-official-bytecode-6113.md).

## Corpus

| Set | Size | Role |
| --- | --- | --- |
| Official 6.113-era bodies | **19** | Primary counts below |
| Non-official GS2 bodies (separate held corpus, own reader) | **199** | Control: none of 45 / 46 / 47 / 190 |

Container checks match the earlier note on every official body: segments 1–4 once each, segment 1 word **0**, no trailing newline, markers `F0`–`F6` only. **[cap]**

## Opcodes 45, 46, 47 and 190

Client VMs already name these: 45 stores the top into a local slot without popping, 46 pushes a slot, 47 turns the top into a resolved variable reference; together they cache a variable for reuse. 190 is `loadparams`. Open compilers do not emit 45–47. **[bin]** ([gs2-vm-by-version.md](../client-internals/gs2-vm-by-version.md); [gs2-client-vm.md](gs2-client-vm.md))

| Check | Result on these 19 | Tag |
| --- | --- | --- |
| Bodies that emit any of 45 / 46 / 47 | **15 of 19** (four small/medium bodies have none) | [cap] |
| Counts | **403**×45, **1703**×46, **403**×47, **2**×190 | [cap] |
| 47 then 45 | **Every** 47 is immediately followed by 45 (**403 / 403**) | [cap] |
| Named alloc recovery (47→45 with a recoverable name) | **403 / 403** | [cap] |
| Slotted function ranges | **129**; first allocs dense **`0..n−1`** in **129 / 129** | [cap] |
| Opcode 190 | **2** instructions, both **no** operand; pattern is standalone 190 then index/call — **not** `190→47→45` | [cap] |
| Builtin `params` selected as a cached slot | **0** in this corpus | [cap] |

So the official compiler **does** emit the cache trio heavily on real server output, and **can** emit 190 for the builtin `params` read. Caching `params` into a numbered slot is **not** required by these bodies. **[cap]**

### Control corpus

Walking **199** non-official GS2 bodies with an independent reader found **0** instructions of opcodes 45, 46, 47 or 190. Official-body slot and `params` usage is therefore a real official-output feature, not a decoder artefact. **[cap]**

## `temp.*` members

Slot allocation for a temporary member recovers as: load-temp → name → member-access → resolve (47) → store-slot (45).

| Check | Result | Tag |
| --- | --- | --- |
| Temp-member slot allocs | **151 / 403** | [cap] |
| Plain-id slot allocs | **252 / 403** | [cap] |
| Distinct `temp.<member>` names among allocs | **78** | [cap] |
| No-loop slotted names that are temp members | **8 / 10** of the no-loop allocs | [cap] |

Official output **does** cache `temp.*` members, not only plain identifiers. **[cap]**

## Five-use / in-loop shape (still not a proven AST rule)

| Check | Result | Tag |
| --- | --- | --- |
| Slotted ranges that also contain `loopcheck` (opcode 9) | **123 / 129** | [cap] |
| Slotted ranges **without** a loop | **6** ranges, **10** slot allocs | [cap] |
| No-loop allocs with slot-load (46) count **≥ 5** | **10 / 10** (minimum loads = 5) | [cap] |
| No-loop allocs with loads &lt; 5 | **0** | [cap] |
| In-loop allocs with loads &lt; 5 | **259 / 393** (allowed if an “any in-loop” rule fires) | [cap] |

Bytecode **shape still fits** “no loop ⇒ hot enough (≥5 loads via 46); in-loop may be colder.” It does **not** prove a compiler AST predicate: offline bytes cannot recover exact source reference counts, nor which name-loads share a cacheable identifier versus a property name. A naive “opcode-22 count ≥ 5 ⇒ must slot” test is **rejected** (GUI property-name noise). A rule “function contains `loopcheck` ⇒ every hot temp slots” is **too strong** (counterexample shapes exist). The assignment rule stays **[inf]** until a compile fixture with known source, or an official emitter read, lands. **[cap][inf]**

## Still open

- Prove or refute the five-use / in-loop threshold with a controlled compile fixture (plain id and `temp.*`, inside vs outside a loop body).
- Whether GS2 lambdas are excluded from the slot pass (no generated lambda-style names in these 19 tables).
- Client-side function lookup: hash map vs linear table (**4.20r8**, **5.00r7**, **6.x**).

Segment-2 wire order for these same 19 bodies is tracked as a separate note (dotted-last suffix, dense slot ids, hash-bucket order refuted).
