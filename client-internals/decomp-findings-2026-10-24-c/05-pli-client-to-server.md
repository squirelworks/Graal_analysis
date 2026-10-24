# 05 Client-to-server ids (PLI) per build

Table: `pli_sent_ids_by_build.tsv`; adds/removes in `id_changes_between_builds.tsv`. Names are from the repo's `packet-ids.md`.

| build | ids with a direct send | count |
|---|---|---|
| 2.00 (and rev1-3) | 0-24, 26-30, 32-34, 80-81 | 35 |
| 2.01, 2.01 rev1, 2.02, 2.02 rev1 | + 35, 36 | 37 |
| 2.02 rev2 | + 37 | 38 |
| 2.03 to 2.1 test3 | + 38 | 39 |

- 35 = ADJACENTLEVEL (matches the 2.01 changelog "levels are preloaded when you walk on the map"). The payload is a string taken from the neighbouring level object, completed with a second computed string [layout not decoded].
- 36 = HITOBJECTS (2.01; script variable `hitobjects` appears in the same build). [inferred] It is the TCP twin of UDP id 25: the same function first sends id 25 through the peer-channel wrapper, then repeats the message over TCP under 36 when a flag says the server needs it. That agrees with the routing rule in `udp-p2p.md`.
- 37 = LANGUAGE (2.02 rev2; also sent once right after login).
- 38 = TRIGGERACTION (2.03; twin of UDP id 26 in the same way as 36/25 [inferred]). Matches the 2.03 changelog.
- 6 = TOALL (chat) is a real sender in every build. Chat text is clipped to 200 characters before sending. The batch-b remark that 6 could be a scan artefact is withdrawn.
- 80/81 (profile get/set) are present from 2.00 on.
- No direct constant send exists for 25, 31, or any id from 39 up in any 2.0x or 2.1-test build. So the tamper check (39) and the later periodic ids are not part of this family. 42 and 45 never appear.
- No PLI id was removed anywhere in the 2.00 to 2.1 line.

## NewWorld / NewMain
- NewWorld beta1/2: 34 ids. They have 35-38 but lack 7 (HORSEADD), 11 (THROWCARRIED), 15 (BADDYPROPS), 16 (BADDYHURT) and 17 (BADDYADD): horses and baddies are removed from the game in NewWorld.
- NewMain 24/26: 35 ids, same as 2.00 (0-24, 26-30, 32-34, 80-81). They lack 35-38, in line with their older token.
