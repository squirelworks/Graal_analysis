<!-- manual: kind=reference status=draft -->
# 3.10 Image and sound asset conventions

This chapter lists the files a client install carries, the image sheets the engine expects, and which sound and music files each backend plays. How the client positions and mixes a sound in play is in → §4.7.

> Status: draft. The asset tree is from one official install; the 2.22 extension-to-backend dispatch and what 2.05 does after a missing sound arrives are untraced.

## 3.10.1 Image sheets

| File | Size | Role | Source |
| --- | --- | --- | --- |
| `pics1.png` | 2048×512 | standard tiles, 4096 ids of 16 px (→ §3.5.1) | [file] (client-internals/client-assets.md#tile-sheets) |
| `picso.png` | 1024×512 | offline tileset, sheet type 1 | [file] (client-internals/client-assets.md#tile-sheets) |
| `sprites.png` | 128×452 | sprite sheet | [file] (client-internals/client-assets.md#tile-sheets) |
| `letters.png` | — | bitmap font | [file] (client-internals/client-assets.md#tile-sheets) |

The tile definition line that selects a sheet is in → §3.5.2.2.

## 3.10.2 The levels tree

Files on disk under `levels/` in the measured install [file] (client-internals/client-assets.md#levels-counts-files-on-disk):

| Directory | Files | Contents | Source |
| --- | ---: | --- | --- |
| `ganis/` | 93 | 86 `.gani` (→ §3.3) plus images | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `midis/` | 49 | music | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `heads/` | 35 | 33 png, 2 mng | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `weapons/` | 33 | weapon images, 2 txt | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `bomys/` | 29 | bomy images and ganis | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `emoticons/` | 29 | png and mng | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `webgifs/` | 26 | downloaded images, mostly png (→ §3.9.3 `saveimages`) | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `backpals/` | 23 | background palettes | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `bodies/` | 20 | body images | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `images/` | 19 | other images | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `smilies/` | 15 | — | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `baddies/` | 10 | one sheet per baddy | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `shields/` | 7 | — | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `swords/` | 6 | — | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `npcs/` | 5 | script text | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `horses/` | 4 | — | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `hats/` | 4 | — | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `tutorial/` | 4 | — | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `letters/` | 2 | `blueletters`, `graal2002letters` | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `snapshot/` | 2 | `ss_arrow`, `ss_bomb` | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |
| `tiledefs/` | 1 | the offline tile definition line | [file] (client-internals/client-assets.md#levels-counts-files-on-disk) |

| Top-level item | Contents | Source |
| --- | --- | --- |
| `maps/` | `bigmap.txt` and minimap material (→ §3.2.5) | [file] (client-internals/client-assets.md#other-top-level) |
| `arrays.dat`, `arrays2.dat`, `.sig` files | → §3.5.3 to §3.5.5 | [file] (client-internals/client-assets.md#other-top-level) |
| `bass.dll`, `basswma.dll`, `hvdi.dll` | sound, WMA add-on and voice libraries (→ §3.10.4) | [file] (client-internals/client-assets.md#other-top-level) |
| `readme.txt` | documents HawkVoice (LGPL), joystick calibration and the classic controls: F1 options, F4 editor, F5 load, arrows or IJKL walk, S or space strike, A act, M map | [doc] (client-internals/client-assets.md#other-top-level) |

## 3.10.3 Sound and music in 2.05

| What | Backend | Source |
| --- | --- | --- |
| sound effects (`.wav`) | DelphiX wave list on DirectSound | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |
| music, Windows MCI path | an invisible media player component (MCI) | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |
| music, Winamp path | a component that remote-controls a running Winamp 1.x or 2.x | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |
| music volume | `midiOutSetVolume` (MCI path) or Winamp IPC messages | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |

| Rule | Detail | Source |
| --- | --- | --- |
| options | `musicon`, `usewinamp`, `soundfxon`, `reversestereo` (→ §3.9.3) | [2.05] (client-internals/sound-and-music.md#options-graalconfigtxt) |
| backend switch | chosen at game start and again whenever More Options closes; switching stops the current track and frees the old backend; turning music off stops the track | [2.05] (client-internals/sound-and-music.md#options-graalconfigtxt) |
| loop prefix | a leading `+` on a file name means looped; it is stripped | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| missing file | online, the client asks the server for the file by the same path that fetches images; the sound plays on a later trigger once the file has arrived | [2.05][inf] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| dispatch | `.wav` → effect path, only when `soundfxon`; any other extension → music path, only when `musicon`; `.mid` is the common case | [2.05] (client-internals/sound-and-music.md#one-entry-point-for-every-sound) |
| named effects | fifteen effects are known by name: `arrow`, `axe`, `bomb`, `crush`, `extra`, `fire`, `horse2`, `item`, `lift`, `lift2`, `put`, `steps`, `sword`, `thunder`, `water` (`.wav`) | [2.05] (client-internals/sound-and-music.md#effect-path-wav) |
| effect cache | each file is loaded once and cached by name; `stopsound` finds the cached wave by file name, ignoring the path | [2.05] (client-internals/sound-and-music.md#effect-path-wav) |
| MCI types | `.mid` goes to the MCI sequencer; other types depend on the MCI drivers installed | [2.05][inf] (client-internals/sound-and-music.md#music-path-mci) |
| MIDI loop | a `.mid` track replays when it ends, so MIDI music loops until `stopmidi` or another track | [2.05] (client-internals/sound-and-music.md#music-path-mci) |
| Winamp types | in Winamp mode music is whatever Winamp's input plugins accept, MP3 included | [2.05] (client-internals/sound-and-music.md#music-path-winamp) |
| Winamp start | the component finds the player by window class `Winamp v1.x`; if none is running it reads the Winamp path from `Software\CLASSES\Winamp.File\shell\Play\command` and starts it | [2.05] (client-internals/sound-and-music.md#music-path-winamp) |

The voice cap, positional pan and volume rules and the GS1 sound commands are in → §4.7.

## 3.10.4 Sound libraries in 2.17, 2.22 and 2.31

| Area | 2.05 | 2.17, 2.22, 2.31 | Source |
| --- | --- | --- | --- |
| library | DelphiX, MCI, Winamp | `bass.dll`, imported with the same functions in all three: samples, tracker music, file streams, URL streams, stream length and position, channel attributes and recording; `winmm` is still imported, with MIDI device queries added | [2.17][2.22][2.31] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp) |
| effects | DirectSound wave list | BASS samples | [inf] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp) |
| music files | MCI (MIDI) or Winamp | BASS streams and tracker modules; MIDI still through MCI | [inf] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp) |
| internet radio | n/a | BASS URL streams, `radio` and `radiovolume`, judged from names | [inf] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp) |
| Winamp | `usewinamp` | removed: no component, key or window class | [2.22] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp) |
| volume options | none | `midivolume`, `mp3volume`, `radiovolume`, `sfxvolume`, `voicevolume` | [2.22] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp) |
| voice chat | n/a | microphone capture through BASS recording, encoded with the `hvdi.dll` HawkVoice codec; an `emoticonmicro.png` icon shows over a talking player | [2.22] (client-internals/sound-and-music.md#voice-chat-222) |
| voice options | n/a | `microon`, `microinputdevice`, `microactivatebyvolume`, `microactivationlevel`, `microactivatekey`, `voicecodec`, `voicevolume` | [2.22] (client-internals/sound-and-music.md#voice-chat-222) |
| WMA | n/a | 2.17.1 loads `basswma.dll` at run time by name and uses its stream functions; 2.22, 2.31 and GraalEditor 2.3.1.1 neither import nor name it, so the shipped DLL is a leftover and WMA music is not supported there | [2.17][2.22] (client-internals/sound-and-music.md#basswmadll) |
| extension dispatch | → §3.10.3 | unmeasured | [2.22] (client-internals/sound-and-music.md#open) |
