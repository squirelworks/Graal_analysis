# Carry/throw, hit and shoot messages (gap #26)

Date: 2026-11-16. Research-gaps / research-list rank **#26** (focus 2.220, 2.310, 5.x). Also E#311 / E#312 / E#323.

**Question:** What layouts and server expectations do `PLI_THROWCARRIED` (11), `PLI_HITOBJECTS`, `PLI_SHOOT` (40) and `PLI_SHOOT2` (48) have? Also the last byte of a shot (E#312) and the blast hit zone (E#311).

**Answer so far:**

| Piece | Status | Evidence |
|---|---|---|
| `PLI_SHOOT` / `PLI_SHOOT2` field scales (angle, zangle, power) | **Settled** for 5.00r7–6.03r7 readers/senders | `shoot-5007.md` **[bin]** |
| 5.00r7 **sends 40 only** (no 48); receives SHOOT2 | **Settled** | same **[bin]** |
| 5.12+ **send 48** with 2-byte X2 gravity | **Settled** | same **[bin]** |
| GServer-v2 one-byte gravity | **Mismatch** vs every client read | same **[srv][bin]** |
| GServer-v2 master 40/48 re-send rules | **Settled as [srv]** | `gserver-v2-master-handlers.md` |
| `PLI_THROWCARRIED` (11) layout / real throw capture | **Open** | PARITY “no”; needs L |
| `PLI_HITOBJECTS` layout / server expectations | **Open** | PARITY “no” |
| Last byte of a shot (E#312) | **Open** | App. E |
| Blast hit zone (E#311) | **Open** | App. E |
| 2.22 level-object / throw routines (E#323) | **Open** | unread **[bin]** |

Tags: **[bin][srv][doc]**. No new combat lab in this pass.

## seihai-gserver

PARITY: carry/throw, HITOBJECTS, SHOOT, SHOOT2 all **no**. Baddies path is separate (lab partial). Do not implement until a real-client throw/shoot capture pins layouts for the focus builds.

## Still open / next

1. L: 2.22 carry → throw decode (id 11 body).
2. L: HITOBJECTS on bush/chest/NPC hit.
3. S: 2.22 throw/explosion routines (E#323); settle E#311/E#312.
4. Then PARITY rows past “no”.
