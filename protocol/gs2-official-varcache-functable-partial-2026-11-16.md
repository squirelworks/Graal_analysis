# Official GS2 bodies: variable-cache opcodes and function-table order (partial)

Date: 2026-11-16. Tags: **[cap]** for the offline walk of held official bodies; **[bin]** / **[doc]** / **[inf]** where cited notes already say so.

Leads-only confirm against a third-party claim. No third-party code. Bodies, keys, script names and server names stay out of this repository — counts and structure only.

## Input

A **partial** re-walk of **7** official login-weapon GS2 bodies from the same 6.113-era capture family as [gs2-official-bytecode-6113.md](gs2-official-bytecode-6113.md) (that note’s full set is 19: six class + thirteen weapon). These seven decrypt with the held PLO 197 session keys and match the published CRCs. The other twelve of that nineteen are not in this pass. **[cap]**

Container checks match the earlier note on every body here: segments 1–4 once each, segment 1 word **0**, no trailing newline, markers `F0`–`F6` only. **[cap]**

## Rank 1 — opcodes 45, 46, 47 and 190

Client VMs already name these: 45 stores the top into a local slot without popping, 46 pushes a slot, 47 turns the top into a resolved variable reference; together they cache a variable for reuse. 190 is `loadparams`. Open compilers do not emit 45–47; the third-party compiler also skips 190. **[bin]** ([gs2-vm-by-version.md](../client-internals/gs2-vm-by-version.md#opcodes-the-open-compilers-do-not-name); [gs2-client-vm.md](gs2-client-vm.md#names-the-client-gives-the-opcodes); [gs2-official-bytecode-6113.md](gs2-official-bytecode-6113.md#opcodes-seen))

| Check | Result on these 7 | Tag |
| --- | --- | --- |
| Bodies that emit any of 45 / 46 / 47 | **6 of 7** (one small body has none) | [cap] |
| Counts | 268×45, 1084×46, 268×47 | [cap] |
| 47 then 45 | **Every** 47 is immediately followed by 45 (268/268) | [cap] |
| Slot operands | Dense 0-based integers per function; highest slot index seen is 10 | [cap] |
| Opcode 190 | **2** instructions, both in the largest body, **no** operand; absent from the other six | [cap] |

So the official compiler **does** emit the cache trio on real server output, and **can** emit 190. That widens the earlier “190 is emitted” line from the nineteen-body note with per-opcode counts. **[cap]**

What this pass **cannot** settle: the claimed rule “slot a variable after five uses in a function, or anywhere inside a loop.” Among 308 functions across the seven bodies, 80 use slots and 77 of those also contain `loopcheck` (opcode 9). Many functions **without** slots still contain loops and large numbers of name-loads (opcode 22), including builders with hundreds of 22s. Offline bytecode alone does not recover which source names were candidates, so the threshold stays **[inf]** until a compiler-side fixture or a fuller corpus+source pair.

## Rank 2 — segment-2 function-table order

The lead under test is that the function table is ordered by a case-insensitive name hash, against emitters that keep source order.

On these seven tables:

- Order is **not** case-insensitive alphabetical (0/7). **[cap]**
- Order is **not** ascending by entry opcode index (0/7). Index drops are common: a later table row often points earlier in the instruction stream. **[cap]**
- Order is **not** sorted by several common case-insensitive string hashes tried offline (multiplicative 31/33/37/128/131, djb2-style, sdbm, Java-31, ELF/Borland-style, a xor-shift). None matched any body. **[cap]**
- `public.` prefixes are mixed through the list, not grouped first. Dotted `object.method` names are often contiguous by object, not always. **[cap]**

So the **serialized** segment-2 list is not a name-hash sort. The shape fits **declaration / encounter order** for the name list, with opcode indices assigned when bodies are laid out (which explains index drops). Whether a client’s **runtime** lookup still hashes names is a separate static read — not shown by this walk. **[cap][inf]**

## Ranks 3–5 (pointers only)

| Lead | From these bodies | Where to look next |
| --- | --- | --- |
| Segment-1 GS1 event mask | Always 0 here, as in the nineteen-body note | Event-mask / `needEvent` dispatch in stock **4.20r8**, **5.00r7**, and **6.00** images **[bin]** |
| Top-level code re-run before each event (PG1) | Not visible in static bytecode | Bounded live fixture on stock **4.20r8**, **5.12**, **6.03r7**; Linux 4.04r2 already has a bounded event experiment elsewhere **[lab]** |
| GR-V1.05 multi-layer levels | Not a script-body question | Level reader in **5.00r7** and **6.00** images **[bin]** |

## Against the earlier nineteen-body note

- Confirms again: no trailing `0x0A`, segment 1 zero, 190 can appear. **[cap]**
- Adds: 45/46/47 are common on official output; 47 is always paired with 45; 190 is rare in this login-weapon slice. **[cap]**
- Adds: segment-2 wire order is not a CI name-hash sort on this sample. **[cap]**

## Still open

- ~~Repeat ranks 1–2 on the full nineteen-body set (six class + thirteen weapon).~~ Rank 1 deepen: [gs2-official-varcache-19-2026-11-16.md](gs2-official-varcache-19-2026-11-16.md). Rank 2 order: separate note.
- Prove or refute the five-use / loop threshold with a controlled compile fixture.
- Client-side function lookup: hash map vs linear table (**4.20r8**, **5.00r7**, **6.x**).
- When segment 1 is non-zero and how the VM uses it.
