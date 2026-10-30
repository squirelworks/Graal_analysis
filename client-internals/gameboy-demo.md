# Graal Game Boy Color demo (1999)

Date: 2026-10-29, emulator run added 2026-10-30

This note covers the full disassembly of `Graal V1.1 Adventure Demo (PD) [C].gbc` (262,144 bytes, MD5 2b2fef91…, the same bytes as `graal.gb` in `graalgb.rar`).
The first look at this ROM is in `precursors-and-fan-builds.md`.

The disassembly itself is in the project's shared folder under `graal-decompile/gameboy-demo/`, not in this repo. That folder holds RGBDS-syntax sources for all 16 banks, the graphics as `.2bpp` files, PNG renders of every room, the scripts that produce them, and a README.
The sources reassemble to a byte-identical ROM. That was checked with a small assembler written for this job; RGBDS itself was not run.
This note is cleaned: it has no code and no code addresses. ROM locations are given only where they describe a data format.
The first sections come from reading the code. The section "Seen in an emulator" adds what the running ROM did, and corrects the static read where they differ.

## What it is built with

- **GBDK 2.x and its LCC C compiler.** The start-up code is GBDK's crt0: interrupt handler chains, the `.mode` table, `add_VBL` and the rest. The game code has LCC's fingerprints: arguments on the stack, `switch` statements as jump tables, and `int` constants read from a per-bank constant pool.
  Of 161 functions, 41 are GBDK library or crt0 routines (`set_bkg_data`, `set_win_tiles`, `set_sprite_palette`, `joypad`, `memcpy`, `arand`, the multiply and divide helpers and so on). The other 120 are the game.
- **Everything runs in the VBlank interrupt.** `main` sets up the screen, loads room 0, installs one VBlank handler with `add_VBL`, turns on sound, switches the CGB to double speed and returns. From then on crt0 just idles. The handler does one game tick: OAM DMA, scrolling, the window slide and music on every VBlank, and the game logic on every second one (about 30 Hz).
- **Banking.** One helper writes the MBC1 bank register and remembers the bank. Code in banks 1 and 3 is reached through small bank-0 wrappers that switch, call and switch back.

## Header and bank map

The cartridge type is `$02` (MBC1+RAM), but the RAM size byte is 0. The CGB flag is `$80`, so the ROM runs on both models. Only banks 0 to 5 hold anything. Banks 6 to 15 are all `$FF`.

| Bank | Contents |
|---|---|
| 0 | crt0, the GBDK library, and the core game: room loader, input, text box, Select menu, collision, the VBlank tick |
| 1 | Entity update and AI, entity drawing, lifting and throwing, camera, the music player and its note table |
| 2 | Graphics: two tilesets of 256 tiles, the 82-tile font, walk bitmaps, five BG palette sets, animated tiles, 172 sprite tiles |
| 3 | Objects (lifted and thrown things), sound effects, entity set-up, sprite sorting, two AI routines, the character table with heads, palettes and names |
| 4 | Room pointer table and rooms 0 to 4 |
| 5 | Rooms 5 and 6 |

## Screen and coordinates

- A room is exactly one 32×32-tile BG map, which is 256×256 pixels. Nothing is streamed: the loader writes the whole map to VRAM, and the camera scrolls over it.
- Positions are 16-bit values in half pixels. A map tile is 16 units (8 pixels).
- Directions are numbered 0 up, 1 left, 2 down, 3 right. That is the same order as the PC client.
- The window layer holds the text box and the Select menu, and slides up from the bottom of the screen.
- Sprites are 8×16. The game builds them in a WRAM buffer, sorts them by Y, and copies them to the DMA page every tick.

## Room format

Bank 4 starts with a table of seven 16-bit header pointers. Rooms 0 to 4 are in bank 4 and rooms 5 and 6 in bank 5; the loader picks the bank as room / 5 + 4.

**Header (13 bytes):**

| Offset | Size | Field |
|---|---|---|
| 0 | 2 | map pointer |
| 2 | 1 | tileset (0 outdoor, 1 indoor) |
| 3 | 1 | BG palette set (0 to 4) |
| 4 | 1 + 2 | link count, link list pointer |
| 7 | 1 + 2 | text count, text list pointer |
| 10 | 1 + 2 | NPC count, NPC list pointer |

- **Map:** 1,024 tile ids, then 1,024 CGB attribute bytes (palette, VRAM bank, flips), both 32×32. The loader keeps two WRAM copies of the tile ids: one as loaded and one that changes when things are lifted. Collision reads the second one.
- **Link (8 bytes):** x, y, width, height, new x, new y, then the target room as a 16-bit number. A new x or y of −1 keeps the player's coordinate. This is the PC client's link record (`file x y w h newx newy`), with a room number in place of the file name. The player's tile is tested against the rectangle on every step.
- **Text (4 bytes):** x, y and a pointer to a zero-terminated string. A text at (0, 0) is never read from the map; NPCs and events show it by index. Signs are read only while the player faces up and the tile above is solid.
- **NPC (16 bytes):** x and y in tiles, direction, character type, two unknown bytes, a text index (−1 for none), five movement bytes (a mode, then patrol bounds), a 16-bit flag word whose eleven low bits are copied into separate entity fields, and a 16-bit event number.
  Flag bit 0 makes the NPC turn to face the player and chase once lined up. The other flags are still unknown.
- **Event 1** is the only event in the demo, on the captive in room 4. It is a timed script that counts down a timer in the entity. The captive walks a few steps, stops, lifts the stone in front of it, turns and throws it, and then text 1 opens ("Now press Select…"). While it runs, the player is held in the lower part of the room.
- **Walk bits:** each tileset has a 256-bit walkable bitmap in bank 2, plus a second 256-bit set that the object code reads when something is put down. What that second set means is not settled.

## The seven rooms

The six outdoor rooms form a 2×3 grid. Room 1 is the inside of the house in room 6.

```
 room 4 (captive)   room 6 (house, "That's your house!")
       |                    |
 room 3 (two chasers) room 5 ("Hello!")
       |                    |
 room 0 (start) ---- room 2
```

| Room | Tileset | Links to | NPCs (character type) | Texts |
|---|---|---|---|---|
| 0 | outdoor | 2 (east), 3 (north) | – | a sign: "Welcome to Graal! Demo version by Stefan Knorr" |
| 1 | indoor | 6 (the door) | – | – |
| 2 | outdoor | 0 (west), 5 (north) | Ryu | – |
| 3 | outdoor | 4 (north), 0 (south) | Pach Soldier, Squall | – |
| 4 | outdoor | 3 (south) | Fung Si Yun (the captive), event 1 | the captive's two texts |
| 5 | outdoor | 2 (south), 6 (north) | Mandi, Lunar, Mandi | "Hello!" (all three NPCs) |
| 6 | outdoor | 5 (south), 1 (the house door) | Vincent, Squall | a sign: "That's your house!" |

The "Welcome to Graal" text is an ordinary sign in the first room, not a title screen. There is no title screen: `main` goes straight to room 0.

Room 4's texts, as the 18-character lines lay them out:

> Thanks for freeing me! I will follow you and help you completing your task. But first let me show how to lift stones! Press A to lift, A again to throw!
>
> Now press "Select" and switch to "Fung Si Yun"

PNG renders of all seven rooms with their real palettes, and of the whole grid, are in the shared folder under `png/`.

## Text

- The text box is three lines of 18 characters at the bottom of the screen. The strings are padded with spaces so that words break at the right places.
- A new press on the d-pad while the box is open shows the next three lines. After the last page the box closes. In play, only a direction other than the one the player faces turns the page; pressing the facing direction does nothing.
- Character codes: `0x20` space, `0x21`–`0x3A` A–Z, `0x3B`–`0x54` a–z, `0x55`–`0x5E` 0–9, then punctuation (`0x5F` "!", `0x62` ".", `0x63` ",", `0x67` used both as an apostrophe and as a quotation mark). The tile drawn is the code minus `0x20`; the font sits at tile 0 of CGB VRAM bank 1.

## Characters

Bank 3 holds a table of 31 character types. Each type has a name, three CGB OBJ palettes and a 16×16 head with two frames. Several types reuse another type's head with new colours.

| # | Name | # | Name | # | Name | # | Name |
|---|---|---|---|---|---|---|---|
| 0 | Fung Si Yun | 8 | Zoraas | 16 | Oldman | 24 | Green Pach |
| 1 | Pach Soldier | 9 | Mad Max | 17 | Gold Soldier | 25 | Blue Lizard |
| 2 | Ninji | 10 | Pachukite | 18 | Gold Squall | 26 | Fire |
| 3 | Lunar | 11 | Matt | 19 | Gold Zoraas | 27 | Silver |
| 4 | Squall | 12 | Brandon | 20 | Gold Max | 28 | Theif (sic) |
| 5 | Vincent | 13 | Bob | 21 | Gold Matt | 29 | Red Squall |
| 6 | Mandi | 14 | Athena | 22 | Gold Silver | 30 | Water Athena |
| 7 | Ryu | 15 | Lizardon | 23 | Red Max | | |

Recoloured heads: Gold Soldier and Green Pach use Pach Soldier's head; Gold Squall and Red Squall use Squall's; Gold Zoraas uses Zoraas's; Gold Max and Red Max use Mad Max's; Gold Matt uses Matt's; Blue Lizard uses Lizardon's; Water Athena uses Athena's; Gold Silver uses Silver's.

These names are the character types of the demo, not only baddies. NPCs in rooms pick one by number, and so does the player.

- The player starts as type 0. Fung Si Yun, the captive in room 4, is type 0 too.
- **Select** opens a carousel in the window that shows three heads and the name of the middle one. Left and right turn it, and each step changes the player's own character type by one, wrapping through all 31.
  So the Select menu, as coded, is a free character picker over every type. It is not limited to the companion that the room 4 text mentions.

## Entities

- There are at most eight entities. Entity 0 is the player and the rest come from the room's NPC list. Each one is 50 bytes.
- Fields that are understood: position, character type, direction, text index, event number, state, animation frame, OBJ palette, movement mode and bounds, a timer, a knock-back velocity, and the id of a carried object (−1 for none).
- States: 0 idle, 1 walking, 2 reading a text, 3 swinging the sword, 4 knocked back, 5 chasing the player, 8 carrying, 9 lifting.
  The update routine dispatches on the state. Movement mode 1 is a random walk; modes 2 to 4 patrol inside bounds kept in the record, and their exact rules were not worked out.

## Player controls

| Button | Effect |
|---|---|
| D-pad | Walk; turn the page in a text box (see below); turn the Select carousel |
| A | The character's A item: lift and throw for Fung Si Yun, a bomb for Ninji, a boomerang for Ryu, nothing for the rest (see below) |
| B | Sword, unless carrying. Every character has one; only its colour changes |
| Select | Open or close the character carousel |
| Start | Toggle music |

Lifting works on 2×2 map objects. The game looks two tiles ahead and compares the object's top two tile ids with a list of four liftable kinds: three kinds of bush and stone, and a dropped object.
For the first three it writes that kind's "lifted" 2×2 tiles into the map; for a dropped object it puts back the room's original tiles. The player goes into the lifting state, then carries the object as a sprite.
A thrown object is tracked as an object of its own. In play it always broke where it came down, and nothing was written back into the map (see below). The "dropped object" kind in the list was never seen.

## Sound

- There are eight one-shot sound effects on the two pulse channels and the noise channel. They are skipped while music plays.
- A music player is in bank 1, with a 72-entry table of note periods. **Start** turns it on and off.
- The player enables cartridge RAM before it reads, and its one song pointer is `$A000`, the start of cartridge RAM. The header declares no RAM, and nothing in the ROM writes to that area. So the demo carries no song of its own, and what Start plays depends on whatever answers at `$A000`.
  This is a static reading. It may be a leftover from a development cartridge that had a song loaded into its RAM.

## Seen in an emulator

The ROM was run in PyBoy 2.8.1 in CGB mode, headless, with scripted input, screenshots every one or two frames, and the entity records read from WRAM while it ran.
Contact sheets of every test, and the scripts that made them, are in the shared folder under `graal-decompile/gameboy-demo/emulator/`.
Times are in 60 Hz frames. The game logic runs every second frame, so one logic tick is 2 frames.

**Start and screen**

- The Nintendo logo is followed straight away by room 0. There is no title, no HUD and no health display at any time.
- The CGB really is put into double speed.
- The camera keeps the player in the middle of the screen and stops at the room edges.

**Walking**

- The player moves 4 pixels per logic tick, which is 2 pixels a frame or 120 pixels a second. A room (256 pixels) takes about 2 seconds to cross.
- **Against a wall** the player keeps facing the wall and the walking animation keeps running in place. There is no push pose, however long the button is held.

**Text**

- Walking up into a sign (the stone post in room 0) or into an NPC with a text opens the box. It slides up from the bottom over a few frames.
- Capital letters are drawn in red and everything else in black.
- Select still opens the character menu while a text box is up.

**Sword**

- B swings the sword in an arc from one side to the front of the facing direction. One swing takes about 24 frames. Holding B swings again and again.
- A hit on an NPC knocks it a few pixels away, and it blinks for a moment. Nothing dies.
- The soldiers in room 3 chase the player and swing back. Their hits knock the player back the same way. Pinned against the top of the room, the player was knocked back over and over and could not get away, but nothing else happens: there is no damage and no game over.

**Lifting, carrying and throwing (Fung Si Yun only)**

- A in front of a bush, the stone post or another liftable 2×2 object swaps it for its "lifted" tiles at once (a dark stump for a bush). The object is drawn as a sprite where it stood for 10 ticks (20 frames), and then appears over the player's head.
- **While carrying**, the player is drawn facing the screen with both arms up, whatever the walking direction, and the object covers the player's head completely. So the carried object hides the head; it does not hide the whole player.
- A throws the object in the facing direction. It flies for about 6 ticks, then breaks into four leaf pieces that hang for about 8 ticks and vanish. This happened both when it hit a tree and on open grass. Nothing was put back into the map.
- Only character type 0 can lift. With any other type, A next to a bush did nothing.

**Respawn**

- Lifted bushes do not grow back while you stay in the room. One was still a stump after two minutes.
- Leaving the room and coming back restores every bush and stone, because the room is reloaded from ROM.

**The character menu and A items**

- The menu fills the whole window. It shows three heads with arrows either side, the middle character's name with capitals in red, and "Button B" and "Button A" with an item icon under each.
- Every character has a sword under B, in one of three colours (red for most, blue for Pach Soldier and Gold Soldier, purple for Mandi).
- Only three characters have anything under A, and the icon is chosen in code by the character number:
  - **Fung Si Yun (0):** a bush, meaning lift and throw.
  - **Ninji (2):** a bomb. A puts it on the ground in front. It sits for about 110 frames, flashes for about 70 more, and then blows up as a large plus-shaped blast about three tiles each way. The screen jumped as the blast went off, which looks like the blast knocking the Ninji player back; that was not checked in the entity record.
  - **Ryu (7):** a boomerang. It flies about four tiles in the facing direction and comes back to the player, about one second in all.
- This is more than the static read found. The A items are a second action set, picked by character, and the room 4 text ("switch to Fung Si Yun") is about getting the lift action.

**Rooms and NPCs**

- All seven rooms loaded and looked like the PNG renders made from the ROM.
- Room 2: Ryu stands still. Room 5: Mandi, Lunar and Mandi stand still; by the room data, each says "Hello!".
- Room 3: the first soldier patrols left and right along the top of the room at 1 pixel a frame, half the player's speed. The second wanders. Once lined up with the player, both chase at a little over 1 pixel a frame and swing their swords.
- Room 6: Vincent and Squall wander around the house.
- **Room 4, the captive.** Walking into Fung Si Yun opens the first text. When it closes, he walks two tiles left, lifts the bush there, turns and throws it, and the second text opens ("Now press Select and switch to Fung Si Yun"). This matches the event script in the code.
  The player and the captive look the same, because the player also starts as Fung Si Yun. The text reads as if the player was meant to start as someone else.

**Sound**

- The sound effects play (a noise burst for the sword).
- **Start silences the game.** With nothing at the song address, reading it gives `$FF` (as on a cartridge without RAM). The music player then writes 0 to the master volume and the channel routing, and Start again does not undo it. From then on the sword and every other effect are silent until the game is reset.
  How `$FF` is read here depends on the emulator, but it is also what a real cartridge without RAM usually returns.

## Compared with the PC client

- The same link record: a rectangle plus a new x and y, with −1 to keep a coordinate.
- The same direction numbers, and the same lift, carry and throw of 2×2 bushes and stones with A. Here the liftable objects are a fixed list of tile pairs.
- Rooms are fixed 32×32-tile maps, not 64×64 levels. Positions are in half pixels, and there is no NPC scripting: NPC behaviour is a few built-in movement modes, flags and event numbers.
- The text alphabet is a straight ASCII-like run, not the PC sign alphabet.

## What a Seihai "Game Boy demo" profile would need

This is the look and feel the run showed, as a list for a profile that copies the demo.

- One 256×256-pixel room at a time, with no scrolling between rooms: a link loads the next room with the screen off.
- Movement at 2 pixels a frame (logic at 30 Hz, 4 pixels a tick). No push pose against walls; the walk cycle keeps running.
- A text box of three lines of 18 characters in the window, sliding up, capitals in red. Paging by a d-pad direction other than the one faced.
- No HUD, no health, no death. Hits only knock back.
- Sword on B for everyone. A depends on the character: lift and throw, bomb, boomerang, or nothing.
- Carried objects cover the head, and the carrier is drawn facing the screen.
- Thrown objects always break. Nothing respawns until the room is loaded again.
- A Select menu that picks any of the 31 characters, with their head, name and B/A icons.
- No chat and no network. There is no chat bubble in the demo.

## Open

- The music data format, since no song is in the ROM. Pressing Start mutes the game rather than playing anything.
- Several entity fields and most NPC flag bits.
- The exact patrol rules of movement modes 2 to 4. The run showed a left-right patrol and a wander, not the rules behind them.
- Whether the Select carousel was meant to stay a free picker in a later version.
- The "dropped object" kind in the liftable list, which was never seen in play.
