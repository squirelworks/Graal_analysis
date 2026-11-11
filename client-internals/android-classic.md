# Android Classic and Era, 1.6 to 2.2: host, frame, collision, board, render and chat

The later Android clients are a separate line from the Windows, Linux and Mac clients in this repo. This note is a static reading of their packages. No Android device, emulator or server was used, and nothing here should be projected back onto the period clients. Evidence `VX-ANDROID-20261109`. **[bin]**

## What was read

**[file]** The ten supplied APK files reduce to seven distinct packages. File names are not a reliable version label, so each package is named by the version and build number inside it:

| Package | Version | Build |
| --- | --- | --- |
| Classic | 1.6 | 6108 |
| Classic | 1.7 | 6110 |
| Era | 1.7 | 6110 |
| Classic | 1.8 | 6158 |
| Era | 2.0 | 6192 |
| Classic | 2.0 | 6194 |
| Classic | 2.2 | 6201 |

**[bin]** Across them there are 15 native engine libraries and three identical store-helper libraries, for ARM32, ARM64, x86 and x86-64. All 16 distinct native files have symbol inventories. Only two were read in depth: Classic 1.7 for ARM32 (3,207 routines) and Classic 1.8 for x86 (1,033 symbols at 965 entry points). The host details below come from Classic 1.7's Java wrapper; every engine detail comes from Classic 1.8 x86. The exact package digests are held by the research owner.

## Host and engine

**[bin]** The Java host owns the app lifecycle, the EGL surface, input, Java audio, the keyboard, web and video views, and store and social features. It loads the native engine and passes it the language, the APK, data and storage paths, the display size and density, and any start-up link. Then it calls the native frame entry over and over. Java swaps buffers only when that entry says a frame is ready to draw. When the surface is recreated, the host asks the engine to reload its textures.

**[bin]** Touch events are passed as numbers: down and pointer-down are 1, move is 2, up and pointer-up are 3, anything else is 0. Each pointer carries its id and whole-number view coordinates. While one pointer goes down or up, the other pointers are sent as moves. Key down and key up are separate types, and Back is sent as a named device event. Newer wrappers copy the input arrays and queue them through a runnable, so 1.7's threading should not be assumed for them.

**[bin]** Audio keeps up to 16 sound effects cached by file name and evicts the one played longest ago. Music is a separate object with its own loop flag. The engine passes volume as a whole number, and Java divides it by 100.

## The frame gate

**[bin]** In Classic 1.8 x86 an elapsed-time gate runs before input, timers and drawing. The interval starts at 50 ms and can be changed. A call that comes too early returns "nothing to draw". When a frame is due, the deadline moves on by one interval if the call is only a little late; if it is very late, the deadline is reset to now, so missed frames are not caught up. A frame that passes the gate handles queued input, graphics and texture-reload state, then timers, then drawing. This is a configured gate, not a measured 20 frames per second, and it says nothing about animation timing or about the period clients.

## Collision

**[bin]** The point wall test checks NPCs first, then bombs, then chests, and only then the tile wall rule. A boolean option adds a check for other players. A reproduction that tests only tiles would miss things that visibly block the player.

## The board

**[bin]** The ordinary board is a 64 by 64 grid, row by row, two bytes per tile. The accessor for neighbouring levels picks the neighbour and then keeps only the low six bits of each coordinate, so coordinates wrap into 0 to 63. This accessor does not describe every map format.

## Animation and drawing

**[bin]** The renderer picks a frame and a direction row; a "single direction" flag forces row 0. It then draws each part of that row, resolving its sprite. In the world modes that were read, a part's whole-number offset is divided by 16 before it is added to the object and level position, so 16 offset units are one world unit. One other mode draws in direct units. Height adjustment and a special body-sprite path are handled separately.

**[file]** In the older packages a GANI is plain text with ordered sprite rectangles, placements per direction, `WAIT`, sound, defaults, loop and fallback settings, and script blocks. `WAIT` is kept as written, not turned into milliseconds.

## Global chat

**[bin]** Outgoing chat goes through a handler table that can be reconfigured. On the ordinary route the message is cut to 220 stored bytes, a one-byte prefix equal to the stored length plus 32 is written, the text follows, and the result goes to the transport. A special route raises a local event instead, and a disabled route sends nothing. This is a byte limit, not a character limit, and the prefix is not a fixed message id.

**[bin]** Incoming messages are dispatched through a 256-entry handler table indexed by an unsigned command byte. Some handlers run at once and others are queued. The queue policy, the outer framing, compression, encryption and which command maps to which handler were not recovered.

## Resources

**[file]** Classic 1.6 and 1.7 each ship 48 plain-text GANIs, and Era 1.7 ships 96. Classic 1.8 ships 48 GANIs that are not plain text, Era 2.0 ships 95, and Classic 2.0 and 2.2 ship 593 each. Native resource and DES helpers were found. Decode trials did not reproduce any known plain text **[lab]**, so no decoder is claimed. The opaque files are kept as they are, and the assets stay out of the reproduction repo.

## Tests that follow

**[inf]** These are proposed acceptance tests, none run against the original Android client: a host profile with a touch sequence and a texture reload; a fake-clock frame gate; a 64×64 board with layered collision; the animation model with 16 offset units per world unit; the chat builder at lengths 0, 219, 220 and 221; and a GANI decoder accepted only after a known-plaintext round trip.

The Classic 1.8 GS2 machine is in [protocol/gs2-android-classic-18.md](../protocol/gs2-android-classic-18.md).
