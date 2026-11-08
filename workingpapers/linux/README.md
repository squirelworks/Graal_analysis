# Linux teardown workingpapers

The owner-held Linux collection includes input verification, extracted-installer
records, static dependency preflights and bounded debugger/launch results. Use the
individual result records to decide whether a particular client experiment passed.

`[lab]` Source `LINUX-VERIFY` records verification of 564 input files and five
extracted installer files, plus debugger smoke checks for both Intel word sizes.
Those checks concern harmless test programs; they do not establish that every
archived client launches or that its graphics work. This handoff launched no client
or server; server and server commit for the tooling checks are none.

`[bin]` Source `LINUX-PREFLIGHT` indexes archived 3.04, 4.04r2, 4.20r6, 4.20r8,
6.01r1 and 6.03r7 variants. The two indexed 3.04 inputs have the same SHA-256
digest despite their different folder labels. Static dependencies and strings
remain preflight observations, not proof that those subsystems execute.

- [ ] Read the matching individual launch/debug result before claiming a client runs.
- [ ] Separate missing dependencies, compatibility failures and successful startup.
- [ ] Preserve exact input and fixture identities for a future bounded behaviour test.

See [the source index](../sources.tsv). Raw debugger text, address-bearing reports
and extracted executables remain in the owner's private workingpapers.
