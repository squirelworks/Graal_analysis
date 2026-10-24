# 11 Emotes and non-walk GANIs

Snapshots read: Graal_analysis `8da6800` (`formats/gani.txt`, `protocol/udp-p2p.md`, `packet-layouts.md`, `versions-133-139.md`, `player-props.md`), Seihai `06aacfd` (`assets/gani.rs`), GServer-v2 (`msgPLI_SHOWIMG`, `TPlayerProps.cpp`).

## What it is
Two separate things.

### A. Animation state
- **2.1+ (incl. 2.22, 2.31)**: `PLPROP_GANI` (10) is a string gani name (`idle`, `walk`, `sword`, `spin`, ...). The receiver fetches `<name>.gani` with WANTFILE if it lacks it. GServer stores it and forwards it; when it is `spin` it fabricates four HITOBJECTS (02).
- **2.05**: prop 10 is the pre-2.1 bow form. The animation is in `PLPROP_SPRITE` (17): `sprite % 4` = direction and `sprite / 4` = a sprite number S. **[2.05][dec]** The 2.05 decompile (2026-10-24) gives the exact table, see "2.05 sprite prop" below. The UDP movement datagram has a trailing byte that looked like the first letter of the animation name (`W`, `I`, `S`); the client also keeps a table that maps gani-name substrings to one letter (`attack` A, `carry` C, `dead` D, `hurt` H, `idle` I, `kick` K, `lift` L, `ride` R, `sit` T, `spin` U, `swim` V, `sword` S, `walk` W, `def` X and a few more, used to shorten cached gani file names; full table in `../decomp-findings-2026-10-24/gani-short-codes.tsv`).
- Props that interact: CARRYSPRITE (19), STATUS bits, HORSEGIF (21), HEADGIF/BODYIMG, `PLPROP_GATTRIB1-30` (gani parameters `#P1..`).
- GANI file grammar (SPRITE, ANI/ANIEND frames, PLAYSOUND, LOOP, SETBACKTO, DEFAULTHEAD...) is in `formats/gani.txt`. Seihai's parser covers frames, loops and `PLAYSOUND`; effects and scripts are not run.

### B. Emotes
- Emotes are **images shown over a player's head**. On the wire: `PLI_SHOWIMG` (24) client to server, rest passed through; GServer re-emits it as `PLO_SHOWIMG` (32) with `s player id` in front to the level area (`msgPLI_SHOWIMG`, `sendPacketToLevelArea`). In 2.05 the same payload also goes over UDP id 15. **[srv][cap]**
- Layout seen: four GCHARs (index, x, y, name length) then the image name, for example the AFK emoticon `emoticon_afk_stay.mng`, re-sent about every 3 s while shown. Trailing bytes follow. **[cap]**
- Triggers: 1.38+ Ctrl+letter (A AFK, B BRB, Z Zzz stay until the player moves; others from D, E, F, G, H, L, M, O, P, R, S, T, W, X; 1.39 adds C, K, Y). The assets include an `emoticons` folder (29 png/mng files). 2.17+ also has chat-line emoticons.
- **Correction (2026-10-24 decompile of 2.05 rev2; the 1.39 build has the same routine).** The key path is **local only and sends no packet**. Ctrl+A to Ctrl+Z (no text field focused, player not dead or locked) lowercases the letter and walks the client's loaded file list for the **first file whose name starts with `emoticon_<letter>`** and whose extension is png, mng or gif (a prefix match: Ctrl+A matches `emoticon_afk_stay.mng` if it is the first `emoticon_a...` file in the list). The image is drawn at the player's x+2, y-5 (a little lower when a second flag is set) for **50 ticks (2.5 s)**. There is no letter-to-name table and no hard-coded AFK/BRB/Zzz string in the client: the mapping is whatever files exist. `PLI_SHOWIMG` (24) is sent **only by the script command `showimg`**, never by the key handler. The earlier wording of this spec (Ctrl+letter sends SHOWIMG) was an inference from the captured packets and is wrong for the key path.
- **Open:** how other players see a Ctrl+letter emote. The captured SHOWIMG frames (AFK image re-sent about every 3 s) are not explained by the key handler; they may come from a server-side NPC or script that calls `showimg`, or from a path not yet traced. Treat the emote *send* as unknown. (Lab batch c, 2.31 and 2.22: the stock server relays any client 24 payload unchanged as 32 and no client reacted to a 1-byte payload; the real 2.31 payload is a single byte 9 sent about every 5.1 s, not an emote form: `../decomp-findings-2026-10-24-b/08-lab-findings-levelchange-24-178.md`.)
- `PLO_SHOWIMGNPC` (166) shows images on NPCs.

## 2.05 sprite prop **[2.05][dec]**
Derived from the 2.05 rev2 decompile; tables are in `../decomp-findings-2026-10-24/` (`sprite-step-table.tsv`, `gani-to-step.tsv`, `gani-name-table.tsv`, `status-bits-prop18.tsv`, `player-modes.tsv`).
- Byte on the wire = 32 + direction + 4 x S (the 32 is the usual GCHAR offset, so the decoded prop is `dir + 4 x S`, matching `sprite % 4` and `sprite / 4` above).
- S comes from the current animation step through a step table, and **only while the active gani is the default `def` gani and the step is 38 or lower**. Other ganis do not change the sprite number. The sender writes 0 for names it does not know. A hurt player is special-cased: S = 32 (decoded `0x80 + dir`).
- Step to S (steps 0 to 38): `0, 4, 5, 4, 3, 2, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 11, 12, 14, 15, 16, 17, 23, 18, 19, 20, 19, 18, 21, 22, 21, 18, 24, 25, 26, 27, 28, 29`. Steps 9 to 13 (S 6 to 10) are the sword swing and the only ones that can hit (see 02).
- Gani name to step rule: idle and def = frame; walk and walkslow = frame+1; kick 9; sword, ridesword, spin = 9 + (frame mod 5); push 14+frame; grab 19; pull 20+frame; lift 23; carrystill and hiddenstill 24; carry and hidden 25+frame; shoot 33; ridestill 34, ridefire 35, rideeat 36; ride 35 + (frame and 1); sit 37; sleep 38; hurt and ridehurt 39; dead 40 (not sent).
- **Swim, lava and dead are not on the wire.** All three are sent as sprite 0 (idle) plus direction. Swim is a local mode (10) entered on water tile type 11 (with a splash); lava (tile type 12) shows the local `lava` gani. The dead state is carried only by the STATUS prop dead bit (see 04). There is **no swim sprite**, so a 2.05 client cannot tell a swimmer from an idle player by prop 17.
- The 31 built-in gani names (index 0 to 30): idle, walk, walkslow, kick, sword, ridesword, spin, push, grab, pull, lift, carrystill, hiddenstill, carry, hidden, shoot, ridestill, ridefire, rideeat, ride, sit, sleep, hurt, ridehurt, dead, maps1, maps2, maps3, swim, lava, carried.
- Caveat: the "only for `def`" condition was read from the sender and is recorded as observed, not confirmed on the wire.
- STATUS prop (18) bits: 0x01 editor or paused, 0x02 hidden (mode 14 or hidden timer), 0x04 male, 0x08 dead (see 04), 0x10 weapons allowed, 0x20 a numeric field is 0 or more (meaning not traced), 0x40 has charged spin.

## Seihai today
- Parses gani files and keeps a walk animation player (`set_walk_gani`, `walk_frame`). Does not send SPRITE animation indexes beyond walking, does not draw other players' non-walk animation, and has no emote send/receive (PLO 32 not handled). Other players are drawn from props.

## Steps for Claude
1. For 2.22+ profiles: on movement/attack/lift state changes send `PLPROP_GANI` with the gani name; draw other players using the gani named in their props, loading it via the asset path or WANTFILE.
2. For 2.05: send prop 17 as `dir + 4 x S` using the step table above (idle = S 0, walk = frame+1 mapped through the table, sword swing S 6 to 10, and so on). Send sprite 0 plus direction while swimming and while dead (no swim sprite exists). To draw other 2.05 players, invert the table: `S -> pose`, with the caveat that several steps share an S. Do not invent a swim sprite.
3. Implement `PLO_SHOWIMG` (32): decode, spawn a timed overlay above that player (x,y given in the packet, name from the packet), expire after about 3 s unless refreshed.
4. Emote key (2.05 behaviour): on Ctrl+letter, find the first file in the loaded asset list whose name starts with `emoticon_<lowercase letter>` and has a png, mng or gif extension; draw it locally at the player's x+2, y-5 for 50 ticks (2.5 s). **Send nothing.** Send `PLI_SHOWIMG` (24) only from a script `showimg` command, with the captured field layout. Whether other players should see a key emote is open; if Seihai wants that, treat it as a Seihai choice (sending SHOWIMG is protocol-legal) and mark it so.
5. Draw `.mng` as a first frame only (GIF/MNG decoders are not in Seihai); skip PNG variants gracefully.
6. Add the `hurt`, `dead`, `sword`, `lift`, `grab`, `push` poses as the combat/inventory/death work (02-04) needs them.

## How to test
- Lab: Wine 2.05 client sends an AFK emoticon (Ctrl+A) next to a Seihai session; check PLO 32 arrives and decodes. Replay the existing two-player capture through `SessionState` for ids 15 and 24.
- Load every `.gani` in the lab world `ganis` folder with `Gani::parse` as a smoke test.

## NEEDS
Filled by the 2026-10-24 2.05 decompile: the sprite-index to animation table and the Ctrl+letter lookup (both above). 2.22+ needs nothing: names are plain strings.

Still open:
- How other players see an emote (the key path sends nothing; see the correction above). A lab capture of a real 2.05 client pressing Ctrl+A next to a second client would settle it.
- Swim on the wire: none found in 2.05. Whether 2.22 sends a `swim` gani name (prop 10) is covered by the 2.1+ notes, not by this decompile.
- Some mode values and STATUS bit 0x20 (see `../decomp-findings-2026-10-24/player-modes.tsv`).
- 1.39 sprite and gani behaviour was not re-read (the emote routine is the same).
