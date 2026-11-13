# v5 — properties

Date: 2026-11-08 · Tags: **[bin][ghidra]**

## Script-facing names · **high** (late 5)

5.314 has no single `account,alpha,…` comma registry and no `setplayerprop` string. Names are referenced from two script property tables. Combined list (order is the reference order, not a wire order):

| Group | Names |
|---|---|
| Identity | `account`, `guild`, `communityname`, `platform`, `language`, `languagedomain`, `isadmin`, `isloggedin` |
| Body | `bodyimg`, `headimg`, `headset`, `horseimg`, `sprite`, `shield`, `shieldimg`, `shieldpower`, `sword`, `swordimg`, `swordpower`, `glovepower` |
| Stats | `hearts`, `fullhearts`, `maxhp`, `rupees`, `bombs`, `darts`, `gralats`, `rating`, `ratingd` |
| Pose | `alpha`, `aniparams`, `anistep`, `height`, `width`, `stretchx`, `stretchy`, `rotation`, `hurtdx`, `hurtdy`, `layer` |
| Attach | `attached`, `attachid`, `attachtype`, `attachedtoobject` |
| Social flags | `isbuddy`, `isignored`, `isignoring`, `ismale`, `isfemale`, `ismuted`, `ismuting`, `ischannel`, `ischannelopen`, `ischanneluser`, `isexternal`, `isguildpm`, `ismasspm` |
| World | `level`, `levelname`, `playersindex`, `npcsindex`, `mapicon`, `playerlisticon`, `messagebubble`, `chatoffset`, `paused` |
| Carry tests | `peltwithnpc`, `peltwithbush`, `peltwithsign`, `peltwithvase`, `peltwithstone`, `peltwithblackstone` |
| Types | `TServerNPC`, `TServerWeapon`, `TServerPlayer`, `TGaniObject`, `isweapon` |

5.303 has the same marker names (`account`, `sword`, `headimg`, `onRemotePlayerChats`). Confidence they share this list: medium (string presence, tables not re-read).

## Wire property ids · **high** (switch exists) · **high** (three names)

The applicator switches on the GCHAR byte (`id = byte − 0x20`) for ids 0–82. Most arms are unnamed. Arms with a string in that arm only:

| id | Evidence |
|---|---|
| 11 | `head0.png` |
| 12 | `onRemotePlayerChats` |
| 17 | `setani` |

Ids 37–41, 46–49, and 54–74 share one length-prefixed arm. Ids 1, 3–7, 14, 22, 25–29, and 77 share a tail that also mentions `onPlayerChanges` (the tail, not a per-id name).

Sword and shield **image filenames** (`sword1.`–`sword4.`, `shield1.`–`shield3.`) live in a separate image-index switch. That switch is not this wire-id table. PLO id 19 mentions the words `sword` and `shield`; that is not proof that wire prop id 8 is sword.

## 5.0.0.7 · **high** (names present) · **open** (ids)

`GraalEngine.dll` has `setplayerprop` and `playerhp`, which late-5 does not spell that way. `sword1.` and `head0.png` are also in that DLL. Numeric prop ids were not re-decoded. No comma registry string.
