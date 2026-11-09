# Evidence handling and agent handoff

Follow [AGENTS.md](../AGENTS.md) at the repository root. This directory contains
reviewed, curated public plain-behaviour summaries. Raw research inputs and
private retrieval records remain outside the repository.

## Source classes

- `[bin]`: a static artifact observation. This does not establish execution.
- `[cap]`: a recorded runtime observation, limited to its hooks and capture window.
- `[lab]`: lab configuration or verification, not a client feature claim.
- `[inf]`: an inference that still needs a confirming experiment.

Raw decompiles, memory images, reconstructed binaries, addresses, disassembler
names, real service hosts, credentials, private filenames and full artifact
digests stay out of the public handoff. The source index lists only public
source identifiers, platform and evidence kind; it cannot retrieve or
independently authenticate owner-held artifacts.

## Distribution boundary

Graal_analysis holds decompile-derived plain-behaviour findings. Do not copy
these findings, tables, code or source material into the clean-room Rust repos.
Those repositories may link to notes here; their implementation work follows
their own protocol documents, captures and tests. This index does not certify
a clean-room separation by itself.

## Reuse checklist

- [ ] Keep claims tied to the scope and limitations actually documented in the public note.
- [ ] Keep inferred mechanics separate from directly captured behaviour.
- [ ] Redact private identifiers, filenames, paths, hosts, addresses, and raw-code details before publication.
- [ ] Preserve public source identifiers and untested conditions in downstream notes; retain exact source identity privately.

No new lab is authorized by this index. Follow the repository's lab-location and
network rules, and obtain any explicit owner authorization that a new experiment requires.
