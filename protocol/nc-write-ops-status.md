# NC write operations (gap #40)

Date: 2026-11-16. Research-gaps / research-list rank **#40**. Gap: seihai-npcserver#22 (“Complete NPC Control objects”); E#425; `protocol/npc-control.md`.

**Question:** What are the wire layouts for NPC attribute write/reset/add and class/weapon create/update/delete?

**Answer so far (inventory — not a full settle):**

| Op | Client→NC id | Server→NC id (known) | Layout known? | Evidence |
|---|---|---|---|---|
| NPC get / open | 103 | — | `i3 id` | `npc-control.md` **[bin]** |
| NPC delete | 104 | 159 | `i3 id` | same |
| NPC reset | 105 | — | `i3 id` | same |
| NPC script get/set | 106 / 109 | 160 | `i3 id` (+ script on set) | same; escaping → gap #41 / seihai-rc#56 |
| NPC flags get/set | 108 / 110 | 161 | `i3 id` (+ flags) | same |
| NPC add | 111 | 158 | comma text vs props — **open details** | checklist § “Check on loopback” |
| NPC attributes | — | 157 | rest = lines | view-only in 2004 NC |
| Class delete | 119? | 188 | bare name vs length-prefixed — **open** | checklist item 4 |
| Weapon add/script | — | 33 (and large-script path) | GSHORT vs GINT3 — **open** | checklist item 5 |
| Local-NPC list after 114 | — | — | **unread** | checklist item 6 |

Tags: **[bin][doc]**. No new NC lab in this pass. Do not copy GPL NPC-server code into MIT repos.

## Still open

| Item | Status |
|---|---|
| Attribute **write** path (if any beyond flags/script) | **Open** S+L |
| Class create/update/delete full layouts | **Open** |
| Weapon create/update/delete full layouts | **Open** |
| Prop-order / clear-vs-leave on NC_NPCADD 158 | **Open** L |
| seihai-npcserver#22 acceptance scope | **Open** after layouts |

## Lab next

Loopback NC (Wine 2004 / RC3) against seihai-npcserver or the fork: dump each write once with known fixtures; fill the open rows above without pasting GPL.
