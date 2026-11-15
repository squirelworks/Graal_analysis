# PLO 194 — client reset (`PLO_RESETCLIENT`, was `CLEARWEAPONS`)

Date: 2026-11-16

Server → client id **194** is an **empty** packet. Lab gservers send it
before the weapon list at login (and also on the RC burst). How much a
**game** client clears depends on the build generation.

Tags: **[bin]** · **[srv]** / **[cap]** for send habit · **[inf]** where
noted. Earlier write-up: `unknown-ids-2026-11-06.md` §PLO 194.

## Layout

Empty body. No fields. **[bin]**

## Name

| Label | Role |
|---|---|
| `PLO_RESETCLIENT` | Preferred (gs2lib / Seihai suite since 2026-11-11) |
| `PLO_CLEARWEAPONS` | Older Seihai / community name — too narrow for 5.x+ |
| RC burst text | Still often written “CLEARWEAPONS” in capture notes |

## What focus clients clear **[bin]**

| Build | Effect of 194 |
|---|---|
| **4.20r8** (and same-era 4.x) | Clears the **weapon and class script lists** and their **name index** (`v4x-clients.md`) |
| **5.00r7** | Clears **every loaded level** and the **level caches** — broader than weapons/classes alone (`v5x-clients.md`) |
| **6.03r7** | Resets state on the main game object, deletes objects in two global lists (read as weapons/classes), empties further containers — **more** than 4.x (`unknown-ids-2026-11-06.md`) |
| **1.39–2.310** | No receive case for 194 |

Handled from **4.04r2 through 6.03r7** in the version chain. **[bin]**

## Server / RC habit **[srv]** **[cap]**

- GServer-v2 (lab) sends empty 194 before the weapon list at login.
- RC login burst includes 194 early (`rc-capture-2026-11-04.md`: after
  signature, before staff chat / player list). That is the **server’s**
  habit toward RCs, not a second game-client clear table.

## Others Work lead — `login*` keep (L5 / B1)

**Claim (lead only):** 194 keeps weapons whose **origin server** name
starts with `login`, deletes level/global NPCs, and resets the selected
weapon.

| Piece | Our stance |
|---|---|
| Selective keep of `login*`-origin weapons on **4.20r8** | **Unconfirmed / tension.** Our 4.20r8 read is a **full clear** of weapon **and class** lists, not a selective keep. |
| Broader NPC / selected-weapon side effects | Not traced as a separate 194 checklist on stock focus builds this pass. |
| Implement “keep `login*`” in Seihai | **Do not**, until a stock re-read + loopback **L** confirms it. |

### Related but different: `login*` on the **132** path

On the classic weapon-bytecode path, 4.x **marks** a weapon when the
**current server name** starts with `login` (same test used to keep
Login-server update packages apart) — see `unknown-ids-2026-11-06.md`
§PLO 132. That shows the client has a `login*`-server concept. It is
**not** proof that **194** preserves those weapons.

## pyReborn contrast **[inf]**

pyReborn’s handler clears only its weapon list. Every stock client we
read clears **at least** weapons+classes (4.x) or **more** (5.x/6.x).
Treat their 194 as under-clearing relative to real clients
(`client-internals/pyreborn-study/README.md`).

## Open (needs stock binaries / loopback — not Share corpus)

1. Re-read stock **4.20r8** and **6.03r7** 194 handlers for any
   `login*`-origin filter (Others Work live claim).
2. Loopback **L**: Login-mode weapons present → 194 → which survive.
3. Whether 5.12 / 5.24 match 5.00r7’s “levels + caches” reading or the
   6.x broader reset (5.12 is in the handled set; effect not separately
   written up).
4. Selected-weapon / level-NPC side effects as an explicit checklist.

## Implications for Seihai

- Keep the id named **`PLO_RESETCLIENT`** (empty).
- When a login burst starts sending 194, assume **full clear** of the
  script lists the client generation is known to wipe — not a
  `login*`-keep filter.
- Login-mode weapon survival across serverwarp remains a **lab** question
  (research-list guest / Login tracks), not a 194 decode shortcut.
