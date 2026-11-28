<!-- manual: kind=reference status=draft -->
# 4.7 Sound

This chapter gives how the client places, limits and triggers sounds while playing. The backends, the options and the file types are in → §3.10.3 and §3.10.4.

> Status: draft. The 2.05 rev 2 rules include an audio-device runtime check. Later BASS and 6.x evidence has its separately scoped static/file limits in → §3.10.4, §3.10.5 and §4.7.5.

For a separately identified early 1.40 comparison input, class metadata binds a `TWinamp` published method named `ID3Tag` to a helper that calls `SetForegroundWindow`, then submits Alt down, 3 down, 3 up and Alt up through `keybd_event`, with scan codes from `MapVirtualKeyA`. This is selected static component evidence, not proof of application invocation, successful focus, an observed dialog, audio playback or first appearance. [bin][doc] (client-internals/early-windows-callback-variants.md#selected-140-added-import-bindings)

Across that comparison input and the separately identified 1.40 rev 1 input, this complete method body, its method table, selected class metadata and declared PE import-directory byte span match. This does not establish equal stored-handle values, external callees, matching callers, runtime effects or whole-client equivalence. [bin] (client-internals/early-windows-callback-variants.md#selected-140-revision-resource-and-method-comparison)

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

Two lift sounds exist, and one byte picks between them. The rules below give the byte, its default, the command that clears it, and an earlier note they correct [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205).

| Rule | Detail | Source |
| --- | --- | --- |
| choice | one byte on the player object picks the lift and hurt sound: set gives `lift.wav`, clear gives `lift2.wav` | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| default | new players start with the byte set | [2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| `setgender female` | the sound changed to `lift2.wav`; that the command clears the byte is inferred from that | [live][inf] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| correction | an earlier note took `lift2.wav` for heavy objects and `fire.wav` for the fireball; both were wrong | [live] (client-internals/live-checks-editor-offline-sound.md#corrections-to-earlier-notes) |

## 4.7.5 Later sound names, controls and call sites

These are static names, file declarations and script-help descriptions from the later survey, not measured timing, audibility or complete runtime API contracts. The corresponding backend and file-content boundaries are in → §3.10.5. [file][bin] (client-internals/sound-files-6x.md)

| Observation | Checked scope and limit | Source |
| --- | --- | --- |
| Default effect names | both checked backends name `arrow`, `arrowon`, `axe`, `bomb`, `chest`, `compudead`, `extra`, `fire`, `frog`, `item`, `item2`, `jump`, `lift`, `lift2`, `nextpage`, `put`, `steps`, `stonemove`, `sword`, `swordon`, `thunder`, `water`, with `.wav` extensions | [bin] (client-internals/sound-files-6x.md#back-ends) |
| Options and startup guard | `sfxvolume`, `midivolume`, `mp3volume`, `radiovolume`, `soundfxon`, `musicon`; the named sound-test guard sets volumes to zero after a sound-startup hang in the static reading | [bin] (client-internals/sound-files-6x.md#back-ends) |
| GANI cues | `PLAYSOUND` in the 6.1.1.3 files most often names the two walk sounds, then lift, axe, water, sword, jump, put, chest, sign and world-specific effects; 5.00r7 also names death, rain, crush, bomb and arrow-hit effects | [file] (client-internals/sound-files-6x.md#how-worlds-call-them) |
| GS1 calls | level text uses `play` for birds, arrows and snow/house/grass walking sounds; no plain-text music call was found within the inspected text | [file] (client-internals/sound-files-6x.md#how-worlds-call-them) |
| Script-help capabilities | names describe player-position playback, looped playback at x/y/volume (0–1), stopping one/all, is-playing, pitch (0.5–1.5 or note name), current music and `onMusicDataReceived` | [bin] (client-internals/sound-files-6x.md#how-worlds-call-them) |
| 6.03r7 additions | names describe a GANI sound-at-animation-start option and a list of WAVs to suppress; call ordering and actual playback were not measured | [bin] (client-internals/sound-files-6x.md#how-worlds-call-them) |

The survey attributes further music calls to encrypted class/weapon caches; this is a lead, not a recovered callable contract. Package presence and help/function names cannot settle codec acceptance, scheduling or failure behavior (→ App. E#325). [file][doc] (client-internals/sound-files-6x.md#how-worlds-call-them)
