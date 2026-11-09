# v7 Graal3DEngine: player / object properties

> Wire PLPROP/NPCPROP/BDPROP tables: see `v7-graal3d-property-streams.md`.

Date: 2026-11-08

Target: Worlds `WorldsSetup64-614` `unpacked_Graal3DEngine.dll`. Tags: **[bin]** · **[doc]** GServer/gs2lib player-props + 6.1.1.3 cleartext used as a cross-check.

No addresses in this file. Raw extracts: `Graal_analysis/_work/ghidra_v7_614/props_gs2_*.json`, `registry_to_plprop_semantic.json`, encode/decode decomps.

---

## 1. What “properties” means here

Two related surfaces:

| Surface | Role |
|---|---|
| **Script property namespace** | Named fields on actors / weapons / NPCs (`nick`, `bodyimg`, `x`, …) exposed to GS2 / client scripts |
| **Wire `PLAYERPROPS` stream** | `(GCHAR id, value)*` packet body synced client↔server |

v7 still has the outbound remapper slot for **`onsendplayerproperties`** (slot 44) and inbound flag siblings. Cleartext `PLO_*` / `PLI_*` / `onSendPlayerProperties` spellings are **absent**; names are encrypted or live only in the script property list below. **[bin]**

RTTI-style names from 6.1.1.3 (`TPlayerProperties`, `TServerPlayerProperties`) do **not** appear as cleartext in v7-614. **[bin]**

---

## 2. Script-visible property list (95 names) **[bin]**

A single comma-separated registry is installed on script objects that wrap **`TServerNPC` / `TServerWeapon`** (constructor path splits the string into a name vector).

List order below is the **registry index** (0…94) as stored in the binary. This is the **script-facing catalog**, not the on-wire PLPROP id space.

| Id | Name | Id | Name | Id | Name |
|---|---|---|---|---|---|
| 0 | account | 32 | horseimg | 64 | peltwithnpc |
| 1 | alpha | 33 | hp | 65 | peltwithbush |
| 2 | ani | 34 | hurtdx | 66 | peltwithsign |
| 3 | aniparams | 35 | hurtdy | 67 | peltwithvase |
| 4 | anistep | 36 | id | 68 | peltwithstone |
| 5 | ap | 37 | isadmin | 69 | peltwithblackstone |
| 6 | attached | 38 | isblocking | 70 | platform |
| 7 | attachid | 39 | isblockingprojectiles | 71 | playersindex |
| 8 | attachtype | 40 | isbuddy | 72 | playerlisticon |
| 9 | attachedtoobject | 41 | ischannel | 73 | rating |
| 10 | attr | 42 | ischannelopen | 74 | ratingd |
| 11 | blue | 43 | ischanneluser | 75 | red |
| 12 | body | 44 | isexternal | 76 | rotation |
| 13 | bodyimg | 45 | isfemale | 77 | rotationcenter |
| 14 | bombs | 46 | isignored | 78 | rupees |
| 15 | chat | 47 | isignoring | 79 | save |
| 16 | chatoffset | 48 | isloggedin | 80 | shield |
| 17 | colors | 49 | ismale | 81 | shieldimg |
| 18 | communityname | 50 | ismuting | 82 | shieldpower |
| 19 | darts | 51 | language | 83 | stretchx |
| 20 | dir | 52 | languagedomain | 84 | stretchy |
| 21 | fullhearts | 53 | layer | 85 | sprite |
| 22 | glovepower | 54 | level | 86 | sword |
| 23 | gmap | 55 | levelname | 87 | swordimg |
| 24 | gralats | 56 | mapicon | 88 | swordpower |
| 25 | green | 57 | maxhp | 89 | useowncenter |
| 26 | guild | 58 | messagebubble | 90 | width |
| 27 | head | 59 | mode | 91 | x |
| 28 | headimg | 60 | mp | 92 | y |
| 29 | headset | 61 | nick | 93 | z |
| 30 | hearts | 62 | npcsindex | 94 | zoom |
| 31 | height | 63 | paused |  |  |

### Notes on the catalog

- **`attr`** is a single registry entry — on the wire this expands to the classic `GATTRIB1`…`GATTRIB30` family (PLPROP 37–41, 46–49, 54–74). Script sees one name; encode/decode still uses numbered PLPROP ids. **[bin][doc]**
- Combat / Zelda-ish stats, presence flags, attachment / carry, transform, and animation names match the 6.x surface.

---

## 3. Wire codec: classic PLPROP still in v7 **[bin]**

v7 embeds the long-standing **`(GCHAR id, value)*`** player-property stream. Encode and decode switches were recovered in the native player object:

| Direction | Behavior |
|---|---|
| **Encode** | `switch(id)` emitting GCHAR-prefixed fields; the selected numeric-ID 8/9/15/16 arithmetic is qualified below; historical name/getter interpretations are not independently validated by this correction; Z uses `value + 0x52` (= +50 + 0x20 GCHAR bias) when the legacy path is active |
| **Decode** | Matching `switch` over the same id space (including gattribs through ~82 / `communityname`); sword reverse is `gchar − 30` then optional image |

[bin] **Exact build-614 correction (2026-11-09):** the retained two-stage encoder dispatch covers input IDs 0–82 inclusive using 83 one-byte selector entries and a 43-entry target table. Eleven input IDs take the default target: **3, 25, 27, 28, 29, 30, 34, 36, 50, 51, 77**. The other 72 are nondefault dispatch inputs, not 72 independently validated accepted/emitting properties. These compiled-table counts are not source-language case-label counts; they replace the earlier “54 labels” claim. They do not map input IDs to the separate 95-name script registry or independently establish getter/property-name meanings.

[bin] Source `V7-019-SANITIZED-20261109` identifies the sanitized correction packet, SHA-256 `2f2d7610109ff2a6e12c05aefb0ceec360d69b79e629ffd37ec5cea42432f77b`. The exact supplied Windows amd64 WorldsSetup64-614 unpacked plugin has SHA-256 `daa141bbd306cc6c588ebe6d8823fd04497ca4150837a59b49e8097f27b776c3`. The researcher reports 20 retained exact-byte assertions with PE-mapped decoding; the publisher reviewed the structured report and recomputed saved dispatch counts. Neither operation re-executed the client or independently reproduced the original-to-unpacked derivation. Runtime behavior, inbound decoder behavior, nonfinite/out-of-range conversions and complete helper semantics remain unvalidated. The selected numeric arithmetic below does not newly establish historical property names.

### Encoding cheat-sheet (v7-confirmed subset)

| Id | Classic name | v7 encode notes |
|---:|---|---|
| 0 | NICKNAME | GSTRING (length-clamped) |
| 1 | MAXPOWER | GCHAR |
| 2 | CURPOWER | GCHAR from hearts×scale |
| 4–6 | ARROWS / BOMBS / GLOVE | GCHAR |
| 7 | BOMBPOWER | constant GCHAR |
| 8 | SWORDPOWER (historical name) | Selected arithmetic adds 30, clamps to 10–50, substitutes zero for 30, then applies byte bias 32; name/getter and optional image behavior are not revalidated here |
| 9 | SHIELDPOWER (historical name) | Selected arithmetic adds 10, clamps to 10–13, substitutes zero for 10, then applies byte bias 32; name/getter and optional image behavior are not revalidated here |
| 11 | HEADGIF | head-default path or `len+100` + image (classic form) |
| 15 / 16 | X / Y (historical names) | Selected path doubles the value, uses a floor-style helper with successive 0.5 and 0.0001 addends, then byte bias 32; finite values in the representable conversion range only |
| 35 | BODYIMG | GSTRING |
| 45 | Z | legacy: `GCHAR(z + 50)` (via `+ 0x52` with GCHAR bias) |
| 78–80 | X2 / Y2 / Z2 | higher-precision path present |
| 82 | COMMUNITYNAME | GSTRING |

Full id→encoding table for ids not re-listed above: treat **[doc]** `~/FU/Graal_analysis/protocol/player-props.md` as still authoritative; v7’s switches did not invent a new numbering. **[bin][doc]**

### STATUS / ADDITFLAGS

Unchanged from classic (**[doc]**): prop 18 bit flags (paused/hidden/male/dead/…); prop 33 additflags.

---

## 4. Script registry ↔ wire PLPROP (semantic) **[bin][inf]**

Registry index ≠ wire id. Useful overlaps:

| Registry name | Wire PLPROP id | Wire name |
|---|---:|---|
| nick | 0 | NICKNAME |
| fullhearts / maxhp | 1 | MAXPOWER |
| hearts / hp | 2 | CURPOWER |
| rupees / gralats | 3 | RUPEESCOUNT |
| darts | 4 | ARROWSCOUNT |
| bombs | 5 | BOMBSCOUNT |
| glovepower | 6 | GLOVEPOWER |
| sword / swordpower / swordimg | 8 | SWORDPOWER |
| shield / shieldpower / shieldimg | 9 | SHIELDPOWER |
| ani | 10 | GANI |
| head / headimg | 11 | HEADGIF |
| chat | 12 | CURCHAT |
| colors | 13 | COLORS |
| id | 14 | ID |
| x / y / z | 15 / 16 / 45 | X / Y / Z |
| sprite | 17 | SPRITE |
| level / levelname | 20 | CURLEVEL |
| horseimg | 21 | HORSEGIF |
| mp | 26 | MAGICPOINTS |
| ap | 32 | ALIGNMENT |
| account | 34 | ACCOUNTNAME |
| body / bodyimg | 35 | BODYIMG |
| rating | 36 | RATING |
| attr | 37+ | GATTRIB family |
| language | 52 | PLANGUAGE |
| communityname | 82 | COMMUNITYNAME |

Many registry entries (`alpha`, `isbuddy`, `peltwith*`, `zoom`, …) are **script/local only** in this catalog — they are not 1:1 PLPROP ids. **[inf]**

---

## 5. Wire / remapper touchpoints **[bin]**

| Remapper slot | Decrypted event | Property relevance |
|---|---|---|
| 44 | `onsendplayerproperties` | primary property sync send hook |
| 45 | `onsendnpcproperties` (6.11 name; gap in v7 pair dump) | NPC prop sync |
| 46 / 47 | `onsendflag` / `onsendunsetflag` | flag set/clear |
| 22 | Shot (own slot) | projectile fire |
| 23 | BaddyProperties (shares remapper cell with 22) | baddy prop stream (C→S) |
| 14 / 15 | weaponhit / playerhurt | combat → hearts/hp side effects |

Script-side position setters still cleartext: `onServerSetPlayerX` / `Y` / `Z`, plus `SetPlayerPosition`. **[bin]**

Outbound slot-44 bridge is a thin multi-target dispatcher; the actual field packing is the encode switch above. **[bin]**

---

## 6. Related client strings **[bin]**

- Nickname UX: `nickname_new`, `nicknamelimit`, `limitnicknames`
- Item art stubs: `sword1.png`…, `shield1.png`…, `fullheart`, `goldensword`, `mirrorshield`, …
- Gani: `.gani`, `gani::`, `TGaniObject`, `TGaniParam`

---

## 7. Open questions

1. Exact dirty-field vs full-snapshot policy Worlds servers use when emitting the stream.
2. Whether every PLPROP id through 82 is exercised on the Worlds production path, or a subset.
3. Per-index wire packing when script writes `attr[n]` (family start id 37 confirmed; stride not re-traced this pass).
