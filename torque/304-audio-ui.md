# Sound and the native options in Linux 3.04

Date: 2026-11-07. Static read of the Linux `graalexe` 3.04 decompile. Nothing was run. Tags as in [README.md](README.md).

`graal/sounds.cpp` is fmod, not Torque's OpenAL audio. The control that starts the 2D session also registers the audio preferences and the volume methods. The shipped-script side of the menus is in [study-torque-clients.md](study-torque-clients.md); this note is the native side. **[bin]**

## Fmod

The first play calls `FSOUND_Init` with mix rate 44100, 64 channels and a flags value of 2. Failure logs `Failed to open fmod audio.` and later play calls return without starting a sound. A call with an empty name, or a volume at or below zero, also returns. Pan is clamped to the range minus one through one, and volume to zero through one. **[bin]**

A name ending in `.wav` is loaded with `FSOUND_Sample_Load` and scaled by `$pref::Audio::sfxvolume`. A name ending in `.mid` is loaded with `FMUSIC_LoadSong`, set to loop, played with `FMUSIC_PlaySong`, and scaled by `$pref::Audio::midivolume`. A name whose extension is one of `mp2`, `mp3`, `ogg`, `wma` or `asf` is opened with `FSOUND_Stream_Open` and played with `FSOUND_Stream_Play`. The mp3 and radio volume preferences are the other two scales on that music path. A volume preference below 1 skips the music. Files are looked up under `sounds`. **[bin]**

`client.cpp` and `scriptfunctions.cpp` call this unit for `item.wav`, `extra.wav`, `thunder.wav`, `bomb.wav`, `axe.wav` and `sword.wav` ([304-net.md](304-net.md), [304-npcs.md](304-npcs.md)). **[bin]**

## Prefs and the microphone control

`gui/guiGraalCtrl.cc` registers these next to the Graal preferences ([304-adventure.md](304-adventure.md)): `$pref::Audio::reversestereo`, `microon`, `midivolume`, `mp3volume`, `radiovolume`, `voicevolume`, `sfxvolume`, `microactivationlevel`, `microactivatebyvolume`, `choosenvoicecodec`, `microinputdevice`. **[bin]**

The console methods `updateMidiVolume`, `updateMp3Volume`, `updateRadioVolume` and `updateMicroActivationLevel` call into `sounds.cpp`. The microphone level is shown on the control named `OptMicrovolumeDisplay`. **[bin]**
