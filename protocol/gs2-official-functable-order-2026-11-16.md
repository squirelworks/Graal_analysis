# Official GS2 bodies: segment-2 function-table order (full 19)

Date: 2026-11-16. Tags: **[cap]** for the offline walk of held official bodies; **[inf]** where models remain unproven.

Leads-only confirm against a third-party claim. No third-party code. Bodies, keys, script names and server names stay out of this repository — counts and structure only.

Corpus: the same **19** official 6.113-era GS2 bodies as [gs2-official-bytecode-6113.md](gs2-official-bytecode-6113.md). Slot-id density cross-checks [gs2-official-varcache-19-2026-11-16.md](gs2-official-varcache-19-2026-11-16.md).

## What the partial seven-body note already showed

The earlier [partial walk](gs2-official-varcache-functable-partial-2026-11-16.md) found that, on seven login-weapon tables, segment-2 order is **not** case-insensitive alphabetical, **not** ascending by entry opcode index, and **not** a plain sort by several common case-insensitive string hashes. **[cap]**

This pass repeats those negatives on all **19** and adds the structural positives that hold.

## Settled structure on all 19

| Check | Result | Tag |
| --- | --- | --- |
| Qualified / dotted names (`object.method`, after stripping a leading `public.`) form a **contiguous suffix** | **19 / 19** (vacuous when a body has none) | [cap] |
| Among qualified rows, wire order = increasing segment-4 op-index | **10 / 10** bodies that have any qualified row | [cap] |
| Wire unqualified order = ascending op-index | **1 / 19** only | [cap] |
| Op-index **drops** along the wire list (a later row points earlier in the stream) | **18 / 19** bodies | [cap] |
| Case-insensitive alphabetical sort of unqualified = wire | **1 / 19** | [cap] |
| Slot alloc ids dense `0..n−1` per slotted function | **129 / 129** slotted ranges | [cap] |
| Slot id == raw `hash(name) & 31` for every slot in a function | **4 / 129** (chance level) | [cap] |

So:

1. **Dotted / qualified names always come last** as one contiguous block. **[cap]**
2. **Slot numbers are dense indices `0..n`**, not raw hash-bucket ids. **[cap]**
3. Unqualified prefix order is **neither** pure source/op-index order **nor** a plain CI name-hash sort. **[cap]**

## Hash-bucket order — refuted as the official rule

A third-party lead claimed unqualified segment-2 rows are emitted by dumping a Delphi-style name-hash bucket table (seeded multiplicative hash, growing bucket array, newest-first within a bucket) over emit/registration order.

On these 19 bodies, treating that bucket dump as the **official** serialisation rule is **refuted**. Exact full-table matches under that model do not survive as a stock rule once the registration input and the enlarged independent re-walk are held fixed; keep **dotted-last + dense slots**, and do **not** treat “implement the bucket dump” as confirmed official behaviour. **[cap]**

Whether a client’s **runtime** lookup still hashes names is a separate static read — not shown by the wire list. **[inf]**

## Still open

- Recover the exact unqualified reorder rule (beyond “not source order, not CI-alpha, not bucket-dump”).
- Whether runtime name lookup hashes on **4.20r8**, **5.00r7**, and **6.x**.
- Slot *prologue order* vs first-seen AST order for large functions (density of ids is closed; encounter order is not fully recovered).
