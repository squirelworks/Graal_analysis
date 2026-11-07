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
  *Done in #152.*

- [x] **2. Leak scrub.** One PR per kind: (a) #154 `.pyc`; (b) #153 `FUN_` names;
  (c) #156 IPs/LAN/personal machines; (d) #157 official hostnames; follow-up #158
  loopback dotted literals → plain words / `<loopback>`. Guest password untouched.
  *Done when* the four leak greps in `AGENTS.md` return nothing (third line: review
  hits by eye).

- [x] **3. CI for the checks.** `.github/workflows/checks.yml`: four AGENTS.md leak
  greps (fail on any hit; IP grep has no loopback whitelist), `pytest tools/lab-servers`,
  smoke `resolve.py` + synthetic GR-V1 `grv1-decoder`. Fail-demo branch
  `cursor/ci-leak-checks-fail-demo-b5fd` proved the IP step red.
  *Done in #159.*

- [ ] **4. pyReborn study into the repo.** Needs Squirrel's `pyreborn-vs-seihai.md` and
  `parser-probe-main.rs` (project files). Add as `client-internals/pyreborn-study/`
  with the MIT note; keep `file:line` citations; drop pasted pyReborn code.
  *Blocked until Squirrel provides the files.* Tracked in #244 (on hold).

- [x] **5. Graal3D collision as plain behaviour (unblocks `seihai-g3d` G3D-1).**
  Per-face step test in `graal3d/collision.md` with tags: radius 5, step height 30,
  slope (ny > 0 / attach > 0.2), wall distances 3 / −5, probe order. Static PE float
  read of `Graal3D.exe` (no decompile on Drive; no C committed). Wine lab still needs
  native `d3drm.dll` for live confirmation.
  *Done in #164.*

- [x] **6. Graal3D camera (unblocks G3D-2).** Follow distance 220, look height +80,
  turn ±5°/tick, pitch −0.15 rad, follow rule **[bin]** (`graal3d/camera.md`, #163).
  Field of view is the Direct3DRM initial field **0.5**: a square window from −0.5
  to 0.5 on the front plane at distance 1, opening `2×atan(0.5)` ≈ 53.13° on either
  axis. No field constant in the client PE **[bin]**; the value is the library
  default **[doc]** (SDK `SetField` / `SetFront` remarks, and Wine's native-matching
  `d3drm` viewport test). The degree figure is arithmetic on that plane **[inf]**.
  Live confirmation of the follow numbers still needs native `d3drm.dll`.
  The far plane stays open (`graal3d/camera.md`): library initial back plane 100
  **[doc]**, a later DelphiX fork calls `SetBack(5000)`, and the February 2000
  exe was not re-read for `SetBack`.
  *FOV pinned in `graal3d/camera.md`.*

- [x] **7. NPC-Control protocol note (unblocks `seihai-rc` stage 5).** Write
  `protocol/npc-control.md` from `tools/remotecontrol.md`, Squirrel's `npccontrol`
  material and a loopback NC run against the GServer-v2 lab.
  *Done in #155.*

- [x] **8. `#n` in `setcharprop` (server brief A3.6).** What original servers did with
  `#n` in a `setcharprop` value, from lab evidence (GServer13 1999 under Wine on
  loopback, and the 2.05 client). Add to `npc-library/gs1-reference-205.md` or a short
  `server-notes/` note.
  *Answer in `server-notes/setcharprop-hash-n.md` (#160): value `#n` → action player's
  nick **[srv]**; GServer13 has no `setcharprop` **[bin]**; live GServer-v2+2.05 lab
  still open.*

- [ ] **9. Damage and file-transfer open points (loopback captures).** Partial close
  without new Wine (#165): strike + link for bomb/arrow/baddy powers
  (`damage-sources.md`), CURPOWER + respawn + default-weapon partial
  (`lab-captures-2026-10-25`), GWEBL001/`PLO_LEVELMODTIME`
  (`formats/gwebl001-cache.md`), save folders 1.39/2.00 + empty-stream guard (batch k),
  pre-2.1 settled-name no re-check (batch e `01-request-lists`). Static read of 2.05 rev 2
  and 2.22 (`decomp-findings-2026-10-25-e/04-name-index-case-link.md`): file-index order
  (newer file in 2.22, first hit in 2.05), plain A–Z case fold, and packet 40's link
  (a horse does not change it). **Still open:** full vs empty login default checks
  (the set, and whether they share a frame); maps folder in 2.1–2.16 (the client
  archive still has no build between the 2.1 test builds and 2.22). Tracked in #245.

- [x] **10. Long handler layouts per build.** PLAYERPROPS (9), OTHERPLPROPS (8),
  NPCPROPS (3) and LEVELLINK (1) for 2.00, 2.04, 2.05 rev 2, 2.17.1, 2.22 and 2.31,
  plus UDP ids 0/15/22 for 2.00–2.04 and gen-3 insertion for 2.01–2.04.
  Tables: `version-profiles/plo-*-layouts.tsv`, `udp-ids-200-204.tsv`,
  `gen3-insertion-200-205.tsv`. Open questions 1, 3, 4 in batch-c `10-…` struck.
  *Done in #162.* (2.04 / 2.01–2.03 `.c` not on Drive; those rows are endpoint +
  batch-c bracketed.)

- [ ] **11. 1998 to 1.41 rules (matrix unknown #1).** Death, hurt and knockback, sword
  reach and the wall test for 1.39 first, then 1.32 and ~~1st Graal~~. Decompiles plus Wine
  runs against GServer13 or the 1998 relay on loopback.
  *1.39 done in #161 / `version-profiles/matrix/rules-139.md`. 1st Graal done in
  `version-profiles/matrix/rules-1st-graal.md` (static read of the VCL-lossy export;
  the death-counter increment is not tagged). 1.32 remains: the Decompile folder
  was listed again on 2026-11-01 (client exports and Accessories) and still has
  no 1.32 export, so no death, hurt or wall number was added.* Tracked in #246 (on hold).

- [ ] **12. Keep Seihai's fixture reader working.** Any PR that edits
  `version-profiles/*.toml` or `client-internals/version-profiles/*.toml` runs Seihai's
  `tools/gen_profile_fixture.py` against the edited file. Do not commit the generated
  fixture to `seihai` from here.

- [ ] **13. Deferred: a capture of a real 5.x/6.x `Login` session** (matrix unknown #3).
  On hold. Do not connect. Tracked by GitHub issue #247. The decision stays open.
  `protocol/login-session-known.md` records what a Login server is already known to
  send and which steps are still unobserved. Resume only in this order, the same
  order as #247: (1) the owner comments yes or no on #247; (2) if yes, write the
  capture plan before any connection; (3) redact per `AGENTS.md` and write the note;
  (4) tick this task. Public servers stay off until that written yes is on the issue.
  - [x] Owner-supplied capture, 2026-11-07, port 14900, Windows 6.113.
    The clear hello is `GNP1905C`; the bytes after it are ciphertext, so the
    Login server's packet ids stay unobserved.
    `protocol/v6113-list-capture.md`. The parent item stays open.
  - [x] Full capture, 2026-11-07, 15236 frames. TCP 14900 is present.
    Three completed sessions start with `GNP1905C`; one SYN is unanswered.
    No UDP datagram to those remotes, and no UDP on 14900, 14901 or 14899.
    `protocol/v6113-udp.md`. The parent item stays open.

- [x] **14. Graal Technical Reference Manual: the 15-PR work plan.** Spec: issue #191.
  All fifteen PRs merged; `manual/` is on main with the checker, the carry check and
  the three-OS PDF build. TRM 0.0.3 (347 pages) and 0.0.4 (377 pages) are published.

- [ ] **15. TRM roadmap to 1.0.0.** The checklist is in issue #191 ("Roadmap to
  1.0.0"): 0.0.5 coverage proof (`tools/manual/coverage.py` and one prose PR per
  Part) is next, then 0.0.6 implementability, 0.0.7 triage of the unknowns, 0.0.8
  release quality, 1.0.0 sign-off (Squirrel's call). Tick the items in #191 as PRs land.

- [ ] **16. Torque study and the 3.04 plan. On hold, no target release** (Squirrel,
  2026-11-05). The study and plan are merged (#242, stage checklist #250):
  `torque/study-torque-clients.md`, `torque/rebuild-plan-3.04.md`. Follow-ups wait in
  #243 (stage 0 reference captures of the real 3.04, the TGE 1.x licence check, Part X).
  The rebuild is graal-delphi's (squirelworks/graal-delphi#109); its stage 1 script VM is
  parked there in `common/torque/`. Do not start on it unless Squirrel lifts the hold.
  - [x] Read the 3.04 Linux engine (2026-11-07): `torque/engine-304.md`.
    Stock TGE stays in the binary; Graal's game is `GuiGraalCtrl`. The hold
    on writing the module stands.
  - [x] Unpacked Windows 6.00r2 and 6.00r4 (static read): no Torque 3D subsystem.
    `GuiGraal3DCtrl` is a GUI type beside `GuiGraalCtrl`. Torque field names and
    `GuiTilesCtrl` are absent from these two images.
    `client-internals/engine-600r2.md`, `client-internals/engine-600r4.md`.
    The rebuild stays on hold.
  - [x] Read the skipped packed listings (2026-11-07). The two v4 exe
    listings are one Thinstall loader. Packed 5.12 still names its Delphi
    forms. `fmod.dll` is the UPX export list. Packed 6.037 and 6.113 export
    a `QPlay.exe` TLS surface and not Torque.
    `torque/skipped-v4-read.md`, `torque/skipped-v5-read.md`,
    `client-internals/skipped-v6-read.md`. The hold stands.
  - [x] Unpacked Windows 4.2.0.8, static read (2026-11-07). The launcher
    draws by host slots until a 3D start replaces them. `GraalEngine.dll`
    runs the session and has no `SimObject` console. `GameObject` in
    `Graal3DEngine.dll` is a `SceneObject`. `torque/4208-launcher.md`,
    `torque/4208-engine.md`, `torque/4208-g3d.md`. The hold stands.
  - [x] Read 5.0.0.7 for behaviour (2026-11-07): the launcher session,
    `TAdventure` and the script space, and the 3D mission, terrain and
    protocol-24 check. `torque/5007-launcher.md`, `torque/5007-engine.md`,
    `torque/5007-g3d.md`. The hold on writing the module stands.

- [ ] **17. v6 own-engine reading.** The 6.x clients are Graal's engine. This pass
  is the June 2011 Windows exports and two packed exes. A readable engine for
  the packed 6.037 and 6.113 executables is still open.
  - [x] Unpacked 6.00r2 and 6.00r4 are `quattro_lib`: OpenGL drawing, a GS2
    shell, `TServer*` world objects and `TSocket`. Packed 6.037 and 6.113
    decompile as packer stubs. `client-internals/engine-600r2.md`,
    `engine-600r4.md`, `packed-6037.md`, `packed-6113.md`.
  - [x] The packed 6.037 and 6.113 listings were read past the stub
    (2026-11-07). The export directory is named `QPlay.exe` and lists
    CyaSSL, zlib and ciphers; the bytes at those exports are not the
    library, and the engine is still not in these two files.
    `client-internals/skipped-v6-read.md`. Item 17 stays open.
  - [x] GS2 container, opcodes, and weapon/class load for 4.2.0.8,
    5.0.0.7, and unpacked 6.00r2 and 6.00r4.
    `protocol/gs2-client-vm.md`. Item 17 stays open.
  - [x] Effects of the GS2 opcodes the client VM accepts and the
    Preagonal compiler does not emit, including folds 200–242.
    `protocol/gs2-client-only-opcodes.md`. Item 17 stays open.
  - [x] Windows 6.1.1.3 re-read after the 2026-11-07 gap archive.
    The archive is the existing cleaned notes, not an unpacked image.
    The executable is still the `QPlay.exe` stub: one `KERNEL32` import,
    CyaSSL and zlib export names, no login, no GS2 switch, no Torque class.
    Neighbour diff against unpacked 6.00: `client-internals/engine-6113.md`,
    `protocol/v6113-wire.md`, `protocol/gs2-6113.md`. Issho is not
    implemented. Item 17 stays open.
  - [x] Read the 6.1.1.3 decompile itself (2026-11-07). The listing is
    106 functions. Three are the entry (clear a breakpoint byte, mix four
    kilobytes, breakpoint). The other 103 are export names whose bodies
    do not implement the CyaSSL or zlib calls, and the file has no GS2
    switch, GUI class or socket import.
    `client-internals/decompile-6113.md`. Item 17 stays open.
  - [x] Unpacked Windows 6.037 (static read, 2026-11-07). The listing
    is the `quattro_lib` engine: a code section, `TSocket`, and a GS2
    switch with cases 54, 121 and 200–242 and without 48 or 49.
    `GuiTilesCtrl` is constructed. `GuiGraal3DCtrl` is not a string.
    The packed 6.037 shell is unchanged. `client-internals/unpacked-6037.md`.
    Item 17 stays open.
  - [x] Static read for the 6.x repro checks (2026-11-07). The setprotocol
    header is filled `T`, then `I`, then `E`, then `L`. Ids 93 and 163 on
    the 6.1.1.3 generation-5 path send id 50 first. `onToall` takes a
    player and a text. The bind method's name was not found; the events
    are `onBind` and `onBindFailed`. `protocol/v6-repro-facts.md`.
    Item 17 stays open.
  - [x] Version resources on the skipped packer stubs (2026-11-07):
    `torque/skipped-version-stamps.md`. The two v4 exe uploads are one
    decompile, file version 4.0.4.2. The hold on writing the module stands.
    Manual §10.1.13.

## Handoff

The project moves to Cursor on 2026-11-07. Graal_analysis work there continues
from this list and #191 (TRM 0.0.5 is next). Start with graal-delphi's
`HANDOFF-CURSOR.md` (state of both repos, rules, on-hold work, open decisions),
then this file and `AGENTS.md`.
