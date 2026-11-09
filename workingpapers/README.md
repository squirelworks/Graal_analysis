# Platform workingpapers

Research handoff collected on 2026-11-08, with the completed Windows extraction
indexed on 2026-11-09. These notes separate static findings,
captured behaviour and lab preparation. They are not a claim that every client
or platform has been run successfully.

- [macOS](macos/README.md): its own teardown folder, with architecture findings
  and the separate Tiger and Lion preparation states.
- [Windows](windows/README.md): completed code-recovery inventory, original-carrier
  3D provenance, startup capture and controlled offline transition.
- [Linux](linux/README.md): completed engine teardown, function-recovery coverage,
  scripting catalogs and bounded runtime observations.
- [Exact 2.05r2 object members](../npc-library/gs1-object-members-205r2.md): compiled bindings and qualified offline controls.
- [Exact 2.05r2 message expansion](../npc-library/gs1-message-codes-205r2.md): static catalog and qualified original-client controls.
- [Original 2.05r2 condition truth](../npc-library/gs1-condition-truth-205r2.md): finite computed truth, condition-name parsing and constant-comparison folding.
- [Evidence sources](sources.tsv): stable source identifiers, original project
  file locations and SHA-256 digests for retrieval from the owner's project files.
- [Handling and handoff](handling.md): source boundaries and requirements for later agents.

Raw project files remain with the owner. The local `workingpapers/catalog.json`
indexes the full private collection; it is not included here because its raw
contents and filenames can contain material prohibited by this repository.
The source identifiers in these notes refer to the narrower index above.

No client, server, debugger or VM was started or controlled while preparing this
handoff. These notes summarize existing records. Each observation keeps the
scope of the earlier run that produced it.
