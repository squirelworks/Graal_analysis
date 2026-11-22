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
