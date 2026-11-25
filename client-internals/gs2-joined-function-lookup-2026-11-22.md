# Joined functions in selected ordinary-call paths

Date: 2026-11-22. Static source, selected instructions and bounded data reads; no native client execution. **[bin]**

The earlier [engine reading](gs2-vm-from-engines.md) left ordinary joined-class function visibility open after following a current-script lookup. Event masks, event-name scans and concatenated top-level instructions do not by themselves answer that question. The paths below follow ordinary function calls separately. **[bin][inf]**

## Inputs and meaning of the result

The three audited inputs are a separately retained 4.20r8-labelled Windows input, a selected archive-labelled Windows 5.00r7 backup and the exact recorded Linux 6.03r7 x64 executable. Archive labels do not authenticate a vendor release; the Linux carrier matches its static export but not independently every historical lab executable. Findings stay with those selected inputs. Owner-held evidence: GS2-JOIN-FUNCTION-20261122 in the [evidence index](../docs/evidence-index.tsv). **[bin][inf]**

Here a plain-name call means the selected ordinary-call route uses a name without choosing a named class in the program helper's separate qualified-name branch. The older program-entry path and later current-object paths must remain distinct. These are statically followed lookup mechanisms, not a recovered source compiler grammar or expression-evaluation order. Lookup modes and execution checks differ across the paths below. **[bin]**

## Separately retained older input

The 4.20r8-labelled input's numeric call opcode is independently linked to its own handler and call helper. Its plain string-name route calls lookup on the machine's selected program with the permissive mode. The selected same-owner explicit-object route uses that path too; a different object's script program is looked up with the stricter mode. This returns an integer instruction entry, rather than the function objects used in the later paths below. **[bin]**

The program lookup normalizes the name and searches its own function table. An own match is accepted in the permissive mode; the stricter mode requires the stored entry flag. A missing or rejected match proceeds through the joined-program list from its first entry upward. The same lookup is called recursively on each child, with the same mode. On success it adjusts the child's integer entry by the surrounding own and preceding joined instruction counts. The first accepted match is returned. **[bin]**

The selected class-attachment path appends deduplicated class references to that joined list. Function registration stores a normalized name, entry and flag. Thus recursion reaches actual joined function entries; this is not just an event-mask change or an inference from top-level instruction walking. The locally active instruction piece must not be equated with the complete lookup scope. **[bin][inf]**

This lookup also has a separately bound `::`-qualified branch. That byte literal and the VM branch do not recover the complete source grammar. This older ordinary-call path is not evidence of a receiver-linked-function-variable stage, the later function-object convention or every cross-object visibility rule. **[bin][inf]**

## Selected Windows backup

The ordinary call path resolves the name against the current object. Its scripted-function lookup first considers linked function variables on that object. A permitted linked entry can satisfy the call before program-table fallback. This is not merely a lookup of the instruction piece currently being executed. **[bin]**

On fallback, the program lookup checks its own function table, then visits the joined-program list in ascending list order. Each child is searched recursively with the same name; the first nonnull result is returned. The selected function-table comparisons ignore case. This supplies a concrete route from an ordinary current-object call to a joined function, independently of event delivery. **[bin]**

Joining also has a separate preparation layer. A selected attachment path appends a class and invalidates instruction caches. Its update path transfers function links into owner variables: joined function tables are visited in reverse list order, followed by the main program's own functions. Later linking can replace a previous selected target in the same owner slot. Some join modes gate update work, so immediate transfer after every join is not established. **[bin]**

The alias-building pass and the recursive lookup must remain distinct. The latter is own-table-first, then ascending recursive joins; the former performs reverse-join writes followed by own-function writes. Object-variable lookup, case variants, existing variables, virtual creation and compatibility gates are not exhaustively covered. These traversals do not establish one unconditional collision policy for all such cases. **[bin][inf]**

After a function is found, the ordinary call path applies a separate visibility condition based on whether the receiver is the current object. It selects same-context or cross-object execution as applicable. Missing or ineligible lookup can enter other paths, including class-download handling; it is not universally an immediate zero result or proof that the function does not exist. **[bin]**

## Exact recorded Linux input

The numeric call opcode is independently bound through this executable's handler table to its own call helper. The selected string-name route obtains the current receiver, calls that receiver's scripted-function lookup and checks eligibility before selecting frame entry or cross-object execution. This connection comes from the ordinary-call handler, not an event-function scan or a similar Windows layout. **[bin]**

The receiver lookup checks its linked-variable hash first, follows selected link wrappers and applies compatibility checks. Its fallback obtains the receiver context's program and calls the program-name lookup. On the branch without the separately bound `::` selector, the program checks its own function table first. On a miss it recursively visits the joined-program list in ascending list order and returns the first nonnull result. Function registration ties the returned objects to their owning program and entry; the constructor exposes the recursive list as `joinedclasses`. This read does not follow Linux class attachment or function-alias transfer, so the backup's preparation sequence must not be assigned to Linux. **[bin]**

Thus joined-program functions are reachable through this selected plain-name ordinary call path too. This does not transfer the backup's case policy, alias-construction order or every receiver behavior to Linux. The qualified-name branch and its separator do not establish all source syntax or overload rules. Nor does a successful table lookup bypass the subsequent call's visibility and execution gates. **[bin][inf]**

## Remaining boundary

For these three selected inputs, joined functions participate in ordinary-call lookup, beyond event masks and top-level instruction walking. The earlier current-script-only observation was incomplete for the separately traced older program lookup, as well as insufficient to describe the later receiver-based paths. This correction stays with the selected inputs, not every executable carrying those version labels. **[bin][inf]**

This does not establish authenticated behavior for every version, all join/update modes, arbitrary cyclic join graphs, recursion limits, collisions, custom receivers, host/native fallbacks or actual runtime delivery. It supplies no compiler or VM implementation port. The broader cross-build question remains partial. **[bin][inf]**

## Collisions and join modes on the focus builds (G090, 2026-11-25)

Static read of the stock 4.20r8, 5.00r7, 5.12 and Windows 6.03r7 engines; nothing run. **[bin]** unless marked.

**Inputs.** The stock 5.00r7 engine read here is very likely the same file as the "archive-labelled backup" above: every retained backup copy is byte-identical to it, and the findings above all match. No other 5.00r7 engine was found to compare against. **[inf]**

### Same function name in the object and a joined class

| Call kind | Who runs | Builds |
| --- | --- | --- |
| Ordinary call | one function: the object's own first, then the first-joined class (including that class's own joins, depth first), then the next class | 4.20r8, 5.00r7, 5.12, 6.03r7 |
| Ordinary event (`timeout`, `playerchats`, …) | **one** handler, chosen in the same order | read directly on 4.20r8, 5.00r7 and Windows 6.03r7; 5.12 inferred from its identical join code |
| `onCreated`, `onInitialized` (and `onInitFrame` from 5.00r7) | **every** matching handler, once each: the object's own first, then the classes in join order | same |

4.20r8 and 5.00r7 repeat the created/initialized pass until nothing new turns up, so a class joined inside `onCreated` also gets its own `onCreated` in the same pass. In 4.20r8, two functions in one script whose names differ only in letter case collapse to one, and the later definition wins (names are stored lower-cased; see [G087](gs2-vm-quirks-by-version.md#focus-build-matrix-g087-2026-11-25)).

### Join modes

| Build | Ways to join | Effect |
| --- | --- | --- |
| 4.20r8 | `join()`, a "simple" join, and replacing the whole class list | Adds the class at once; a repeat join is ignored. Functions are looked up fresh on each call, so an already-loaded class is callable immediately. An unknown class is joined as an empty placeholder, requested from the server, and its functions appear when it arrives. Leaving takes effect at the next event dispatch. No permission check. |
| 5.00r7, 5.12 | `join()` with a "simple" flag (class-list joins use the simple form) | Both modes create the placeholder (requesting it if needed) and ignore repeats. A permission check requires the class's level not to exceed the object's; on failure nothing is joined and nothing is logged. Only a non-simple (script) join updates the object's stored function links at once; a simple join is reachable through the normal lookup but its links wait for a later update. 5.12's join code is instruction-for-instruction the same as 5.00r7's. |
| 6.03r7 | as 5.x | As 5.x, and `join()` also requires the caller's level to be at least the target object's. A failed check logs `Object doesn't have rights to join class …`. Deferred leaving and the class-list path were not traced. |

Still open after the static read: runtime confirmation, cyclic join graphs and recursion limits, and 6.03r7's leave/class-list paths. The first three are answered by the lab run below; 6.03r7's leave/class-list paths and its join-rights check remain open.

## Runtime check on 5.12, Windows 6.037 and 4.20r8 (G090, 2026-11-25)

Loopback Wine lab, the lab server's own GS2 compile, results read from the client's own chat. On 5.12 and 6.037 the test weapon came from the server (197/140); on 4.20r8 it was injected as 33 + 132, because the lab server sends 4.20r8 a `//#GS2` weapon as source text in 33, which does not run (as on [5.00r7](../protocol/scripted-weapons-5x-status.md#lab-gs2-weapon-fixture-on-500r7-g307-2026-11-25)). Classes were injected as answers to 161: 133 on 5.12 and 4.20r8, 197 + 140 on 6.037. Rows `gs2rt512-*`, `gs2rt6037-*` and `gs2rt420-*` in [probe-results.tsv](../protocol/probe-results.tsv). **[lab]**

| Check | 5.12 | 6.037 | 4.20r8 |
| --- | --- | --- | --- |
| Object and joined class both define `foo()`: an ordinary call runs the object's | yes | yes | yes |
| Two joined classes define `bar()`, the object none: the first-joined class's runs | yes | yes | yes |
| Object and class both define `onTimeout`: one handler, the object's | yes | yes | yes |
| Object and class both define `onCreated`, class already loaded at the join: the object's runs to the end, then the class's | yes | yes | yes |
| Cyclic join (`cC` joins `cD` in its `onCreated`, `cD` joins `cC`) | no hang; each `onCreated` once | same | same |
| A function calling itself 10 000 deep | "Callstack overrun" logged; that statement is dropped, later events still run | overrun logged; the deepest call returns nothing, so the result is 9999 | as 6.037 |

Not predicted by the static read:

- When the class body arrives after the `join()` (the client had to ask 161), the class's `onCreated` never runs, and the script waits: the weapon stayed silent until the class arrived, then ran its overdue scheduled event at once. With 161 unanswered it never ran.
- `join()` of an already-loaded class from a later event (not from `onCreated`) does not run the class's `onCreated`.
- The 6.03r7 join-rights check was not tested.

