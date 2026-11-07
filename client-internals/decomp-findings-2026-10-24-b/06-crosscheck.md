# Cross-check against the repo (after PRs #30 and #31)

## New facts (not in the repo before this pass, or only marked unverified)
- Tamper-check derivation: two chained CRC-32 words over the client's own memory, 5-byte non-GINT5 encoding with unmasked middle bytes. All six lab values reproduced. Words per build: `version-profiles/tampercheck-words.tsv`.
- 2.31 timer: a counter modulo 64 on a 50 ms timer gives 3.2 s; phases 1, 10, 20, 30, 31 (probe, CRC A, window scan, CRC B, send). The 3.2 s is derived, not only observed.
- Payload layouts for every server id above 48 plus 25, 39, 41, 47, 156, 165, 166, 168 to 189 that the repo had as names or blank cells: `version-profiles/plo-layouts-217-231.tsv`. Notable: 49 (x and y halved, z unused, gmap cell, then level), 75 (length-prefixed fields), 150, 171 and 172 (comma text, at least 4 fields), 178 (at least 4 comma fields, 1 to 3 used), 181, 182 and 183 reply ids (client 44 and 45), 184 (only `.png`), 185 (height cell formula), 186 (GSHORT tiles).
- `PLO_SIGNATURE` (25) semantics: value 1 quits; value 0 quits unless the host is the loopback address.
- Login tokens for the whole 2.0x family are confirmed from the binaries and all match the repo (`version-profiles/version-tokens-by-build.tsv`).
- Client to server id sets per 2.0x build (`version-profiles/pli-sent-ids-by-build-20x.tsv`): 2.00 lacks 35 to 38; 35 and 36 arrive in 2.01, 37 in 2.02 rev2, 38 in 2.03.
- 2.31 `PLO_LEVELNAME` (6) now also compares against the current level; 68 clears the stored file size; 156 has an extra step.
- 2.00: login string shape with plain account and password, no `arrays2.dat`, and runs under Wine once the data files are supplied.
- `PLO_NPCACTION` (26) is handled by 2.00 to 2.03 only.

## Confirmations
- Handled-id set sizes (80 for 2.22, 81 for 2.31; 2.31 drops 44, adds 84 and 189) match `version-profiles/2.22-2.31.md` and `protocol/client-versions.md`.
- The 2.1 test builds send the 2.05 token, as `client-internals/version-id-map.md` says.
- The `protocol/packet-ids.md` names for 168 to 189 match the 2.22 and 2.31 behaviour (ghost, minimap, kingdoms, new world mode, serverwarp, RPG window, status list, process list, screenshot, board heights, board modify 2).
- 2.31 dropping 44 is consistent with the `protocol/packet-ids.md` note "client 5.07+ ignores it".
- The 10-raw-bytes description of PLI 39 (PR #30) is explained by the unmasked encoding.

## Corrections made in this change
- `PLO_HIDENPCS` (151): was "probably removes NPCs with id < 1000"; decoded as ids 1 to 999 of the active level.
- `version-profiles/version-coverage-2026-10-24.md` and `client-internals/version-profiles/141-217.toml` say a lab needs an allow-list "patch" for 2.00. A plain allow-list config entry is enough (`04-v2.00-client.md`). The report now carries a status update; the TOML note is unchanged (it only says stock GServer-v2 treats the token as unknown, which is still true).
- `version-profiles/2.22-2.31.md` lists client to server ids 36, 42 and 45 as unmatched; that is still true (this pass did not scan 2.17/2.22/2.31 send sites). Listed in `05-open-items.md`.

## Corrected by batch c
- Id 6 (`PLI_TOALL`) is a real sender in every 2.0x build, not a possible scan artefact (`04-v2.00-client.md` corrected).
- 2.04 only drops id 26; id 25 is handled in every build. Nothing is swapped.
- The 2.00 builds (r0 to r3) share handler shapes and one token. Batch c supersedes the 2.00 and 2.05 statements here where they differ: `../decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md`.
