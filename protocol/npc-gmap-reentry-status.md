# NPC GS2 state across gmap re-entry (gap #22)

Date: 2026-11-16. Research-gaps / research-list rank **#22** (focus 4.208, 5.x, 6.037). Gap: seihai#497; E#318 (offline level reload).

**Question:** On a real client, does a level NPC’s GS2 state survive leaving and re-entering a gmap cell, or restart? Seihai restarts it.

**Answer so far:**

| Piece | Status | Evidence |
|---|---|---|
| Seihai behaviour: NPC execution **restarts** on gmap cell re-entry | **Documented intent** | seihai#497 **[doc]** |
| Offline level reload semantics (E#318) | **Open / related** | App. E — may inform but is not gmap re-entry |
| Real 6.03r7 / 5.12 counter-NPC fixture across cell leave/re-enter | **Open** | gap method — needs L |
| Whether class/weapon GS2 differs from level-NPC GS2 here | **Open** | not separated in the issue |

Tags: **[doc]**. No fixture lab in this pass.

## Lab that settles it

1. Loopback gmap (≥2 cells) with a level NPC whose GS2 increments a counter / flag each `timeout` or `onCreated`.
2. Actor: 6.03r7 then 5.12; walk out of the cell and back; decode whether the counter continues or resets; watch S→C NPC props / script re-delivery.
3. Compare Seihai vs fork if both are available on loopback.

## Still open

| Item | Status |
|---|---|
| Survive vs restart on 6.03r7 | **Open** L |
| Same on 5.12 | **Open** L |
| 4.20r8 if in scope after 5.x/6.x | **Open** L |
| seihai#497 implementation choice | **Blocked** on lab |
