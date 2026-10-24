# 11 Emotes and non-walk GANIs

Snapshots read: Graal_analysis `8da6800` (`formats/gani.txt`, `protocol/udp-p2p.md`, `packet-layouts.md`, `versions-133-139.md`, `player-props.md`), Seihai `06aacfd` (`assets/gani.rs`), GServer-v2 (`msgPLI_SHOWIMG`, `TPlayerProps.cpp`).

## What it is
Two separate things.

### A. Animation state
- **2.1+ (incl. 2.22, 2.31)**: `PLPROP_GANI` (10) is a string gani name (`idle`, `walk`, `sword`, `spin`, ...). The receiver fetches `<name>.gani` with WANTFILE if it lacks it. GServer stores it and forwards it; when it is `spin` it fabricates four HITOBJECTS (02).
- **2.05**: prop 10 is the pre-2.1 bow form. The animation is in `PLPROP_SPRITE` (17): `sprite % 4` = direction and `sprite / 4` = an index into the client's built-in animation list. The 2.05 string table shows the animation names it knows: attack, bomb, carry, dead, grab, hurt, idle, jump, lift, pull, push, ride, sleep, spin, swim, sword (plus walk). The index-to-name order is **not** documented. The UDP movement datagram has a trailing byte that looked like the first letter of the animation name (`W`, `I`, `S`).
- Props that interact: CARRYSPRITE (19), STATUS bits, HORSEGIF (21), HEADGIF/BODYIMG, `PLPROP_GATTRIB1-30` (gani parameters `#P1..`).
- GANI file grammar (SPRITE, ANI/ANIEND frames, PLAYSOUND, LOOP, SETBACKTO, DEFAULTHEAD...) is in `formats/gani.txt`. Seihai's parser covers frames, loops and `PLAYSOUND`; effects and scripts are not run.

### B. Emotes
- Emotes are **images shown over a player's head**: `PLI_SHOWIMG` (24) client to server, rest passed through; GServer re-emits it as `PLO_SHOWIMG` (32) with `s player id` in front to the level area (`msgPLI_SHOWIMG`, `sendPacketToLevelArea`). In 2.05 the same payload also goes over UDP id 15. **[srv][cap]**
- Layout seen: four GCHARs (index, x, y, name length) then the image name, for example the AFK emoticon `emoticon_afk_stay.mng`, re-sent about every 3 s while shown. Trailing bytes follow. **[cap]**
- Triggers: 1.38+ Ctrl+letter (A AFK, B BRB, Z Zzz stay until the player moves; others from D, E, F, G, H, L, M, O, P, R, S, T, W, X; 1.39 adds C, K, Y). The letter-to-file mapping is built at run time and only AFK, BRB, Zzz are known. The assets include an `emoticons` folder (29 png/mng files). 2.17+ also has chat-line emoticons.
- `PLO_SHOWIMGNPC` (166) shows images on NPCs.

## Seihai today
- Parses gani files and keeps a walk animation player (`set_walk_gani`, `walk_frame`). Does not send SPRITE animation indexes beyond walking, does not draw other players' non-walk animation, and has no emote send/receive (PLO 32 not handled). Other players are drawn from props.

## Steps for Claude
1. For 2.22+ profiles: on movement/attack/lift state changes send `PLPROP_GANI` with the gani name; draw other players using the gani named in their props, loading it via the asset path or WANTFILE.
2. For 2.05: keep a small enum `Pose` with the names above and a table `sprite/4 -> Pose`. Only `walk` (index from the existing movement code) and `idle` are verified; leave the rest as an editable table with a loud TODO, not guesses.
3. Implement `PLO_SHOWIMG` (32): decode, spawn a timed overlay above that player (x,y given in the packet, name from the packet), expire after about 3 s unless refreshed.
4. Emote send: map Ctrl+A/B/Z to `emoticon_afk_stay.*`, brb, zzz names found in the assets folder (check file names at run time) and send `PLI_SHOWIMG` (24) with the captured field layout.
5. Draw `.mng` as a first frame only (GIF/MNG decoders are not in Seihai); skip PNG variants gracefully.
6. Add the `hurt`, `dead`, `sword`, `lift`, `grab`, `push` poses as the combat/inventory/death work (02-04) needs them.

## How to test
- Lab: Wine 2.05 client sends an AFK emoticon (Ctrl+A) next to a Seihai session; check PLO 32 arrives and decodes. Replay the existing two-player capture through `SessionState` for ids 15 and 24.
- Load every `.gani` in the lab world `ganis` folder with `Gani::parse` as a smoke test.

## NEEDS
"the 2.05 sprite-index to animation table" (which `sprite / 4` is walk, sword, lift, grab, push, pull, hurt, dead, swim, ...) and "the 2.05 Ctrl+letter to emoticon file mapping". Either a decompile of the 2.05 player-sprite-to-gani lookup and the emoticon key handler, or a lab capture of one 2.05 client doing each action while logging prop 17 values. 2.22+ needs nothing: names are plain strings.
