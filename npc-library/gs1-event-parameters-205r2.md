# GS1 event parameters and #p in exact 2.05r2

Evidence GS1-EVENT-PARAMS-205R2-20261109-01. Researcher-verified executable SHA-256: b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08. This record traces the parameter producer, queue, dispatch wrapper, splitter, and message consumer using original-matching recovered bodies and selected fresh original instructions. That static record makes no runtime claim; the separately identified original-client controls below add bounded observations. Neither record generalizes to later profiles.

## Producer and consumer linkage

`#p(index)` reads the same shared string list that the event-dispatch wrapper clears and fills from the actor's pending parameter text. The wrapper uses comma as the separator. The index expression is expanded and evaluated numerically, converted through the ordinary integer helper, and checked against list length; an out-of-range or negative index yields empty text. `paramscount` reads this list's count.

This list is separate from `#t(index)` and `tokenscount`: tokenize/tokenize2 clear and fill the token list, while event dispatch fills the parameter list. A tokenize call alone therefore does not establish or replace event parameters.

## Queue ownership and overwrite rules

Each actor has a pending event-name list but only one pending parameter-text field shared by those events. An accepted queue request adds its event name and replaces that text field. It does not store a separate payload alongside each event.

A name already present in the pending list is rejected without changing parameter text. An action-prefixed name is also rejected when any action-prefixed name is already pending. For a newly accepted action event, the queue records its supplied source context as well. Exact list lookup case rules are not newly traced here.

Consequently a second accepted distinct event can overwrite the parameters that an earlier pending event will later observe. A rejected duplicate cannot. This is a queue-level static result; precise frame scheduling determines whether two script requests reach the same pending batch.

## Commands and local delivery

`callnpc` resolves its caller-relative NPC selector and queues the expanded event string through the no-parameter wrapper. `callweapon` resolves its zero-based weapon index, centers its script actor on the player, and queues the expanded event string through that same wrapper. Neither command splits comma text inside its event string into parameters. Their wrapper supplies empty parameter text; accepting such an event can overwrite previously pending text with empty text.

`triggeraction` supplies an action name and a distinct parameter-text argument. Its local path prefixes the name with action, tests the trigger point against eligible level NPCs, and queues that name together with the parameter text. Weapon delivery has its own local-player proximity/source gate. The connected send path is additional behavior, not needed for an offline parameter fixture. Queue delivery is not direct synchronous execution of the receiving script.

A bounded local test can use an owned receiver with a visible character body and an action handler that displays `#p(0)`, `#p(1)`, and `paramscount`. An owned sender triggers a point within that body using synthetic action name lab and parameter text alpha,beta. Under a fresh receiving dispatch, the expected splitter result is two entries, alpha and beta. Fixture grammar, targeting, queue batching, and visible output must still be validated by the coordinating runtime pass. A separate callnpc control should use a known receiver selector and a simple event name; adding commas to that event name does not turn them into parameters.

## Splitting grammar

The splitter repeatedly processes the remaining byte string. An unquoted token ends at its first comma. If the remaining string starts with a double quote, that opening quote is removed and the token ends at the next double quote instead; commas inside that token are ordinary characters. Token text is trimmed at both ends using bytes below 33. The remainder after the delimiter is likewise trimmed before the next iteration.

Unquoted empty fields are skipped; a quoted empty field is retained. Thus alpha,,beta yields two entries, while a quoted empty entry can contribute an empty string to the list. A trailing comma does not create a final empty entry. An opening quote without a closing quote consumes the rest as one quoted token. This helper contains no escape-sequence decoding or backslash-aware quote search. Text after a closing quote is processed as the next remainder; it is not required to begin with a comma. These are splitter mechanics, separate from the script parser's own quoting rules used to construct the parameter text.

## Lifetime and nested context

At dispatch entry, a nonnull player context causes the shared parameter list to be cleared and rebuilt from the actor's pending text. A null-player early exit does not rebuild it. Normal end cleanup conditionally clears the actor's pending event list, text, and action source; the condition's global control meaning remains unresolved here.

That cleanup does not itself clear the shared parameter list. It can therefore continue to contain the current or last dispatched context until another dispatch rebuilds it. A nested dispatch wrapper saves and restores actor pending fields, but no corresponding snapshot and restoration of the shared parameter list is visible in that wrapper. Implementations should not assume #p is an immutable per-event snapshot or permanently owned by its NPC. Full reentrant scheduling and script continuation behavior remain separate questions.

This closes the narrow producer linkage for #p while leaving broader message-expansion questions and event scheduling limits explicit. No packet, public-server, or later-version behavior is inferred from this local chain.

## New end-to-end original-client controls

[2.05][lab] GS1-PARAM-RUNTIME-205R2-20261109-04 adds four owned offline runs. A sender waits through a requested positive sleep before triggering a point inside a character NPC receiver. An initial two-NPC control displays count2 and alpha,beta through #p0/#p1. This validates the local producer-to-consumer chain independently of network delivery. Later multi-receiver controls exercise the splitter and pending-event rules. The companion runtime-observations.json retains each stimulus, result and readable run.

[lab] Parameter text alpha,beta gives two entries. Alpha,,beta with a trailing comma still gives two. A quoted empty field between alpha and beta gives three entries with an empty middle entry. Alpha followed by a quoted beta,gamma and then delta gives three entries, keeping the comma in the middle value. A quote in the middle of an unquoted token does not protect its comma: alpha,b"c,d",omega gives four entries alpha, b"c, d", omega. These are accepted script stimuli and resulting parameters; they do not qualify all script-level quoting or RFC CSV behavior.

[lab] One receiver is first queued an action with alpha,beta, then a distinct callnpc probe before it dispatches. Both handler markers show count0. This corroborates an actor-shared pending payload overwritten by an accepted no-parameter call. Separate controls queue a second different action-prefixed name, or repeat the same action name, before dispatch. Both retain the first parameter value; the second distinct-action handler does not replace the primary result. The queue trace supplies the general rejection rule; these runtime cases do not prove every name-comparison or frame-scheduling policy.

[lab] A continuation control saves the received count2/alpha/beta into an independent string, requests sleep0.2, and then displays count0 with empty #p entries after resume. This is an observed parameter-lifetime boundary for that normal local fixture, not evidence for an immutable coroutine payload. It does not isolate whether cleanup or a subsequent event overwrite is the decisive step, measure elapsed timing, or prove behavior under arbitrary nested dispatch.

[lab] The first multi-receiver layout had overlapping long quoted-parameter labels. Their values are taken from a single-column repeat. The ordinary-empty-field result is read from the earlier clear layout because the sender's SENT text overlays that position in the repeat. No absent or obscured label is classified as zero/empty. Producer completion, receiver handler markers and counts distinguish non-delivery from accepted empty parameters.

[lab] All four runs use the exact unchanged original Windows2.05r2 executable under Wine with private virtual displays and isolated user/PID/network namespaces. No server is used. Target files are completed with explicitly labeled2.31 donor assets and owned synthetic levels, not an authentic complete original2.05 distribution. Every supervisor exits0 and cleanup completes. Original screenshots, raw functions, queue/wrapper instruction windows and exact fixture/harness identities remain private. No live pending-field or AST memory was inspected.

The narrow #p producer linkage is now established for this exact build. Preserve broader E#203 residual field/scanner/formatter/renderer tasks. General reentrant global-context restoration, every event category, every source context, precise scheduling, network action acceptance, and other profiles remain open. The observed callnpc result is not a callweapon runtime test; the latter shares the no-parameter wrapper in the static trace.

Evidence retrieval: static and runtime identifiers are indexed in [workingpapers/sources.tsv](../workingpapers/sources.tsv). Digests, executable identity and observations are researcher supplied; the editor matched four sanitized handoff file digests without inspecting private evidence or the binary.
