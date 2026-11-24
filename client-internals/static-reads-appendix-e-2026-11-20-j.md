# Static reads for Appendix E, eleventh batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (the existing decompiler output of the Linux 6.03r7 x64
client, a decompiler read of the Linux 6.01r1 x64 client on the lab host A, and a byte search of
the unpacked Windows 6.00r2, 6.00r4 and 6.03r7 executables; no client run). Only behaviour is given
here. Covers three of the open items of App. E#209.

## The 6.x loop-limit name

6.x keeps many short names scrambled and unscrambles them at run time, one byte at a time, with a
rule that depends on the string's length and the byte's position (`v6x` findings). With that rule:

- 6.00r2, 6.00r4, 6.01r1 and 6.03r7 each hold one 12-byte scrambled string that unscrambles to
  `ma?looplimit`. Eleven bytes follow the rule. The third byte does not: under the rule, an `x`
  would have to be stored as a zero byte, which would end the string, so a different byte is stored
  there.
- No other scrambled or plain string in these builds contains `looplimit`.

So the 6.x property is still `maxlooplimit`. This matches the 2026-11-19 script fuzz run, where
setting `maxlooplimit` on 6.03r7 changed the limit (`protocol/script-fuzz-2026-11-19.md`).

## Event names and the function table (6.03r7)

When the client fires an event on a script, it looks the event name up in that script's function
table:

- The hash of the name folds `A` to `Z` to lower case before mixing each byte.
- The comparison between the name and a table entry also folds `A` to `Z`.

So the lookup does not depend on letter case. `onTimeout`, `onTimeOut` and `ontimeout` find the
same function. The global builtin registry uses the same hash, and its comparison also folds case (it unscrambles a stored scrambled name byte by byte as it compares).

## How a server trigger reaches a weapon (6.03r7)

`PLO_TRIGGERACTION` (48) carries a two-character id, coordinates and then an action text.

1. The action text is split at its first comma into an action and the rest.
2. If the action is exactly `clientside` (lower case, compared with case), the rest is split again
   at its first comma into a weapon name and the parameters.
3. The client makes a pending trigger with that weapon name, the event name `actionclientside`
   and the parameters, and adds it to the player's pending list. If more than 100 are pending, the
   oldest are dropped.
4. The pending list is checked when a trigger is added, and from one other, larger player routine that was not followed. A trigger is handed to a weapon of the player
   whose name is exactly equal (compared with case) and that is ready. It is then removed. A
   trigger for a weapon the client does not have yet waits.
5. The weapon fires the event `actionclientside` with the parameters.

On the sending side, a script `triggeraction` whose target is exactly `serverside` or `servernpc`
goes to the server instead of to a local object.

Because event lookup ignores case (above), a weapon function written `onActionClientSide` handles
the event, in any letter case. The `on` prefix is how scripts name every event; the code that adds
it before the lookup was not followed here.

## Not covered

- The other unread VM builds of E#209: Mac 4.04r2, Mac 5.12, the December 2006 Mac 4.20r6, 6.015,
  6.034, Android Era and Classic other than 1.8. Mac 6.004 and 6.015 installers are held on the
  lab host A.
- Where the `on` prefix is added, and whether the function table that scripts call through uses the
  same lookup as event firing.
- The other E#209 checklist items (the Linux 4.20r6 fusion re-read, the 5.00r7 event-queue cap on a
  stock image). Maths on 6.1.1.3 and Mac 6.11r1 is settled for the power/square-root rule in
  [static-reads-appendix-e-2026-11-24-g082.md](static-reads-appendix-e-2026-11-24-g082.md).
