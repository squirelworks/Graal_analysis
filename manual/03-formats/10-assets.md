<!-- manual: kind=reference status=draft -->
# 3.10 Image and sound asset conventions

This chapter lists the files a client install carries, the image sheets the engine expects, and which sound and music files each backend plays. How the client positions and mixes a sound in play is in → §4.7.

> Status: draft. The asset tree is from one official install; the 2.22 extension-to-backend dispatch and what 2.05 does after a missing sound arrives are untraced.

## 3.10.1 Image sheets

The client draws from a few large image sheets. The table gives each sheet's size and role [file] (client-internals/client-assets.md#tile-sheets).

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

The table lists the other top-level items of the client's `levels` tree and points to where each is described [file] (client-internals/client-assets.md#other-top-level).

| Top-level item | Contents | Source |
| --- | --- | --- |
| `maps/` | `bigmap.txt` and minimap material (→ §3.2.5) | [file] (client-internals/client-assets.md#other-top-level) |
| `arrays.dat`, `arrays2.dat`, `.sig` files | → §3.5.3 to §3.5.5 | [file] (client-internals/client-assets.md#other-top-level) |
| `bass.dll`, `basswma.dll`, `hvdi.dll` | sound, WMA add-on and voice libraries (→ §3.10.4) | [file] (client-internals/client-assets.md#other-top-level) |
| `readme.txt` | documents HawkVoice (LGPL), joystick calibration and the classic controls: F1 options, F4 editor, F5 load, arrows or IJKL walk, S or space strike, A act, M map | [doc] (client-internals/client-assets.md#other-top-level) |

## 3.10.3 Sound and music in 2.05

2.05 plays sound through three back ends. Each row gives what is played and which back end plays it [2.05] (client-internals/sound-and-music.md#205-at-a-glance).

| What | Backend | Source |
| --- | --- | --- |
| sound effects (`.wav`) | DelphiX wave list on DirectSound | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |
| music, Windows MCI path | an invisible media player component (MCI) | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |
| music, Winamp path | a component that remote-controls a running Winamp 1.x or 2.x | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |
| music volume | `midiOutSetVolume` (MCI path) or Winamp IPC messages | [2.05] (client-internals/sound-and-music.md#205-at-a-glance) |

The rules below give the sound options, how a back end is chosen, and how a sound file is named, found and fetched [2.05] (client-internals/sound-and-music.md#options-graalconfigtxt).

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

From 2.17 the BASS library replaces most of that. The table compares 2.05 with 2.17 to 2.31 area by area. Several rows are judged from imported names, and are tagged as inferred [2.17][2.22][2.31] (client-internals/sound-and-music.md#217--222--231-bass-replaces-directsound-and-winamp).

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

## 3.10.5 Later audio backends and surveyed file formats

The later study inspected held 4.x–6.x sound files, RIFF format chunks, update-list entries, GANI/level text and executable strings/imports. No client was run. The rows distinguish backend evidence, actual file content and manifest names; none supplies a native decoder-acceptance test. [file][bin] (client-internals/sound-files-6x.md)

| Checked input | Static backend evidence | Limit | Source |
| --- | --- | --- | --- |
| Windows 6.00 betas through 6.03r7 | statically linked FMOD 3, using FSOUND/FMUSIC; beta strings also name the FMOD library, not FMOD Ex 4.x | backend identity does not independently validate each codec or stream | [bin] (client-internals/sound-files-6x.md#back-ends) |
| Linux 6.03r7 x64 | SDL_mixer 1.2 calls for effects, panning and music over ALSA | decoded formats depend on the particular SDL_mixer build | [bin] (client-internals/sound-files-6x.md#back-ends) |
| Both checked backends | music/stream filter names `.mp2`, `.mp3`, `.ogg`, `.wma`, `.asf`; FFmpeg is loaded on demand for video | filter names alone do not demonstrate audio playback | [bin] (client-internals/sound-files-6x.md#back-ends) |

The file survey reports the following RIFF formats. Its stated total of 255 distinct WAVs disagrees with the format sum of 254 and the channel sum of 254 (193 mono, 61 stereo). Keep these as reported subtotals until the census is reconciled (→ App. E#325); no missing category or corrected total is inferred. [file][doc] (client-internals/sound-files-6x.md#what-the-files-are)

| RIFF format tag | Reported count | Source |
| --- | ---: | --- |
| 1, PCM | 202 | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| 85, MPEG Layer 3 in WAV | 43 | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| 17, four-bit IMA ADPCM | 6 | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| 6, A-law | 3 | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| MS ADPCM or mu-law | none reported in this corpus | [file] (client-internals/sound-files-6x.md#what-the-files-are) |

Reported rates span 5000–48000 Hz, including 8012, 11000 and 27000. One walk sound with a `.wav` extension instead starts with an ID3 tag and contains MP3 data: extension-only assumptions do not describe every surveyed file. This is content evidence, not proof of the original client's sniffing or decode path. [file] (client-internals/sound-files-6x.md#what-the-files-are)

| Surveyed set | Content found | Source |
| --- | --- | --- |
| 4.04r2, 4.20r6, 4.20r8 | WAV files: IMA ADPCM at 8000 Hz; eight-bit PCM at 5000/22050 and sixteen-bit PCM at 8000 | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| 5.00r7 | mixed-rate PCM, 43 stereo 24000-Hz MPEG-in-WAV, three stereo 22050-Hz A-law, one IMA ADPCM and six MP3 music files | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| 6.00r2 as served to the lab | eight-/sixteen-bit mono PCM at 8000–22050 Hz | [file] (client-internals/sound-files-6x.md#what-the-files-are) |
| 6.1.1.3 install | 68 WAVs: eight-/sixteen-bit mono/stereo PCM at 5000–48000 Hz and 8000-Hz IMA ADPCM; eight MP3 music files | [file] (client-internals/sound-files-6x.md#what-the-files-are) |

MIDI was found on disk only in the pre-4.x installs of this survey, but later manifests include MIDI; one music package lists 48 MIDI entries. Ogg appears in later manifests, with no corresponding Ogg file available on disk in this study. The collected update lists contain 4760 WAV, 98 MIDI, 67 MP3 and four Ogg entries; list entries are not a count of distinct decoded or playable files. WMA/ASF appeared in the filter strings but not the surveyed world data. [file][bin] (client-internals/sound-files-6x.md#what-the-files-are); [bin] (client-internals/sound-files-6x.md#back-ends)

These formats are corpus-backed compatibility-test targets, not a measured statement that every 6.x client decodes each one. Verify exact backend/build playback separately; static call-site and option evidence is in → §4.7.5. [file][doc] (client-internals/sound-files-6x.md#so-a-6x-compatible-client-needs)
