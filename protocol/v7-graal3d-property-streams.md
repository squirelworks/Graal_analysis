# v7 Graal3DEngine: property streams

Date: 2026-11-08

Target: Worlds `WorldsSetup64-614` `unpacked_Graal3DEngine.dll`. Tags: **[bin]** v7 switches · **[doc]** GServer / earlier client prop tables where v7 matches.

No addresses in this file. Related: `v7-graal3d-player-properties.md` (script registry), `v7-graal3d-pli-plo-tables.md` (PLI slot 44 / `tclient_set*props`).

---

## 1. Wire model

A prop stream is **`(GCHAR id, value)*`** to end of message. No per-prop length prefix — the reader must know each id’s encoding. Unknown ids stop the loop (already-applied props stay). **[doc][bin]**

| Stream | Typical header before the prop loop | Script inbound |
|---|---|---|
| Self player | (none beyond packet framing) | `tclient_setplayerprops` |
| Other player | `GSHORT` player id | `tclient_setotherplayerprops` |
| NPC | `GINT3` npc id | `tclient_setnpcprops` |
| Baddy | `GCHAR` baddy id | `tclient_setbaddyprops` |

Encodings: `c` = GCHAR (`byte − 0x20`), `s` = GSHORT, `i3` = GINT3, `i5` = GINT5, `str` = GSTRING.

Outbound PLI: logical slot **44** `onSendPlayerProperties` packs the player encode switch. **[bin]**

---

## 2. Player props (PLPROP) **[bin][doc]**

### v7 coverage

| Direction | Id labels present in switch |
|---|---|
| **Encode** | 0–36, 42–45, 50–53, 74–82 |
| **Decode** | 0, 2, 8–13, 15–21, 23–24, 30–36, 37–76, 78–82 (broad; includes full GATTRIB span) |

### Id → name → encoding

| Id | Name | Enc | v7 notes |
|---:|------|-----|----------|
| 0 | NICKNAME | str | |
| 1 | MAXPOWER | c | heart containers |
| 2 | CURPOWER | c | hearts×scale |
| 3 | RUPEESCOUNT | i3 | gralats |
| 4 | ARROWSCOUNT | c | |
| 5 | BOMBSCOUNT | c | |
| 6 | GLOVEPOWER | c | |
| 7 | BOMBPOWER | c | encode uses a constant |
| 8 | SWORDPOWER | c(power+30) + str(image) | **confirmed** `+30` path |
| 9 | SHIELDPOWER | c(power+10) + str(image) | **confirmed** `+10` path |
| 10 | GANI | str | |
| 11 | HEADGIF | c(len+100)+image or default head index | classic form still present |
| 12 | CURCHAT | str | |
| 13 | COLORS | 5×c | |
| 14 | ID | s | |
| 15 / 16 | X / Y | c(round(2×coord)) | half-tiles **confirmed** |
| 17 | SPRITE | c | |
| 18 | STATUS | c | bits: paused/hidden/male/dead/weapons/hide sword/spin |
| 19 | CARRYSPRITE | c | |
| 20 | CURLEVEL | str | |
| 21 | HORSEGIF | str | |
| 22 | HORSEBUSHES | c | |
| 23 | EFFECTCOLORS | c | |
| 24 | CARRYNPC | i3 | |
| 25 | APCOUNTER | s(+1) | |
| 26 | MAGICPOINTS | c | |
| 27–29 | KILLS / DEATHS / ONLINESECS | i3 | |
| 30 | IPADDR | i5 | |
| 31 | UDPPORT | i3 | |
| 32 | ALIGNMENT | c | AP 0–100 |
| 33 | ADDITFLAGS | c | |
| 34 | ACCOUNTNAME | str | |
| 35 | BODYIMG | str | |
| 36 | RATING | i3 | packed rating/deviation |
| 37–41 | GATTRIB1–5 | str | |
| 42 | ATTACHNPC | c(type)+i3(id) | |
| 43 / 44 | GMAPLEVELX / Y | c | |
| 45 | Z | c(z+50) legacy | **confirmed** `+50` bias path |
| 46–49 | GATTRIB6–9 | str | |
| 50 | JOINLEAVELVL | c | |
| 51 | PCONNECTED | — | disconnect marker |
| 52 | PLANGUAGE | str | |
| 53 | PSTATUSMSG | c | |
| 54–74 | GATTRIB10–30 | str | decode covers this span |
| 75 | OSTYPE | str | |
| 76 | TEXTCODEPAGE | i3 | |
| 77 | UNKNOWN77 | ? | encode lists it; treat as hostile to old clients **[doc]** |
| 78–80 | X2 / Y2 / Z2 | s pixel-precision | present |
| 81 | UNKNOWN81 | c | encode lists it |
| 82 | COMMUNITYNAME | str | |

### STATUS / ADDITFLAGS **[doc]**

- STATUS `0x01` paused · `0x02` hidden · `0x04` male · `0x08` dead · `0x10` allow weapons · `0x20` hide sword · `0x40` spin.
- ADDITFLAGS `0x01` no mass msg · `0x02` one level · `0x04` no toall · `0x08` voice off.

---

## 3. NPC props (NPCPROP) **[bin][doc]**

v7 decode switch labels: **0–47, 53–77** (gap at 48–52 matches classic “unknown aborts stream” zone for some clients).

| Id | Name | Enc |
|---:|------|-----|
| 0 | IMAGE | str |
| 1 | SCRIPT | s(len)+text |
| 2 / 3 | X / Y | c (half-tiles / px÷8 family) |
| 4 | POWER | c |
| 5 | RUPEES | i3 |
| 6 / 7 | ARROWS / BOMBS | c |
| 8 / 9 | GLOVE / BOMBPOWER | c |
| 10 / 11 | SWORD / SHIELD image | c(power+30/+10)+str or c(0) |
| 12 | GANI | str |
| 13 / 14 | VISFLAGS / BLOCKFLAGS | c |
| 15 | MESSAGE | str |
| 16 | HURTDXDY | 2×c |
| 17 | ID | i3 |
| 18 | SPRITE | c |
| 19 | COLORS | 5×c |
| 20 | NICKNAME | str |
| 21 | HORSEIMAGE | str |
| 22 | HEADIMAGE | c(len+100)+image |
| 23–32 | SAVE0–9 | c |
| 33 | ALIGNMENT | c |
| 34 | IMAGEPART | s x, s y, c w, c h |
| 35 | BODYIMAGE | str |
| 36–40 | GATTRIB1–5 | str |
| 41 / 42 | GMAPLEVELX / Y | c |
| 43 | Z | c(z+50) |
| 44–47 | GATTRIB6–9 | str |
| 48 | UNKNOWN48 | abort risk on old clients **[doc]** |
| 49–52 | SCRIPTER / NAME / TYPE / CURLEVEL | str |
| 53–73 | GATTRIB10–30 | str |
| 74 | CLASS | str |
| 75 / 76 | X2 / Y2 | as player X2/Y2 |
| 77 | Z2 | as player Z2 |

---

## 4. Baddy props (BDPROP) **[doc]** (+ v7 inbound name)

`tclient_setbaddyprops` is present. Full per-id encode/decode walk for baddies in v7 is **not finished** this pass; classic table still applies unless proven otherwise:

| Id | Name | Notes |
|---:|------|-------|
| 0 | ID | |
| 1 / 2 | X / Y | c(tiles×2) |
| 3 | TYPE | 0 graysoldier … 9 dragon |
| 4 | POWERIMAGE | c(power)+str(image) |
| 5 | MODE | walk/look/hunt/hurt/bumped/die/… |
| 6 | ANI | c |
| 7 | DIR | c packed directions |
| 8–10 | VERSESIGHT / HURT / ATTACK | str |

---

## 5. Script registry vs wire **[bin]**

The **95-name** script catalog on `TServerNPC` / `TServerWeapon` (`account`, `nick`, `attr`, …) is **not** the PLPROP id space. Overlaps are semantic only (see `v7-graal3d-player-properties.md`). Script `attr` maps to the GATTRIB family (wire 37+).

Attached / showimg-style fields appear as script names (`attached*`, `peltwith*`, body/head/sword/shield `*img`) rather than new wire id blocks in the player encode switch.

---

## 6. Diff vs 6.0.3.7 / 6.1.1.3

| Topic | 6.0.3.7 / 6.1.1.3 | v7-614 |
|---|---|---|
| PLPROP numbering | classic | **same** |
| Sword/shield/head/X/Y/Z encodings | classic | **confirmed unchanged** |
| Cleartext `onSendPlayerProperties` | 6.11 yes | encrypted; remapper slot 44 |
| `tclient_setplayerprops` family | 6.11 yes | encrypted; recovered |
| Highest encode ids through 82 | modern clients | present |

Nothing in the recovered switches indicates a Worlds-specific renumbering of PLPROP/NPCPROP.

---

## 7. Open

1. Finish baddy encode/decode case walk in v7.  
2. Dirty-field vs full-snapshot policy on Worlds servers.  
3. Exact `attr[n]` → GATTRIB id stride when set from script.
