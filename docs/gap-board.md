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

## Counts

| Kind | Items |
|---|---|
| static | 264 |
| lab | 99 |
| static+lab | 28 |
| missing | 13 |
| owner | 10 |
| maybe-never | 7 |
| umbrella | 5 |
| **Total** | **426** |

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
| 1 | Server fuzz: GServer 1.21 gen-2 sweep on a quiet host, the unauthenticated id 8 on one connection, and post-login cases with a per-case guest reset | `server-fuzz-c2s-targets` lines 54, 107, 109 | free |
| 2 | GServer 1.25 and 1.27: lab login of both clients and the player, NPC and baddy prop ranges | `gserv-125-127-builds` lines 128, 132 | free |
| 3 | Serve a multi-layer level to 5.12 and 6.03r7 with the reader repair from seihai-gserver-v2 #118; live result still open | `gr-v105-fuzz` source repair and remaining level walk; `gr-v105-empty-tiles` line 33 | free |
| 4 | NC write operations through `ncprobe.py` (attribute, class and weapon writes) | `nc-write-ops-status` line 38 | free |
| 5 | The protocol-19 server order with a real 4.04r2 and 3.153 | `protocol19-server` lines 164, 165 | free |

### Lab host B, Tiger VM

| # | What | Board rows | State |
|---|---|---|---|
| 1 | Mac PowerPC receiver positive control: one valid raw frame, then zlib members near each capacity boundary; the gmap height reader on a known-good map | `macos-ppc-receive-framing` line 56; `macos-ppc-receive-decompression` line 70; `gmap-heights-mac-ppc` line 90; `NEXT.md` line 304 | free |

### Lab host A, Lion or Sequoia VM

| # | What | Board rows | State |
|---|---|---|---|
| 1 | Mac 6.004 with its clock held before the beta limit, on the Sequoia guest | E#618 | free |
| 2 | An unchanged Mac client run to the context helpers, recording the real arguments | `NEXT.md` line 302 | free |

E#618's full answer needs a macOS 10.9-era guest with OpenGL. None is held; building one is
an owner call.

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
