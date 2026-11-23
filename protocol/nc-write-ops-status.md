# NC write operations (gap #40)

Date: 2026-11-16; lab write layouts 2026-11-24. Research-gaps / research-list rank **#40**. Gap: seihai-npcserver#22 (“Complete NPC Control objects”); E#425; `protocol/npc-control.md`.

**Question:** What are the wire layouts for NPC attribute write/reset/add and class/weapon create/update/delete?

**Answer so far:**

| Op | Client→NC id | Server→NC id (known) | Layout known? | Evidence |
|---|---|---|---|---|
| NPC get / open | 103 | — | `i3 id` | `npc-control.md` **[bin]** |
| NPC delete | 104 | 159 | `i3 id` | same |
| NPC reset | 105 | — | `i3 id` | same |
| NPC script get/set | 106 / 109 | 160 | `i3 id` (+ script on set) | same; escaping → gap #41 / seihai-rc#56 |
| NPC flags get/set | 108 / 110 | 161 | `i3 id` (+ flags) | same |
| NPC add | 111 | 158 | C→S comma text; S→C prop list — **settled** below | **[lab]** 2026-11-24 |
| NPC attributes | — | 157 | rest = lines; **view-only** (no C→S attribute-set id) | **[bin][lab]** |
| Class create/update/delete | 113 / 112 / 119 | 163 / 162 / 188 | **settled** below | **[lab]** 2026-11-24 |
| Weapon create/update/delete | 117 / 116 / 118 | 33 / — / — | **settled** below (list via 167) | **[lab]** 2026-11-24 |
| Local-NPC list after 114 | — | — | **unread** | checklist item 6 (out of this write-layout pass) |

Tags: **[bin][doc][lab]**. Do not copy GPL NPC-server code into MIT repos.

## Write layouts (2026-11-24) **[lab]**

Evidence id: `NC-WRITE-20261124`. Loopback only. Standalone `nc7132001` under Wine behind `tools/probe/ncprobe.py`, driven by `tools/probe/lab/runnc.sh` + `lab/nc-write.plan` (stub upstream holds the socket; fixtures come from inject/drop). 28/28 shots alive; `drop s2c 80` exercised once (drop withholds peer traffic; explicit `s2c` inject still logs).

### Attribute write path

No client→NC attribute-set id exists beyond script (109) and flags (110). Server→NC **157** is view-only (`rest = lines`); the attribute viewer has no Save-to-server path in the NC table. **[bin][lab]**

### NC_NPCADD 158 — prop order and clear-vs-leave

Server→NC body: `GINT3 id`, then any subset of props, any order:

| Prop | GCHAR | Value |
|---:|---|---|
| 50 | name | `str` (GCHAR length + text) |
| 51 | type | `str` (`OBJECT`, `ANIMAL`, …) |
| 52 | level | `str` (level name) |

- **Order:** three full-prop orderings (`50-51-52`, `52-51-50`, `51-50-52`) all accepted; a fourth add with order `52-51-50` on a new id also painted. **[lab]**
- **Leave:** a follow-up 158 that omits a prop **leaves** the previous value on the row (name-only / type-only / level-only updates). **[lab]**
- **Clear:** sending prop 50 with an empty `str` clears the name; omitted type/level stayed (`OBJECT` / `seed.nw` on id 10 after empty-name). Present-but-empty clears that prop; absent leaves it. **[lab]**

Client→NC **111** is comma text, not props: `name,id,type,scripter,start level,x,y` (fixture dumped via `c2s` inject). **[lab]**

### Class create / update / delete

| Direction | Id | Layout |
|---|---:|---|
| S→C add | 163 | bare name (`rest = text`, no length prefix) |
| S→C get/update body | 162 | `str name` + rest = script |
| S→C delete | 188 | bare name (same as 163); a length-prefixed `str` form was also injected for contrast |
| C→S save | 113 | `str name` + rest = script |
| C→S delete | 119 | bare name (length-prefixed form also dumped) |

So class **delete** on the wire matches bare name for both 188 and 119; length-prefixed is not required. **[lab]**

### Weapon create / update / delete

| Direction | Id | Layout |
|---|---:|---|
| S→C add/update | 33 | `str name`, `str image`, **GSHORT** script length, then that many script bytes |
| S→C list | 167 | repeated `str name` |
| C→S save | 117 | `str name`, `str image`, rest = script (no separate length field) |
| C→S delete | 118 | bare name |

A fixture that put a **GINT3** where the GSHORT belongs mis-framed the script length (GSHORT reads the first two of the three bytes). Use **GSHORT** on 33. Large script set packets (109 / 113 / 117) still follow the RAWDATA path described in `npc-control.md` when oversized — not re-probed here. **[lab]**

## Still open

| Item | Status |
|---|---|
| Attribute **write** path (if any beyond flags/script) | **Settled** — none; 157 view-only |
| Class create/update/delete full layouts | **Settled** (above) |
| Weapon create/update/delete full layouts | **Settled** (above; large-script RAWDATA unchanged) |
| Prop-order / clear-vs-leave on NC_NPCADD 158 | **Settled** — any order; omit=leave; empty str=clear |
| Local-NPC list after 114 | **Open** (checklist item 6; not part of write-layout dump) |
| seihai-npcserver#22 acceptance scope | **Open** after layouts (product acceptance, not wire) |

## Lab tooling

- [x] Tooling for this now exists: `tools/probe/ncprobe.py` is a cipher-free NCL proxy that logs every NC packet both ways and can inject/drop on either side (selftest `tools/probe/ncselftest.py`). `tools/probe/lab/runnc.sh` + `lab/nc-core.plan` drive receive-handler fuzz; `lab/nc-write.plan` dumps the write layouts (prop order, clear-vs-leave, length-prefix form) into `proxy.log`. Receive-handler crash fuzz stays separate from this write-layout gap.
