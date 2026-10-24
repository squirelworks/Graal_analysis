# New facts and contradictions against Graal_analysis and the laundry notes

## Contradicts or corrects
1. **Emote lookup (laundry 11-emotes-ganis.md step 4)** assumed Ctrl+letter maps to named files and sends PLI_SHOWIMG (24). In 2.05 the key path is local only (no packet). The lookup is a *prefix* match on `emoticon_<letter>` in the file list. SHOWIMG (24) is sent only by the script command `showimg`.
2. **1st Graal room name** is not always the constant `Zelda2`; one branch builds `Z` + level base + `2` (relay-1998.md says 1st and 2nd use `Zelda2`).
3. **TPersonAction** is the NPC "Set Npc's Action" script editor, not a player action menu.

## New (not in existing notes)
- Death sequence timings (timer cap 30, input lock until 28, dead status bit from 28), respawn hearts by AP, respawn destination rule, no respawn packet.
- Wire sprite table (step to sprite) and the gani name to step rules; no swim sprite on the wire.
- Status-bit meanings (prop 18) and mode values.
- Sword hit evaluated on the victim; reach 0 to 4 tiles, lateral under 2, AP 100 immune.
- F7 popup item order for 2.05 and PM recipient encoding.
- Send helper drops payloads that contain a newline (1.39 and 2.05).

## Confirmed (no change)
- 1.39 token, host and port, login layout, no cipher, framing, send id list, receive id list.
- 1st Graal port 14801, `NZelda2#def`, `Graalsav1`, D type set.

## Labels
The upload labels for the three bundles do not match their contents (the 2.05 build was not in the folder labelled for it). File names were used to decide.
