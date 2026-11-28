# Research gap board (2026-11-20)

Every open research gap in the repository, in one table that anyone can claim from:
[`gap-board.tsv`](gap-board.tsv). It collects three sources as they stood on `main` on
2026-11-20:

- the open entries of Appendix E ([`manual/app-e-open-questions.md`](../manual/app-e-open-questions.md), §E.1),
- every unticked `- [ ]` box in the notes and in [`NEXT.md`](NEXT.md) (the anti-cheat
  defence checklist, the publication plan and the drive-salvage placement list are left out,
  because they are not research questions),
- the rows still open in the `client-internals/decomp-findings-*/open-questions.tsv` files.

Three new gaps found while building the board are added at the end (5.12, 2.02 and 6.037
probe coverage). Four `open-questions.tsv` rows already closed by a later batch were left out.

## Columns

2026-11-28 update: G053 is partial. Three selected early clients share a [conditional form-creation Interval write](../client-internals/early-form-timers-2026-11-09.md#selected-form-creation-interval-write); this does not identify the condition, enumerate all timer or idle-handler writes, or establish runtime cadence under it. The prior elapsed-frame lab remains separate; all 426 IDs remain.

2026-11-28 update: G038's [selected 1.41 rev 1 extra-field question](../client-internals/combat-baddy-tile-by-version.md#selected-141-rev-1-extra-hit-fields) is answered: three added bytes identify a level NPC, changing the range source and kill-credit tail. This is one retained input's static path, not all variants or runtime acceptance; all 426 IDs remain.

2026-11-28 update: G050 remains partial. The [selected 2.22 port-conversion follow-up](../client-internals/decomp-findings-2026-10-25-g/03-id178-comma-text.md#selected-222-port-conversion-boundary) traces normal integer conversion directly to the imported 16-bit boundary without an intervening port-domain comparison. Real-service text/item 0, conversion-failure recovery, other inputs and runtime remain open; all 426 IDs remain.

2026-11-28 update: G099 is answered for the [selected 2.22 input paths](../client-internals/laying-items-and-hiding.md#selected-222-feature-mask-follow-up): item selection checks bit 0x10 and weapon cycling bit 0x20 of the command-written mask. A clear cycle bit leaves ordinary weapon handling available. Runtime, other inputs and G100's 3.04 cost table remain separate; all 426 IDs remain.

2026-11-28 update: G097 is partial. The [selected F2 guard follow-up](../client-internals/gui-windows-fkeys.md#selected-f2-null-form-guard-follow-up) binds null-form behavior in 2.22 and a modified 2.31 input, plus selected 2.22 receive-179 creation. The 2.17 comparison, other creation paths and runtime behavior remain open; all 426 IDs remain.

2026-11-28 update: G076 remains partial. The [v22 rejection-status follow-up](../client-internals/graal2002-level-open.md#v22-rejection-status-and-warning-text-boundary) traces gated `failed` text submission and localization of the separate warning string; it does not identify the v22 warning-dialog caller or establish runtime display. All 426 IDs remain.

2026-11-28 update: G078/G141 share one [selected local-entry helper comparison](../client-internals/v21-local-enter.md#name-matched-helper-selected-static-comparison). The public image, v22 and 2.05 revision 2 pass two doubles equal to 31 to a record-construction/list-append path; v22 adds a two-byte guard. This answers the selected state-effect questions, not rendered/gameplay meaning, callback/error behavior or all builds. The earlier lab's visible-no-difference result remains separate from internal state. All 426 IDs remain.

2026-11-24 update: G147 now has a [three-input reader comparison](../client-internals/v2100-gani-reader.md#selected-reader-comparison-with-ver7-and-v22-2026-11-24). The selected public image, ver7 and v22 agree on the documented normal storage contracts, with separate reader/data/helper checks. This closes only that finite comparison; whole-reader/callee/runtime equivalence, malformed/error behavior and other builds are not established. All 426 IDs remain.

2026-11-23 update: G146's [keyword-removal question](../client-internals/v2100-gani-reader.md#keyword-removal-and-field-counts-static-follow-up-2026-11-23)
is answered on the selected reader's normal path: a concrete list method deletes
index zero before count checks, binding minima six/five/two/one after the keyword.
This does not establish malformed/runtime behavior; G147's later comparison has its own finite scope above.

2026-11-23 update: G145's [header-word recovery](../client-internals/v2100-gani-reader.md#block-opener-and-third-flag-static-follow-up-2026-11-23)
is answered for the same examined input: `ANI` selects the block mode and `LOOP`
sets a distinct stored flag. This does not establish rendered repetition or flag
defaults/interactions; G147 is covered separately above and all 426 IDs are retained.

2026-11-23 update: G144's [placement-prefix spelling question](../client-internals/v2100-gani-reader.md#placement-prefixes-static-follow-up-2026-11-23)
is answered for the examined public-labelled 2.1.0.0 input: `PARAM` and `ATTR`,
with raw literal bytes and separate instruction paths. Rendering and malformed-input
behavior are not established; G147 is covered separately above. The stable inventory
still contains 426 IDs.

2026-11-23 update: G070 has a [versioned source comparison](../server-notes/file-cache-and-script-size-2026-11-23.md)
separating the later fork's file-checksum exception, cached package metadata and
parsed map state from NC script input and classic script-output bounds. Original
4.02 behavior, the historical RC editing limit and old-engine breakage remain open;
this is partial coverage, not a completed historical confirmation.

2026-11-25 update: G305 (why fuzz case 30789 crashes 6.03r7) is answered in
[script-fuzz-2026-11-19](../protocol/script-fuzz-2026-11-19.md#why-case-30789-crashes-603r7-static-read-2026-11-25):
the crash is in `substring` (opcode 115), not `getangle`/`^`. A one-char `substring(2.00001, 0x7FFFFFFF)` hits a signed `start+length`
overflow that skips the length fixup in all three builds; 4.20r8 caps the copy at 1,000,000 bytes and 5.12 checks the ~2 GB allocation,
but 6.03r7 dropped both guards and faults. Checkbox closed.

2026-11-25 update: G323 (4.20r8 login-account script API) is answered in
[v4-login-account-contract](../protocol/v4-login-account-contract.md#login-account-script-api-by-build-g323-2026-11-25):
4.20r8 has no `getLoginAccountName()` and no `GuiAccountPasswordCtrl` (both arrive in 5.00r7), but has `Adventure_setAccountName` /
`Adventure_setPassWord` and a `password` flag on `GuiTextEditCtrl`, which every build masks with `*`. Checkbox closed.

2026-11-25 update: G262 (large-file receive on 4.208 to 6.037) is answered in
[large-file-thresholds-focus](../protocol/large-file-thresholds-focus.md#receive-handlers-on-4208-to-6037-g262-2026-11-25):
all four stock engines handle 68, 69 and 84; 84 only feeds progress, 69 never checks it, and no receive-side size constant exists.
`large_files` and `large_file_size` for these builds are now read, not inferred. Checkbox closed.

2026-11-25 update: G255 (genuine 5.12 send set) is answered in
[ids-sent-512-status](../protocol/ids-sent-512-status.md#full-send-sets-500r7-and-genuine-512-g255-2026-11-25):
every send site in both engines uses a fixed id; 5.00r7 sends 62 ids and 5.12 the same minus 21 (`PUTNPC`) and 40 (`SHOOT`),
plus 48 (`SHOOT2`). Scripts cannot send an arbitrary id. Profile rows updated. Checkbox closed.

2026-11-25 update: G173 and G098 (5.12 versus 5.00r7 prop value widths) are answered in
[player-props-5x-status](../protocol/player-props-5x-status.md#genuine-512-has-the-same-widths-g173--g098-2026-11-25):
every id in the self, other, NPC and baddy parsers has the same width in both engines. One behaviour change found on the way:
5.12 drops NPC scripts (prop 1) except a sparring-zone marker. Checkboxes closed.
2026-11-24 update: G065 (GS1 gone in 5.12) is answered in
[gs1-commands-by-version](../npc-library/gs1-commands-by-version.md#512-no-gs1-command-table-2026-11-24):
`gs1scan.py x86` finds 0 commands in the genuine 5.12 engine against 193 in the 5.00r7 control; 59 names are
gone and the other 134 survive only as GS2 built-ins. Checkbox closed.

2026-11-24 update: G084 (5.00r7 event-queue cap) is answered in
[gs2-vm-loader-diff](../client-internals/gs2-vm-loader-diff.md#500r7-event-queue-cap-g084-2026-11-24):
both event receivers refuse at 1000 queued events in the unpatched engine and in both patched
engines; the patches touch only the licence check and auto-update gates. A January 2007 4.x
engine uses 10000 in the same routines. Checkbox closed.

2026-11-24 update: G252 and G254 (Windows 5.00r7 gen-5 cipher step) are answered in
[gen5-cipher-step-5x](../protocol/gen5-cipher-step-5x.md#settled-for-windows-500r7-g3d22067):
a static read of the stock engine shows zlib/bzip2 bodies step `min(floor(len / 4), 4)` times and
raw bodies `min(ceil(len / 4), 12)`, in both the receive and send routines, so 5.00r7 shares
5.12's round-down. Checkboxes closed.

2026-11-24 update: G284 (NC write ops via ncprobe) settled in [nc-write-ops-status](../protocol/nc-write-ops-status.md#write-layouts-2026-11-24-lab):
158 any-order props with omit=leave / empty-str=clear; class 163/162/188 and weapon 33 GSHORT
layouts dumped; no attribute write beyond script/flags. Local-NPC list after 114 remains open.

2026-11-24 update: G248 (loopback `conf.gs` harness for Windows 6.113) is
**PARTIAL / OPEN** in [conf-gs-fuzzing](../protocol/conf-gs-fuzzing.md#g248-close-2026-11-24):
Phase A container fuzz via `tools/connfuzz/` against stock 6.113 fails closed
on all 18 one-field mutations; Phase B / first encrypted frames remain OPEN
(trust-anchor NO-GO; session-key recovery stopped). Not closed.

2026-11-24 update: G082 (maths on unpacked 6.1.1.3 and Mac 6.11r1) is answered in
[static-reads-appendix-e-2026-11-24-g082](../client-internals/static-reads-appendix-e-2026-11-24-g082.md):
both builds keep `b == 2` → `a * a` and take a positive `b == 0.5` in **double**
precision. The 6.03r7 single-precision square root does not transfer. Checkbox
closed.

2026-11-24 update: G148 (Themida cutoff dates for 5.30r3 / 5.31r4 / 6.00r2 /
6.00r4) is answered in
[v5v6-expiry-and-black-screen](../client-internals/v5v6-expiry-and-black-screen.md#how-the-expiry-works-530r3-to-600r4):
clock binary search — stops from 2011-01-01 / 2011-03-21 / 2011-08-27 /
2011-09-09. Checkbox closed.

2026-11-24 update: G328 (4.11 value holder) is answered in
[v4x-windows-403r3-411](../protocol/v4x-windows-403r3-411.md#what-the-engine-gained):
holder wraps local-player CURPOWER (8-byte float), MAXPOWER, RUPEESCOUNT,
ARROWSCOUNT, BOMBSCOUNT, GLOVEPOWER, SWORDPOWER, SHIELDPOWER, ALIGNMENT,
MAGICPOINTS, plus local mode/status ints beside STATUS/SPRITE. Checkbox
closed.

2026-11-24 update: E#618 / G029 (Mac 6.004 / 6.015 game frame) is **partial** in
[mac-6004-beta-gate](../client-internals/mac-6004-beta-gate.md): 6.015 logs in and
requests level files but its main view stays blank on Lion and Sequoia; 6.004's
beta quit is a wall-clock gate past **2011-09-08 19:22:31 UTC** (same stop day as
Windows 6.00r4); clock-held live frame blocked from this host (no reachable Mac
guest).

2026-11-24 update: **G028 / E#616** (first Crypto) is **partial** in
[v7-connector-payload-cipher.md](../protocol/v7-connector-payload-cipher.md): the
connector container's 256-byte RSA block is signature-only (not an AES key wrap);
payload cipher, plaintext script and `?p=` DES key remain open on stock v7.

2026-11-24 update: **G156** (second Crypto / NEXT replaced-key avenue) is **answered**
in [v7-connector-trust-anchor.md](../protocol/v7-connector-trust-anchor.md): stock v7
Worlds trust-anchor swap is a **NO-GO** (packed Themida verify; held unpacked dumps are
analysis-only, not runnable patched clients). Production plaintext / host/port / login
stay Maybe never under **G028 residuals** (untouched here).

2026-11-24 update: **G246** (7.x vs 6.11 connector script token/template/cipher) is
**partial** in [v7-connector-script-diff.md](../protocol/v7-connector-script-diff.md):
outside-script diffs stay settled in `connector-script.md` §7a; production script
token/template/cipher remain **uncompared** (decrypt blocked — G156 trust-anchor NO-GO
+ G028 residuals untouched).

2026-11-24 update: **G332** (7.x vs 6.11 connector id tables) is **partial** in
[v7-connector-id-tables.md](../protocol/v7-connector-id-tables.md): remapper install
model and PLI `onSend*` slot names match 6.11; production 7.x pair lists remain
**uncompared** (decrypt blocked — G156 trust-anchor NO-GO + G028 residuals
untouched).

2026-11-24 update: **G334** (Windows 6.113 capture decrypt) is **partial** in
[v6113-capture-decrypt.md](../protocol/v6113-capture-decrypt.md): clear prefix +
RC4@287 reconfirmed on three capture streams; post-287 decrypt **blocked**
(exact-session key never recorded; operator private key unheld — **G335** not
started; memdump alone insufficient; other-session keys do not transfer).

2026-11-24 update: **G335** (last Crypto / client→server `0xfc` padding) is
**partial** in [gen6-c2s-0xfc-padding.md](../protocol/gen6-c2s-0xfc-padding.md):
C→S envelope settled (256-byte RSA to the operator public key; parse-key decrypt
is garbage; S→C PKCS#1 v1.5 type-2 and §4c plaintext already closed); exact C→S
encoding-message padding **blocked** (operator private key **unheld**).

2026-11-24 update: **G129** (first Machine-identity / Mac PowerPC
`IOMACAddress` property read + hash) is **partial** in
[mac-ppc-machine-identity-property.md](../client-internals/mac-ppc-machine-identity-property.md):
property-read (six raw `IOMACAddress` bytes from the primary Ethernet service)
and plain MD5-hex hash settled on 4.04r2 / 4.20r6 / shared v5; login comma-list
call graph still open.

2026-11-24 update: G344 (`addtiledef` at 3.04 login) is answered in
[304-tile-types](../torque/304-tile-types.md#login-capture-2026-11-24): a loopback
GServer-v2 / gs2emu profile that admits `G3D03014` sends no `addtiledef` /
`addtiledef2` / `removetiledefs` at login (`CLEARWEAPONS` + `NPCWEAPONDEL` only;
no `NPCWEAPONADD`; no tiledef text on the wire). Checkbox closed.

2026-11-24 update: G155 (iPhone tokens G3D29090 / G3D2504D) is **partial**: `G3D29090` placed on Classic+ 1.10 and Adrenaline Golf Free 1.1 ([iphone-version-tokens](../client-internals/iphone-version-tokens.md)); `G3D2504D` still L after the expanded IPA pass. Lab wire capture not run (no device).

2026-11-24 update: G316 (half-open double-login slot / persist) is answered in
[server-fuzz-c2s-targets](../protocol/server-fuzz-c2s-targets.md): on GServer 1.28b2
two login lines in one frame complete a normal login (`9,14,100,…`) — **not** half-open.
Held sessions occupy ordinary player slots (canary fails once ~8 are held); close frees
immediately (no ghost). Persist while TCP held (≥10–30 s). Checkbox closed.

2026-11-24 update: G273 (3.x public listserver login on 14922/14923) is **answered** in
[g3d30123-public-listserver-2026-11-24](../protocol/g3d30123-public-listserver-2026-11-24.md):
owner-approved list-only `G3D30123` one-frame login got a modern list on public **14922**
and **14923** (legacy+modern on 14923). 3.04/3.153 `port_status` moves assumed→confirmed.
The 2026-11-24 drop of this row (#823) is reversed.

2026-11-24 update: **G002 / E#3** (public 5.x/6.x Login session) is **partial** in
[g002-public-login-603r7-2026-11-24](../protocol/g002-public-login-603r7-2026-11-24.md):
official Login on **14900** answers Windows 6.03r7 guest (`G3D0311C`) with S→C **25** then
**16** (`Please update your version..`); no 190 / `basepackage.gupd` lobby for that token.
Official accepting-client lobby still open (community Login only).

2026-11-24 update: **G019 / E#403** (classic logins on public 14922) is **partial** in
[g019-classic-login-14922-2026-11-24](../protocol/g019-classic-login-14922-2026-11-24.md):
public **14922** answers a classic shape-B login with two plain-zlib frames (id 0 list + ids 2/3/5/6),
overturning the 2026-10-25 classic→14922 silence. Historical 2001 behaviour and a stock 2.17.1
capture stay open.

2026-11-24 update: **G020 / E#404** (public refuse 2.05 / classic on 14923) is **partial** in
[g020-classic-login-14923-2026-11-24](../protocol/g020-classic-login-14923-2026-11-24.md):
public **14923** answers a classic shape-B login with **three** plain-zlib frames (id 0 list ×2
with 6 then 4 rows, then ids 2/3/5/6). Richer than the 2026-10-25 single legacy list. Seihai 2.05
`port_status` assumed→confirmed. Game-server S2 2.05 refuse / older version-table hypothesis
still open (no game login).

2026-11-24 update: G314 (post-login per-case guest account reset) is answered in
[server-fuzz-c2s-targets](../protocol/server-fuzz-c2s-targets.md): on GServer 1.28b2,
`idsweep`+`body` with `srvfuzz --reset-cmd` restoring the pristine guest account before
each case produced **no** sticky `NPCWEAPONADD` (id 33) on any canary; empty `id-40` /
`id-222` reply `none` when the account is clean. The 2026-11-19 cumulative run's first
dirty canary was after empty `id-25`. Checkbox closed.

2026-11-24 update: G313 (unauthenticated S→C id 8 / `OTHERPLPROPS`) is answered in
[server-fuzz-c2s-targets](../protocol/server-fuzz-c2s-targets.md): on GServer 1.28b2 a solo
pre-auth frame/login run with no canary produced no id 8; the normal canary harness
reproduced id 8 on every frame case (body `0x21 0x53`). Canary-guest artifact; checkbox
closed.

2026-11-24 update: G160/G299 (rc205 / native i386 GTK2 staging) closed in
[rc-fuzz follow-up](../protocol/rc-fuzz-2026-11-19.md#width-canary-follow-up-2026-11-23):
lab image now has i386 GTK2 + `libgtksourceview-1.0`; native `GSERV025` (2006/01/20,
`RC_NATIVE=1`) logs in and completes `rc-widths` (no crash/disconnect; `Players:` 0→1).
Wine/GTK Pango for Windows `RC2_2.05` unchanged. CAN nickname cell still needs Player
List (G159). G158 umbrella leftovers are G159/G298 (CAN cell / rc3 paint).

2026-11-24 update: G302 (RC2 2.05 two-RC Admins/Players confirm on the GServer-v2 fork) was
attempted earlier the same day and **blocked** on missing i386 GTK2 — see
[rc-list-online lab status](../protocol/rc-list-online.md#lab-status-2026-11-24-lab).
Native single-RC staging later cleared (G160); Wine/GTK Pango still blocked. Re-run
two-RC with `RC_NATIVE=1`; source checkbox stays open.

2026-11-24 update: G300 (pre-2002 `rcpre` gen 2, and `rc2002` embedded NC) is answered in
[rc-fuzz](../protocol/rc-fuzz-2026-11-19.md): `rcpre` (`GSERV022`) took `rc-core` with no
crash/desync; `rc2002` (`GSERV023` + `NCL11012`) opened the NC socket through `ncprobe` and
took `nc-core` (45 injects, no crash). The `LOCALRIGHTS` harness fix for native `PLO 79` is in
`runrc.sh`. Source and `NEXT.md` boxes were already ticked; this closes the board row.

2026-11-23 update: G159/G298 (RC width canary window) and G160/G299 (rc205 staging)
advanced in [rc-fuzz follow-up](../protocol/rc-fuzz-2026-11-19.md#width-canary-follow-up-2026-11-23):
Wine virtual desktop makes rc2004 readable for `rc-widths`; rc3 client area stays
black; CAN01–06 still need the Player List open. (G160/G299 native GTK2 staging closed
2026-11-24 — see above.)

2026-11-21 update: G424 has a [100-case selected own-prop scan on Windows
5.12 under Wine](../protocol/probe-wine512-widths-2026-11-21.md), with 96 landed
and four lost canaries across the 91-case scan and nine nonzero follow-ups. This is partial coverage, not a full width/semantic
table; G424/G191 and the remaining plans stay open.

2026-11-21 update: G190 has a [documentary 2.14–2.16 feature-family
reconciliation](../client-internals/214-216-feature-evidence.md), including a
pinned reference-server large-file gate. G190 remains open for earlier
families, unlisted details and exact client/revision evidence.
2026-11-21 update: G424 now has a [controlled 32-case Windows 5.12 core slice
under Wine](../protocol/probe-wine512-core-2026-11-21.md). G424 and G191 remain
open: other plans/builds and the full width sweep are not completed. The older
failed attempt adds no accepted rows; existing PLO 195 coverage stays separate.

| Column | Meaning |
|---|---|
| `id` | Board id, `G001` on. Stable for this board; a later board renumbers. |
| `source`, `where_in_source` | The file and line (or Appendix E entry, or TSV row) the gap comes from. |
| `gap` | The question, shortened from the source. Read the source before starting. |
| `kind` | `static` (a binary, file or source read), `lab` (needs a run), `static+lab` (read first, then a run), `owner` (only Squirrel can supply or decide), `missing` (no copy of the build or input is held), `maybe-never`, or `umbrella` (a parent item whose children are listed separately). |
| `runs_on` | For static work, any host or the cloud. For lab work, the VM the run belongs on (see the queue below). |
| `priority` | `high` for Appendix E entries, `NEXT.md` items and the new probe gaps; `medium` for the rest. |
| `claimed_by` | `free`, or the thread working on it. |

The kinds were assigned from the wording of each item and spot-checked by hand, so a few
will be wrong. Many boxes are older than the batches that may have answered them: check the
source note and `INDEX.md` for a newer note before starting, and if the gap is already
answered, tick the box in the source with a link instead of redoing it.

2026-11-21 update: **G192's named starting rows were relabelled**, not measured.
The [client-id evidence reconciliation](../protocol/client-id-inference-scope.md)
keeps their outgoing sets inferred, separates Windows and Mac 6.015, and corrects
the stale Windows token-evidence label. The note lists the remaining per-build
measurements; other inference-ledger rows and G168's broader identity work remain open.

2026-11-22 reconciliation: G134, G135 and G137 are answered at the original
named-build observable scope in the [particle/list/format note](../client-internals/showimg-particles-and-gs2-format.md#selected-linux-603r7-mechanisms-and-published-lab-reconciliation).
This credits the existing published labs, with three-build timing versus four-build
clearing and 0.5-second observation limits; the new selected static input is separate.
G136 and overall E#210 remain open/partial. Stable board IDs and the historical
426-row inventory are retained.

2026-11-25 update: two follow-ups from G273's [public list check](../protocol/g3d30123-public-listserver-2026-11-24.md)
are added as new rows. **G427** traces list reply id 6, seen on both ports and not in earlier
notes. **G428** repeats the check with a stock 3.04 or 3.153 client (owner OK given for the community
listserver only, not the official one). The
board now has 428 IDs.

2026-11-25 update: G428's [stock 3.04 run](../protocol/g428-stock-304-public-list-2026-11-25.md)
answers G428. A stock 3.04 sends the same one-frame login. It works on 14922, but on 14923
the server's first frame is plain zlib and the client disconnects. G427 is partial: id 6 was
the text `000` on both ports.

## Counts

| Kind | Items |
|---|---|
| static | 264 |
| lab | 100 |
| static+lab | 29 |
| missing | 13 |
| owner | 10 |
| maybe-never | 7 |
| umbrella | 5 |
| **Total** | **428** |

Lab items by where they run: Windows 10 VM on lab host B or Linux VM under Wine 74, Linux VM on lab host B
with the lab servers 24, Linux VM on lab host B (Linux clients) 14, Android-x86 or mobile 6, lab host B
Tiger VM 5, lab host A Lion or Sequoia VM 4.

## Issues

Every row is also in one GitHub issue, so an agent can take work without reading the TSV. The
entry point is the research gap roadmap, #746 (a child of #370). Lab issues: #743 (Windows
clients on lab host B), #733 (servers, RC and NC), #734 (Linux clients), #730 (Tiger), #731 (Lion
and Sequoia), #732 (Android, iOS, v7). Static issues: #740 (NEXT.md and Appendix E), #744 (1.x to
2.x), #745 (protocol), #741 (4.x to 7.x, GS2 VM, Mac), #738 (Torque), #735 (Linux teardowns),
#736 (formats and tools), #739 (version profiles), #737 (NPC scripting). Blocked rows: #742.
When a row is done, tick it in its issue as well as in the source note.

## External research reservation (2026-11-22)

Grok owns the following research scopes by external reservation: `G028`, `G156`, `G246`, `G332`, `G334`, `G335`, `G082`, `G148`, `G328`, `E#618`, `G129`, `G285`, `G286`, `G287`, `G158`, `G284`, `G300`, `G302`, `G313`, `G314`, `G316`, `G273`, `G155`, `G344`, `G248`.

**Ended 2026-11-24.** Grok's run stopped when its usage ran out. The four rows it had not
started (`G285`, `G286`, `G287`) are `free` again; every other row, G129 included (partial,
#838), carries its own done/partial/open state.

This was ownership metadata only, not a result, closure or authorization to probe or operate.
All existing input, evidence, approval and completion limits remain in force; other agents
should avoid duplicate work. The TSV changes only the claimant for the 24 stable G rows,
retaining any prior partial/status qualification. `E#618` is a separately reserved evidence
item, not a new G row: the board still has 426 IDs.

## How to claim

1. Pick a `free` row. Static rows need no queue.
2. Set `claimed_by` to your thread in the same PR that answers it, or in a one-line PR first
   for long work.
3. Answer it in a topical note, tick the box in the source note with a link, and drop or mark
   the row here.

## Lab queue

Each queued run below is written out step by step in [`experiments.md`](experiments.md), with its expected output, where the result goes and the issue it closes.

Labs run one at a time per host, inside VMs only (no bare-metal runs). Lab host A has little
memory: a watchdog powers VMs off when the host's free memory falls under about 3 GB, so do not
boot a second large VM there while one is running. Check what is running before booting. The
queue below is the suggested order; take the next free entry whose VM is idle.

### Lab host B, Windows 10 VM and Linux VM

| # | What | Board rows | State |
|---|---|---|---|
| 1 | Probe coverage: the 4.x/5.x plan set on 5.12 and 6.037, the gen-3 plan on 2.02, 2.02 rev 1 and 2.02 rev 2, and the RC width canary on native Windows | the three new rows; `NEXT.md` lines 76, 77, 239; `rc-fuzz` lines 118, 119 | free |
| 2 | Appendix E lab batch: E#210, E#304, E#203, E#507, E#324, E#325, E#15, E#610 | those E rows | claimed (Appendix E batch thread) |
| 3 | 4.04r2 pickup field read around each action, in the repeatable Wine scene (E#611), after the static read of the field | E#611; `404r2-carry-state` lines 57–60 | free |
| 4 | Client test harness #398 on 4.20r8, 5.00r7, 5.12, 6.03r7 and 6.113 | `NEXT.md` line 222 | free |
| 5 | 5.00r7 and 5.12 throw capture (id 11) and the loopback GS2 weapon fixture (which ask and body ids fire) | `ids-sent-512-status` line 30; `scripted-weapons-5x-status` line 37 | free |
| 6 | `PLO_SHOOT2` with known gravity on 5.0.0.7 | `shoot-5007` line 127 | free |
| 7 | The 2002 builds ver7 to ver13: ids 2, 4, 17, 18, 154 and 155 (baddy, chest, horse drawn or not); v22 and 1.40 login frames | `graal2002-and-140-builds` lines 297, 298 | free |
| 8 | 6.03r7 product-id slot on Windows 10 (32-bit registry view) | `pcid` line 138 | free |
| 9 | 2.05 rev 2 and 2.22 F-key windows with a hosts-file list host; 1.39 closing on F6 | `gui-windows-fkeys` lines 184, 185 | free |

### Lab host B, Linux VM with the lab servers

| # | What | Board rows | State |
|---|---|---|---|
| 1 | Server fuzz: GServer 1.21 gen-2 sweep on a quiet host (unauthenticated id 8 and per-case guest reset closed 2026-11-24) | `server-fuzz-c2s-targets` line 54 | free |
| 2 | GServer 1.25 and 1.27: lab login of both clients and the player, NPC and baddy prop ranges | `gserv-125-127-builds` lines 128, 132 | free |
| 3 | Serve a multi-layer level to 5.12 and 6.03r7 with the reader repair from seihai-gserver-v2 #118; live result still open | `gr-v105-fuzz` source repair and remaining level walk; `gr-v105-empty-tiles` line 33 | free |
| 4 | NC write operations through `ncprobe.py` (attribute, class and weapon writes) | `nc-write-ops-status` line 38 | partial — layouts settled 2026-11-24 (G284); local-NPC list after 114 open |
| 5 | The protocol-19 server order with a real 4.04r2 and 3.153 | `protocol19-server` lines 164, 165 | free |

### Lab host B, Tiger VM

| # | What | Board rows | State |
|---|---|---|---|
| 1 | Mac PowerPC receiver positive control: one valid raw frame, then zlib members near each capacity boundary; the gmap height reader on a known-good map | `macos-ppc-receive-framing` line 56; `macos-ppc-receive-decompression` line 70; `gmap-heights-mac-ppc` line 90; `NEXT.md` line 304 | free |

### Lab host A, Lion or Sequoia VM

| # | What | Board rows | State |
|---|---|---|---|
| 1 | Mac 6.004 with its clock held before the beta limit, on the Sequoia guest | E#618 | partial — static gate settled 2026-11-24; clock-held live still blocked |
| 2 | An unchanged Mac client run to the context helpers, recording the real arguments | `NEXT.md` line 302 | free |

E#618's remaining live answer needs a reachable Lion / Sequoia / 10.9-era guest with
OpenGL and the clock held for 6.004. Building or restoring that guest is an owner call.

### Android-x86 or mobile

| # | What | Board rows | State |
|---|---|---|---|
| 1 | The GS2 loop budget and event-queue limits in an Android runtime | `NEXT.md` line 250 | free |

## Static work to start with

These are free, high value and need no queue. Each can run on the cloud with a binary copy
from the Share, or on either host.

- The 4.04r2 pickup-bound field (E#611, `404r2-carry-state` lines 57 and 58), which also
  unblocks lab queue entry 3.
- The Windows 5.00r7 frame codec for short compressed frames, both directions
  (`gen5-cipher-step-5x` line 36), and the full 5.12 send floor (`ids-sent-512-status` line 29).
- The Mac 4.20r6 and Windows 4.04r2 frame-cipher step rule, and the Mac server-to-client switch
  for 4.04r2 and 5.12 (`NEXT.md` line 221).
- The 2.22 carry pose, glove property value, swimming and carrying speed factors, push and pull
  probes and the second passable list (`decomp-findings-2026-10-25-l` and `-m` rows).
- The 2002 level reader: the one-character marker, the `Unsupported file type!` caller and the
  v22 Control-NPC helper (`graal2002-level-open` lines 69–73), and the two v22 flag bytes
  (`v21-level-record-gate` line 21).
- Events, flags, variables and functions per 1.x build (`NEXT.md` line 219).
- The Mac 6.11r1 handler-table extent and opcode 7 (`NEXT.md` line 288).

2026-11-28 update: **G139** and **G140** are answered for the selected binary readers in the [level-record comparison](../client-internals/v21-level-record-gate.md). The chest gate uses a fresh header comparison, and the examined ver8–ver13 subset matches ver7 in the two selected scan loops.
