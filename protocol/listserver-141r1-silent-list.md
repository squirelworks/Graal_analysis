# 1.41 rev 1 list reply and the silent-list timer

Date: 2026-11-16. Research-gaps / research-list rank **#13** (focus 1.411).

**Answer (client side):** the catalogued 1.41 rev 1 game client opens a plain list socket and **sends nothing**. It only reads. A listserver that waits for a client login never fills its list. The lab / seihai `silent_list_after_ms` (and the Python lab `--greet-delay`) are **server-side accommodations for that client behaviour**, not a second list protocol. Whether the original 2001-era listserver spoke first the same way is still **unobserved** (no surviving listserver binary or capture of that era against a silent client).

Tags: **[bin]** list receive handler; **[lab]** 2026-11-12 Wine loopback and the 2026-11-13 harness; **[doc]** cross-links below. No new binary session in this pass.

## What 1.41 rev 1 sends and accepts

| Direction | Behaviour | Evidence |
|---|---|---|
| Client → list | Nothing on connect and nothing afterwards (no list name, account, or key). Window shows "Getting server list ...". | `listserver.md` §1.41 rev1 **[bin][lab]** |
| Framing | Same as shape A: `u16be` length + zlib body, messages split on `\n`. | `listserver.md` **[bin]** |
| List → client id 0 | Full list: `c count`, then per server `c` field count + that many `str` fields. After id 0 the client closes the link. | `listserver.md` **[bin][lab]** |
| List → client id 1 | **One more server entry** (same field layout as a row of id 0). | `listserver.md` **[bin]** |
| List → client id 2 | **Ignored** (status / end-of-list is not handled here). Ids 3 and 4 also do nothing on this game client. | `listserver.md` **[bin]** |

Connect then uses the chosen row’s address and port for the game login (`GNW13110`, generation 3). **[lab]**

Do not confuse this with **RC 1.41** (2002), which *does* send id 0 `rc` then id 1 account/password, and which treats id 1 as another entry and **id 2 as end-of-list** (`tools/npc-control.md`). That is E#401’s RC claim; it is a different program from the game client.

## Is `silent_list_after_ms` “what the original listserver did”?

| Settled | Still open |
|---|---|
| The **game client** requires a server-first id 0 list. Without it the window hangs on "Getting server list ...". **[lab]** | What a **2001-era** production listserver sent to a silent 1.41 (timing, whether it ever waited for a login that never came) is unobserved. E#402 / the 2000-era reply question stays open for that era. |
| Lab Python listserver: `--greet-delay` (1.5 s in the 2026-11-12 writeup) then shape-A id 0. With that delay, real 1.41 rev 1 filled its list and played. **[lab]** | A period listserver binary would settle historical timing; none is in the public notes. |
| seihai-listserver: `silent_list_after_ms` (0 = off; README suggests ~500 for real 1.41). Shape S = “nothing from client → shape A reply after the wait”. Harness note: about 500 ms of client silence before the list. **[lab]** | Exact original delay, if any, unknown. |

So for Seihai and lab practice: treat silent-list as **required by the client**, and label “matches original listserver timing” as **[inf]** until a period capture exists.

## Lab practice

- Point 1.41 rev 1 at a loopback list port; set `silent_list_after_ms` (or `--greet-delay`) non-zero.
- Keep clients that *do* speak first (2.00–2.17) on the same ports: the wait is only used when the first frame never arrives.
- 1.39 and earlier do not use this path at all (`client-internals/how-139-gets-online.md` once merged; until then `versions-133-139.md`).

## Open after this note

- Historical 2001 listserver behaviour / timing (owner-held or archive binary).
- E#401’s remaining question: whether the **2002** listserver’s use of ids 1 and 2 matched RC, the game client, or later Reborn STATUS-as-id-2. Game-client handling of 1 and 2 is settled above.
