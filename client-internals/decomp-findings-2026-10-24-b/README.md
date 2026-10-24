# Decompile findings, batch b (2.00, 2.17.1, 2.22, 2.31 + Drive clients), 2026-10-24

Derived facts only. No code, addresses or decompiler names. Lab-only runs (loopback network, private display). Built from decompiles of 2.00, 2.17.1, 2.22 and 2.31, plus the Drive clients set and lab captures.

| File | Content |
|---|---|
| 01-tamper-check-id39.md | how the 10 bytes of client PLI 39 are built; per-build words; when sent |
| 02-server-to-client-layouts.md | payloads for server ids above 48 and for 25, 39, 41, 44, 47, 156, 168-189; 2.17.1 vs 2.22 vs 2.31 |
| 03-periodic-ids-2.31.md | 2.31 timer: PLI 39 every 3.2 s, PLI 24, PLI 46 |
| 04-v2.00-client.md | 2.00 login, id tables, token allow-list, lab setup |
| 05-open-items.md | what is settled and what is still open |
| 06-crosscheck.md | new facts, confirmations and corrections against the repo |
| 07-lab-findings-46-186-200.md | lab: PLI 46 on every level entry, 186 trailer behaviour, 2.00 listserver handshake (observed vs synthetic) |
| ../drive-clients-inventory.md | what the Drive clients set contains; Wine status |

Tables (all under `version-profiles/`):

| File | Content |
|---|---|
| plo-layouts-217-231.tsv | one row per server id: fields, version gates, confidence |
| plo-handled-ids-by-build.tsv | handled server-to-client ids per build, 2.00 to 2.31 |
| pli-sent-ids-by-build-20x.tsv | client-to-server ids per 2.0x build |
| tampercheck-words.tsv | CRC words and lab bytes per build (companion to `version-profiles/tampercheck-values.tsv`) |
| version-tokens-by-build.tsv | login tokens per build |
| lab-enterlevel-231.tsv | PLI 46 sends of one 2.31 gmap run |
| lab-boardmodify2-186-trailer.tsv | `PLO_BOARDMODIFY2` trailer and length test cases (synthetic frames) |
| lab-200-listserver-handshake.tsv | 2.00 listserver and gserver handshake with provenance |
| drive-clients-exes.tsv | every exe in the Drive clients set (folder, size, PE file version) |
