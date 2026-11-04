<!-- manual: kind=reference status=draft -->
# 4.7 Sound

This chapter gives how the client places, limits and triggers sounds while playing. The backends, the options and the file types are in → §3.10.3 and §3.10.4.

> Status: draft. Read from 2.05 rev 2 and checked in a running 2.05 rev 2 client with an audio device; the 2.17 to 2.31 BASS clients are read only as far as → §3.10.4 goes.

## 4.7.1 Placing a sound (2.05)

Every sound goes through one entry point, called from about two dozen places: GS1 commands, gani `PLAYSOUND`, pickups, bombs, swords and baddies (→ §3.10.3 for the loop prefix, missing files and dispatch):

| Rule | Detail | Source |
| --- | --- | --- |
| arguments | the file, the level offset x and y, and the x and y of the sound in tiles | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| listener | the player at (x + 1.5, y + 2) | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| gmap | a sound from a neighbouring gmap level is first shifted by ±64 tiles (→ §3.2) | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| pan | (sound x − listener x) × 150, clamped to ±10000 DirectSound pan units; `reversestereo` negates it | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| volume | a negative attenuation growing with the distance on both axes, clamped at −10000 (hundredths of a dB) | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| looped effects | kept in the player's looped-sound list; leaving a level or entering the editor stops every looped effect in it | [2.05] (client-internals/sound-and-music.md#effect-path-wav) |
| voices | at most 8 effects play at once; a ninth request is dropped | [2.05] (client-internals/sound-and-music.md#effect-path-wav) |
| reuse | a cached effect is replayed from its buffer with the new pan, volume and loop settings | [2.05] (client-internals/sound-and-music.md#effect-path-wav) |
| after a missing file arrives | what 2.05 does then is unmeasured | [doc] (client-internals/sound-and-music.md#open) |

## 4.7.2 GS1 sound commands (2.05)

The commands' syntax is in → §8.2; their effect on the sound system:

| Command | Effect | Source |
| --- | --- | --- |
| `play file` | one-shot at the NPC's position, its x and y plus half its image size | [2.05] (client-internals/sound-and-music.md#gs1-sound-commands-in-205) |
| `playlooped file` | the same, with the loop prefix | [2.05] (client-internals/sound-and-music.md#gs1-sound-commands-in-205) |
| `stopsound file` | stops a cached effect found by file name; the path is ignored | [2.05] (client-internals/sound-and-music.md#gs1-sound-commands-in-205) |
| `stopmidi` | stops the current music, MCI or Winamp | [2.05] (client-internals/sound-and-music.md#gs1-sound-commands-in-205) |
| `setmusicvolume l,r` | MIDI-out volume (MCI) or Winamp volume and pan, each 0 to 1 | [2.05] (client-internals/sound-and-music.md#gs1-sound-commands-in-205); [2.05] (client-internals/feature-specs/01-sound.md#exact-client-behaviour-from-client-internalssound-and-musicmd-205) |
| 2.17 and later | the same commands plus `musicpos` and `musiclen` | [2.17][2.22] (client-internals/feature-specs/01-sound.md#exact-client-behaviour-from-client-internalssound-and-musicmd-205) |

## 4.7.3 Which action plays which sound (2.05)

Matched by the client's lookup of each file under `sounds\` while the action ran:

| Action | Sound | Source |
| --- | --- | --- |
| walking on the ground | `steps.wav` when a move starts, then `steps2.wav` about every 0.2 s | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| swimming | `water.wav` about every 0.8 s (→ §4.2.10) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| riding a horse | `horse.wav` and `horse2.wav`, alternating about every 0.4 s | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| sword swing | `sword.wav`; with the battle axe, `axe.wav` (→ §4.3) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| lifting | `lift.wav` or `lift2.wav` by the gender byte (→ §4.7.4) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| getting hurt | the same `lift.wav` or `lift2.wav`, from `hurt`, an explosion, a thrown ball or a baddy hit | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| dying | `dead.wav` (→ §4.4) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| laying a bomb | `put.wav` | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| bomb or explosion | `bomb.wav`: `putbomb` of any power, `putexplosion`, `putexplosion2` power 2, the end of a fireblast or nuke | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| jolt explosion | `thunder.wav` (`putexplosion2` power 3) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| launching a projectile | `arrow.wav` for arrows, fireballs, fireblasts, nukes and `shootball`, and for arrows from shooting baddies and the dragon | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| fire spy | `fire.wav` (`spyfire`) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| a thrown object or a leap landing | `crush.wav`; `water.wav` for the water leap (type 5) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| picking up a laid item | `extra.wav` (→ §4.5) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| opening a chest | `chest.wav`, also when the chest has a sign; no item sound follows | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| turning a sign page | `nextpage.wav` (→ §4.6.2.2) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| pushing a stone block | `stonemove.wav` about once a second while it moves (→ §4.2.7) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| ledge jump | `jump.wav` (→ §4.2.6) | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| frog | `frog.wav` when it hops | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| baddy walking | `steps.wav` | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| baddy dies | `compudead.wav` | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| baddy draws its sword | `swordon.wav` at its call site; six baddy types tried, none played it | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| an arrow hitting the player | `arrowon.wav` at its call site; not reached in the lab | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| `item.wav`, `item2.wav` | used only in the sign-reading routine and a server-message handler; the chest and laid-item tests did not play them | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| another player's bomb or item, online | `bomb.wav` or `thunder.wav`, `item.wav`, `extra.wav`, from server messages | [2.05][inf] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| gani `PLAYSOUND`, GS1 `play` and `playlooped` | the named file | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |

## 4.7.4 lift.wav and lift2.wav

| Rule | Detail | Source |
| --- | --- | --- |
| choice | one byte on the player object picks the lift and hurt sound: set gives `lift.wav`, clear gives `lift2.wav` | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| default | new players start with the byte set | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| `setgender female` | the sound changed to `lift2.wav`; that the command clears the byte is inferred from that | [live][inf] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| correction | an earlier note took `lift2.wav` for heavy objects and `fire.wav` for the fireball; both were wrong | [live] (client-internals/live-checks-editor-offline-sound.md#corrections-to-earlier-notes) |
