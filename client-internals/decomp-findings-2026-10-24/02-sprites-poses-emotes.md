# 2.05 rev2: sprite index, poses and emotes (derived)

Tables: `gani-name-table.tsv`, `gani-short-codes.tsv`, `gani-to-step.tsv`, `sprite-step-table.tsv`, `status-bits-prop18.tsv`, `player-modes.tsv`.

## How the sprite prop (17) is built
- Wire value = 32 + direction + 4 x S.
- S comes from the current animation step through the step table, only when the active gani is the default "def" gani and the step is 38 or lower.
- Hurt is special: S = 32 (value 0x80 + direction as seen in the byte).
- Other ganis do not change the sprite number. (Inferred: they travel by the gani prop.)
- Each gani name maps to a step by a small rule list (`gani-to-step.tsv`): walk is frame+1, sword/ridesword/spin are 9 + frame mod 5, push 14+frame, pull 20+frame, grab 19, lift 23, carry still 24, carry 25+frame, shoot 33, ride variants 34 to 36, sit 37, sleep 38, hurt 39, dead 40.
- Caveat: the "only for def" condition was read from the sender and is documented as observed. The same sender sets everything to 0 for unknown names.

## Swim, lava and dead on the wire
- There is **no swim sprite on the wire**. Swim, lava and dead are all sent as sprite 0 (idle) plus direction.
- Swim is local mode 10, entered on tile type 11 with a splash. Local gani "swim" is name-table index 28 and "lava" is index 29, but neither has a sprite value.
- Tile type 12 shows the "lava" gani.
- Inferred: other players can tell a swimmer apart only through the gani prop, not the sprite.

## Gani name table
31 names, index 0 to 30 (`gani-name-table.tsv`). The short-code table (`gani-short-codes.tsv`) maps substrings to one letter and is used to shorten cached gani file names.

## Emotes (Ctrl+letter)
- Holding Ctrl and pressing A to Z (while no text field has focus and the player is not dead/locked) calls the emote routine with that letter.
- The routine lowercases the letter and walks the loaded file list. It takes the **first file whose name starts with** `emoticon_<letter>` and whose extension is png, mng or gif. (A prefix match, so Ctrl+A matches `emoticon_afk_stay` if that file is first in the list.)
- The image is placed at the player's x+2, y-5 (a little lower if a second flag is set) and shown for 50 ticks (2.5 s).
- The emote is data driven. No letter-to-name table exists in the client, and there are no hard-coded AFK/BRB/Zzz strings.
- **No network send was found on the key path.** The PLI_SHOWIMG (24) sender is reached only from the script command `showimg`. How other players see an emote (the captured AFK image) is therefore not explained by the key handler. Treat that as open.
- The same routine and file-name scheme exist in 1.39, so emotes are not new in 2.05.

## Status prop (18)
See `status-bits-prop18.tsv`. Dead (0x08) is delayed as described in `01-death-respawn.md`.
