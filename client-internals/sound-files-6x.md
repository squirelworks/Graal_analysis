# Sound and music files in the 4.x to 6.x clients and their worlds

Date: 2026-11-13. A file survey: no client was run. It read every sound and music file in the held
4.x, 5.x and 6.x client installs and copies (WAV format from each file's RIFF `fmt ` chunk), the
`FILE` lines of the update-package lists (`*.gupd`) in a 6.1.1.3 install, GANI `PLAYSOUND` lines and
plain-text level scripts, and the strings and imports of the 6.x executables. **[file][bin]** The 2.x
side is in [sound-and-music.md](sound-and-music.md) and manual §4.7.

## Back ends

| Build | Audio | Tag |
| --- | --- | --- |
| Windows 6.00 betas to 6.03r7 | **FMOD 3** (the FSOUND / FMUSIC API), statically linked; classes `TSoundEffectFMOD`, `TSoundPlayerFMOD`; the betas also name `fmod.dll`. No FMOD Ex 4.x | [bin] |
| Linux 6.03r7 x64 | **SDL_mixer 1.2** (`Mix_LoadWAV_RW`, `Mix_PlayChannelTimed`, `Mix_SetPanning`, `Mix_LoadMUS`, `Mix_PlayMusic` …) over ALSA. Which formats play depends on the SDL_mixer build | [bin] |
| both | music and stream file filter `.mp2 .mp3 .ogg .wma .asf`; FFmpeg loaded on demand for video only | [bin] |

Built-in default effects named in both: `arrow.wav`, `arrowon.wav`, `axe.wav`, `bomb.wav`,
`chest.wav`, `compudead.wav`, `extra.wav`, `fire.wav`, `frog.wav`, `item.wav`, `item2.wav`,
`jump.wav`, `lift.wav`, `lift2.wav`, `nextpage.wav`, `put.wav`, `steps.wav`, `stonemove.wav`,
`sword.wav`, `swordon.wav`, `thunder.wav`, `water.wav`. Options: `sfxvolume`, `midivolume`,
`mp3volume`, `radiovolume`, `soundfxon`, `musicon`. A `soundtest_testfile.txt` guard sets every
volume to 0 after a hang during sound start-up. **[bin]**

## What the files are

255 distinct WAVs across all eras: **[file]**

| Format tag | Files |
| --- | --- |
| 0x1 PCM | 202 |
| 0x55 MPEG Layer 3 inside a WAV | 43 |
| 0x11 IMA ADPCM (4-bit) | 6 |
| 0x6 A-law | 3 |
| MS ADPCM, mu-law | none |

Rates run from 5000 to 48000 Hz, including odd ones (8012, 11000, 27000); 193 mono and 61 stereo.

| Set | What it holds |
| --- | --- |
| 4.04r2, 4.20r6, 4.20r8 | WAV only: IMA ADPCM at 8000 Hz (`cauldron_bubbles`, `fire_torch0-2`, `spell_firelaunch`, `walk_grass2/4`, `water`, `nextpage`), PCM 8-bit 5000 and 22050, 16-bit 8000 |
| 5.00r7 | PCM at mixed rates; 43 MPEG-in-WAV (stereo 24000); 3 A-law (stereo 22050); 1 IMA ADPCM; 6 MP3 under `levels/music/` |
| 6.00r2 (as served to the lab) | PCM 8 and 16-bit mono, 8000–22050 |
| 6.1.1.3 install | 68 WAV (PCM 8 and 16-bit, mono and stereo, 5000–48000; IMA ADPCM at 8000) and 8 MP3 in `levels/music/` |

- **One `.wav` is really an MP3 file** (it starts with an ID3 tag): `sounds/steps2.wav`, the walk
  sound named in `walk.gani`. A client has to sniff the content, not trust the extension. **[file]**
- **MIDI** appears only in pre-4.x installs on disk, and in update packages (48 `.mid` in the Era
  Legacy music package). **[file]**
- **Ogg Vorbis** is shipped by 6.x-era servers: the Era Legacy sound package lists
  `era_timpani8.ogg` and `era_timpani9.ogg`. None was on disk. **[file]**

Update-package `FILE` lines by type: png 7,515, wav 4,760, gif 2,368, gani 289, mng 225, txt 110,
mid 98, mp3 67, exe 30, dll 12, nw 8, ogg 4, ttf 3. **[file]**

## How worlds call them

- GANI `PLAYSOUND` in the 6.1.1.3 install: `steps2.wav` and `steps.wav` most of all, then `lift`,
  `axe`, `water`, `sword`, `jump`, `put`, `chest`, `sign` and world-specific names; 5.00r7 adds
  `dead`, `rain`, `crush`, `bomb`, `arrowon`. **[file]**
- GS1 `play` in levels: `bird01–03.wav`, `arrow.wav`, `walk_snow.wav`, `walk_house2.wav`,
  `walk_grass2/4.wav`. **[file]**
- No plain-text music call was found: music names appear only in update packages and downloaded
  `levels/music/*.mp3`. The calls are in the encrypted class and weapon caches. **[file]**
- The 6.x script help names the sound functions by what they do: play at the player, play looped at
  x, y and volume (0..1), stop one or all, is-playing, pitch between 0.5 and 1.5 or by note name,
  current music, and the event `onMusicDataReceived`. 6.03r7 adds a gani "sound at animation
  start" and a list of WAVs not to play. **[bin]**

## So a 6.x-compatible client needs

Effects: WAV PCM 8 and 16-bit, mono and stereo, at any rate from 5000 to 48000 Hz; IMA ADPCM;
MPEG-in-WAV; A-law; MP3 data under a `.wav` name; and Ogg Vorbis. Music: MP3 and MIDI, with Ogg for
the file filter. `.wma` and `.asf` appear only in the filter string; no world data uses them. **[inf]**
