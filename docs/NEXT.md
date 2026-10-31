# Next work (ordered)

One change per branch and PR. Verify `origin/main` and the open PR list before
starting; do not stack on unmerged PRs. Skip items that say "Squirrel decides" or
that need missing Squirrel-only files; take the next task. Binding rules live in
`AGENTS.md` and `.cursor/rules/graal-analysis.mdc`.

Done-checks also require: leak check clean, `README.md` contents updated, matching
open-point closed.

## Tasks

- [x] **1. Repo rules and task list.** Add `AGENTS.md`, `.cursor/rules/graal-analysis.mdc`,
  and this file. Fix the README opening line to match its Boundary section
  ("no raw decompiles, code or binary addresses").
  *Done in this PR; strike after merge to `main`.*

- [x] **2. Leak scrub.** One PR per kind: (a) #154 `.pyc`; (b) #153 `FUN_` names;
  (c) #156 IPs/LAN/personal machines; (d) #157 official hostnames; follow-up #158
  loopback dotted literals → plain words / `<loopback>`. Guest password untouched.
  *Done when* the four leak greps in `AGENTS.md` return nothing (third line: review
  hits by eye).

- [x] **3. CI for the checks.** `.github/workflows/checks.yml`: four AGENTS.md leak
  greps (fail on any hit; IP grep has no loopback whitelist), `pytest tools/lab-servers`,
  smoke `resolve.py` + synthetic GR-V1 `grv1-decoder`. Fail-demo branch
  `cursor/ci-leak-checks-fail-demo-b5fd` proved the IP step red.
  *Done in this PR; strike after merge to `main`.*

- [ ] **4. pyReborn study into the repo.** Needs Squirrel's `pyreborn-vs-seihai.md` and
  `parser-probe-main.rs` (project files). Add as `client-internals/pyreborn-study/`
  with the MIT note; keep `file:line` citations; drop pasted pyReborn code.
  *Blocked until Squirrel provides the files.*

- [ ] **5. Graal3D collision as plain behaviour (unblocks `seihai-g3d` G3D-1).**
  Per-face step test into `graal3d/collision.md` with tags. Static read needs the
  decompile from Squirrel; confirm with a loopback Wine run where possible.
  *Blocked until Squirrel provides the Graal3D decompile (unless lab-only path works).*

- [ ] **6. Graal3D camera (unblocks G3D-2).** Camera height, look point, field of view
  and follow rule into `graal3d/camera.md`. Needs decompile and/or lab confirmation.

- [x] **7. NPC-Control protocol note (unblocks `seihai-rc` stage 5).** Write
  `protocol/npc-control.md` from `tools/remotecontrol.md`, Squirrel's `npccontrol`
  material and a loopback NC run against the GServer-v2 lab.
  *Done in #155.*

- [x] **8. `#n` in `setcharprop` (server brief A3.6).** What original servers did with
  `#n` in a `setcharprop` value, from lab evidence (GServer13 1999 under Wine on
  loopback, and the 2.05 client). Add to `npc-library/gs1-reference-205.md` or a short
  `server-notes/` note.
  *Answer in `server-notes/setcharprop-hash-n.md`: value `#n` → action player's nick
  **[srv]**; GServer13 has no `setcharprop` **[bin]**; live GServer-v2+2.05 lab still open.*

- [ ] **9. Damage and file-transfer open points (loopback captures).** Partial close
  without new Wine (this PR): strike + link for bomb/arrow/baddy powers
  (`damage-sources.md`), CURPOWER + respawn + default-weapon partial
  (`lab-captures-2026-10-25`), GWEBL001/`PLO_LEVELMODTIME`
  (`formats/gwebl001-cache.md`), save folders 1.39/2.00 + empty-stream guard (batch k),
  pre-2.1 settled-name no re-check (batch e `01-request-lists`). **Still need Wine:**
  packet 40 owner/parent field; full vs empty login default checks; file-index scan
  order; case-folding ASCII; maps folder in 2.1–2.16 (no binary).

- [x] **10. Long handler layouts per build.** PLAYERPROPS (9), OTHERPLPROPS (8),
  NPCPROPS (3) and LEVELLINK (1) for 2.00, 2.04, 2.05 rev 2, 2.17.1, 2.22 and 2.31,
  plus UDP ids 0/15/22 for 2.00–2.04 and gen-3 insertion for 2.01–2.04.
  Tables: `version-profiles/plo-*-layouts.tsv`, `udp-ids-200-204.tsv`,
  `gen3-insertion-200-205.tsv`. Open questions 1, 3, 4 in batch-c `10-…` struck.
  (2.04 / 2.01–2.03 `.c` not on Drive; those rows are endpoint + batch-c bracketed.)

- [ ] **11. 1998 to 1.41 rules (matrix unknown #1).** Death, hurt and knockback, sword
  reach and the wall test for 1.39 first, then 1.32 and 1st Graal. Decompiles plus Wine
  runs against GServer13 or the 1998 relay on loopback.
  *1.39 done in `version-profiles/matrix/rules-139.md` (this PR); 1.32 and 1st Graal remain.*

- [ ] **12. Keep Seihai's fixture reader working.** Any PR that edits
  `version-profiles/*.toml` or `client-internals/version-profiles/*.toml` runs Seihai's
  `tools/gen_profile_fixture.py` against the edited file. Do not commit the generated
  fixture to `seihai` from here.

- [ ] **13. Later, Squirrel decides:** a capture of a real 5.x/6.x `Login` session to
  fill matrix unknown #3. Ask before planning; public servers are off-limits without
  Squirrel's OK.
