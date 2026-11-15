# `PLI_ENTERLEVEL` (46) on focus 5.x / 6.037

Date: 2026-11-16. Research-gaps / research-list rank **#18** (focus 5.007, 5.120, 6.037).

**Question:** which focus builds send `PLI_ENTERLEVEL`, with what layout, and what reply do they wait for?

**Answer so far:**

| Build | Sends 46? | Layout / when | Reply waited for | Evidence |
|---|---|---|---|---|
| 2.22 (context) | **No** | — | — | lab + static **[cap][bin]** |
| 2.31 (context) | **Yes** | `c 1` on every level entry (login, gmap edges, doors, links, server warps), just before first props of the new level | None recorded; not paired with a re-sent id 39 | `lab-enterlevel-231.tsv`; feature-specs; packet-ids **[cap][bin]** |
| **6.037** | **Yes** | Listed in the 6.03r7 constant send set; note says “on level entry, as in 2.31” | Not separately documented for 6.x | `v6x-clients.md` **[bin]** |
| **5.007 / 5.120** | **Unread** | No send-site writeup in the v5 notes yet | Unknown | gap / profile-audit **[doc]** |
| seihai-gserver | Does not handle | — | — | `PARITY.md` row “no” **[doc]** |

Tags: **[bin]** 6.03r7 / 2.31; **[cap]** 2.31 lab; **[doc]** PARITY. No new binary session in this pass — **5.00r7 and 5.12 still need S** (and optional L).

## What is settled

- **Name and payload on 2.31:** `PLI_ENTERLEVEL`, body `GCHAR 1` (literal). Timing: first in the client frame that announces the new level, before props (and before `PLI_ADJACENTLEVEL` / cell props on gmap walks). **[cap]**
- **6.03r7 includes id 46** among constant send ids (`44–48` range in the outgoing list) and the per-id table maps it to level entry like 2.31. **[bin]** Treat layout as **`c 1` by carry from 2.31** until a 6.037 capture confirms (**[inf]** for the byte, **[bin]** for “sends 46”).
- **No dedicated server reply** is documented for 46: GServer-v2 / notes treat it as a content-free notice. seihai-gserver does not implement a handler yet.

## What is still open (focus)

| Item | Status |
|---|---|
| 5.00r7 send site / layout | **Open** (S of wrappers; profile still carries older pli sets) |
| 5.12 send site / layout | **Open** (same) |
| 6.037 live confirmation of `c 1` and entry moments (login, warp, gmap edge) | **Open** (L; low risk given static list) |
| Whether any focus build waits for a specific PLO after 46 | **Open** (none known; settle by capture) |
| seihai-gserver handler | **Open** (implementation once layout is fixed for 5.x) |

## Lab / static next steps

1. S: 5.00r7 and 5.12 (engine) constant id-46 call sites — confirm presence and immediate payload.
2. L (loopback): 6.03r7 level entry decode; optional 5.12 once S says it sends.
3. Only then add a seihai-gserver `ENTERLEVEL` row beyond “no”.
