# GS2 loader and VM quirks by version

Date: 2026-11-16. A compact cross-version quirks table for how GS2-capable clients
**load and run** bytecode, so era scripts can be tied to the build they shipped on.
Compile-time pass rates are a related signal; they are not the VM.

This page does not replace the graded per-build table
([gs2-vm-loader-diff.md](gs2-vm-loader-diff.md)) or the opcode side-by-side
([gs2-vm-by-version.md](gs2-vm-by-version.md)). It restates published readings in
plain behaviour, adds one loopback timer lab on Linux 6.03r7, and flags where
corpus spelling can bite at run time. No new disassembly. Unity 7.x was not opened.

## Evidence tags

| Tag | Meaning here |
| --- | --- |
| [bin] | Client image reading already published in this repository |
| [cap] | Offline walk of held official bytecode bodies (counts and structure only) |
| [lab] | Loopback run or corpus aggregate |
| [doc] | Published profile or clean-room note (our words) |
| [srv] | Lab server path summarised in our words (no GPL paste) |
| [inf] | Inference past a reading |

Builds whose client VM was **read**: 3.153 (Mac PowerPC); 4.20r6 Mac PowerPC and
Linux 4.20r6 (selector / `waitfor`); 4.20r8 Windows; 5.00r7 Windows; 6.00r2 / 6.00r4
Windows; 6.01r1 / 6.03r7 Linux; 6.113 / unpacked 6.1.1.3; Android Classic 1.8
(**interim** — see Android below). Unread siblings borrow the nearest earlier row
**[inf]** as in the by-version note. Unity 7.x unread.

### Android Classic 1.8 (interim)

Only Classic 1.8's native engine has a published GS2 machine note
([../protocol/gs2-android-classic-18.md](../protocol/gs2-android-classic-18.md)).
Era and other Classic builds stay open on every VM dimension in the graded table.
Refresh the Android cells here when a further Classic/Era GS2 reading lands — own
words only. **[bin]**

---

## 1. Headline differences

1. **Opcode sets grow, then drop.** 4.20r8 adds `waitfor` (11) and fusion 200–233.
   5.00r7 adds 48, 49, 54 and 121. **6.x drops 48 and 49**, keeps 54 and 121, adds
   sentinel 164 and fusion 234–242. A script whose compiler emitted 48 or 49 is
   **5.x-only** at runtime. **[bin]**
2. **Frame slots 45 / 46 / 47 exist on every read client VM; open compilers often
   emit none.** Official 6.113-era bodies use them heavily (every 47 is followed by
   45 on the seven-body slice; dense slot indices). A Seihai-shaped emit path can
   still run without slots; hot official bodies differ in shape. **[bin][cap]**
3. **Segment loader is stable.** Big-endian type and length words; types **1–4**;
   trailer `0x0A` is **not** required; a disk wrapper byte that is not a type 1–4
   stops the plain walker as a bad type. Writers usually emit 1→2→3→4; readers
   accept any order. **[bin]**
4. **Event casing is a real corpus risk.** Weapon and world corpora show both
   `onTimeout` and `onTimeOut`, and similar splits on other event names.
   `scheduleEvent` **lowercases** before store; `cancelEvents` matches without
   case **[bin]**. Whether timer **dispatch** finds `onTimeOut` when looking for
   `ontimeout` is **not** closed by a spelling × client matrix. Clean-room and
   reproduction loaders fold; treat stock fold as **probable but unproven for
   every era**. **[bin][doc][lab][inf]**
5. **Timer quantize changes by era.** Classic GS1 floors can drop `T < 0.05` to
   never-fire. On **Linux 6.03r7**, with Seihai-compiled bytecode on a loopback
   lab path, periods **ceil to 50 ms** and sub-0.05 values **do fire** (~20/s).
   **[lab]** Do not copy a 4.x floor table onto 6.x.
6. **Maths / platform quirks.** Integer paths use `floor(x + 0.0001)` on every
   desktop VM that was read. Remainder tolerance differs (kept on the 4.20 family;
   dropped on 3.153 / 5.x / 6.x). Shifts: **PowerPC mod 64** vs **x86 mod 32**.
   Value stack: **256** (3.153) → **10000** (4.x / 5.x) → **uncapped helper**
   (6.x / Android Classic 1.8). **[bin]**
7. **Most corpus “fail to compile” gaps are compile-time**, not missing VM opcodes:
   strict rejects of legacy constructs; GS1 commands with no GS2 lowering. The rows
   below matter for scripts that **already compile** but diverge or miss events at
   run time across eras. **[lab]**

---

## 2. Per-build opcode and fusion matrix

| Build | Handled opcodes (summary) | Fusion | Notes | Tag |
| --- | --- | --- | --- | --- |
| 3.153 | 1–10, 20–27, 30–47, 50–53, 60–103, 110–120, 130–142, 150–151, 163, 180–184, 189–190 | none | No 11; stack 256 | [bin] |
| 4.20r6 Mac | +104 | none in that Mac read | Object compare; Linux 4.20r6 is a different image (see Events / Linux note) | [bin] |
| 4.20r8 | +11, +200–233 | load-time rewrite | First fused set | [bin] |
| 5.00r7 | +48, 49, 54, 121 | 200–233 | Object / list literals; three-operand member store; string-or-add | [bin] |
| 6.00r2 / r4 | as 4.2 +54, 121, 234–242; **no 48 / 49** | +234–242 | Clock step 0.05 not found in those images | [bin] |
| 6.01r1 / 6.03r7 | +0, +164; same drop of 48 / 49 | 200–242 | Computed-goto; end-of-script sentinel 164 (loader-appended, not in file) | [bin] |
| 6.113 | same family as 6.03 for cases read | same | No new opcode past the 6.00 set | [bin] |
| Android Classic 1.8 (**interim**) | 165 dispatch cases; 43 fusions | yes | Value stack uncapped like 6.x; event queue refuses at **1000** (not 9999). Refresh when a fuller Classic/Era GS2 note lands | [bin] |

### Client-only / open-compiler gaps (eras that have the case)

| Op | From | Behaviour (short) | Tag |
| --- | --- | --- | --- |
| 45 `setreg` | all read | Copy TOS → frame slot *n* (0..1023), leave TOS | [bin] |
| 46 `getreg` | all read | Push frame slot *n*; out of range → 0 | [bin] |
| 47 `makeprop` | all read | Resolve top into a variable ref (slot cache with 45 / 46) | [bin] |
| 48 / 49 | **5.00r7 only** | Object literal / number-list literal (*n* clamped 0–10000 for 49) | [bin] |
| 54 | 5.00r7 on | Three-operand member store (details still incomplete on 5.00r7) | [bin] |
| 66 / 67 | all read | Non-short-circuit `&&` / `\|\|` as 0 / 1 values | [bin] |
| 121 | 5.00r7 on | `+` joins if either side is a string, else adds | [bin] |
| 164 | 6.x (Linux family) | Loader sentinel; never in file bytes | [bin] |
| 190 | all read | Push `params` object (official bodies use this, not a slotted TypeVar `"params"`) | [bin][cap] |
| 200–233 | 4.20r8 on | Immediate arith / assign / compare / slot fusions | [bin] |
| 234–242 | 6.x | Var+member, var+call, 47+45, imm array index, … | [bin] |

Unknown opcode / default: Android continues without a pop **[bin]**; some 4.2 unnamed
bytes fall through a helper and skip instruction slots **[bin]** — the skip rule
differs by build. Do not assume one rule.

Detail and grades: [gs2-vm-by-version.md](gs2-vm-by-version.md),
[gs2-vm-loader-diff.md](gs2-vm-loader-diff.md),
[../protocol/gs2-client-only-opcodes.md](../protocol/gs2-client-only-opcodes.md).

---

## 3. Slot rules

| Rule | Builds | Evidence | Tag |
| --- | --- | --- | --- |
| Slot index 0..1023; frame list grows to index; empty stack / no frame stops | all read | client-only opcodes note | [bin] |
| setreg leaves the value; getreg out of range pushes 0; setreg out of range does not write | all read | same | [bin] |
| Official compiler: hot locals use 47 then 45; reads via 46; dense 0..*n*−1 | 6.113-era bodies | seven-body slice: every 47 followed by 45; dense indices | [cap] |
| Builtin `params` → opcode 190, not a slotted TypeVar | 6.113-era | rare 190 sites; not rewritten as 47→45 | [cap] |
| Seihai / many open emitters: **no** 45 / 46 / 47 | clean-room docs | still a shape gap vs official bodies | [doc][cap] |
| Fusion 228–233 / 242 consume slot load + convert / inc-dec+pop / makeprop+store | 4.20r8+ / 6.x | by-version + client VM | [bin] |

**Era link:** Slot caching is a **compiler-era** habit, not “old clients lack slots.”
Early VMs already have 45–47; later official bytecode depends on them for hot locals.
A script compiled without slots can still run on 4.x–6.x; an **official** body that
assumes fusion 242 needs a 6.x-capable loader.

Published walks: [../protocol/gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md),
[../protocol/gs2-official-varcache-functable-partial-2026-11-16.md](../protocol/gs2-official-varcache-functable-partial-2026-11-16.md).

---

## 4. Segment parsing

| Topic | Behaviour | Builds | Tag |
| --- | --- | --- | --- |
| Layout | BE u32 type, BE u32 length, body; types **1–4** | all read | [bin] |
| Order | Any order accepted; writers usually 1, 2, 3, 4 | 4.2+ | [bin] |
| Stop | Type outside 1–4 or a truncated header ends the walk | 4.2+ | [bin] |
| Trailing `0x0A` | Not required by the loader; ends the walk like junk | 4.2+ | [bin] |
| Disk wrapper before segments | Not stripped by the plain `setScript` walker; type ≠ 1–4 → empty load | 4.2 | [bin] |
| Seg1 | One BE u32 → GS1-style event bit mask | all | [bin] |
| Seg2 | BE index + NUL name; leading `public.` (7 chars) stripped + public flag | all | [bin] |
| Seg3 | NUL strings | all | [bin] |
| Seg4 | Opcodes + `F0`–`F6` operands (BE; `F2` rejects negative) | all | [bin] |
| Decoded instruction size | 24 B on Windows 4.2 notes; **20 B** on Android Classic 1.8 | — | [bin] |
| Peephole | After decode; first op rewritten; PC skips swallowed ops (indices stable) | 4.20r8+ | [bin] |
| Jumps | Operand + piece base (0 inside one script; joined classes shift the base) | 4.2+ | [bin] |

**Wire delivery (not a loader quirk, but era-facing):** S→C 131 / 132 / 133 / 134 / 193
feed `setScript` / class / gani / weapon CRC paths; id 140 is not a case in the 4.2
control dispatch that was opened. **[bin]**

---

## 5. Event-name matching (`onTimeout` vs `onTimeOut`)

### What the client queues / normalizes

| Mechanism | Name form | Case | Tag |
| --- | --- | --- | --- |
| Script attach | queues `created` | literal internal | [bin] |
| Init | `initialized` | literal | [bin] |
| `sleep` (op 8) | saves under `timeout`; due → `istimeout` | literal internals | [bin] |
| Host `setTimer` / timeout property | schedules / fires toward handler `onTimeout` via internal `timeout` | see below | [doc][lab] |
| `scheduleEvent` | **lowercases** the name before store; later queues that name | fold on schedule | [bin] |
| `cancelEvents` | match **case-insensitive** | fold on cancel | [bin] |
| `waitfor` (op 11) | strips a leading `on` after lowercase (Linux 4.20r6: normalize then strip) | fold + strip | [bin] |
| Object-directed events | name starting with `on` treated as directed | prefix rule | [bin] |
| `script_event` bitmask names | `playerenters`, `playertouchsme`, … (no `on` prefix in the table) | fixed table | [bin] |

### Function lookup

| Implementation | Matching | Tag |
| --- | --- | --- |
| Client reproduction loader | lowercases both sides; action `"timeout"` looks up `"on"+"timeout"` with a fallback if the name already has `on` | [doc] |
| Stock 4.2 / 5.0 / 6.x | schedule / cancel fold case **proven**; built-in event dispatch folds case on 4.20r8, 5.00r7, 5.12 and 6.03r7 ([focus-build matrix](#focus-build-matrix-g087-2026-11-25)) | [bin][inf] |
| Three separately identified static inputs | Selected older Windows suffix and backup Windows full-name event scanners fold names, with helper-state qualifications; exact recorded Linux event lookup has matching ASCII-folded registration/query hashes and candidate comparison, plus a separate case-insensitive multi-handler comparison. This is [event-specific evidence](gs2-event-handler-case-2026-11-22.md), not ordinary-call or string-presence inference | [bin][inf] |
| Android Classic 1.8 | schedule lowercases; string compare ignores case | [bin] |
| seihai-core | timer looks up the exact name `onTimeout`; `scheduleevent` keeps the rest of the spelling after stripping `on`, so `onTimeOut` stays distinct | [doc] |
| GServer-v2 wrappers | bind the exact JavaScript identifiers `onTimeout` / `onActionServerSide` | [srv][doc] |

### Focus-build matrix (G087, 2026-11-25)

Static read of the 4.20r8, 5.00r7, 5.12 and 6.03r7 Windows engines (Linux 6.03r7 lookup from the earlier note); nothing run. **[bin]** unless marked.

Built-in events are matched **without regard to ASCII letter case** in all four builds, by two mechanisms:

- **4.20r8** (read in full): on script load every function name is stored lower-cased; calls, including `this.(name)()`, lower-case the name before lookup. The event scanner lower-cases the event name and compares it with each stored name that starts with `on`, minus that prefix.
- **5.00r7 and 5.12** (same code): build `on` + event name and compare it with every full function name, lower-casing both sides.
- **6.03r7**: the Linux build lower-cases both sides at lookup. The Windows build compares `on` + name with every function name case-insensitively for `created`, `initialized` and `initframe`, and finds every other event through a case-insensitive hash of `on` + name (the same hash as 4.20r8). **[bin]**
- **Locale**: none of this depends on the Windows locale. 4.x and 5.x use the C library's `tolower` with no locale set; 6.x does its own A–Z conversion.

| Handler spelling | 4.20r8 | 5.00r7 | 5.12 | 6.03r7 |
| --- | --- | --- | --- | --- |
| `onTimeout` | fires | fires | fires | fires |
| `onTimeOut` | fires | fires | fires | fires |
| `ontimeout` | fires | fires | fires | fires |
| `ONTIMEOUT` | fires | fires | fires | fires |
| `onActionServerSide` / `onactionserverside` | only if a script queues the event by name (no client engine produces it; clients produce `actionclientside`) | same | same | same |

Two exceptions, the same in all four builds:

1. **Some events need a lower-case `on` in the source.** On load, a handler marks its event as listened-to only if its source name starts with exactly `on`. Events gated by that mark are delivered only when it is set: `playerenters`, `playertouchsme`, `playertouchsother`, `playerchats`, `playerhurt`, `playerdies`, `playerlaysitem`, `playerendsreading`, `compusdied`, `emoticon`, `mousedown`, `mouseup`, `mousewheel`, `exploded`, `wasshot`, `waspelt`, `keypressed`, `actionprojectile2`, `playerleaves`, `washit`, `shapetrigger`, `playanimation`; 6.03r7 adds `pkzonechanges`. So `ONPLAYERENTERS` and `OnPlayerChats` never fire, while `onPLAYERENTERS` does. `timeout` and `created` are not gated, so `ONTIMEOUT` still fires. Marking and delivery check are [bin] on 4.20r8 and 5.00r7; on 5.12 and 6.03r7 the marking is [bin] and the delivery check is inferred from the identical mechanism.
2. **Script-queued event names** (`scheduleevent` and the like): only a lower-case `on` is stripped, so `timeout`, `Timeout`, `TIMEOUT` and `ontimeout` reach `onTimeout`, while `OnTimeout` and `ONTIMEOUT` match nothing. [bin] in all four builds (for 5.12 the strip itself; the rest of its event path is inferred to match 5.00r7).

For writers: spell handlers `on` + anything; avoid an upper-case `ON`/`On` prefix, and pass event names to `scheduleevent` without `on` or with a lower-case `on`. A server-side or clean-room VM that matches handler names exactly (seihai-core, GServer-v2 wrappers above) differs from every focus client here.

#### Runtime check (G087, 2026-11-25)

Loopback Wine lab on 5.12, Windows 6.037 and 4.20r8 with small GS2 weapons compiled by the lab server (5.12 and 6.037 delivered by the server; 4.20r8 injected as 33 + 132). Results came from the client's chat, or on 4.20r8 from its PLI 18 reports of `client.*` variables. Rows `evc512-a`, `evc6037-a`, `evc420-a` in [probe-results.tsv](../protocol/probe-results.tsv). 5.00r7 was not run. **[lab]**

| Test | 5.12 | 6.037 (Windows) | 4.20r8 |
| --- | --- | --- | --- |
| Timer handler `onTimeout`, `ONTIMEOUT`, `ontimeout`, `OnTimeOut`, `oNTimeout` | all fire | all fire | all fire |
| Timer handler `Timeout` (no `on`) | never | never | never |
| `scheduleevent` names `Foo`, `foo`, `FOO`, `onFoo`, `OnFoo`, `ONFOO`, `onfoo` → `onFoo` | all seven reach it | all seven | all seven |
| `trigger` names `Bar`, `bar`, `BAR`, `onBar` → `onBar` | reach it | reach it | reach it |
| `trigger` names `OnBar`, `ONBAR` → `onBar` | no | **yes** | no |
| Handlers named `ON…`, `On…`, `oN…`, called by `trigger` or `scheduleevent` | run | run | run |
| Handler with no `on`, called the same way | never | never | never |
| `playerenters` handler `onPlayerEnters`, `onPLAYERENTERS`, `onplayerenters` | fire | fire | fire |
| `playerenters` handler `ONPLAYERENTERS`, `OnPlayerEnters` | never | **fire** | never |
| `foo()` then `FOO()` in one script, called as `foo`, `FOO`, `Foo` | **first** wins | **first** wins | later wins |

Against the static matrix:

- Case-insensitive matching of built-in events: confirmed on all three.
- Exception 1 (gated events need a lower-case `on`): confirmed on 4.20r8 and 5.12 for `playerenters`; **refuted on Windows 6.037**, where every spelling fires (its delivery check had been inferred). Other gated events were not tested.
- Exception 2 (only a lower-case `on` is stripped from queued names): **refuted for `scheduleevent`** on all three builds, where `OnFoo` and `ONFOO` still reach `onFoo`. It holds for `trigger` on 4.20r8 and 5.12, and not on 6.037.
- Duplicate names differing only in case: the later definition wins on 4.20r8, as read; on 5.12 and 6.037 the **first** wins.

So for writers the safe rule stays the same: spell handlers `on` + anything, and pass event names to `trigger` without `on` or with a lower-case `on`.

### Corpus exposure (compile-side)

Published weapon surveys count `onTimeout` heavily among client handlers
([../npc-library/gs2-weapon-corpus-2026-11-14.md](../npc-library/gs2-weapon-corpus-2026-11-14.md)).
Broader world / weapon aggregates also show both `onTimeout` and `onTimeOut`, and
non-majority spellings of `onActionServerSide`, `onPlayerChats`, `onPlayerEnters`,
`onPlayerTouchsMe` and similar. Exact tallies depend on the export set; the point
for this page is the **split**, not a single census. **[lab]**

**Runtime implication:** If a build's handler lookup is case-sensitive against the
**source casing preserved in segment 2**, an `onTimeOut` unit never receives timer
fires even when compile succeeds. If lookup folds (as schedule / cancel and the
reproduction loader do), both spellings work. A spelling × client lab matrix is
still required (at least Windows 6.03 / Linux 6.03r7 and one 5.x) — not filed as a
product issue from this page alone. **[lab][inf]**

The selected-input follow-up narrows this conditional warning: it supplies actual event-consumer case-matching mechanisms, including explicit Linux ASCII folding, rather than a demonstrated casing mismatch. Windows helper state, source normalization, event production and a complete native spelling matrix remain open. **[bin][inf]**

### Queue limits

| Build | Event queue refuse | Tag |
| --- | --- | --- |
| Windows 4.2 / 5.0 family (4.20r8 settled) | >9999 → overrun text | [bin] |
| Android Classic 1.8 | refuse at **1000**; `onAllRCChat` dropped silently at the limit; `istimeout` / `created` / `initialized` go front | [bin] |

A backup 5.00r7 image also showed a 1000 cap; that file may have been patched, so it
is not proof the shipped 5.00r7 used 1000. **[bin]**

---

## 6. Maths, text, limits, clock

| Rule | 3.153 | 4.20r6 | 4.20r8 | 5.00r7 | 6.x | Android 1.8 | Tag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `int` / bitwise / index | `floor(x+1e-4)` | same | same | same | same | toward-0 on some paths; native bool uses `floor(v+1e-4)` | [bin] |
| `a % b`, b=0 | 0 | 0 | 0 | 0 | 0 | 0 | [bin] |
| `%` formula | no +1e-4 | **with** +1e-4 | **with** | no | no | floor form | [bin] |
| `a ^ b` | pow / sign branches | + `b==0.5` √ | same | same | `b==2` first; √ float on 6.03r7/6.01r1 only — 6.1.1.3 and Mac 6.11r1 keep √ double | partial | [bin] |
| shifts | **mod 64**, past 31 → 0/−1 | same PPC | **mod 32** x86 | mod 32 | mod 32 | — | [bin] |
| number == | ±1e-4 | same | same | same | same | same | [bin] |
| string == | bytes (3.153 note) | — | — | — | — | **ignore case** | [bin] |
| value stack | **256** | 10000 | 10000 | 10000 | none | none (grow 100) | [bin] |
| call depth | 10000 | 10000 | >9999 frames → overrun | same | 10000 | 10000 | [bin] |
| loop | 10000 | 10000 | 10000 | +`maxlooplimit` 100–1e6 | field default 10000 | 10000 (generation) | [bin] |
| 2D clock | — | 0.05 / pass | 0.05 | 0.05 | 0.05 **lab** on 6.03r7; image 0.05 not found on 6.00 | interval or realtime | [bin][lab] |

### Linux 6.03r7 timer lab

Loopback only. Stock Linux 6.03r7 client; Seihai-compiled GS2 `setTimer` / `onTimeout`
bytecode (and GS1 `timeout=` lowered to the same delivery path) on a lab gserver.
Rate from on-screen counters between fixed wall marks. **[lab]**

| T (s) | Observed rate (/s) | Matches |
| --- | --- | --- |
| 0.01 | ~20 | fires (not classic floor-drop) |
| 0.02 | ~20 | fires |
| 0.05 | ~20 | 20 |
| 0.07 | ~10 | 10 |
| 0.1 | ~10 | 10 |
| 0.15 | ~6.5 | ~6.67 |
| 0.5 | ~2 | 2 |
| 1.0 | ~1 | 1 |

**Verdict:** rate ≈ `1 / (ceil(T / 0.05) * 0.05)` with a minimum of one 50 ms step.
Sub-0.05 values fire at ~20/s. GS1 `timeout=` lowered by Seihai matched GS2
`setTimer` on this path. Classic GS1 floor (drop `T < 0.05`) must not be applied
blindly to this 6.x client. **[lab]**

Earlier cadence work on 3.x / 4.x / 5.00r7:
[update-cadence-3x-6x.md](update-cadence-3x-6x.md);
[../live-runs/open-issues-2026-11-14/README.md](../live-runs/open-issues-2026-11-14/README.md#2a-gs1-timeout-sweep-offline-engines).

---

## 7. Name resolution and call quirks

| Topic | Stock read (4.2) | Notes | Tag |
| --- | --- | --- | --- |
| Reserved | `temp`, `params`, `this`, `thiso`, `player`, `playero`, `level`, `client` / `clientr` / `serverr`, `join` / `leave` on thiso | `$` special in the 3.153 note; **not** special in the 4.2 resolver that was opened | [bin] |
| Lookup order | with → active frame child → thiso **property only** → level → universe (+ create) → fallback `playero` | Differs slightly from the 3.153 account | [bin] |
| Failed call | slot ← 0; optional `Function … not found` | — | [bin] |
| `adventure.*` | refused unless the variable name starts with `login` | — | [bin] |
| Joined classes | OR event masks; instruction walk concatenates | The earlier current-script-only description was incomplete for the separately retained older input: its program lookup recurses through joins. Two later selected inputs also reach joined function tables through their own ordinary-call routes; cross-build/runtime and collision limits remain [in the follow-up](gs2-joined-function-lookup-2026-11-22.md) | [bin][inf] |

---

## 8. Server side vs client VM

| Topic | Server path (own words) | Client | Tag |
| --- | --- | --- | --- |
| Role | Compile source → bytecode; NPC timers in **1/20 s frames**; queue `onTimeout` when the countdown hits 0 | Run bytecode; 50 ms script clock on the 2D / 6.03r7 lab | [srv][doc][lab] |
| `timeout` property | `(int)(t*20)` frames; 0 = off | Host `setTimer` / property bridge | [srv][doc] |
| GS1 vs GS2 engines | Separate GS1 visitor / GS2 manager; sleep resumes via TIMEOUT | One GS2 machine | [srv] |
| Delivery | NPC / weapon / class bytecode to clients | Loader §4 | [srv][bin] |

Server quirks that **do not** change client opcode tables can still change era pass
rates when worlds expect missing option keys or similar — track those separately
from this VM table.

Reference rows: [gs2-vm-loader-diff.md](gs2-vm-loader-diff.md#reference-implementations).

---

## 9. Clean-room / reproduction gaps (observations)

Neutral observations against stock behaviour. Prefer this table over filing product
issues unless the owner asks.

| Gap | Where | Vs stock | Severity for era scripts | Tag |
| --- | --- | --- | --- | --- |
| No emit of 45 / 46 / 47 slot cache | seihai-core compiler | Official 6.113-era bodies use heavily | Low for correctness; high for parity / perf | [cap][doc] |
| Numbers compare exact; string case TBD | seihai executor | Stock ±1e-4; Android strings ignore case | Medium for equality-heavy scripts | [doc][bin] |
| `waitfor` incomplete on older notes; reproduction has a path | clean-room / repro | 4.20r8+ clients | Medium for scripts using waitfor | [doc] |
| Reproduction profile gates opcodes | client-repro loader | Must match the folder's real client | High if the wrong profile is used | [doc] |
| Event casing matrix unfinished | all | Corpora contain `onTimeOut` | High **if** any stock path is case-exact | [lab][inf] |

---

## 10. Compile pass rates vs runtime bites

World / weapon corpus surveys grade **compilers** (strict vs legacy, GS1 lowering).
They do not change a client's opcode set, slot rule or clock. Mode-split counts stay
in those notes:
[../npc-library/gs2-weapon-corpus-2026-11-14.md](../npc-library/gs2-weapon-corpus-2026-11-14.md),
[../npc-library/gs2-world-corpus-2026-11-12.md](../npc-library/gs2-world-corpus-2026-11-12.md),
[../npc-library/gs2-strict-probes-2026-11-13.md](../npc-library/gs2-strict-probes-2026-11-13.md).
**[lab]**

| Aggregate signal | Likely cause class | VM row that can also bite **after** compile |
| --- | --- | --- |
| Strict mode below legacy on GS2 tiers | Strict rejects legacy constructs | — |
| GS1 strict ≈ legacy | Lowering table, not strictness | Server / client command coverage |
| Top GS1 breakers (`putexplosion`, `puthorse`, …) | No GS2 lowering | N/A to the opcode matrix |
| Event casing splits (`onTimeOut`, …) | Source spelling | **§5** — runtime miss if lookup is exact |
| GS1-only hard tiers | Pre-GS2 / mixed | Out of GS2 VM scope |

**Era-specific runtime (not a compile %):**

- A world on **5.x** may rely on ops **48 / 49** → break on **6.x** clients. **[bin]**
- A **3.153-era** mind stack **256** and no waitfor / fusion. **[bin]**
- PowerPC Mac 4.20r6 shift / mod rules ≠ Windows 4.20r8. **[bin]**
- 6.x timer ceil ≠ classic GS1 floor. **[lab]**

---

## 11. Still open

- [ ] Fuller Android Classic / Era GS2 static findings → replace interim Android cells (§2 / §5 / §6).
- [x] ~~Full spelling × client matrix~~ [static matrix for the four focus builds](#focus-build-matrix-g087-2026-11-25) done 2026-11-25: case-insensitive everywhere, with two 4.20r8 prefix exceptions. Runtime on 4.20r8, 5.12 and Windows 6.037: [lab 2026-11-25](#runtime-check-g087-2026-11-25), which refutes exception 2 for `scheduleevent` and exception 1 on 6.037. Earlier: [Selected static event-handler comparisons](gs2-event-handler-case-2026-11-22.md) are followed; Linux ASCII matching is bound, while Windows helper state and other builds remain qualified.
- [x] ~~Full semantics of 48, 49, 54; `waitfor` timeout-expiry return value on 4.20r8.~~ Static semantics settled earlier; the lab run of 2026-11-25 confirms at runtime on 4.20r8, 5.12 and Windows 6.037 that `waitfor(obj, event, 1)` returns 0 after 1.0 s with no event and 1 as soon as the event comes (0.3–0.4 s in the test), and that the caught event's own `on…` handler then does not run ([runtime check](gs2-joined-function-lookup-2026-11-22.md#runtime-check-on-512-windows-6037-and-420r8-g090-2026-11-25)). **[lab]**
- [ ] 4.04r2 / mid-5.x / 6.00r2 clock step confirmation where still partial; Unity 7.x VM.
- [x] Cross-build/runtime joined-class function visibility; [three selected ordinary-call lookup chains](gs2-joined-function-lookup-2026-11-22.md) are statically followed, and [collisions and join modes](gs2-joined-function-lookup-2026-11-22.md#collisions-and-join-modes-on-the-focus-builds-g090-2026-11-25) are read on the four focus builds (2026-11-25). Runtime confirmation and cyclic joins: [lab 2026-11-25](gs2-joined-function-lookup-2026-11-22.md#runtime-check-on-512-windows-6037-and-420r8-g090-2026-11-25). 6.03r7 leave, class list and join rights: [static + lab](gs2-joined-function-lookup-2026-11-22.md#603r7-rights-check-leave-and-the-class-list-g090-2026-11-25).
- [ ] Further world-scan aggregates → refresh §10 only.

Also tracked with grades in [gs2-vm-loader-diff.md](gs2-vm-loader-diff.md#still-open)
and App. E#209.

---

## Related notes

- [gs2-vm-by-version.md](gs2-vm-by-version.md)
- [gs2-vm-from-engines.md](gs2-vm-from-engines.md)
- [gs2-vm-loader-diff.md](gs2-vm-loader-diff.md)
- [gs2-6113.md](gs2-6113.md)
- [linux-420r6-selector11.md](linux-420r6-selector11.md)
- [../protocol/gs2-client-vm.md](../protocol/gs2-client-vm.md)
- [../protocol/gs2-client-only-opcodes.md](../protocol/gs2-client-only-opcodes.md)
- [../protocol/gs2-android-classic-18.md](../protocol/gs2-android-classic-18.md)
- [../protocol/gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md)
- [../npc-library/gs2-weapon-corpus-2026-11-14.md](../npc-library/gs2-weapon-corpus-2026-11-14.md)
