# Agent rules for Graal_analysis

Owner: Squirrel (GitHub `squirelworks`). Merges and tags: Chiaki only. Agents open
PRs; they never merge, never push to `main`, never create a tag or release.

## No real servers, no binary addresses

- **No real server IPs, ports or hostnames** (public Graal servers, the official
  listserver and login hosts, anyone's LAN machines) in notes, TOML/TSV tables, logs,
  scripts or screenshots. Use the loopback address, a second loopback address (fake
  outside interface), the lab ports (14802, 14803, 14804, 14900, 14921–14923), or
  placeholders `<listserver-host>`, `<login-host>`, `<public-host>`, `<lan-host>`.
  When a historical host matters, describe it ("the 1999 list host, same as 1.39's")
  rather than naming it. Do not write dotted IP literals anywhere in the repo.
- **No binary addresses**: no code or data addresses, RVAs or file offsets (`0x4dab…`, `004…`; see `tools/leak-check/`), no Ghidra/IDA names (`FUN_…`,
  `DAT_…`, `LAB_…`), no decompiled C. Findings are written as plain behaviour with a
  source tag (`[2.05]`, `[bin]`, `[lab]`, `[cap]`, `[srv]`, `[doc]`, `[inf]`).
- The repo is **public**. Treat every commit as published.

## Labs

- **Cloud loopback only**: servers you start yourself on the loopback address (or a
  second loopback address as a fake outside interface), in a container, VM or CI runner.
- **Never use Squirrel's own machines** (their Linux PC, Windows PC, Mac) for labs,
  captures or builds.
- **No public servers** (no logins, no listserver registration, no captures against
  them) without Squirrel's explicit OK in writing.
- Never run old Graal tools from the archives outside a sandbox: `ListServer.exe` and
  several clients phone home. Wine + Xvfb in a container or a qemu guest is fine.
- Every lab note records: client + version, server + commit, what was done, before,
  after, and log/pcap file names (redacted per the host/IP rules above).

## Decompile and pyReborn material stays here

- `Graal_analysis` is the **only** repo where decompile-derived findings, pyReborn
  study notes, GPL server notes and the reference decoders/scripts live.
- **Never copy any of it into the clean-room Rust repos** (`seihai`, `seihai-gserver`,
  `seihai-listserver`, `seihai-rc`, `seihai-npcserver`, `seihai-servertools`): not text,
  not tables, not code, not the Python decoders. Those repos may *link* to a note here;
  their code is written from their own protocol docs, lab captures and tests.
- Raw decompiles (Ghidra `.c`/`.xml`/`.html`, `.idc`, `.gzf`) never enter any repo.
- Working papers stay private and owner-held; there is no `workingpapers/` folder in this repo. Publish reviewed findings as ordinary topical notes (`version-profiles/`, `client-internals/`, `protocol/`, `formats/`, `torque/`, `npc-library/`) with their evidence limits. Never publish owner-side paths, raw artifact names, package/member names, full artifact digests, private availability/status fields, lab-status handoffs or retrieval instructions. Cite owner-held evidence by public ID in `docs/evidence-index.tsv`, which may contain only the non-sensitive ID, platform and evidence kind.
  Squirrel holds them (Drive / project files). If a task needs one, ask Squirrel for
  it and commit only the plain-behaviour result.
- pyReborn (`hosler/pyReborn`, `reborn-protocol`, `pygserver`) is MIT: summarise and
  cite (`file:line`), do not paste code. Its "reversed official client" citations are
  hints only; confirm against our own decompile notes or a lab run.
- GPL patches for the lab servers (`tools/lab-servers/*.patch`) stay here and in the
  GPL fork (`seihai-gserver-v2`, `seihai-gs2lib`), nowhere else.

## Git and PRs

- **Verify merge state before you start any task**: `git fetch origin main`, check that
  dependency PRs are merged and that no open PR already covers the task. If a PR you
  depend on is still open, do not stack on it; take the next task.
- One change per branch and PR. Commit message: short summary, then why, then what
  evidence (lab run, static read, or "none").
- Before pushing, run the leak checks below on your diff. A PR that adds a host,
  address or `FUN_` name is not ready.
- Add the new note to `README.md`'s contents list in the same PR, and close the item in
  the matching open-points file (tick its `- [ ]` box, strike it and link the new note).
  Every incremental fix or open-point list is a GitHub task list (`- [ ]` / `- [x]`),
  including `docs/NEXT.md` and issue bodies.
- **Stop and ask Squirrel** (leave the task, go to the next) where a task says
  "Squirrel decides".
- Leave the built-in guest password as it is on `main`. Do not redact it again.

## Leak checks (run from repo root before push)

```
git ls-files | grep -E '\.pyc$'
python tools/leak-check/check_addresses.py
git grep -nE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' | grep -vE '\b[0-9]\.[0-9]+\.[0-9]+\.[0-9]+\b'
git grep -niE 'graalonline\.com|graal\.in\b|graalreborn\.(com|net)'
```

(The third line skips version strings like `2.2.2.0`; review its hits by eye.)

## Task list

See `docs/NEXT.md` for the ordered open work, issue #191 for the manual's roadmap
to 1.0.0, and graal-delphi's `HANDOFF-CURSOR.md` for the state of both repos.

## Cursor Cloud specific instructions

Python 3.12 is already on the image. The environment install adds pytest for the login user (`python3 -m pip install --user pytest`). That is the only package `.github/workflows/checks.yml` installs. `python3 -m pytest` is the command to use; the `pytest` script also lands on `~/.local/bin`, which login shells already include.

From the repo root:

- `python3 -m pytest tools/lab-servers -q` starts the lab listserver, drives every login shape, and stops it. That test has to be the only gserver connected, so do not leave another listserver or gserver bound to the lab ports.
- Smoke `client-internals/version-profiles/resolve.py` on a profile TOML, and `formats/grv1-decoder/grv1.py` on a level, the same way the workflow does. Both use the standard library only.

Do not start archived Graal clients or Wine here. Those clients phone home, and the client archives are not in this checkout. Lab servers stay on the loopback address.

## macOS builds

GitHub CI runs the `leak-and-smoke` and `manual` checks on Linux, Windows and macOS 15 (hosted `macos-15` runners). The manual PDF is built on Linux and Windows only. The lab's Sequoia VM is for reproducing a macOS failure by hand.
