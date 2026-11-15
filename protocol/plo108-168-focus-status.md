# PLO 108 sub 1 and PLO 168 on focus 4.208 / 6.037

Date: 2026-11-16. Research-gaps / research-list rank **#43** (focus 4.208, 6.037). Owner kept Graal_analysis#254 open with next steps listed — this note only consolidates what is already recorded.

**Questions:** who reads the stored 108 sub-1 value outside the connection code? Is 168 really “login done”?

## PLO 168 (`ONLINEMODE` / proposed `LOGGEDIN`)

| Claim | Status | Evidence |
|---|---|---|
| Empty body; every client from 2.05 on handles it | **Settled** | `unknown-ids-2026-11-06.md` **[bin]** |
| Sets a one-shot flag / local-player reset | **Settled** (behaviour) | same; 4.20 / 6.03r7 set one byte on the player object **[bin]** |
| Means “login done” | **Medium confidence** — still the best label, not proven against an official Login capture | **[bin]** + **[srv]** habit; lab 168 then 194 from GServer-v2 is lab-only **[cap]** |

So: treat 168 as **“logged-in flag / local reset”** with confidence high on the flag, medium on the English name. Closing the name needs an official Login/list capture (owner-gated for public).

## PLO 108 subtype 1

| Claim | Status | Evidence |
|---|---|---|
| Subtype 0 is the ping the client answers with `PLI_PONG` (162) | **Settled** for 6.x | `v6x-clients.md` **[bin]** |
| On **6.03r7**, injected sub-1 values 0/1/5/30/300 do **not** change ping answers, C→S 24 cadence, or disconnect over 60 s windows | **Settled (negative lab)** | `live-runs/open-issues-2026-11-14` §3 / #254 **[lab]** |
| Who **reads** the stored sub-1 value outside the connection/ping path (4.20r8 / 6.03r7) | **Still open** | #254 owner next steps; needs S cross-ref **[bin]** |
| Same sub-1 behaviour on **4.20r8** | **Open** | no matching injection lab in the notes |

seihai-gserver#56 (108 out, 162 back; no 108 to 5.x in one ping capture) stays a separate server-side observation.

## Open after this note

1. Static reader search for the stored 108 sub-1 field in **4.20r8** and **6.03r7** (outside ping).
2. Optional: repeat the sub-1 injection on **Windows 4.20r8** / Windows 6.03r7 with assets staged.
3. Official Login capture for 168 naming (plan-hold / owner OK).

Tags: **[bin]**[lab][cap][doc]. No new binary session in this pass.
