<!-- manual: kind=reference status=draft -->
# 2.4 PLI message reference (client to server)

Field notation is in → §0.6, the message envelope in → §2.1.2, and the login message (the first message of a connection) in → §2.3. Server-to-client messages are in → §2.5, prop streams in → §2.6, and the staff tools' own ids in → §7. Every id, with its wire byte, is indexed in → App. A.

> Status: draft. Layouts are given where a note measured or read them; ids with no layout in the notes say `unmeasured`.

## 2.4.1 Conventions

Every client-to-server message (PLI) follows the same few rules. The table states them once, with the builds they hold for, so the chapter's per-message tables need not repeat them [srv][2.05] (protocol/packet-layouts.md).

| Rule | Builds | Source |
| --- | --- | --- |
| A PLI is `GCHAR(id)`, the payload, then `\n`, sent inside the frame of the build's generation | 1.21 to 6.x | [srv][2.05] (protocol/packet-layouts.md); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Ids are logical; the wire byte is the id + `0x20` | all binary generations | [srv] (protocol/packet-ids.md) |
| Coordinates marked `x×2` are half-tiles; the receiver divides by 2 | 2.05 and the server | [srv][2.05] (protocol/packet-layouts.md) |
| Id 0 is overloaded: the login line starts with GCHAR 0 because that byte is the client type, and later `PLI_LEVELWARP` messages also use id 0; the server tells them apart by connection state | 2.x | [srv][2.05] (protocol/packet-ids.md#client--server-pli_) |
| In 6.x the login message is sent under id 5 (`PLI_BOMBDEL`) inside the mode-3 frame | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 6.x sends every PLI through one send method taking `(id, body)`; it writes `id + 32`, the body and `\n` | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Before ids 93 and 163, 6.x first sends id 50 (`PLI_RAWDATA`) with a 3-byte length (three 7-bit groups, capped at `0x37FFFF`) | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Before a long id 93 payload, 4.20r8 and 5.00r7 send id 50 with an `i3` length | 4.20r8, 5.00r7 | [bin] (protocol/v4x-clients.md#cipher-and-framing); [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| A server re-emits most level-object PLIs to the rest of the level with `s player id` added in front; the PLO forms are in §2.5 | server | [srv] (protocol/packet-layouts.md#combat-and-objects-both-directions) |

What a server does with an id it does not handle is its own choice, and clients do not depend on it. Our GServer-v2 build (GS2Emu 4.0.0-beta) was swept with every id 0–223 and an empty body from a live 6.03r7 session; the rows record that build's behaviour as a reference point for a clean-room server [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build).

| Observation | Server | Source |
| --- | --- | --- |
| Handled: 0–41, 44, 46–48, 50, 80, 81, 130, 152, 154, 157–159, 161 and 223; every other id from 18 to 223 is unknown to it, the RC range 51–79 included | GServer-v2 | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| An unknown id is logged and counted; after three, the server sends `PLO_DISCMESSAGE` ("Disconnected for sending invalid packets.") and drops the client, and 6.03r7 logs in again by itself | GServer-v2 | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| Four handled ids do not check an empty body: 17 (`PLI_BADDYADD`) reads its missing fields as `0 − 32` and makes a type-224 baddy that ends the 6.03r7 session; 31, 41 and 130 log junk values and continue. A server should check each body's length, and a baddy's type, before acting | GServer-v2 | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |
| Empty 34 gets `PLO_FILEUPTODATE`, empty 159 gets 105 and 106, and 39 (`PLI_TAMPERCHECK`) gets no reply and no log line (→ App. E#320) | GServer-v2 | [lab][srv] (protocol/probe-targets-2026-11-18.md#server-side-every-clientserver-id-at-our-gserver-v2-build) |

Whether a level-object PLI also goes, or only goes, over the UDP peer channel is in → §2.9.

## 2.4.2 Ids sent by build

The *First sent* column of the tables below names the earliest build in this table that sends the id; a later gap is noted only where the later list is complete. A list marked *floor* holds only the ids the binary passes to its send routine as constants; sends that pass the id in a register are not counted [bin] (client-internals/version-profiles/v121-v132.toml).

| Build | Ids sent | Complete? | Source |
| --- | --- | --- | --- |
| 1.21 | 0–13, 15–26 | yes: every send passes a constant id (→ §2.4.2) | [bin] (client-internals/version-profiles/v121-v132.toml); [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |
| 1.28 beta 2 | 0, 15–21, 23, 25, 28, 29 | floor (fewer constants than 1.21 for the reason above) | [bin] (client-internals/version-profiles/v121-v132.toml) |
| 1.3 test | 0, 14–21, 23, 25, 28–30 | floor | [bin] (client-internals/version-profiles/v121-v132.toml) |
| 1.31 | 0, 10–21, 23–30 | floor | [bin] (client-internals/version-profiles/v121-v132.toml) |
| 1.32 | 0–30 | yes: every send passes a constant id (→ §2.4.2) | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |
| 1.33 to 1.37 | 0–31 | yes for constant ids; a few register sends uncounted | [bin] (client-internals/version-profiles/v133-v139.toml) |
| 1.38 | 0–24, 26–33 | as above | [bin] (client-internals/version-profiles/v133-v139.toml) |
| 1.39 | 0–24, 26–33, 80, 81 | as above | [bin] (client-internals/version-profiles/v133-v139.toml) |
| 1.41 rev1 | 0–24, 26–30, 32, 33, 80, 81 | yes: every game-client send passes a constant id | [bin] (client-internals/version-profiles/141-217.toml) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| 1.42 (NewMain), NewMain 24 and 26, 2.00 (rev0–rev3) | 0–24, 26–30, 32–34, 80, 81 | yes: every game-client send passes a constant id | [bin] (client-internals/version-profiles/141-217.toml); [bin] (version-profiles/pli-sent-ids-by-build-20x.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/pli_sent_ids_by_build.tsv) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| 2.01 (+rev1), 2.02, 2.02 rev1 | 0–24, 26–30, 32–36, 80, 81 | yes: every game-client send passes a constant id | [bin] (version-profiles/pli-sent-ids-by-build-20x.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/pli_sent_ids_by_build.tsv) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| 2.02 rev2 | 0–24, 26–30, 32–37, 80, 81 | yes: every game-client send passes a constant id | [bin] (version-profiles/pli-sent-ids-by-build-20x.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/pli_sent_ids_by_build.tsv) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| 2.03, 2.04, 2.05 (rev0–rev2), 2.1 test 2 and test 3 | 0–24, 26–30, 32–38, 80, 81 | yes: every game-client send passes a constant id | [bin] (version-profiles/pli-sent-ids-by-build-20x.tsv) ; [bin] (client-internals/decomp-findings-2026-10-24-c/pli_sent_ids_by_build.tsv) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| NewWorld beta 1, beta 2 | the 2.1 test set without 7, 8, 11, 15, 16, 17, 20; settled → §2.4.2 | yes: no send passes the id in a register; neither beta sends 8 or 20 | [bin] (client-internals/version-profiles/141-217.toml); [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| 2.14 to 2.16 | profile hypothesis: the inherited 2.1-line set plus 41 | inferred; no exact 2.14–2.16 send-site read or outgoing capture establishes this set | [inf] (protocol/client-id-inference-scope.md#214216-retain-the-send-set-hypothesis) |
| 2.17 (the 2.17.1 binary) | 0–24, 26–30, 32–41, 43–45, 80, 81 | yes: every game-client send passes a constant id | [bin] (client-internals/version-profiles/141-217.toml) ; [bin] (version-profiles/pli-send-sites-141-217.md#result) |
| 2.22 | 0–24, 26–30, 32–35, 37–41, 43, 44, 80 | floor; 36, 42 and 45 not matched to a call site | [bin][cap] (version-profiles/2.22-2.31.md#wire-protocol); [bin] (version-profiles/2.22-2.31.toml) |
| 2.31 | the 2.22 set without 21, plus 46 | floor | [bin][cap] (version-profiles/2.22-2.31.md#wire-protocol); [bin] (version-profiles/2.22-2.31.toml) |
| 3.04 (Linux) | 0–24, 26–30, 32–38, 40, 41, 43, 80, 81 | yes, every game-code send site; listserver sends excluded | [bin] (version-profiles/3.04-3.153.md#client--server-ids); [bin] (version-profiles/3.04-3.153.toml) |
| 3.153 (Mac OS X) | the 3.04 set plus 46, 50, 93, 96–98, 152, 154–158 | no: 2, 3, 15, 24, 29 and 80 assumed from 3.04 | [bin][inf] (version-profiles/3.04-3.153.md#client--server-ids) |
| 4.04r2 | 1, 2, 4–10, 12–19, 21–24, 26, 28, 29, 32, 33, 35–37, 41, 44, 50, 79–81, 92, 96, 130, 152, 154, 157, 158, 161 | floor | [inf][cap] (version-profiles/4.04-4.20.toml) |
| 4.20r6 (Mac) | the 4.04r2 set plus 34, 46, 162 | floor | [inf][cap] (version-profiles/4.04-4.20.toml) |
| 4.20r8 | 1, 2, 4–10, 12–19, 21–24, 26, 28, 29, 32, 33, 35–37, 41, 44, 50, 79–81, 92, 96, 130, 152, 154, 157, 158, 161, 162 | floor; some sends pass the id in a register | [bin] (protocol/v4x-clients.md#client--server-ids); [bin] (version-profiles/4.04-4.20.toml) |
| 5.00r7 | 1, 2, 4–10, 12–19, 21–24, 26, 28, 29, 32–37, 41, 44, 47, 50, 79–81, 92, 93, 96–98, 130, 152, 154–159, 161 | floor; also sends 11 with an empty body on a throw (→ §2.4.2) | [bin] (protocol/v5x-clients.md#client--server-ids-500r7); [bin][cap] (version-profiles/5.00-6.03.toml); [lab] (protocol/lab-appe-hostb-2026-11-20.md#throw-id-on-500r7-e4) |
| 5.12 | 1, 2, 11, 23, 24, 34, 37, 38, 44, 47, 157 (seen in capture) | floor | [cap] (version-profiles/5.00-6.03.toml) |
| 5.24r4 | the 5.12 set plus 158 (seen in capture) | floor | [cap] (version-profiles/5.00-6.03.toml) |
| 5.30r3 | 1, 11, 37, 38 (seen in capture) | floor | [cap] (version-profiles/5.00-6.03.toml) |
| 5.31r4 | 2, 37 (seen in capture) | floor | [cap] (version-profiles/5.00-6.03.toml) |
| 6.00r2, 6.00r4 Windows | proposed: 0–20, 22–24, 26–30, 32–38, 41, 44–48, 50, 79, 92, 93, 96–98, 130, 152, 154–159, 161, 162 | inferred from Linux 6.01r1; their own receive-switch reads and login observations do not establish this outgoing set | [inf] (protocol/client-id-inference-scope.md#windows-600r2r4-receive-reads-do-not-settle-outgoing-ids) |
| 6.015 Windows profile (6.007 / 6.015 builds) | same proposed set as the preceding row | inferred from Linux 6.01r1; the captured Windows token association does not validate packet sets; excludes Mac 6.015 | [inf] (protocol/client-id-inference-scope.md#windows-60076015-and-mac-6015-separate-the-identities) |
| 6.01r1 | the 6.03r7 set without 160 | unmeasured | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 6.034 | as 6.03r7 | inferred | [inf] (version-profiles/5.00-6.03.toml) |
| 6.03r7 | 0–20, 22–24, 26–30, 32–38, 41, 44–48, 50, 79, 92, 93, 96–98, 130, 152, 154–162 | yes | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (version-profiles/5.00-6.03.toml) |

Token associations, receive-switch ids and outgoing sets have separate evidence. The 2.14–2.16 and Windows 6.00r2/r4/6.015 rows above remain hypotheses; a named sibling's complete set does not make them complete. Windows 6.007 and 6.015 now have a captured token association, superseding the profile's earlier “never captured” description, while their packet-set inference flags remain [inf][cap] (protocol/client-id-inference-scope.md).

**Settled question, formerly E#4: Whether 5.00r7 sends id 11.** Whether 5.00r7 sends `PLI_THROWCARRIED` (11) when the player throws was open, because two lists of its sent ids disagreed; a lab throw with the id recorded settled it [lab] (protocol/lab-appe-hostb-2026-11-20.md#throw-id-on-500r7-e4).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the send wrappers have no 11. B: the profile lists 11, and 5.12, 5.24r4 and 5.30r3 captures send it | [bin] (protocol/v5x-clients.md#client--server-ids-500r7); [bin][cap] (version-profiles/5.00-6.03.toml) |
| Before | A static read found the backup engine's throw path sending 11 with an empty body | [bin] (client-internals/windows-404r2-500r7-static-2026-11-09.md#500r7-sends-id-11-when-throwing) |
| Settled | An unchanged 5.00r7, reaching the lab through a connect shim with its licence untouched, sent 11 with an empty body on each of 2 throws, after the lift's board change and ganis | [lab] (protocol/lab-appe-hostb-2026-11-20.md#throw-id-on-500r7-e4) |
| Verdict | Verified: Claim B holds; the wrapper list missed the throw path | [lab] (protocol/lab-appe-hostb-2026-11-20.md#throw-id-on-500r7-e4) |

**Settled question, formerly E#6: client-to-server constants of 1.21 and 1.32.** Whether 1.21 sends id 14 and 1.32 sends id 22 was open, because two reads of their send sites disagreed; a static read of both send routines settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | Claim A: 0 and 10 to 26 in 1.21, 0 and 10 to 30 in 1.32. Claim B (profile): no 14 in 1.21, no 22 in 1.32. Best guess: neither is sent | [bin] (protocol/gserv-1999.md#message-ids); [bin] (client-internals/version-profiles/v121-v132.toml) |
| Settled | Every call to each build's send routine passes a constant id. 1.21 sends 0 to 13 and 15 to 26 (no 14). 1.32 sends 0 to 30, so it sends both 14 and 22; its 22 goes out when a list lookup finds no match, its 29 when one does | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |
| Verdict | Half right: the profile is right for 1.21 and missed 22 in 1.32. Both claims also left out 1 to 9, which both builds send | [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |
| Left over | What 14 and 22 carry in these builds | [inf] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6) |

**Settled question, formerly E#11: client-to-server ids the NewWorld betas lack.** Two reads disagreed on whether the NewWorld betas send ids 8 and 20 [bin] (client-internals/version-profiles/141-217.toml).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The betas send the 2.1 test set without 7, 8, 11, 15, 16, 17 and 20 | [bin] (client-internals/version-profiles/141-217.toml) |
| Claim B | The betas send 34 ids, the 2.1 test set without 7, 11, 15, 16 and 17 only | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| Settled | Claim A: every send site in both betas was re-read; none sends 8 or 20 (nor 7, 11, 15, 16, 17), none passes the id in a register, and the betas send 32 ids | [bin] (version-profiles/pli-send-sites-141-217.md#newworld-betas-ids-8-and-20-app-e11) |
| Note | Claim B's count of 34 was 39 less five, the arithmetic that hid the gap | [inf] (client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md) |

The id table above says which ids a build can send. The rules below add the exceptions found in particular builds: ids with no sender, ids a family drops or adds, and a limit on one sender [2.05] (protocol/packet-ids.md#client--server-pli_).

| Rule | Builds | Source |
| --- | --- | --- |
| No sender was found for 25 (`PLI_TOWEAPON`) or 31 (`PLI_PACKETCOUNT`) | 2.05 | [2.05] (protocol/packet-ids.md#client--server-pli_) |
| 6.x sends none of 21 (`PUTNPC`), 25, 31, 39 (`TAMPERCHECK`) or 40 (`SHOOT`) as a constant | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 3.04 and 3.153 send no 39 or 44, unlike their Windows twin, and add 36 and 81 | 3.04, 3.153 | [bin] (version-profiles/3.04-3.153.md#client--server-ids) |
| 6 (`PLI_TOALL`) is a real sender in every build of the family, with the chat text cut to 200 characters before sending | 2.00 to 2.1 test | [bin] (client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md); [bin] (client-internals/decomp-findings-2026-10-24-c/10-open-questions-and-corrections.md#corrections-to-batch-b--earlier-notes) |
| No id is removed anywhere from 2.00 to 2.1 test 3, and none of 25, 31 or any id from 39 up has a constant send, so the tamper check (39) is not part of this family | 2.00 to 2.1 test | [bin] (client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md); [bin] (client-internals/decomp-findings-2026-10-24-c/id_changes_between_builds.tsv) |
| 36 and 38 look like TCP copies of UDP 25 and 26: one routine sends the UDP message, then repeats it over TCP when a flag says the server needs it; what sets the flag is unknown | 2.01 to 2.1 test | [inf] (client-internals/decomp-findings-2026-10-24-c/05-pli-client-to-server.md) |
| 2.02 rev1 has no `PLI_LANGUAGE` (37) send site and sends none in the lab; rev2 is the first build that sends 37 | 2.02 rev1, rev2 | [bin][cap] (client-internals/version-profiles/141-217.toml) |
| Ids 4.x adds over 3.x: 44 (window list for PLO 182), 50 (large-packet length), 157 and 161 (file requests carrying an `i5` time), 158 (weapon by name), 162 | 4.20r8 | [bin] (protocol/v4x-clients.md#client--server-ids) |

A full read of the 1.21 and 1.32 send routines settled the earlier disagreement: 1.21 never sends 14, and 1.32 sends 22. Both also send 1 to 9 [bin] (client-internals/static-reads-appendix-e-2026-11-20.md#client-to-server-ids-of-121-and-132-e6).

The six Graal 2002 inputs in §1.1.5 were read for their send sites. ver7, ver8 and ver9 send 0–6, 9, 10, 12–14, 18, 19, 21–24, 26–30, 32–38, 80 and 81; ver10 and ver13 add 39; v22 sends 0–24, 26–30, 32–39, 80 and 81. ver7 to ver13 never send 7, 8, 11, 15, 16, 17 or 20, which matches their receive side. The token does not predict the set, so do not assign the 2.1 test or 2.17.1 row to these builds; when each id is sent is still open in App. E#15 [bin] (client-internals/static-reads-appendix-e-2026-11-20-hostb-final.md#client-to-server-ids-of-the-six-graal-2002-builds-e15-send-sites).

## 2.4.3 Level navigation

These are the messages a client sends to move between levels and servers. Each row gives the id and name, the payload layout, the first build that sends it, and what the server does in reply [srv][2.05] (protocol/packet-layouts.md#level-navigation-client--server).

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 0 | `PLI_LEVELWARP` | `c x×2, c y×2`, `rest` = level name | 1.21 | warps the player and sends the level (→ §2.5) | [srv][2.05] (protocol/packet-layouts.md#level-navigation-client--server) |
| 30 | `PLI_LEVELWARPMOD` | `i5 modtime, c x×2, c y×2`, `rest` = level name | 1.3 test | as 0, but the server can answer with only the changes since `modtime` | [srv][2.05] (protocol/packet-layouts.md#level-navigation-client--server) |
| 35 | `PLI_ADJACENTLEVEL` | `i5 modtime`, `rest` = level name; `modtime` is all zeros when the level is not cached | 2.01 | sends a gmap neighbour for preloading | [srv][2.05] (protocol/packet-layouts.md#level-navigation-client--server) |
| 41 | `PLI_SERVERWARP` | `rest` = server name | 2.17 (2.14 inferred) | the game server asks the listserver and answers with `PLO_SERVERWARP` (178) | [cap] (protocol/packet-ids.md#client--server-pli_); [cap] (version-profiles/lab-serverwarp178.tsv) |
| 46 | `PLI_ENTERLEVEL` | `c 1` | 2.31; not 3.04 | none recorded | [cap] (protocol/packet-ids.md#client--server-pli_); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |

The rules below say when a build picks one of those messages over another, and what else a warp sends [2.05] (protocol/packet-layouts.md#level-navigation-client--server).

| Rule | Builds | Source |
| --- | --- | --- |
| 2.05 sends 30 instead of 0 when it has the level cached, in memory or in its web-level cache | 2.05 | [2.05] (protocol/packet-layouts.md#level-navigation-client--server) |
| A warp to the level the player is already in only moves the player and sends nothing, in most states | 2.05 | [2.05] (protocol/packet-layouts.md#level-navigation-client--server) |
| A real warp also sends UDP id 24 to gmap neighbours (→ §2.9) | 2.05 | [2.05] (protocol/packet-layouts.md#level-navigation-client--server) |
| 2.17 has one send site for 30 instead of two | 2.17 | [bin] (client-internals/version-profiles/141-217.toml) |
| 46 is sent on every level entry (login, gmap edge crossings, doors, edge links, server warps), just before the first props message of the new level, in the same frame | 2.31 | [cap] (protocol/packet-ids.md#client--server-pli_); [cap] (version-profiles/lab-enterlevel-231.tsv); [cap] (client-internals/decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md#pli_enterlevel-46-real-231-client-observed); [cap] (client-internals/decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md#a-pli_enterlevel-46-on-doors-edge-links-and-server-warps); [cap] (version-profiles/lab-levelchange-46-222-231.tsv) |
| 46 comes from one send site at the start of the routine that switches the current level, whenever connected; its `GCHAR 1` is a constant in the code; 2.17.1 and 2.22 have no send site | 2.31; 2.17.1, 2.22 | [bin] (client-internals/decomp-findings-2026-10-25-g/02-id46-level-switch.md) |
| At login, 46 is the first message of the client's second frame, before 35 and 44 | 2.31 | [cap] (version-profiles/lab-enterlevel-231.tsv) |
| On a gmap cell crossing the props after 46 carry the new cell in props 43 or 44 and a local coordinate that starts again at the cell edge | 2.31 | [cap] (version-profiles/lab-enterlevel-231.tsv) |
| 2.22 sends no 46; 2.31 does not re-send id 39 on level entry | 2.22, 2.31 | [cap] (protocol/packet-ids.md#client--server-pli_) |

The client's handling of the `PLO_SERVERWARP` reply is in → §2.5; the listserver side is in → §6.

**Id 46 on the focus builds.** 2.22 does not send 46; 2.31 sends `c 1` on every level entry before the new level's props; 6.03r7 has 46 in its constant send set for level entry, with `c 1` carried from 2.31 until a capture; 5.00r7 and 5.12 are unread. No server reply to 46 is known. [cap][bin][inf] (protocol/enterlevel-focus-builds.md) A link or warp into a level the client does not hold has only adjacent evidence: a gmap warp (49) without the `.gmap` on disk hangs loading; a plain `.nw` door into an absent level is unobserved on 2.22 and 6.03r7. [bin][srv] (protocol/nonlocal-level-warp-status.md) Clients before 2.05 load no gmap; how a period server presented a gmap world to them is unobserved. [bin][inf] (protocol/pre-gmap-in-gmap-world.md)

## 2.4.4 Props

Three messages carry property streams from the client: its own player, NPCs and baddies. The table gives each one's layout and what the server does with it. The streams themselves are in §2.6 [srv][2.05] (protocol/packet-layouts.md#other-client--server-senders-205).

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 2 | `PLI_PLAYERPROPS` | `rest` = PLPROP stream (→ §2.6) | 1.33 | stores the props and forwards them to the level as `PLO_OTHERPLPROPS` | [srv][2.05] (protocol/packet-layouts.md#other-client--server-senders-205); [srv] (protocol/chat-pm-rc.md#chat-bubble) |
| 3 | `PLI_NPCPROPS` | `rest` = NPCPROP stream (→ §2.6) | 1.33 | passed through | [srv][2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 15 | `PLI_BADDYPROPS` | `rest` = `c id` + BDPROP stream (→ §2.6) | 1.21; not NewWorld betas | re-emitted as `PLO_BADDYPROPS` (2) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |

Movement has no message of its own. The rules below show how walking rides on player props, with example bodies decoded byte by byte, and when 2.05 sends which props [srv][2.05] (protocol/login-and-walk.md#walk-frames-are-pli_playerprops).

| Rule | Builds | Source |
| --- | --- | --- |
| There is no movement message: a walk step is a `PLI_PLAYERPROPS` carrying X (15), Y (16) and SPRITE (17), so a walk frame starts with `"` (`0x22`) | 2.05, 2.17 | [srv][2.05] (protocol/login-and-walk.md#walk-frames-are-pli_playerprops) |
| Example bodies: `1-` is SPRITE 13; `/[` is X 59 (29.5 tiles); `0f` is Y 70 (35.0 tiles); `*$walk/I` is GANI `walk` then X 41 | capture of 2026-10-04; the `walk` frame from 2.17 | [cap][inf] (protocol/login-and-walk.md#walk-frames-are-pli_playerprops) |
| `sprite % 4` is the direction: 0 up, 1 left, 2 down, 3 right | 2.22, server | [srv][doc] (protocol/login-and-walk.md#walk-frames-are-pli_playerprops) |
| 2.05 sends prop groups {0, 11, 13, 18, 31, 33} at session start, {42, 15, 16} on attach or a position change, and a per-tick diff of changed props | 2.05 | [2.05] (protocol/login-and-walk.md#walk-frames-are-pli_playerprops) |
| The guarded first-update construction orders props 0, 11, 13, 18, 31, 33; incoming self-properties id 9 clears one necessary gate, while other startup/update conditions remain and native emission is unmeasured | Graal 2002 ver10 (2.1.0.2), static only | [bin] (client-internals/graal2002-and-140-builds.md#ver10-initial-player-properties-update-2026-11-15) |
| Local chat is not a message id: it is the CURCHAT prop (12) inside `PLI_PLAYERPROPS`, and server commands typed in chat are parsed from it | server | [srv] (protocol/chat-pm-rc.md#chat-bubble) |
| The login props go out as one `PLI_PLAYERPROPS` right after the first server message, with the head (11) as an index below 100 | 1.41 rev1 | [cap] (client-internals/version-profiles/141-217.toml) |
| Player props stay on TCP while the UDP channel is active | 2.05 | [cap] (protocol/packet-layouts.md#combat-and-objects-both-directions) |

## 2.4.5 Combat and level objects

Layouts read from the 2.05 senders and the server source. The server copy (PLO) and its receiver rules are in → §2.5.

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 1 | `PLI_BOARDMODIFY` | `c x, c y, c w, c h` (whole tiles), then w × h `s tile`, row-major; 2.05 sends exactly one run | 1.33 | rebroadcast as `PLO_BOARDMODIFY` (7) | [srv][2.05] (protocol/packet-layouts.md#board-modify-correction) |
| 4 | `PLI_BOMBADD` | `c x×2, c y×2, c power` (+8 when the bomb is the sender's), `c fuse` | 1.33 | re-emitted as `PLO_BOMBADD` (11) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 5 | `PLI_BOMBDEL` | `c x×2, c y×2` | 1.33 | re-emitted as `PLO_BOMBDEL` (12) with no player id | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 7 | `PLI_HORSEADD` | `c x×2, c y×2, c (dir + 4 × bushes)`, `rest` = image file name | 1.33; not NewWorld betas | re-emitted as `PLO_HORSEADD` (17) | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 8 | `PLI_HORSEDEL` | `c x×2, c y×2` | 1.33; not NewWorld betas | re-emitted as `PLO_HORSEDEL` (18) | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 9 | `PLI_ARROWADD` | `c x×2, c y×2, c flags, c sprite`, then the projectile type sent as `v + 33` (0 arrow, 1 fireball, 2 fireblast, 3 nuke); flags = `dir & 3`, +4 first removes a matching shot, +8 owned | 1.33 | re-emitted as `PLO_ARROWADD` (19) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 10 | `PLI_FIRESPY` | `c (a × 8 + b)` | 1.21 | re-emitted as `PLO_FIRESPY` (20) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 11 | `PLI_THROWCARRIED` | empty | 1.21; not NewWorld betas | re-emitted as `PLO_THROWCARRIED` (21) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 12 | `PLI_ITEMADD` | `c x×2, c y×2, c item` | 1.21 | re-emitted as `PLO_ITEMADD` (22) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 13 | `PLI_ITEMDEL` | `c x×2, c y×2` | 1.21 | re-emitted as `PLO_ITEMDEL` (23) to the other players only | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions); [cap] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| 16 | `PLI_BADDYHURT` | `c id, c (dx + 4) × 16, c (dy + 4) × 16, c power` | 1.21; not NewWorld betas | re-emitted as `PLO_BADDYHURT` (27); applied only by the level leader | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 17 | `PLI_BADDYADD` | `c x×2, c y×2, c type, c power`, `rest` = image | 1.21; not NewWorld betas | answers with `PLO_BADDYPROPS` (2) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 20 | `PLI_OPENCHEST` | `c x, c y` (whole tiles) | 1.21; not NewWorld betas | replies `PLO_LEVELCHEST` (4) with opened = 1 | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 26 | `PLI_HURTPLAYER` | `s victim, c (dx + 4) × 16, c (dy + 4) × 16, c power`, optional `i3 npc` | 1.21 | sends `PLO_HURTPLAYER` (40) with the attacker's id | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 27 | `PLI_EXPLOSION` | `c radius, c x×2, c y×2, c power` (+8 when the explosion is the sender's) | 1.31 | re-emitted as `PLO_EXPLOSION` (36) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 32 | `PLI_ITEMTAKE` | `c x×2, c y×2, c item` | 1.38 | GServer-v2 `master`: shares the 13 handler; relays `PLO_ITEMDEL` to the level, removes the item, and gives it to the sender as a player prop | [2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions); [srv] (protocol/gserver-v2-master-handlers.md) |
| 36 | `PLI_HITOBJECTS` | `c power × 2, c x×2, c y×2`, optional `i3 npc` | 2.01; not matched in 2.22 or 2.31 | re-emitted as `PLO_HITOBJECTS` (46) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| 38 | `PLI_TRIGGERACTION` | `i3 npc` (0 = none), `c x×2, c y×2`, `rest` = `action` or `action,params` | 2.03 | re-emitted as `PLO_TRIGGERACTION` (48) | [srv][2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions); [srv] (protocol/packet-ids.md#client--server-pli_) |
| 40 | `PLI_SHOOT` | GServer-v2 `master` reads `i3 shot id` (0 in tests), `c x`, `c y`, `c z+50`, `c angle` (0–220 = 0–π), `c z angle`, `c speed`, `str gani`, `c params length`, `rest` params | 2.17; not 6.03r7 | GServer-v2 `master`: re-sent to the level area as `PLO_SHOOT` (< 5.07) or `PLO_SHOOT2` (≥ 5.07) | [bin] (client-internals/version-profiles/141-217.toml); [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [srv] (protocol/gserver-v2-master-handlers.md) |
| 48 | `PLI_SHOOT2` | the PLO 191 body without the player id; gravity is 2 bytes ×256, X2-signed | 5.12 (also 5.24r4, 6.00b1, 6.01r1, 6.03r7); not 5.0.0.7, which sends 40 | GServer-v2 `master`: re-sent like 40, in both forms | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (protocol/shoot-5007.md); [srv] (protocol/gserver-v2-master-handlers.md) |

The shot messages encode their fields with fixed steps. The rules below give how 5.0.0.7 to 6.03r7 build them [bin] (protocol/shoot-5007.md#field-scales-all-three-shoot-layouts).

| Rule | Builds | Source |
| --- | --- | --- |
| Angle: `round(angle × 220 / 2π)` after wrapping into [0, 2π), so one step is 2π/220. GServer-v2's own comment reads 0–220 as 0–π | 5.0.0.7 to 6.03r7 | [bin] (protocol/shoot-5007.md#field-scales-all-three-shoot-layouts) |
| Z angle: `round((zangle + π/2) × 220 / π)`, clamped to [−π/2, π/2]; power: `round(power × 44)`, clamped to 0–5. Power is in tiles per 0.05 s step, so 5 is 100 tiles a second | 5.0.0.7 to 6.03r7 | [bin][inf] (protocol/shoot-5007.md#field-scales-all-three-shoot-layouts) |
| `PLI_SHOOT` (40) from 5.0.0.7: shooter GINT3 0, x and y as `round(v × 2)` half tiles inside the gmap level, z as `floor(z + 0.0001) + 50` whole tiles, then the angles, power, gani and shoot params; the same body goes to UDP peers as id 28 | 5.0.0.7 | [bin] (protocol/shoot-5007.md#pli_shoot-40-what-5007-sends-bin) |
| `PLI_SHOOT2` (48): the gmap level offset is `floor(pos / 64 + 0.0001)`; x, y and z become `floor(v × 16 + 0.0001)` pixels, X2-signed in a GSHORT capped at 28671; the angles and power truncate (`floor(v + 0.0001)`) where 5.0.0.7 rounds; gravity is `floor(g × 256 + 0.0001)`, X2-signed, 2 bytes. 5.12 to 6.00b1 also send the body to UDP peers as id 30 | 5.12 to 6.03r7 | [bin] (protocol/shoot-5007.md#pli_shoot2-48-what-512-to-603r7-send-bin) |
| Gravity on the client: a SHOOT2 projectile keeps the gravity it came with; one from GS2 `shoot` or `PLO_SHOOT` uses the script variable `gravity` (default 2). Each step the vertical speed drops by `gravity × 0.05`, from start speeds `power × cos(zangle)` across and `power × sin(zangle)` up | 5.0.0.7 to 6.03r7 | [bin] (protocol/shoot-5007.md#what-the-client-does-with-gravity-bin) |

The table above gives the combat and board messages. The rules below record how they were seen on the wire, including one place where 2.05 and the server read a byte differently [2.05] (protocol/packet-layouts.md#board-change-on-the-wire-cap).

| Rule | Builds | Source |
| --- | --- | --- |
| GServer-v2 reads the bomb's third byte as `(player << 2) \| power`; 2.05 writes `power + 8`, and a receiver takes the power as `v & 7` and bit 3 as "mine" | 2.05 vs server | [2.05] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| Captured bomb: x 78, y 28, power byte 9 (power 1 plus the owner flag), fuse 55 | 2.05 | [cap] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| The fuse is probably in 0.05 s steps (55 ≈ 2.75 s) | 2.05 | [inf] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| When a bomb destroyed bushes, the other player (not the bomb's owner) sent one `PLI_BOARDMODIFY` per destroyed 2 × 2 patch, eight in one frame; why that player reported is not settled | 2.05 | [cap][inf] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| Captured board runs: a cut bush 2 × 2 = tiles 1834, 1835, 1850, 1851; cut grass = 677, 678, 693, 694 | 2.05 | [cap] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| Item drops after a bush cut came from the server (`bushitems` on); no client sent `PLI_ITEMADD` | 2.05 with GServer-v2 | [cap] (protocol/packet-layouts.md#board-change-on-the-wire-cap) |
| The bush and sign pickup path also sends `PLI_BOARDMODIFY` | 2.05 | [2.05] (protocol/packet-layouts.md#board-modify-correction) |
| 2.22 sends 11 only from the throw, after UDP 18, and only when a TCP copy is needed (UDP off, no UDP port, or a player in the level without one); the routine that sends `x×2, y×2` when a laid bomb is picked up, grabbed or removed by a script sends UDP 11 (bomb del) and, as its TCP copy, `PLI_BOMBDEL` (5), not 11 | 2.22 | [bin] (client-internals/static-reads-appendix-e-2026-11-20-f.md#sending) |
| 2.05 sends only weapon type 0 in id 33 (→ §2.4.6) | 2.05 | [2.05] (protocol/packet-layouts.md#weapons) |

The server's respawn of board changes is behaviour and is in → §4.5.

## 2.4.6 Flags, NPCs and weapons

These messages change flags, put or remove NPCs and manage weapons. Each row gives the layout, the first build that sends it and the server's action where it is known [2.05] (protocol/packet-layouts.md#other-client--server-senders-205).

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 18 | `PLI_FLAGSET` | `rest` = flag (`name` or `name=value`) | 1.21 | stores the flag | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 19 | `PLI_FLAGDEL` | `rest` = flag name | 1.21 | removes the flag | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 21 | `PLI_PUTNPC` | `str image, str script file, c x×2, c y×2` | 1.21; not 2.31 or 6.03r7 | GServer-v2 `master`: only with `putnpcenabled`; loads the script file, adds the NPC at (x, y) in the sender's level | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205); [bin] (version-profiles/2.22-2.31.md#wire-protocol); [srv] (protocol/gserver-v2-master-handlers.md) |
| 22 | `PLI_NPCDEL` | `i3 npc id`; only for NPCs with id > 0 | 1.21 | GServer-v2 `master`: deletes that NPC if it exists | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205); [srv] (protocol/gserver-v2-master-handlers.md) |
| 29 | `PLI_NPCWEAPONDEL` | `rest` = weapon name | 1.28 beta 2 | removes the weapon | [srv][2.05] (protocol/packet-layouts.md#weapons) |
| 33 | `PLI_WEAPONADD` | `c type`; type 0 → `c item index`; type 1 → `i3 npc id` (copy an NPC's script as a weapon) | 1.38 | adds the weapon and answers with `PLO_NPCWEAPONADD` (33) | [srv][2.05] (protocol/packet-layouts.md#weapons) |

Four rules limit when those messages are sent at all [2.05] (protocol/packet-layouts.md#other-client--server-senders-205); [lab] (version-profiles/lab-mac-ppc-315-512-flags-2026-11-14.md#results).

| Rule | Builds | Source |
| --- | --- | --- |
| Flags whose name starts with `local.` are never sent | 2.05 | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| When the deleted NPC is one of the player's weapons, 2.05 sends `PLI_NPCWEAPONDEL` (29) with the weapon name instead of `PLI_NPCDEL` | 2.05 | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 2.05 only sends weapon type 0 | 2.05 | [2.05] (protocol/packet-layouts.md#weapons) |
| Only `client.` flags are sent, on `created` and whenever a script changes the value; plain flags (`set name`) and other string flags (`setstring a.b,…`) stay in the client. 5.12's GS2 has no `set` or `setstring` | Mac 3.153, 4.04r2, 4.20r6, 5.12; Windows 4.04 | [lab][cap] (version-profiles/lab-mac-ppc-315-512-flags-2026-11-14.md#results); [lab] (client-internals/live-behaviour-404.md) |

## 2.4.7 Files, scripts and server values

The download replies and their framing are in → §2.7.

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 23 | `PLI_WANTFILE` | `rest` = file name | 1.21 | sends the file (→ §2.7) | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 34 | `PLI_UPDATEFILE` | `i5 modtime`, `rest` = file name | 1.42 (NewMain) | sends the file if it is newer than `modtime` | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205) |
| 47 | `PLI_VERIFYWANTSEND` | `i5 crc32, str file name` | 5.00r7 | sends the file if the client's copy is stale | [srv] (protocol/packet-ids.md#client--server-pli_); [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| 50 | `PLI_RAWDATA` | `i3 length` of the next message (→ §2.4.1) | 3.153 | reads the next *length* bytes as one message | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (protocol/v4x-clients.md#cipher-and-framing) |
| 130 | `PLI_REQUESTUPDATEBOARD` | `c level-name length`, level name, `i5 modtime, s x, s y, s width, s height` | 4.04r2 | GServer-v2 `master`: logs it and sends nothing; the reply is unknown | [srv] (protocol/packet-ids.md#client--server-pli_); [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [srv] (protocol/gserver-v2-master-handlers.md) |
| 152 | `PLI_REQUESTTEXT` | `rest` = gtokenized weapon, type, option, … (GServer-v2 `master`) | 3.153 | answers with the value; GServer-v2 `master` routes `lister`, `pmservers`, `pmguilds` and `packageinfo` requests and replies with 82 | [srv] (protocol/packet-ids.md#client--server-pli_); [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7); [srv] (protocol/gserver-v2-master-handlers.md) |
| 154 | `PLI_SENDTEXT` | `rest` = gtokenized weapon, type, option, … (GServer-v2 `master`) | 3.153 | stores the value | [srv] (protocol/packet-ids.md#client--server-pli_); [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| 157 | `PLI_UPDATEGANI` | `i5` CRC-32 of the client's gani bytecode, `rest` = gani name without `.gani` (GServer-v2 `master`) | 3.153 | sends the gani script; GServer-v2 `master` sends it only when the CRC differs, then always `PLO_UNKNOWN195` with `"SETBACKTO …"` | [srv] (protocol/packet-ids.md#client--server-pli_); [bin] (protocol/v4x-clients.md#client--server-ids); [srv] (protocol/gserver-v2-master-handlers.md) |
| 158 | `PLI_UPDATESCRIPT` | `rest` = script name | 3.153 | sends the weapon or class script | [srv] (protocol/packet-ids.md#client--server-pli_); [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| 159 | `PLI_UPDATEPACKAGEREQUESTFILE` | an order value (meaning unmeasured), package file name, modtime; GServer-v2 `master` instead reads `c` name length, package name, `c` install type (1 install, 2 reinstall), `rest` = one `i5` CRC-32 per package file | 5.00r7 | GServer-v2 `master`: `PLO_UPDATEPACKAGESIZE`, each file whose CRC differs, then `PLO_UPDATEPACKAGEDONE` | [srv] (protocol/packet-ids.md#client--server-pli_); [srv] (protocol/gserver-v2-master-handlers.md) |
| 161 | `PLI_UPDATECLASS` | `i5` CRC of the client's stored class body (0 when none; tables still say modtime), `rest` = class name | 4.04r2 | sends the class as PLO 133 on 3.153–5.12 (not 197) | [srv] (protocol/packet-ids.md#client--server-pli_); [bin] (protocol/v4x-clients.md#client--server-ids); [bin] (protocol/class-bytecode-v4.md) |

The 4.x and 5.x clients reuse some of these ids for new jobs. The rules below record those extra uses [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7).

| Rule | Builds | Source |
| --- | --- | --- |
| 5.00r7's update-package downloader uses 34 and 47 (with and without a modification time) | 5.00r7 | [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| 158 is sent after a cache miss in the client's script cache; 4.x uses it for the `getweapon` path | 4.20r8, 5.00r7 | [bin] (protocol/v4x-clients.md#client--server-ids); [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| 154 is also used by the options and secure-URL code | 5.00r7 | [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |

## 2.4.8 Chat, private messages and profiles

How chat is shown, and the server-to-client forms, are in → §2.8.

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 6 | `PLI_TOALL` | `str message`; 2.05 sends the chat-bar text after a `toall:` prefix, trimmed, at most 200 bytes | 1.33 | sends `PLO_TOALL` (13) with the sender's id | [2.05] (protocol/chat-pm-rc.md#toall) |
| 28 | `PLI_PRIVATEMESSAGE` | `s count`, `count` × `s player id`, `rest` = message (gtokenized) | 1.28 beta 2 | sends `PLO_PRIVATEMESSAGE` (37) to each listed player | [srv][2.05] (protocol/chat-pm-rc.md#private-messages) |
| 80 | `PLI_PROFILEGET` | `rest` = account | 1.39 | answers with `PLO_PROFILE` (75), relayed from the listserver | [srv][2.05] (protocol/chat-pm-rc.md#profiles) |
| 81 | `PLI_PROFILESET` | ten fields, each `c length` + text (→ §2.8) | 1.39; not 6.03r7 | forwards to the listserver | [2.05] (protocol/chat-pm-rc.md#profiles) |

The rules below say how a client chooses between a chat message and the chat prop, and warn about one field a server should not trust [2.05] (protocol/chat-pm-rc.md#chat-bubble).

| Rule | Builds | Source |
| --- | --- | --- |
| The chat-bar text is sent as 6 only when, lower-cased and trimmed, it starts with `toall:`; all other text goes out as the CURCHAT prop (→ §2.4.4) | 2.05 | [2.05] (protocol/chat-pm-rc.md#chat-bubble) |
| 5.00r7 sends 6 for chat-bar `toall` commands | 5.00r7 | [bin][inf] (protocol/v5x-clients.md#client--server-ids-500r7) |
| Field 0 of `PLI_PROFILESET` is the profile owner's account, which can be another online player's; a server must not take it as proof of who is editing | 2.05 | [2.05] (protocol/chat-pm-rc.md#profile-field-list-205-205) |

## 2.4.9 Client checks and housekeeping

These are the ids a client sends for checks and upkeep rather than for play. Several have no known server action, and the table says so rather than guess [2.05] (protocol/packet-layouts.md#other-client--server-senders-205).

| Id | Name | Layout | First sent | Server action | Source |
| ---: | --- | --- | --- | --- | --- |
| 14 | `PLI_CLAIMPKER` | `s player id` | 1.3 test | GServer-v2 `master`: in a sparring level a Glicko-style rating update for both players (skipped for a shared IP); elsewhere a kill for the killer and, with `apsystem`, an AP drop | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205); [srv] (protocol/gserver-v2-master-handlers.md) |
| 24 | `PLI_SHOWIMGPLAYER` | `rest`, passed through | 1.21 | relays it unchanged as `PLO_SHOWIMGPLAYER` (32) with `s sender id` in front | [2.05] (protocol/packet-layouts.md#other-client--server-senders-205); [cap] (version-profiles/lab-showimg24-relay.tsv) |
| 25 | `PLI_TOWEAPON` (was `PLI_UNKNOWN25`; proposed `PLI_WEAPONUPLOAD`) | as `PLO_NPCWEAPONADD`: name, image, script | 1.21; last seen 1.37 | a weapon upload; GServer-v2 beta4 kicks the client for it | [bin] (protocol/unknown-ids-2026-11-06.md); [cap] (protocol/unknown-ids-2026-11-06.md); [bin] (client-internals/version-profiles/v121-v132.toml); [bin] (client-internals/version-profiles/v133-v139.toml) |
| 31 | `PLI_PACKETCOUNT` | `s count` (GServer-v2 `master`) | 1.33; last seen 1.39 | GServer-v2 `master`: logs a warning if the count differs from its own or is above 10000, then resets its count; no disconnect | [bin] (client-internals/version-profiles/v133-v139.toml); [srv] (protocol/gserver-v2-master-handlers.md) |
| 37 | `PLI_LANGUAGE` | `rest` = language name (`English` seen) | 2.02 rev2 | stored | [cap] (version-profiles/2.22-2.31.md#wire-protocol); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 39 | `PLI_TAMPERCHECK` | 10 raw bytes, a constant per build (not two `i5`) | 2.17, 2.22, 2.31; not 3.04, 3.153 or 6.x | GServer-v2 reads and discards it | [cap][bin] (protocol/packet-ids.md#client--server-pli_); [cap][srv] (version-profiles/2.22-2.31.md#wire-protocol) |
| 43 | `PLI_MUTEPLAYER` | `s player id, c on` (1 mute, 0 unmute); one message per click in the player list | 2.17; not 6.03r7 | unmeasured | [cap] (protocol/packet-ids.md#client--server-pli_) ; [cap] (protocol/lab-checks-2026-10-24.md#buddy-ignore-mute-222) |
| 44 | `PLI_PROCESSLIST` | the client's window list, comma-separated window titles | 2.17; not 3.04 | the reply to `PLO_LISTPROCESSES` (182) | [bin][cap] (protocol/packet-ids.md#client--server-pli_); [cap] (client-internals/version-profiles/141-217.toml) |
| 45 | `PLI_PROCESSRUNNING` | `c flag`: 1 if the server's string occurs in the client's own process list | 2.17 | the reply to `PLO_HASPROCESSRUNNING` (183) | [bin] (protocol/packet-ids.md#client--server-pli_); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 162 | `PLI_PONG` (was `PLI_RC_UNKNOWN162`; proposed `PLI_PING`) | game clients: `!` + `s value`; RCs: empty (→ §2.4.9) | 4.20r6 | a ping: the game clients' answer to `PLO_PING`, an RC's 60 s keepalive; accept and ignore, or time it against 108 | [bin] (protocol/unknown-ids-2026-11-06.md); [bin] (protocol/v4x-clients.md#client--server-ids); [bin][inf] (protocol/v6x-clients.md#client--server-ids-601-603); [srv] (protocol/packet-ids.md#client--server-pli_) |
| 252 | `PLI_SET_ENC_KEY` | sets the AES or RC4 key and IV; above 223, so not sendable as one GCHAR (→ §2.10) | newer gs2lib only | unmeasured | [srv] (protocol/packet-ids.md#client--server-pli_) |
| 253 | `PLI_BUNDLE` | several messages in one (→ §2.10) | newer gs2lib only | unmeasured | [srv] (protocol/packet-ids.md#client--server-pli_) |

**Settled question, formerly E#5: meaning of id 162 from the client.** Three readings of client id 162 turned out to be one message, a ping answer [srv] (protocol/packet-ids.md#client--server-pli_).

| Part | Discussion | Source |
| --- | --- | --- |
| Claim A | The 2026-10 gs2lib named 162 `PLI_RC_UNKNOWN162` (upstream now `PLI_PONG`): an empty message from the RC3 beta | [srv] (protocol/packet-ids.md#client--server-pli_) |
| Claim B | 4.20r8 sends 162 as the answer to S→C 108 | [bin] (protocol/v4x-clients.md#client--server-ids) |
| Claim C | 6.01r1 and 6.03r7 send 162 as a reply to a server request: `!` and a 2-byte value (two 7-bit groups, capped at `0x6FFF`) the server sent; probably the ping answer 6.11 calls `onSendPingAnswer` | [bin][inf] (protocol/v6x-clients.md#client--server-ids-601-603) |
| Settled | One message, a ping: 4.20r6, 4.20r8, 6.01r1 and 6.03r7 send 162 only from their 108 handler, with the same code in 4.20r8 and 6.03r7; the 2010 RC and RC3 send it empty every 60 s and have no 108 handler | [bin] (protocol/unknown-ids-2026-11-06.md) |
| Left over | A capture of a game client's answer to S→C 108 is still missing | [inf] (protocol/v4x-clients.md#client--server-ids) |

Ids 24 and 39 were studied from captures. The rules give their timing and the exact bytes seen, and what tests showed about their meaning [cap] (protocol/packet-ids.md#client--server-pli_).

| Rule | Builds | Source |
| --- | --- | --- |
| 24 is also sent on its own about every 5.1 s with one byte (value 9) | 2.31; 2.22 only while another player is in the level; 2.17 every 5 s after login | [cap] (protocol/packet-ids.md#client--server-pli_); [cap] (client-internals/version-profiles/141-217.toml); [cap] (client-internals/decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md#b-pli_showimgplayer-24) |
| The meaning of the 24 payload: receivers showed no visible reaction to the values 0, 1, 5, 9, 14, 58, 95, to the bytes `xx.png`, or to an empty payload, and the server neither disconnected nor logged an invalid packet; the client reads show it is the weapon-image list of → §2.4.9.1 | 2.31 sender, 2.x receiver | [cap] (version-profiles/lab-showimg24-relay.tsv); [bin] (client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md#what-the-text-is) |
| 39 is sent right after `PLI_LANGUAGE` at login | 2.17, 2.22, 2.31 | [cap] (protocol/packet-ids.md#client--server-pli_) |
| 39 bytes: 2.17 `2a 7b ad 19 5e 23 12 43 d8 2c`, 2.22 `25 0e 4d 0f 96 2b 03 ed e6 31`, 2.31 `29 16 55 b7 60 2e 87 c9 eb 82`; identical across logins, accounts and login keys | 2.17, 2.22, 2.31 | [cap] (version-profiles/tampercheck-values.tsv) |
| 39 re-sends: 2.17 once at login; 2.22 at login, on every gmap edge crossing and after every client-initiated level-link request, but not after a server-side warp; 2.31 at login and then about every 3.2 s | 2.17, 2.22, 2.31 | [cap] (version-profiles/2.22-2.31.md#wire-protocol); [cap] (version-profiles/tampercheck-values.tsv) ; [cap] (protocol/lab-checks-2026-10-24.md#tampercheck-client-pli-39); [bin][cap] (version-profiles/tampercheck-words.tsv) |
| How the 39 bytes are computed is a client integrity check (→ §4.10) | 2.17, 2.22, 2.31 | [bin] (version-profiles/2.22-2.31.md#wire-protocol) |
| Because GServer-v2 discards 39, whether a different value would be rejected is unmeasured | server | [srv] (version-profiles/2.22-2.31.md#wire-protocol) |
| 44 is sent just before the login props | 2.17 | [cap] (client-internals/version-profiles/141-217.toml) |

### 2.4.9.1 The id 24 weapon-image list

Id 24 carries the images that the sender's weapon scripts show (`showimg` and the `changeimg*` commands), as changes against the list sent last; the relay is `PLO_SHOWIMGPLAYER` (32):

| Rule | Builds | Source |
| --- | --- | --- |
| a record starts with 0x2a + the image index (0 to 199); tag bytes 0x20 + tag follow with their data; a byte of 0x2a or more starts the next record; an unknown tag skips one data byte; a tag with no data ends the text | 2.05, 2.17.1, 2.22, 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md#what-the-text-is); [2.05] (client-internals/id24-205.md#what-205-sends) |
| tag 0 name (`GCHAR` length + bytes; empty removes the image), 1 x, 2 y (half tiles, or screen units at layer 10 and over; units unconfirmed), 3 layer − 1, 4 visible part (0x20 whole image, or 0x21 + left and top as two 7-bit bytes each + width and height, clamped to 0..16000 and 0..220), 5 red, green, blue and alpha over 200, 6 zoom over 10, 7 draw order − 0x52, 8 mode | 2.17.1 to 2.31 (receiver read in 2.31) | [bin] (client-internals/decomp-findings-2026-10-25-g/image-text-format.tsv) |
| 2.05 sends tags 0 to 6 only: layer only when not 1, part only when its size is above 0, colours only when one is not 1.0, zoom only when not 1.0 | 2.05 | [2.05] (client-internals/id24-205.md#what-205-sends) |
| a leading 0x29 (`GCHAR` 9) marks a full list; after it the receiver removes every image of that player the text did not name; with no images the full list is the marker alone, the one byte every real client was seen to send | 2.05 to 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md#what-the-text-is); [2.05] (client-internals/id24-205.md#what-205-sends) |
| a full list goes out when a countdown wraps: every 61st call in 2.05, every 102 ticks (101 calls, the call after a send skipped) in 2.17.1 to 2.31, which fits the 5.1 s seen at 50 ms a tick; the first tick after login is a wrap; an empty text is not sent | 2.05; 2.17.1 to 2.31 | [2.05] (client-internals/id24-205.md#what-205-sends); [bin][inf] (client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md#sender) |
| a UDP copy goes out when it can (id 15 in 2.05, → §2.9); the TCP copy goes out when UDP is off for the client or does not reach some player in the level; 2.31 always sends the TCP copy; a wrap that finds the test false is lost | 2.05, 2.17.1, 2.22; 2.31 | [2.05] (client-internals/id24-205.md#what-205-sends); [bin] (client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md#the-tcp-test) |
| a new image gets layer 1, colours 200 each, zoom 10 and mode 0; fields other than the name apply only to an image that exists | 2.31 | [bin] (client-internals/decomp-findings-2026-10-25-g/01-id24-image-list.md#receiver) |
| the sender's own value formatting, the "UDP reaches this player" flag of the 2.22 test, and how the images are drawn are unmeasured | 2.17.1 to 2.31 | [doc] (client-internals/decomp-findings-2026-10-25-g/04-open-points.md) |
| an earlier note's four-field form (index, x, y, name) for 2.05 and earlier is wrong for 2.05; builds before 2.05 were not read | 2.05 | [2.05] (client-internals/id24-205.md#correction) |

## 2.4.10 Staff messages sent by game clients

The RC and NC ids (51 to 119, 150, 151, 155, 156, 160) are documented with the staff tools in → §7. Some game clients send a few of them:

| Id | Name | Builds | Use in a game client | Source |
| ---: | --- | --- | --- | --- |
| 79 | `PLI_RC_CHAT` | 4.x, 5.00r7, 6.x | unmeasured | [bin] (protocol/v4x-clients.md#client--server-ids); [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 92, 93 | `PLI_RC_FILEBROWSER_DOWN`, `_UP` | 92: 4.x, 5.00r7, 6.x; 93: 3.153, 5.00r7, 6.x | 93 carries a file-name string and one data chunk, behind id 50 | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (version-profiles/3.04-3.153.md#client--server-ids) |
| 96, 97, 98 | `PLI_RC_FILEBROWSER_MOVE`, `_DELETE`, `_RENAME` | 3.153, 5.00r7, 6.x; 96 also 4.x | file browser | [bin] (protocol/v6x-clients.md#client--server-ids-601-603); [bin] (version-profiles/3.04-3.153.md#client--server-ids) |
| 155, 156 | `PLI_RC_LARGEFILESTART`, `_END` | 3.153, 5.00r7, 6.x | the upload queue: 155, then 93 chunks of at most 32,000 bytes, then 156; the queue pauses while about 64 KB is waiting to go out | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |
| 160 | `PLI_RC_FOLDERDELETE` | 6.03r7 only | folder delete | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |

The 6.11 client sends no fixed ids: a script-loaded table maps each outgoing message to a wire id, so its named send slots are in → §2.10.

## 2.4.11 Login-time order

The login message itself and the server's reply are in → §2.3. What the client sends next:

| Build | Messages after the login message, in order | Source |
| --- | --- | --- |
| 1.41 rev1 | one `PLI_PLAYERPROPS` with the login props, right after the first server message; no file requests | [cap] (client-internals/version-profiles/141-217.toml) |
| 2.02 rev1 | file requests and the login props; no 37 | [cap] (client-internals/version-profiles/141-217.toml) |
| 2.17 | 37, then 39 once; 44 with the window titles just before the login props | [cap] (client-internals/version-profiles/141-217.toml); [cap] (version-profiles/tampercheck-values.tsv) |
| 2.22 | 37 `English`, 39, then 34 for the default images (sword, shield, body, bomb), 23, and 2; 44 in answer to the server's 182 | [cap] (version-profiles/2.22-2.31.md#wire-protocol) |
| 2.31 | 37, 39, then in the second frame 46 before the props, 35 and 44 | [cap] (version-profiles/2.22-2.31.md#wire-protocol); [cap] (version-profiles/lab-enterlevel-231.tsv) |
| 6.01r1, 6.03r7 | 37 right after login; no 39 | [bin] (protocol/v6x-clients.md#client--server-ids-601-603) |

## 2.4.12 Outgoing senders in unpacked 6.1.1.3 and 6.0.3.7

Unpacked 6.1.1.3 has two fixed sends. `sendraw` uses id −1 and appends the caller's bytes. `senddata` sends the id and the body the caller passes. [bin] (protocol/v6113-pli.md)

Fifty-five named actions each read one slot of a 256-wide outgoing table. A negative slot does not send. Slot 254 raises the matching `onSend` script event. Any other value is the packet id. `setoutdatahandlers` fills the table with the all-ones dword, then copies the script list, and stops at 256. [bin] (protocol/v6113-pli.md)

Unpacked 6.0.3.7 has none of those names. Its login send is packet id 5, the upper-cased token. [bin] (protocol/v6113-pli.md)

## 2.4.13 Mac 6.11r1 named-send evidence limits

The Mac x86-64 static study found all 56 Windows-table `onSend…` names with code references and matched 52 preceding table loads to the published Windows slot numbers. This is partial mapping evidence: a slot index is not an observed wire id. No client was run. The Windows table-fill/ordinary-send conclusions in §2.4.12 do not automatically transfer to this Mac input. [bin] (client-internals/mac-611r1-send-slots.md#the-table-and-the-test)

| Observation | Directly checked scope | Source |
| --- | --- | --- |
| Entry storage and suppression | slots 44 and 45 read four-byte entries from the same table; a negative entry returns without sending or raising an event | [bin] (client-internals/mac-611r1-send-slots.md#the-table-and-the-test) |
| Event entry | for those two senders, value 254 selects the named event path, supplying the provided payload or a shared fallback to a common helper | [bin] (client-internals/mac-611r1-send-slots.md#the-table-and-the-test) |
| Matched examples | WantWeaponScript 0, ToAllChat 3, TriggerAction 11, PlayerProperties 44, NPCProperties 45, WindowList 56 | [bin] (client-internals/mac-611r1-send-slots.md#the-table-and-the-test) |
| Four unconfirmed mappings | `onSendShot`, `onSendProjectile`, `onSendPrivateMessage`: no clean load match; `onSendImageUpdate`: unrelated earlier load selected by the scan. These are unresolved, not contrary mappings | [bin] (client-internals/mac-611r1-send-slots.md#the-table-and-the-test) |

Other non-negative values took a path not followed in this Mac study. Ordinary writer reachability and payload preservation, script-side population and a proposed 256-entry capacity therefore remain unconfirmed. The method combined a string/reference/load pattern scan with manual decoding of the two property senders; neither a pattern match nor an event name establishes the full runtime call contract. Resolve those paths and the four mappings before implementing a complete Mac-specific outgoing table from this evidence. [bin][inf] (client-internals/mac-611r1-send-slots.md#how-this-was-checked); (client-internals/mac-611r1-send-slots.md#still-open)
