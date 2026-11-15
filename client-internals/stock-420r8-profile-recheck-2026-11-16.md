# Stock Windows 4.20r8 engine: profile re-check

Date: 2026-11-16. Static only. Nothing was run against a live server. Tags: **[bin]** · **[inf]**.

Evidence: owner-held Windows 4.20r8 "Unpacked" archive (same family as
`CLIENT-HUNT-4X5X-20261113`), opened privately for this pass; compared with the
Packet Logger v2 engine already summarised in
[launchers-420r8-500r7-512.md](launchers-420r8-500r7-512.md) and
[protocol/v4x-clients.md](../protocol/v4x-clients.md).

## Short answer

The stock Windows 4.20r8 `GraalEngine.dll` is readable. Against the Packet Logger
copy it differs only in the known third-party edits (signature-check bypass plus
the zlib hook and the added logger block). Every other engine behaviour the 4.x
notes already published from the Packet Logger copy is stock 4.20r8. **[bin]**

That clears the seihai-core profile-audit uncertainty that said "only the
modified engine DLL was readable; the stock 4.20r8 is in a password-protected
archive" for the 4.20r8 rows. It does **not** by itself promote every carried
value to a fresh native read: some rows still inherit older builds and stay
carried until those fields are re-derived on this binary or in a lab.

## What was compared

- Stock engine and Packet Logger engine: same file size and same PE link time.
- Byte compare: **290** differing bytes, all in the code section. Read-only and
  data sections match. **[bin]**
- Strings present only in the Packet Logger copy: the packet-logger DLL name and
  its three log entry names (plus the spare outgoing name). Stock has none of
  those. **[bin]**
- The three edits match the earlier launcher note: one unconditional jump that
  skips a failed library signature, an eight-byte jump out of zlib's success
  return, and the added loader block in what was zero padding. **[bin]**

No other behavioural surface changed.

## Scanners re-run on the stock engine

Same tools and bounds as the published 4.x notes. Results match the Packet
Logger re-check and the tables already in `protocol/v4x-clients.md`:

| Check | Stock result |
| --- | --- |
| Login token (`g3dref`) | `G3D20126` |
| Receive switch | 99 cases through 196; 100 and 108 still taken before the switch → **101** handled server ids, same set as before |
| Self / other-player prop switches (bound 81) | Same case sets as the 4.x prop table |
| NPC prop switch (bound 77) | Same case set as the 4.x prop table |
| Baddy prop switches (bound 10) | Cases 0–10 |
| GS1 command list (`gs1scan` x86) | 191 names, identical to the Packet Logger engine |

Gen-5 framing, login machine fields, update-package magic, gmap/level magics,
license-file names, and the window-enumeration send path for the tamper messages
are unchanged relative to the Packet Logger engine because those code and data
are outside the 290-byte edit. **[bin][inf]**

## Profile rows that rested on the modified engine

seihai-core `documentation/profile-audit.tsv` has **52** `4.20r8` rows whose notes
flagged the stock archive as unreadable (about 45 distinct profile fields once
duplicates across wording are ignored; the audit lists 52 lines). This pass
re-checked them against stock as follows.

### Cleared: archive uncertainty

For every one of those 52 lines, the stock engine is now the authority for
"what 4.20r8's engine contains." The Packet Logger-only caveat no longer
applies. Prefer the stock copy for any future static read. **[bin]**

### Confirmed on stock today (native engine surfaces)

These match the published 4.x tables and were re-scanned on stock:

- `protocol/plo (server ids handled)` — 101 ids, including 196.
- `protocol/login lobby` — Login-session behaviour already tied to this engine
  (id 190 / lister path); stock matches the earlier read.
- Prop parsers: `props/own-player props`, `props/other-player props` (and the
  related NPC/baddy case sets used with them).
- `protocol/gen5_round_down` — compressed bodies still use floor steps; stock
  and Packet Logger agree.
- `scripts/gs1` — same 191-name list.
- `protocol/encryption` / framing companions that live in this engine — same
  code as Packet Logger outside the logger hook.
- `protocol/listserver` / Login-host path, `protocol/login frame` machine-field
  layout, `protocol/tamper` / `tampercheck` window-list answers, `protocol/showimg
  (id 24)`, `levels/gmap`, `levels/nw`, file-magic / large-transfer helpers, UDP
  support strings — all sit outside the Packet Logger edit, so stock confirms
  the earlier engine reads. **[bin]**

`protocol/pli (client ids sent)` stays a **floor**: some sends still pass the id
in a register. Stock does not widen that set beyond what the Packet Logger copy
already showed. **[bin][inf]**

### Still carried (or inferred), but no longer "stock unknown"

These rows keep their older `set_by` build and their carried/inferred basis.
Stock availability removes only the archive flag; it does not invent a new
native measurement for combat, drops, mannerisms, HUD chrome, and other fields
that were never re-derived in the 4.20r8 engine itself:

- UI / life / world / drops / mannerisms rows carried from 1.x–2.x.
- Inferred 2.1 / 2.3 file and UI steps (`files/*` inferred lines, `ui/minimap`,
  `ui/log_window`, `ui/ghost_mode`, `ui/editor`, `props/bow_prop10`, `life/death`).
- `scripts/gs2` remains the published 4.20r8 VM table (including opcode 11); this
  pass did not re-walk the GS2 interpreter beyond confirming the engine text is
  stock outside the logger patch. **[bin][inf]**

## What this does not claim

- No live 4.20r8 session was run here. Wire confirmation of framing and Login
  machine fields stays with earlier labs where those exist.
- The Packet Logger bypass of `sig.graallib` is still third-party behaviour, not
  stock. Stock keeps the library signature check. **[bin]**
- seihai-core's audit TSV is not edited in this repository; consumers should
  drop the archive caveat when they next refresh that table from these notes.

## Cross-links

- [launchers-420r8-500r7-512.md](launchers-420r8-500r7-512.md) — launcher identity
  and the Packet Logger diff.
- [protocol/v4x-clients.md](../protocol/v4x-clients.md) — protocol and prop tables
  now backed by the stock engine as well as the Packet Logger copy.
