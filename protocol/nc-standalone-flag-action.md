# Standalone NPC Control: one flag-list action's outgoing path

Evidence: **[bin]** bounded static examination of one retained standalone Windows
NPC Control artifact with a flag-list form. Private proof is owner-held under
`NC-FLAG-ACTION-STATIC` in the [evidence index](../docs/evidence-index.tsv).
This is an artifact-specific result, not a protocol definition for every 2001
build or a runtime observation.

## What this adds

The existing [2001–2002 chronology](../server-notes/original-server-builds-1999-2007.md#npc-control-and-remotecontrol-20012002-bin)
already records the earlier flag-list form and its replacement by a weapons
list. It does not establish what every flag-list action sends. The later
[NC layouts](npc-control.md) are scoped to examined 2002/2004 clients; their
NPC-flag operations must not be assigned to this earlier form by analogy.

For one selected action in the examined flag-list form, the recovered static
path constructs a collection payload and passes it to an outgoing buffer
builder. It is therefore more than local presentation **[bin]**.

## Bounded observations

- The action obtains a collection count, represents it as two seven-bit groups
  biased by 32, and iterates that collection **[bin]**.
- It adds each item's length in a biased byte representation and the item's
  contents to the constructed payload **[bin]**. The collection's precise UI
  type and treatment of out-of-range lengths remain unresolved.
- It passes command value **69** and that payload to a direct callee **[bin]**.
  This is the caller's command argument, not an independently captured wire id.
- The callee biases the command byte by 32, concatenates the message parts,
  appends them to a shared object's buffer, and invokes a further routine when
  the combined or buffered length reaches 4096 **[bin]**. That further routine
  and the literal terminator were not examined in this bounded turn.

The construction supports an outgoing-message path. It does **not** establish
the ultimate socket peer, successful delivery, receive-side processing, or the
meaning of the collection on the server. The existing server-source association
of commands 68/69 with server flags is related coverage, not proof that this
artifact uses the same recipient and field semantics.

## Recovery method and limits

The form's event-name candidate was checked against coherent named method
records, an executable PE section and an exact address-to-file mapping. Default
Ghidra analysis did not recognize the selected entry as a procedure. An exact
file-offset selector did not create that missing boundary.

A self-authored bounded headless script in a new private project explicitly
seeded **one entry and one direct callee**. Disassembly and decompilation then
completed for the inferred bodies, without executing the artifact. These are
**analyst-seeded boundaries**, not default REA recognition. Exception-handling
tails outside those bodies, register/type interpretations and indirect calls
remain uncertain. The [Delphi internal-format reference](https://docwiki.embarcadero.com/RADStudio/Florence/en/Internal_Data_Formats_(Delphi))
is guidance only; a modern layout description does not prove this older
artifact's compiler layout. Private records retain the entry derivation,
inferred ranges, scripts, commands, output and launcher limitations.

## Open questions

- [ ] Resolve the collection's UI/type binding and range behavior.
- [ ] Trace the buffer's further routine, terminator and ultimate socket peer.
- [ ] Establish the corresponding receive-side interpretation.
- [ ] Compare the selected path with the nearest known weapons-list baseline
      and the other distinct flag-list artifact; matching forms alone do not
      establish matching code or payloads.

No production implementation or original-client fidelity claim follows from
these observations alone.
