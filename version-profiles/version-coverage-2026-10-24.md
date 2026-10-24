# Version coverage: is Graal_analysis enough for Seihai's multi-version selector?

Date: 2026-10-24 (Asia/Tokyo). Read-only review. No pushes, no PRs, no public connections.

> **Update (same day, after loopback lab runs with real 2.17, 2.22 and 2.31 clients):** the tampercheck gap below is closed. The constants for all three builds are in `tampercheck-values.tsv`, and the payload is 10 raw bytes, not two 32-bit words. The 2.17 listserver flow, the 2.22 gmap edge crossing, the mute payload and the client's short compressed gen-5 frames are now documented in `protocol/listserver.md`, `client-internals/feature-specs/06-gmap-overworld.md`, `.../14-friends-ignore.md` and `protocol/codec-and-framing.md`. 2.17 and 2.31 were accepted by the lab gserver with the merged Seihai. The table and gap list below are left as the original snapshot.
Reviewed: `squirelworks/Graal_analysis` main at 8da6800 (PRs #1 to #26 merged), `squirelworks/seihai` main at 3383300, plus the lab handoff notes and lab run directory (including the 2026-10-24 public 2.22 report) and `seihai_notes/`.
Only derived facts here: no decompile text, addresses, or internal function/data names.

## Short answer

**Yes for the protocol skeleton, no for full per-version behaviour.** Graal_analysis (PRs #24, #25, #26: `client-internals/version-profiles/*.toml` + `resolve.py`, `version-profiles/2.22-2.31.*`, `protocol/client-versions.md`, `version-tokens.md`, `version-id-map.md`) now has, per version, a token, client type, generation, listserver login, server-to-client id set, client-to-server id set, prop ranges, file-transfer flavour and level formats, each tagged bin / cap / srv / doc / inf. That is enough to *select* 1.33 through 2.31 and log in with the right token, cipher and framing. Seihai already has the abstraction (`ClientVersion`, 23 rows in `profile.rs`, `EncryptionGen` gates login and framing, `plo`/`pli` id sets gate dispatch and sends).

What is missing is mostly **payload layouts of the newer packets, the tampercheck content, and live confirmation** of everything except 2.05 and 2.22.

## What Graal_analysis covers

| Topic | Where | Coverage |
|---|---|---|
| Tokens, build to token | `version-tokens.md`, `version-id-map.md` | Complete 1.21 to 2.31 plus 3.x. 2.10-2.16 from gs2lib only |
| Game-server login (type, key byte, token, account, password) | `client-versions.md`, `login-and-walk.md` | 2.05, 2.17, 2.22, 2.31 from binaries. Older rows inherit |
| Generations | `codec-and-framing.md` | gen 2, 3 (2.05 verified on 704 messages), 5 (2.22 verified). Gen 4 (2.19-2.21) server-only |
| Gen-5 client send rules | `client-versions.md` | Size thresholds, XOR limits, queue cap |
| Listserver | `listserver.md` | 2.05 (id 0), 2.17 (id 0 then id 1, host from signed `arrays2.dat`), 2.22/2.31 (id 7 + `GNW30123` + gen 5) |
| PLO set per version | profile TOMLs | Read from binaries for 1.33-2.05 (24 exes), 2.17, 2.22, 2.31. Inferred for 2.1-2.16, 2.3 |
| PLI set per version | profile TOMLs | Binary for 1.41-2.05, 2.17, 2.22, 2.31; 2.22 has 3 unmatched ids (36, 42, 45). Inferred 2.1-2.16 |
| Packet id tables with payloads | `packet-ids.md`, `packet-layouts.md` | Names for all ids. Payload layouts good for 0-48 and 2.05 senders. Thin for 49 and 168-189 |
| Props (player, NPC, baddy) | `player-props.md`, TOML `props_max` | Good to 2.31 (X2/Y2/Z2 encoding documented). Other-player parser for 2.17 not read |
| File transfer | `file-transfer.md` | Complete for pre-2.1, 2.1-2.13, 2.14+. Large-file chunking from server source only |
| Levels | `level-binary*.md`, `glevnw01.txt`, `gmap.md`, `v3x-clients.md` | GR-V1.00-1.04, GLEVNW01, GRMAP001, `.gmap`. Per-version loader lists in TOML |
| Version differences (player-visible) | `version-profiles/README.md`, `2.22-2.31.md`, `feature-timeline.md` | Rich. HUD, windows, keys, GS1 command counts |
| UDP | `udp-p2p.md` | 2.05 captured. Other versions inherit |

## Seihai side: how versions are selected and gated

- `protocol/version.rs`: `ClientVersion` enum (1.33-1.39, 1.41, 1.42, 2.00, 2.01, 2.02, 2.05, 2.1, 2.12-2.16, 2.17, 2.22, 2.3, 2.31). `EncryptionGen` = Gen1/2/3/5.
- `protocol/profile.rs`: one `VersionProfile` row per version, built from templates `CLASSIC`, `BASE` (2.05), `NEW_2_1`, `GEN5`. Fields: client type, generation, listserver port and token, `plo`/`pli` IdSets, language and tampercheck flags, prop sets, file flags, level formats, UI flags, `Basis::{Binary,Inferred}`.
- `net/mod.rs`: `login_versioned` and `login_listserver` branch on `EncryptionGen`; sends are refused when the id is not in the row's `pli`; dispatch drops ids not in `plo`.
- The rows were written from the **earlier** notes (cross-version-timeline, client-versions), before the merged TOML profiles. So Seihai and the TOML disagree in places (below).

## Per-version table

(TSV copy: `version-coverage-2026-10-24.tsv`.)

| Version | Handshake known | Encryption / framing known | Packet table known | Gaps | Verdict |
|---|---|---|---|---|---|
| 2.00 (`GNW24011`) | Yes, bin: type 0, key byte, token, gen 3. List host `www.graalonline.com:14921` DES-hidden (dead; redirect needed) | Yes, gen 3 as 2.05 | PLO 51+2 ids and PLI from binary (4 revs, no differences). Prop parse 0-36 | Token absent from gs2lib: stock GServer-v2 treats it as unknown, so lab needs an allow-list patch. Login props unverified. Never run live. Seihai row reuses the 1.41 PLI set (includes 35/36 which first appear in 2.01) | **Partly**: enough to implement, untested |
| 2.05 rev 2 (`GNW03081`) | Yes, bin + lab | Yes, gen 3, 704 messages | Yes: PLO 59, PLI 0-24/26-30/32-38/80/81 | Port and host per listserver (built-in 14921 vs Reborn 14922/14923); lab patch maps it onto 2.1 behaviour; tampercheck absent | **Enough** |
| 2.01-2.04 (`GNW23021`, `GNW15041`, `GNW20041`, `GNW06051`, `GNW24061`) | Token yes (catalogue); login as 2.05 | Gen 3 | Binary for PLO/PLI deltas per build | Seihai has no 2.02 rev2, 2.03, 2.04 rows (language at 2.02 rev2, trigger at 2.03 not modelled); live untested | **Partly** |
| 2.1-2.16 (`GNW31101` ... `GNW12102`) | Tokens yes (gs2lib). Login inferred as gen 3 | Gen 3 inferred (2.17 is gen 3) | **Inferred** from neighbours and release notes | No binary of any 2.1x release in the archive. 2.1 test builds still send 2.05's token | **Needs binary or capture**; low priority, can ride on 2.05 or 2.17 |
| 2.17 (`GNW22122`, 2.171) | Yes, bin: type 0, gen 3, list via `arrays2.dat` (id 0 then id 1, host and port from file; port default 14922) | Yes, gen 3 | PLO 79, PLI 61 ids from binary; PLO 169-185 present | TAMPERCHECK (39) content untraced (two 32-bit words); other-player prop parser and GS1 count not read; not run live; Seihai `pli` for 2.17 omits 40, 41, 43, 44, 45 and its list port default is 14921 | **Partly** (login/framing enough; behaviour thin) |
| 2.22 (`GNW03014`; list `GNW30123`) | Yes, bin + lab + 4 public gservers + public listserver | Yes, bin + lab + public: 27/27 gserver frames and both list frames decode | PLO 80, PLI from binary (36, 42, 45 unmatched) | Payloads for ids 25, 39, 41, 44, 47, 156, 168, 174, 179, 180, 182 (sent by every public server) are names only; tampercheck is a 10-byte per-build constant (lab value known, not sent by Seihai; public servers did not kick within 20 s); client bz2 send path never seen; Seihai `pli` for 2.22 = 2.17 set (allows 36/38/81, refuses 40/41/43/44) | **Enough** to log in and play; **partly** for full parity |
| 2.3 (`GNW14015`) | Token yes; everything else inferred from 2.31 | Inferred (gen 5) | Inferred | No binary exists | **Partly** (treat as 2.31) |
| 2.31 (`GNW28015`) | Yes, bin: same code as 2.22, `GNW30123` for list | Yes, bin (same thresholds, XOR limits, queue cap) | PLO 81, PLI = 2.22 minus 21 plus 46 | Never run (lab or public); stock GServer-v2 has the token commented out; `MOVE2` (189), `LARGEFILESIZE` (84), `ENTERLEVEL` (46) layouts not documented; tampercheck value unknown; X2/Y2/Z2 encoding documented | **Partly**: one lab capture away from enough |
| 1.33-1.39 / 1.41 / 1.42 | Yes (bin, 1.39 lab-verified as gen 2) | Gen 2 (1.33-1.39), gen 3 (1.41+) | Binary per build | 1.41 list host unknown; no listserver before 1.41 | **Enough** for a selectable row |

## Concrete gaps, ranked

1. **Payload layouts of ids 49 and 168-189 (and 25, 39, 41, 44, 47, 156)** are names or one-liners in `packet-ids.md`. Needed for bigmap/minimap, ghost mode, serverwarp, RPG window, status list, process list, level heights, BOARDMODIFY2, MOVE2, LARGEFILESIZE. *Fillable now:* private public-server captures already on the lab box (never committed; all frames decoded) show most of these ids; the 2.17/2.22/2.31 exes + `.idc` name lists cover the handler arms for a cleaned note. 2.00 export is not needed.
2. **PLI_TAMPERCHECK (39) content** for 2.17, 2.22, 2.31. 2.22 has a lab constant in the TOML; 2.17 and 2.31 are unknown. *Fillable from* a static read of the builder in the `.exe`/`.idc` (2.171, 2.222, 2.31), or a lab capture of each real client under Wine. Needed before a stricter server enforces it.
3. **Seihai rows lag the merged TOMLs.** 2.22/2.31 `pli` should follow the binary list (2.22: no 36/38/81, adds 40/41/43/44; 2.31: minus 21 plus 46); 2.17 `pli` should add 34-36, 40, 41, 43-45; 2.00 should not send 35/36; no rows for 2.02 rev2, 2.03, 2.04; 2.17 listserver port. *Fillable now*: no decompile needed. Wire `resolve.py` output into `profile.rs` (or a generated table).
4. **Doc conflict on the gen-5 XOR group rule.** `codec-and-framing.md` and `client-versions.md` still say `floor(n/4)` capped at 4 for types 4 and 6. Lab (610 frames) and public (27 frames) show one step per group present, a partial last group included. The doc needs correcting, with a note of which side (client send vs server) was read. Also the client-originated bz2 frame (>= 0x1000) is unseen. *Fillable now* from existing captures and the 2.22 `.idc`.
5. **2.1-2.16 and 2.3 have no binary.** Rows are inferred. *Needs new binaries*; nothing on the box covers them. Practical fix: mark them as aliases of 2.05 (2.1 line) or 2.31 (2.3) in the UI.
6. **Live acceptance is unknown for everything except 2.22.** Public Reborn servers may reject 2.17, 2.31, 2.05 or 2.00 tokens, and may treat a missing tampercheck differently. Stock GServer-v2 allows 2.22 only by default. *Needs captures*: lab runs for 2.00 (allow-list patch), 2.17, 2.31 with the real Wine clients; public runs need explicit approval.
7. **Listserver per version.** 2.17 id 0 + id 1 against the Reborn listserver on 14922 is untested; 2.05/2.00 depend on a host redirect. Port should be per-profile and overridable. Needs one capture, not a decompile.
8. **Smaller:** 2.22 PLI ids 36, 42, 45 call sites unmatched; 2.17 other-player prop parser unread; 2.22 `#R` GS1 code meaning; 2.1-2.16 GS1 counts.

## Which gaps the existing exports can fill

| Source on the box | Fills |
|---|---|
| `donors/Graal_2171.exe` + `.idc` + `.names.tsv` | 2.17 tampercheck builder, other-player prop parser, PLI send sites, `arrays2.dat` handling |
| `donors/Graal_222.exe` + `.idc` | Payload layouts for ids above 48, PLI sites 36/42/45, tampercheck, client bz2 path |
| `donors/Graal_231.exe` + `.idc` | `MOVE2`, `LARGEFILESIZE`, `ENTERLEVEL`, 2.31 tampercheck |
| `donors/Graal_v2_00.c` (2.00 export, 193k lines) | 2.00 PLI set cross-check, login props, 2.00 level and prop details |
| Existing public pcaps (box only, never commit) | Payload shapes of 25, 39, 41, 44, 47, 156, 168, 174, 179, 180, 182 and the bigmap/minimap messages |
| **New captures** | Anything about 2.31 and 2.17 live behaviour, 2.00 against a patched lab server, other-player parser behaviour, public acceptance of tokens |
| **New binaries** | 2.1 to 2.16, 2.3 |

Note: the `.idc` files are name tables. Reading the handler bodies still needs a disassembler pass (Ghidra) over the matching `.exe`.

## Recommendation

1. Treat 2.05, 2.22 as the verified baseline; 2.17 and 2.31 as selectable now with "partly" labels.
2. Regenerate the Seihai rows from the TOML (gap 3), then fix the XOR note (gap 4). Both are doc/data work with no new decompile.
3. Run one Ghidra pass each over 2.22 and 2.31 for gaps 1 and 2, write a cleaned note per version, then lab-capture real 2.17 and 2.31 clients to confirm.
4. Ask for approval before any public run for 2.17, 2.31 or 2.05.

## Status update, 2026-10-24 (decompile pass of 2.00, 2.17.1, 2.22, 2.31 and the Drive clients set)

- **Gap 1 (payload layouts of ids above 48 and 25, 39, 41, 44, 47, 156):** closed for 2.17.1, 2.22 and 2.31, except three small items (`PLO_SERVERWARP` field meanings, the `PLO_BOARDMODIFY2` trailer, the extra step 2.31 adds in 156). See `protocol/packet-layouts.md` and `plo-layouts-217-231.tsv`.
- **Gap 2 (tamper-check content):** the lab values for 2.17, 2.22 and 2.31 are in `tampercheck-values.tsv`, and the builder is now understood: two chained CRC-32 words over the client's own memory image (`tampercheck-words.tsv`; `client-internals/decomp-findings-2026-10-24-b/01-tamper-check-id39.md`). Whether any server enforces it is still unknown.
- **Gap 6 (2.00):** a real 2.00 exe and three revisions are in the Drive clients set. The "allow-list patch" wording above means a config entry only: the lab server needs `GNW24011` in its allowed-versions list, no code patch (`client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md`). The 2.00 client still needs its list host redirected to the lab listserver, and its listserver frames have not been exercised.
- **Gap 5 (2.1 to 2.16 and 2.3):** unchanged. The Drive clients set has no 2.1.x to 2.3 builds, only the two 2.1 test builds (`client-internals/drive-clients-inventory.md`).
- **Gap 8:** client to server ids 36, 42 and 45 of 2.22 are still unmatched to call sites.
- Per-build handled server-to-client ids for 2.00 to 2.31 are now tabulated in `plo-handled-ids-by-build.tsv`, and the client-to-server ids per 2.0x build in `pli-sent-ids-by-build-20x.tsv` (2.00 lacks 35 to 38).
