# Planned experiments (2026-11-20)

These are the lab runs that were planned when the Claude threads stopped on 2026-11-20, written so
that Cursor, Codex or a person can run them without the threads' context. Part 1 is the queued
experiments, each with its goal, VM and client, steps, expected output, where the result goes and
the issue it closes. Part 2 lists every other lab row on the [gap board](gap-board.md) by VM.

## Rules for every run

- **VMs only.** Run nothing on bare metal. Each host runs one lab at a time, so check what is
  running before you boot. On lab host A a watchdog powers VMs off when the host's free memory
  falls under about 3 GB, so boot only one large VM there.
- **Loopback or VM-internal servers only.** The probe scripts run inside a `bwrap
  --unshare-net` namespace. Never point a client or a probe at a public server. Starting a public
  server needs Squirrel's written OK.
- **Nothing raw goes in a repository.** Captures, pcaps, screenshots, raw logs, client binaries and
  VM disks stay on the lab VM or in the private archive. Commit only derived tables and write-ups.
- **Write-up shape.** Put the result in a topical note (`protocol/`, `client-internals/`,
  `formats/`, `torque/`) and tag it `[lab]`. Record the client and version, the server and its
  commit, what was done, the before and after state, and the private log names. Probe results also
  go in `protocol/probe-results.tsv`. Tick the source box with a link to the note, tick the row in
  its issue, mark the row in `docs/gap-board.tsv`, and add the note to `INDEX.md` and
  `manual/sources.tsv`.
- **PRs.** Open one properly sized PR for each batch, and run `AGENTS.md`'s leak checks before
  pushing. Agents never merge or tag.
- **Harness.** `tools/probe/README.md` covers the harness. A run is
  `sh tools/probe/lab/<runner>.sh [CLIENT] PLAN RUN`, and its output goes to
  `~/probelab/out/RUN`. The lab inputs (client folders, the gserver build, the worlds and the Wine
  tree) are named in `~/probelab/lab.env` on the lab VM and are not in this repository.

## Part 1. Queued experiments

### Lab host B: Windows 10 VM, or Wine in the Linux lab VM (issue #743)

**X1. Probe coverage for 5.12, 6.037 and the 2.02 family.**
- **Goal:** close the probe holes found while building the board. 5.12 has only the 8-row 195
  gani set. 6.037 has 32 rows. 2.02, 2.02 rev 1 and 2.02 rev 2 have none. Board rows G424, G425,
  G426 and G191.
- **VM and client:**
  - 5.12 runs under Wine with `runwine.sh 512`.
  - 6.037 runs natively in the Win10 VM, with the proxy and `probectl.py` on a `tcp:PORT`
    control address (see the README's "Windows hosts").
  - The 2.02 builds run under Wine with `run12.sh`/`login1x.sh` for gen 3. Add a client entry for
    them as for 2.00 to 2.05 rev 1.
- **Steps:**
  - For 5.12 and 6.037, run each plan in turn: `wine-core`, `widths`, `widths-fix`, `bytes2x`,
    `baddytypes` and `loadgani3w`. For example:
    `sh tools/probe/lab/runwine.sh 512 tools/probe/lab/wine-core.plan x1-512-core`
  - For the 2.02 family, run the 32-case gen-3 plan from
    `python3 tools/probe/fuzz12.py plan 3`, the same set that 2.00 to 2.05 rev 1 ran.
- **Expected output:** one row per case in `probe-results.tsv`: `landed`, `lost`, `crash` or
  `disconnect`, read from the bomb-count canary (`canary.py`). Compare the results with 5.00r7,
  6.03r7 and 2.05 rev 1 respectively.
- **Record in:** `protocol/probe-results.tsv`, plus a short note beside
  `protocol/probe-native-linux-4x-2026-11-19.md`.
- **Closes:** G424, G425, G426 and G191 (#743).

**X2. Remote Control width canary on a readable window.**
- **Goal:** rc2004 and rc3 rendered black under Wine, so CAN01 to CAN06 are unknown, not failed.
  RC2 2.05 hits a GTK Pango font failure under Wine. Board rows G159, G160, G298 and G299.
- **VM and client:** the RC builds in the Linux VM. Use a Wine virtual desktop
  (`wine explorer /desktop=...`), or run RC2 2.05 natively with `RC_NATIVE=1`.
- **Steps:**
  - `sh tools/probe/lab/runrc.sh rc2004 tools/probe/lab/rc-widths.plan x2-rc2004`, then the
    same with `rc3` and `rc205`.
  - Score the run with `python3 tools/probe/rccanary.py` and `canary.py` over the nickname cell.
- **Expected output:** for each RC, CAN01 to CAN06 each marked `alive`, `silent`, `disconnect` or
  `gone`, plus the width each RC prop is read at.
- **Record in:** `protocol/rc-fuzz-2026-11-19.md` (lines 118 and 119) and `docs/NEXT.md` lines 76
  and 77.
- **Closes:** G159, G160 (#733), G298 and G299 (#733).

**X3. 4.04r2 pickup field read during each action (E#611).**
- **Goal:** settle what the pickup-bound field holds. The best guess is the carried object's kind.
- **Before the run:** do the static read first, as `404r2-carry-state` lines 57 and 58 describe
  (G025).
- **VM and client:** 4.04r2 under Wine (`runwine.sh 404`, prefix `wp4`), in the repeatable Wine
  scene.
- **Steps:** record the field before and after each pick-up, carry, throw and drop in the
  repeatable scene. Measure the simulation, animation and render clocks before converting any
  countdowns into time.
- **Expected output:** a table with one row per action, giving the field's value and the object.
- **Record in:** `client-internals/404r2-carry-state.md`, plus an answer to App. E#611.
- **Closes:** G025, G032 and G033 (#743).

**X4. Client test harness #398 on 4.20r8, 5.00r7, 5.12, 6.03r7 and 6.113.**
- **Goal:** the 1.x to 2.31 harness runs are in `live-runs/client-harness-2026-11-13`, and 5.00r7
  is only partly done. Board row G186.
- **VM:** the Win10 VM.
- **Steps:** follow `live-runs/client-harness-2026-11-13/README.md` for each build.
- **Expected output:** the same per-check table that the 1.x to 2.31 runs produced.
- **Closes:** G186 (#743).

**X5. 5.x throw capture and the GS2 weapon fixture.**
- **Goal:** confirm on the wire that id 11 is the throw (E#4 residual), and find which ask and body
  ids fire for a GS2 weapon on 5.00r7 and 5.12.
- **VM and client:** 5.00r7 and 5.12 under Wine (`runwine.sh 500`, `runwine.sh 512`).
- **Steps:** lift and throw an object while the proxy logs `C>S`. Then load a GS2 weapon fixture
  from the lab gserver and log each request id the client sends.
- **Expected output:** the throw packet's id and fields, and the list of ids sent for the weapon.
- **Record in:** `protocol/ids-sent-512-status.md` (line 30) and
  `protocol/scripted-weapons-5x-status.md` (line 37).
- **Closes:** G256 and G307 (#743).

**X6. `PLO_SHOOT2` with known gravity on 5.0.0.7.**
- **Steps:** inject `PLO_SHOOT2` with gravity values of 0, the default and twice the default,
  and take shots along the arc.
- **Expected output:** the arc's peak and range for each gravity value.
- **Record in:** `protocol/shoot-5007.md` (line 127).

**X7. The 2002 builds ver7 to ver13: ids 2, 4, 17, 18, 154 and 155, plus the v22 and 1.40 login
frames.**
- **Goal:** find out whether each build draws a baddy, a chest and a horse it is sent.
- **Steps:** use `run12.sh`, then inject each id with `probectl.py`. Capture the v22 and 1.40
  login frames on their own.
- **Expected output:** a table of build by id, marked drawn, ignored or crashed.
- **Record in:** `client-internals/graal2002-and-140-builds.md` (lines 297 and 298).
- **Closes:** G072 and G073 (#743).

**X8. The 6.03r7 product-id slot on Windows 10.**
- **Goal:** find out why the slot is empty. The likely cause is the 32-bit registry view.
- **Steps:** run 6.03r7 natively and compare `HKLM\SOFTWARE\WOW6432Node` with the 64-bit view.
- **Record in:** `protocol/pcid.md` (line 138).
- **Closes:** G286.

**X9. F-key windows on 2.05 rev 2 and 2.22, and 1.39 closing on F6.**
- **Steps:** edit the guest's hosts file as administrator so that the list host resolves to the
  loopback address. Then press F1 to F12 and record which window opens.
- **Record in:** `client-internals/gui-windows-fkeys.md` (lines 184 and 185).
- **Closes:** G095.

### Lab host B: Linux VM with the lab servers (issue #733)

**S1. Server fuzz on GServer 1.21.**
- **What to run:**
  - The gen-2 sweep again on a quiet host. The first run was invalid because host load caused
    false canary timeouts.
  - The unauthenticated id 8 on a single connection.
  - The post-login cases, with a `guest` account reset before each case.
- **Steps:** `lab/srv13.sh` / `lab/srvq13.sh` with `tools/srvfuzz/`. Use `lab/waitload.sh` with
  `LOAD_MAX=4`.
- **Record in:** `protocol/server-fuzz-c2s-targets.md` (lines 54, 107 and 109).

**S2. GServer 1.25 and 1.27.**
- **Steps:** log both lab clients and a player into each server. Then measure the player, NPC and
  baddy prop ranges.
- **Record in:** `client-internals/gserv-125-127-builds.md` (lines 128 and 132).
- **Closes:** G092.

**S3. The lab gserver's GR-V1.05 reader.**
- **Prerequisite:** the reader and malformed-link repairs already landed in
  [seihai-gserver-v2 #118](https://github.com/squirelworks/seihai-gserver-v2/pull/118).
  Use a build containing `eea7a0b2`; the [source audit](../formats/gr-v105-fuzz-2026-11-19.md#source-repair-reconciled-on-2026-11-21-srv)
  does not establish a live serve.
- **Steps:** serve a generated multi-layer level to 5.12 and 6.03r7 with that repaired build.
  Compare the loaded boards, delivered layers and drawn cells separately; retain a single-layer
  positive control and record the exact server commit. The earlier 5.24r4 repaint issue remains
  a separate qualification if that client is included.
- **Expected output:** a per-client result distinguishing file loading, layer delivery and drawing.
  G226 and the live portion of G227 remain open until that result is measured.
- **Record in:** `formats/gr-v105-fuzz-2026-11-19.md` and
  `formats/gr-v105-empty-tiles-2026-11-16.md`.

**S4. NC write operations.**
- **Steps:** run `runnc.sh 713` with fixtures for attribute, class and weapon writes through
  `ncprobe.py`.
- **Expected output:** the write layouts: property order, clear versus leave, and length prefixes.
- **Record in:** `protocol/nc-write-ops-status.md` (line 38).

**S5. The protocol-19 server order with a real 4.04r2 and 3.153.**
- **Steps:** run the GPL lab server (PR #78). The Mac 3.153 has passed the handshake against
  Seihai (seihai#577). Movement is still open,
  because the Tiger software renderer draws only the sky. Serve the sky textures as `.gif`, which
  the client asks for.
- **Record in:** `torque/protocol19-server.md` (lines 164 and 165).

### Lab host B: Tiger VM (issue #730)

**T1. Mac PowerPC receiver positive control.**
- **Steps:**
  - Send one valid raw frame.
  - Then send valid zlib members near each build's capacity boundary.
  - Then run the gmap height reader on a known-good map.
- **Record in:** `protocol/macos-ppc-receive-framing.md` (line 56),
  `protocol/macos-ppc-receive-decompression.md` (line 70), `formats/gmap-heights-mac-ppc.md`
  (line 90) and `docs/NEXT.md` (line 304).

### Lab host A: Lion or Sequoia VM (issue #731)

**L1. Mac 6.004 with its clock held before the beta limit (E#618).**
- **VM:** the Sequoia guest.
- **Note:** a full answer needs a macOS 10.9-era guest with OpenGL. None is held, and building one
  is Squirrel's call.

**L2. An unchanged Mac client run to its context helpers.**
- **Steps:** record the real arguments the helpers receive.
- **Record in:** `docs/NEXT.md` (line 302).

### Android-x86 or mobile (issue #732)

**A1. GS2 loop budget and event-queue limits in an Android runtime.**
- **Record in:** `docs/NEXT.md` (line 250).

### Seihai and repro lab checks (other repositories)

These close issues in the client and server reimplementations, not gap-board rows.

**R1. seihai#497, which is still untested on real clients.**
- **What to test:**
  - A player-to-player `PLO_TRIGGERACTION` (48) with a non-zero player id.
  - Everything 6.03r7 was checked for, run on 5.12: the script cache, `onMouseDown` with
    `mousex`/`mousey`, gmap re-entry and PLO 48 `clientside`.
- **Setup:** the issue's 2026-11-20 lab comments describe it: real Linux 6.03r7 against
  GServer-v2 seihai.4 or seihai.5, using a 3×1 gmap with an NPC that writes its state into player
  attributes.
- **Expected output:** the same tables as in those comments, filled in for the new cases.

**R2. seihai#461: why the real 4.20r6 leaves a downloaded PNG texture white.**
- **Setup:** use the same Rust gserver world as the 2026-11-20 comment (a 2×2×2 `.3ds` cube with
  one texture map).
- **Steps:** try the map as `.jpg`, try it in the shape's folder, and try other material chunks.
- **Note:** no Windows 3.153 exists. Linux 4.20r6 is the stand-in.
- **Expected output:** a real-client picture with the texture drawn, so that the shading and
  texture rows can be signed off.

**R3. graal-client-repro#430: 6.03r7.**
- **What to run:**
  - Capture an idle real 6.03r7 session long enough to see whether, and when, it sends PLI 24
    (keep-alive).
  - Run the #427 chat drawing and the login file requests side by side with the real client on
    the lab stack.
- **Note:** graal-client-repro#429, the RC4 connector cipher, is code work with a loopback test
  and not an experiment. Its steps are in that issue.

## Part 2. Every lab row on the board, by VM

Generated from `docs/gap-board.tsv`, rows of kind `lab` or `static+lab`. Each VM's issue carries
the same rows as a task list. Read the source line before you start.

### Win10 VM on lab host B or Linux VM (Wine) (#743, 73 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G004 | lab | Graal 2002 and 1.40 send sets and default routes (best guess: each build follows its token's neighbour; 1.40 and v22 logins captured) | `manual/app-e-open-questions.md` E#15 | Lab host B Appendix E batch thread |
| G007 | lab | The rest of the 2.05 # code set (best guess: #E is an empty placeholder (read); bare #5/#6 is a 2.17 scanner change) | `manual/app-e-open-questions.md` E#203 | Lab host B Appendix E batch thread |
| G010 | lab | Particle emitter and format details (best guess: %d truncates, indexof is case-sensitive) | `manual/app-e-open-questions.md` E#210 | Lab host B Appendix E batch thread |
| G012 | lab | Stopping positions and wire rounding (best guess: stopping measured; the wire value is truncated to the half tile) | `manual/app-e-open-questions.md` E#304 | Lab host B Appendix E batch thread |
| G015 | lab | Combat live checks still open (best guess: the spark appears only when a sword meets a sword or a shield) | `manual/app-e-open-questions.md` E#324 | Lab host B Appendix E batch thread |
| G016 | lab | Sound census and playback limits (best guess: none yet; needs a per-backend playback test) | `manual/app-e-open-questions.md` E#325 | Lab host B Appendix E batch thread |
| G024 | lab | 4.04r2 offline gameplay (best guess: it plays like 4.20r6 offline) | `manual/app-e-open-questions.md` E#610 | Lab host B Appendix E batch thread |
| G025 | lab | 4.04r2 pickup semantics (best guess: the bound field is the carried object's kind) | `manual/app-e-open-questions.md` E#611 | free |
| G032 | lab | Measure simulation, animation and rendering clocks before converting countdowns to time. | `client-internals/404r2-carry-state.md` line 59 | free |
| G033 | lab | Capture a complete scene and before/after state for each selected interaction. | `client-internals/404r2-carry-state.md` line 60 | free |
| G039 | lab | 1.21 live: 12 archer kills each gave +1 gralat in the frame of death and nothing else, which does not fit the | `client-internals/combat-baddy-tile-by-version.md` line 149 | free |
| G040 | lab | The sword spark live: not identified in 1.39 frames at about 28 a second (same run). | `client-internals/combat-baddy-tile-by-version.md` line 151 | free |
| G048 | lab | Id 24: the sender's own field formatting (the layout above is the receiver's); a capture of a real client whose weapon shows an image would settle it. The lab cannot do this yet because the real client did not run NPC scripts there. The per-player "UDP reaches this player" flag of the 2.22 test. Dra | `client-internals/decomp-findings-2026-10-25-g/04-open-points.md` line 5 | free |
| G051 | lab | Partly closed. Lab §E: id 7 → wbowi1.png settled; id 8 → wbomb1.png not isolated (bomb image is asked anyway). Also ids 12, 20–23 → named images. Same lab note [cap]. | `client-internals/decomp-findings-2026-10-25-k/03-open-points.md` line 7 | free |
| G052 | lab | Measure actual elapsed tick duration (cadence). | `client-internals/early-form-timers-2026-11-09.md` line 29 | free |
| G061 | lab | Observe original isolated startup, loaded modules and usable gameplay | `client-internals/engine-600r2.md` line 141 | free |
| G062 | lab | Measure elapsed death timing and updater cadence separately. | `client-internals/first-graal-death-counter-2026-11-09.md` line 20 | free |
| G072 | lab | Capture v22 and checked 1.40 login frames independently; no shared-token grade inheritance. | `client-internals/graal2002-and-140-builds.md` line 297 | free |
| G073 | lab | Lab check of ids 2, 4, 17, 18, 154 and 155 on ver7–ver13. Send a baddy, a chest and a horse, and see whether the client draws them. | `client-internals/graal2002-and-140-builds.md` line 298 | free |
| G092 | lab | Player, NPC and baddy prop ranges for 1.25 and 1.27 (the gserv-1999.md | `client-internals/gserv-125-127-builds.md` line 128 | free |
| G095 | lab | 2.05 rev2 and 2.22 live: both need their list host to resolve to the loopback address inside the Windows guest, which takes an administrator edit of the guest's hosts file. The clients are staged in the guest. | `client-internals/gui-windows-fkeys.md` line 184 | free |
| G150 | lab | The lab NPC message text not drawing on 5.24r4/6.03r7. | `client-internals/v5v6-expiry-and-black-screen.md` line 104 | free |
| G163 | lab | Complete the first player-properties discriminator; bounded no-later-chunk observations and a timer-confounded arm do not settle gate sufficiency. | `docs/NEXT.md` line 128 | free |
| G165 | static+lab | Authenticate original startup and API bindings, join the redirected setup edge to window creation/play and observe loaded modules separately. | `docs/NEXT.md` line 136 | free |
| G166 | static+lab | Authenticate the reconstruction, verify the mixed API bindings and connect callers through engine initialization to play; original runtime module behavior remains separate. | `docs/NEXT.md` line 139 | free |
| G167 | static+lab | Trace selected-slice entry through application/window initialization to the game loop; re-test with OpenGL-capable guest display for a first frame. | `docs/NEXT.md` line 143 | free |
| G169 | lab | Complete the original-client reply-arm discriminator in App. E#15; exact native list/game entry is now observed with qualified mixed supporting DATA. | `docs/NEXT.md` line 157 | free |
| G176 | lab | Resolve the sword crop, other-size Windows text positions and Windows current-clock check (App. E#326); this carry adds no new lab run. | `docs/NEXT.md` line 177 | free |
| G177 | static+lab | Reconcile the reported 255 WAVs with both subtotals of 254, and establish exact-build playback separately (App. E#325). | `docs/NEXT.md` line 181 | free |
| G178 | lab | Establish original 2.3 identity and exact-build behavior separately; a repack label or matching community executable cannot settle the missing input. | `docs/NEXT.md` line 186 | free |
| G186 | lab | Client test harness (#398): run 4.20r8, 5.00r7, 5.12, 6.03r7 and 6.113 on the Windows lab desktop; 1.x to 2.31 are in live-runs/client-harness-2026-11-13; 5.00r7 partial (walk 4/4, sword 3/3; place-dependent actions not reached) in the 2026-11-14 run and manual §4.11.12.1. | `docs/NEXT.md` line 222 | free |
| G191 | static+lab | The same probe on 4.20r8, 5.24r4 and 6.037 under Wine, the 0–90 self-prop width table, and a GS2 read-back of player.rupees (next batches). | `docs/NEXT.md` line 239 | free |
| G193 | static+lab | Read the v5 end consumers per event type, the key lookup table and the two post-window start-up helpers; then observe input delivery in a guest. | `docs/NEXT.md` line 243 | free |
| G200 | lab | Feed valid zlib members to an unchanged receiver near each build's capacity boundary, after a raw-frame positive control. | `docs/NEXT.md` line 304 | free |
| G202 | static+lab | Observe the bridge initializer/callback and establish its ABI; static registration is not a live 3D session. | `docs/NEXT.md` line 308 | free |
| G204 | lab | Extend measured gate coverage only with a qualified positive control and pinned new evidence; do not equate login, header recognition, parsing, execution and gameplay. | `docs/NEXT.md` line 312 | free |
| G212 | lab | Measure elapsed cadence without debugger overhead, and runtime timer/idle changes. | `docs/NEXT.md` line 395 | free |
| G216 | lab | Measure joined classes and other event lifecycles before generalizing. | `docs/preagonal-gs2-clean-room-2026-11-07.md` line 88 | free |
| G221 | lab | Measure missing-name and malformed-grid behavior before specifying rejection rules. | `formats/gmap-heights-404r2.md` line 49 | free |
| G234 | lab | Measure caller scheduling frequency/catch-up and later event execution. | `npc-library/gs1-move-205r2.md` line 34 | free |
| G251 | lab | Separate HTML/Wine and native Windows behavior with an appropriate controlled fixture. | `protocol/file-205r2-prefix-lf.md` line 32 | free |
| G253 | static+lab | Optional: publish one 5.12 capture snippet that contains such a short compressed frame so Claim B can be retired in E#2 with a cited decode. | `protocol/gen5-cipher-step-5x.md` line 37 | free |
| G256 | lab | 5.00r7 / 5.12 throw capture to wire-confirm id 11 (E#4 residual). | `protocol/ids-sent-512-status.md` line 30 | free |
| G286 | lab | Why the product-id slot is empty on 6.03r7 under Windows 10: the 32-bit registry view is the likely cause (above); not yet confirmed in a lab. | `protocol/pcid.md` line 138 | free |
| G291 | static+lab | Confirm or reject P4–P6 against that table / two-client capture. | `protocol/player-props-5x-status.md` line 35 | free |
| G293 | lab | Whether the extra flag on the 2.31 gmap lookup changes anything a player can see. | `protocol/plo-156-setactivelevel-231.md` line 90 | free |
| G294 | lab | Whether 24 with an unchanged image name stops before the level-list removal (needs the raw comparison or a lab run). | `protocol/plo-24-29-30-45-205r2.md` line 60 | free |
| G304 | lab | The value waitfor gives when its time runs out. The three cases did not settle it. | `protocol/script-fuzz-2026-11-19.md` line 221 | free |
| G307 | lab | Loopback weapon fixture on 5.00r7 and 5.12: which ask/body ids fire for a GS2 weapon. | `protocol/scripted-weapons-5x-status.md` line 37 | free |
| G327 | static+lab | Trace the 108 probe and the value that 4.11 answers in 162. | `protocol/v4x-windows-403r3-411.md` line 91 | free |
| G332 | static+lab | Whether the 7.x scripts load the same tables. This needs a 7.x reply decrypted for its own launch. | `protocol/v611-id-tables.md` line 201 | free |
| G334 | static+lab | Decrypt the Windows 6.113 capture itself. That needs the session key of that exact session, read from the running client. | `protocol/v611-outgoing-cipher.md` line 65 | free |
| G357 | lab | Stage 0: reference captures of the real 3.04 | `torque/rebuild-plan-3.04.md` line 35 | free |
| G366 | lab | Stage 9: 4.04r2 launcher and engine split | `torque/rebuild-plan-3.04.md` line 44 | free |
| G373 | lab | Verify a complete 3D session before asserting playable compatibility. | `torque/v4-404r2-exe.md` line 42 | free |
| G392 | lab | Validate each selected mechanic with before/after state and captured user action. | `version-profiles/windows-404r2-teardown.md` line 76 | free |
| G393 | lab | Record harness and fixture digests at capture start for reproducible follow-up. | `version-profiles/windows-404r2-teardown.md` line 77 | free |
| G394 | static+lab | Resolve package provenance before authenticating a vendor release label. | `version-profiles/windows-v4-import-provenance.md` line 43 | free |
| G400 | lab | nothing seen on a wire (lab confirmation of the hurt-packet rules) | `client-internals/decomp-findings-2026-10-24-d/open-questions.tsv` row 13 | free |
| G401 | lab | full login set of default checks and framing | `client-internals/decomp-findings-2026-10-25-e/open-questions.tsv` row 3 | free |
| G403 | static+lab | sender-side value formatting of each image field (units of x, y, colours, zoom, order) | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 2 | free |
| G404 | static+lab | the per-player "UDP reaches this player" flag in the 2.22 and 2.17.1 TCP test and how it is set | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 3 | free |
| G405 | lab | whether 2.17.1 sends id 24 in a two-player session and with what period | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 4 | free |
| G406 | static+lab | how the client draws shown images (layer 0 to 4 and 10 and over, light layer) | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 5 | free |
| G409 | static+lab | how the port item becomes a number and whether it is range-checked | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 9 | free |
| G410 | lab | default weapon wire ids vs images | `client-internals/decomp-findings-2026-10-25-k/open-questions.tsv` row 6 | free |
| G413 | static+lab | probe point for chests and signs | `client-internals/decomp-findings-2026-10-25-l/open-questions.tsv` row 5 | free |
| G417 | static+lab | the two A-key probe points near chests by tile id | `client-internals/decomp-findings-2026-10-25-l/open-questions.tsv` row 9 | free |
| G420 | static+lab | the push/pull block probes | `client-internals/decomp-findings-2026-10-25-m/open-questions.tsv` row 6 | free |
| G422 | static+lab | stopping positions on a live 2.22 client | `client-internals/decomp-findings-2026-10-25-m/open-questions.tsv` row 8 | free |
| G423 | lab | wire rounding of a nudged position | `client-internals/decomp-findings-2026-10-25-m/open-questions.tsv` row 9 | free |
| G424 | lab | Windows 5.12 has only the 8-row 195 gani set; the 4.x/5.x plan set (wine-core, widths, widths-fix, bytes2x, baddytypes, loadgani3w) was never run on it | `protocol/probe-results.tsv` (new, 2026-11-20 triage) | free |
| G426 | lab | Windows 6.037 has 32 rows; the full 4.x/5.x plan set has not been run on it | `protocol/probe-results.tsv` (new, 2026-11-20 triage) | free |

### Win10 VM on lab host B (#743, 1 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G425 | lab | Windows 2.02, 2.02 rev 1 and 2.02 rev 2 have no probe rows; 2.00 to 2.05 rev 1 have the 32-case gen-3 plan | `protocol/probe-results.tsv` (new, 2026-11-20 triage) | free |

### Linux VM on lab host B (servers) (#733, 24 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G023 | lab | 3.04 sheet type 5 and server tile definitions (best guess: type 5 is a walk rule (read); servers sent no tile definitions) | `manual/app-e-open-questions.md` E#507 | Lab host B Appendix E batch thread |
| G066 | static+lab | listscriptfunctions. The 4.03 and 6.036 notes say the client prints its script-function documentation with this switch; our launcher reads list the switch (torque/4208-launcher.md, torque/5007-launcher.md). Run once in a sandbox to get each build's GS2 function list. The wiki's Creation/Dev/Script/C | `client-internals/graal-wiki-crosscheck-2026-11-11.md` line 63 | free |
| G094 | lab | A lab login of both clients on a loopback GServer. | `client-internals/gserv-125-127-builds.md` line 132 | free |
| G096 | lab | Why 1.39 closes on F6 when the server is the loopback address. | `client-internals/gui-windows-fkeys.md` line 185 | free |
| G159 | static+lab | A readable window for the width canary (Wine virtual desktop): rc2004 and rc3 both render black/unreadable, so CAN01–06 is unknown, not failed. | `docs/NEXT.md` line 76 | free |
| G160 | lab | rc205 (RC2 2.05) — blocked by a Wine/GTK Pango font failure; staging fix needed. | `docs/NEXT.md` line 77 | free |
| G226 | lab | Live serve of a multi-layer file to 5.12 / 6.03r7 remains unmeasured; the source repair landed in seihai-gserver-v2 #118. [lab][srv] | `formats/gr-v105-empty-tiles-2026-11-16.md` line 33 | free |
| G227 | static+lab | Re-run the level walk with the repaired lab gserver; reader and link-line source repairs landed in seihai-gserver-v2 #118. [srv] | `formats/gr-v105-fuzz-2026-11-19.md` Still open: level walk | Codex server (source reconciliation only; live run unclaimed) |
| G284 | lab | Tooling for this now exists: tools/probe/ncprobe.py is a cipher-free NCL11012 proxy that logs every NC packet both ways and can inject/drop on either side (selftest tools/probe/ncselftest.py). tools/probe/lab/runnc.sh + lab/nc-core.plan drive it against nc7132001 / the Jan-2002 builds. Running the f | `protocol/nc-write-ops-status.md` line 38 | free |
| G292 | lab | Optional: unknown own-id long-value desync lab (called out in v5-props.md). | `protocol/player-props-5x-status.md` line 36 | free |
| G298 | static+lab | A readable window for the width canary on the 2004 RC and RC3 (Wine virtual desktop). | `protocol/rc-fuzz-2026-11-19.md` line 118 | free |
| G299 | lab | RC2 2.05 once its GTK font/render problem under Wine is solved. | `protocol/rc-fuzz-2026-11-19.md` line 119 | free |
| G300 | lab | A pre-2002 rcpre (gen 2), and rc2002 (gen 2) with the embedded NC socket (NC-fuzz thread). | `protocol/rc-fuzz-2026-11-19.md` line 120 | free |
| G302 | lab | A lab run with RC2 2.05 and two RC logins against the GServer-v2 fork, to confirm the | `protocol/rc-list-online.md` line 137 | free |
| G310 | lab | GServer 1.21 (GSERV007) — gen2 sweep (packs reply into one frame; watch framing). First run invalid (host load caused false canary timeouts); redo pending a quiet host. | `protocol/server-fuzz-c2s-targets.md` line 54 | free |
| G313 | lab | Confirm or explain the unauthenticated id 8 — re-run on a single connection with no | `protocol/server-fuzz-c2s-targets.md` line 107 | free |
| G314 | lab | Re-run the post-login cases with a per-case guest account reset, to separate each | `protocol/server-fuzz-c2s-targets.md` line 109 | free |
| G317 | lab | Lab check: send a PLO_SHOOT2 with known gravity to a 5.0.0.7 client and watch the arc. | `protocol/shoot-5007.md` line 127 | free |
| G326 | lab | Listserver VERIACC2 path when the world verifies accounts (our 4.04 lab used localhost / proxy accept without that check). | `protocol/v4-login-account-contract.md` line 37 | free |
| G344 | lab | Whether a 3.04 game server sends addtiledef lines at login; no 3.04-era server capture was checked for them. | `torque/304-tile-types.md` line 84 | free |
| G354 | lab | ShapeBase's main update section and Player's update, packet data and PlayerData (Graal adds at least chat and a name colour), so other players can be shown and a Player can be the control object. Started: PlayerData is ShapeBaseData, then flag, flag → pstring, 19 × f32, int7, 17 × f32, 19 × (flag →  | `torque/protocol19-server.md` line 165 | free |
| G368 | lab | How a server makes a 5.12 player move (movetype and movement data) and what the client then echoes. | `torque/udp-session.md` line 608 | free |
| G407 | lab | what a real service does with id 46 | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 7 | free |
| G408 | lab | what a real list service sends for 178 (item 0 in particular) | `client-internals/decomp-findings-2026-10-25-g/open-questions.tsv` row 8 | free |

### Linux VM on lab host B (#734, 14 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G083 | static+lab | Whether Linux 4.20r6's fusion and opcode 11, published from a handoff the editor did not re-run, match a fresh read of that ELF. | `client-internals/gs2-vm-loader-diff.md` line 289 | free |
| G101 | lab | Isolate signature-helper inputs and measure subsequent script execution separately. | `client-internals/linux-304-startup-reader.md` line 29 | free |
| G107 | lab | Measure other object lifecycles, joined classes and event sources separately. | `client-internals/linux-404r2-events.md` line 54 | free |
| G112 | static+lab | Confirm the static frame operation at a successful live helper stop. | `client-internals/linux-404r2-vm-dispatch.md` line 58 | free |
| G114 | lab | Observe initializer and callback execution, including the unresolved optional path. | `client-internals/linux-420-native-object-bridge.md` line 30 | free |
| G117 | lab | Measure frame drivers, movement timing and the live nonzero branch separately. | `client-internals/linux-420r6-clock-property.md` line 32 | free |
| G123 | lab | Measure handler completion, frame layouts and broader selector semantics independently. | `client-internals/linux-cross-version-dispatch.md` line 33 | free |
| G124 | lab | Connect further payloads to live execution and establish native semantic equivalence. | `client-internals/linux-cross-version-embedded-controls.md` line 33 | free |
| G243 | lab | Measure the remaining delivery, parser, event and cache gates separately. | `npc-library/linux-304-gs1-runtime.md` line 32 | free |
| G269 | lab | Capture version-specific message payloads before asserting field layouts. | `protocol/linux-404r2-receive-scope.md` line 55 | free |
| G270 | lab | Measure the remaining delivery, parser, event and cache gates separately. | `protocol/linux-603-network-gs2.md` line 53 | free |
| G271 | lab | Capture delivery envelopes, descriptors, cache outcomes and callback behavior. | `protocol/linux-cross-version-receive.md` line 34 | free |
| G272 | lab | Measure the remaining delivery, parser, event and cache gates separately. | `protocol/linux-local-login-matrix.md` line 36 | free |
| G381 | lab | Establish a positive cache control and normal-server compiled delivery before marking either gate observed. | `version-profiles/linux-network-bootstrap-evidence.md` line 70 | free |

### Tiger VM on lab host B (#730, 5 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G222 | static+lab | Positive control: an unchanged reader, reached naturally, returns successfully on a known-good map. Then vary only the height data in a one-cell map written for the test. Record storage and rendering separately. | `formats/gmap-heights-mac-ppc.md` line 90 | free |
| G278 | lab | Run a positive control first: an unchanged receiver that accepts one valid raw frame. Then feed it independently generated zlib members at lengths near each capacity boundary. Record the cipher stepping, the decoder's return value, the output bytes and the state that follows, each separately. | `protocol/macos-ppc-receive-decompression.md` line 70 | free |
| G281 | lab | Observe an unchanged Mac receiver consume one valid original local frame, | `protocol/macos-ppc-receive-framing.md` line 56 | free |
| G353 | lab | A real 4.04r2 and 3.153 run against this order (the GPL lab server, PR #78). | `torque/protocol19-server.md` line 164 | free |
| G365 | lab | Stage 8: 3.153 3D play | `torque/rebuild-plan-3.04.md` line 43 | free |

### Lab host A Lion/Sequoia VM (#731, 4 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G029 | lab | Whether Mac 6.004 and 6.015 draw a game frame (best guess: 6.015 logs in and plays (lab); the white frame is the guest's missing OpenGL) | `manual/app-e-open-questions.md` E#618 | free |
| G130 | lab | Observe one unchanged-loader positive control reach consumption and a | `client-internals/macos-v5-animation-group-lifecycle.md` line 35 | free |
| G198 | lab | Run an unchanged Mac client to the context helpers and record the real arguments. Record success and visible output separately. | `docs/NEXT.md` line 302 | free |
| G378 | lab | Re-test with an OpenGL-capable guest display (or Sequoia) to separate | `version-profiles/lab-mac-v6-6015-lion-2026-11-16.md` line 76 | free |

### Android-x86 / mobile lab (#732, 6 rows)

| id | kind | gap | source | claimed |
|---|---|---|---|---|
| G155 | lab | Place G3D29090 and G3D2504D with another decrypted IPA, or capture one iPhone login in the lab (iphone-version-tokens.md). | `client-internals/version-token-catalogue.md` line 322 | free |
| G194 | lab | Run the GS2 loop-budget and event-queue boundaries in an Android runtime. | `docs/NEXT.md` line 250 | free |
| G230 | lab | Establish the exact native resolver and coordinate/slot acceptance before claiming playback compatibility. | `formats/ios-gani-param1-placements.md` line 26 | free |
| G245 | lab | What the per-launch ?p= value binds in the signature. | `protocol/connector-script.md` line 154 | free |
| G246 | lab | Whether the 7.x script differs from the 6.11 one (token, template, cipher). This needs a 7.x reply decrypted for its own launch. What differs outside the script, and what a decrypted reply would need, is in section 7a. | `protocol/connector-script.md` line 155 | free |
| G258 | lab | Run the app. The binary is 32-bit ARMv6 for iOS 3–5; there is no iOS emulator for | `protocol/ios-classic-plus-113-framing.md` line 129 | free |
