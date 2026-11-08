# Evidence handling and agent handoff

Follow [AGENTS.md](../AGENTS.md) at the repository root. The research collection is split
into owner-held raw workingpapers and these public plain-behaviour notes.

## Source classes

- `[bin]`: a static artifact observation. This does not establish execution.
- `[cap]`: a recorded runtime observation, limited to its hooks and capture window.
- `[lab]`: lab configuration or verification, not a client feature claim.
- `[inf]`: an inference that still needs a confirming experiment.

Raw decompiles, memory images, reconstructed binaries, addresses and disassembler
names stay in the owner's project files. Game-server hosts and credentials do
not enter the public handoff. The source index contains digests and retrieval
locations, not the raw artifacts themselves.

## Distribution boundary

Graal_analysis holds decompile-derived plain-behaviour findings. Do not copy
these findings, tables, code or source material into the clean-room Rust repos.
Those repositories may link to notes here; their implementation work follows
their own protocol documents, captures and tests. This index does not certify
a clean-room separation by itself.

## Reuse checklist

- [ ] Retrieve the referenced source by its identifier and verify its SHA-256 digest.
- [ ] Check its client build, platform, fixture and original capture scope.
- [ ] Keep inferred mechanics separate from directly captured behaviour.
- [ ] Record client/version, server/commit or none, action, before/after and redacted evidence filenames.
- [ ] Review hosts, addresses, disassembler names and raw-code exclusions before a PR.
- [ ] Preserve the source identifier and any untested conditions in downstream notes.

No new lab is authorized by this index. Follow the repository's lab-location and
network rules, and obtain any explicit owner authorization that a new experiment requires.
