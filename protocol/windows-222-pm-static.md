# Windows 2.22 control: selected PM paths

## Scope and evidence

[bin] This read covers one identified, modified community Windows 2.22 control,
not an authenticated pristine release. Owner-held evidence
`WIN222-PM-STATIC-20261115` binds the input identity, Delphi named-method records,
initialized executable ranges, selected linear disassembly and receive tables.
The input identity was checked before and after reading. Nothing was executed.
No result is transferred to 2.17.1, 2.31 or another 2.22-labelled image.

[bin] Named-method records anchor the player-list Message action and a message
window's button handlers. Selected direct calls and conditional branches were
read from those entries. Linear decoding is not whole-program recovery:
adjacent inline strings, exception cleanup and truncated slice edges are not
treated as instructions on the selected path.

## Message action and send intent

[bin] The player-list Message action walks list entries, tests their selection
state and collects nonzero recipient identifiers. It prefixes the collected
identifier string with its count in two base-128 digits, each increased by 32.
It compares the resulting recipient representation with existing message
windows, reuses a match, or constructs a window and supplies that representation.
This is a composer route; it does not establish a remote-roster request.

[bin] A named button handler in that window checks the compose-state flag,
obtains text, requires nonempty text and a present connection object, then
concatenates the recipient representation and text. Its direct callee decodes
the count, treats each recipient identifier as two bytes, and reaches a virtual
send call with numeric type 28 and the combined payload. This establishes send
intent at that call boundary. The virtual target, framing, transport delivery
and native visible result were not established by this read.

## Receive dispatch and sender lookup

[bin] The selected receive dispatcher subtracts 32 from the first message byte,
separates the remaining body, bounds the numeric type at 186 and uses an index
table followed by a destination table. Types 55, 56 and 82 all select the same
default cleanup destination as an out-of-range type. This independently
corroborates their omission from the earlier
[handled-ID inventory](../version-profiles/plo-handled-ids-by-build.tsv) for this
control. It does not prove absence from every receive path or every 2.x build.

[bin] Type 37 selects a distinct body. It requires at least two body bytes,
decodes the sender identifier as two base-128 digits offset by 32, removes those
two bytes and searches the existing player collection for a matching identifier.
If no player matches, this handler reaches cleanup without constructing a new
player. A matching player enters message processing: optional quoted-prefix
handling, per-player state updates, an existing message helper and a player-list
update call. The full text-format semantics and visible notification behavior
remain unverified.

## Remaining questions

- [x] ~~Locate the exact control's action, if any, that requests a remote PM roster;~~ none exists in the original 2.22; the roster is filled by 8 ([sixth batch](../client-internals/static-reads-appendix-e-2026-11-20-f.md#no-roster-request));
  follow the actual request builder and its caller rather than assuming the
  later `requestlist` / `pmserverplayers` mechanism.
- [x] ~~Recover the accepted reply and player-creation route for that request, if~~ 8 creates unknown players ([sixth batch](../client-internals/static-reads-appendix-e-2026-11-20-f.md#no-roster-request));
  present. The selected dispatcher gives no handler for 55, 56 or 82.
- [ ] Resolve the virtual type-28 send target and framing separately from send
  intent, and establish the final message display behavior.
- [ ] Corroborate separately against identified 2.17.1 and 2.31 inputs. Shared UI
  method names and historical version labels do not establish shared code.

[inf] These findings constrain the compatibility question: a type-37 reply in
this handler needs an already-known sender identity. They do not supply an
implementation contract for remote identity creation or justify enabling a
modern roster exchange for 2.x.
