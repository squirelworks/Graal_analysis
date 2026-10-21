# Sound and music: 2.05 rev 2, compared with 2.17 / 2.22

Date: 2026-10-21

The 2.05 part is derived from the 2.05 rev 2 binary (sound path, options reader, GS1 sound commands). The later-client part comes from imports, option keys, and strings of `Graal_2171.exe`, `Graal_222.exe`, and `Graal_231.exe`. Names only, no code. Tags: **[2.05]** · **[2.17]** · **[2.22]** · **[inf]**.

## 2.05 at a glance

| What | Backend |
|------|---------|
| Sound effects (`.wav`) | DelphiX `TDXSound` / `TDXWaveList` on DirectSound |
| Music, Windows MCI path | invisible VCL `TMediaPlayer` (MCI, `mciSendCommand`) |
| Music, Winamp path | `TWinamp` component that remote-controls a running Winamp 1.x/2.x |
| Music volume | `midiOutSetVolume` (MCI path) or Winamp IPC messages |

### Options (`graalconfig.txt`)

| Key | Meaning |
|-----|---------|
| `musicon` | play music at all |
| `usewinamp` | send music to Winamp instead of MCI |
| `soundfxon` | play `.wav` effects |
| `reversestereo` | flip the pan sign |

The backend is chosen when the game starts and again whenever the More Options dialog closes. Switching stops the current track, frees the old backend, and creates the new one. Turning music off stops the current track. **[2.05]**

### One entry point for every sound

All sound requests go through one routine that takes `(file, level-offset x, level-offset y, x, y)`. The GS1 commands, GANI `PLAYSOUND`, item pickups, bombs, swords, and baddies all call it. About two dozen call sites use it. **[2.05]**

1. **Loop prefix.** A leading `+` means "looped". The `+` is stripped. Looped effects are added to the player's looped-sound list so that they can be stopped later.
2. **Missing file.** If the file is not on disk and the client is online, it sends a file request to the server (the same path that fetches images). The sound plays on a later trigger once the file has arrived. **[inf]**
3. **Position.** The listener is the player at (x + 1.5, y + 2). A sound from a neighbouring gmap level is shifted by ±64 tiles first.
   - Pan = (sound x − listener x) × 150, clamped to ±10000 (DirectSound pan units). `reversestereo` negates it.
   - Volume = a negative attenuation that grows with the distance on both axes, clamped at −10000 (DirectSound hundredths of a dB).
4. **Dispatch by extension.**
   - **`.wav`** → effect path (below), only when `soundfxon`.
   - **anything else** → music path (below), only when `musicon`. `.mid` is the common case.

### Effect path (`.wav`)

- Fifteen effects are known by name and flagged on use: `arrow, axe, bomb, crush, extra, fire, horse2, item, lift, lift2, put, steps, sword, thunder, water` (`.wav`).
- At most **8** effects play at once. A ninth request is dropped.
- Each file is loaded once into the wave list and cached by name. Later plays reuse the buffer with new pan, volume, and loop settings.
- `stopsound file` finds the cached wave by file name (the path is ignored) and stops it.
- Leaving a level or entering the editor stops every looped effect in the player's list.

### Music path: MCI

- An invisible `TMediaPlayer` is created on the main form with automatic device type, so `.mid` goes to the MCI sequencer. Other types depend on the MCI drivers installed on the machine. **[inf]**
- If the requested file differs from the current one, or nothing is playing, the client sets the file name, opens it, and plays.
- For `.mid` the player's completion notification is turned on. A handler on the main form replays the track when it ends, so **MIDI music loops forever** until `stopmidi` or another track.
- `setmusicvolume left,right` (0..1 each) calls `midiOutSetVolume` with left and right scaled to 0..65535. That is the system MIDI-out volume, not a per-track volume.

### Music path: Winamp

`TWinamp` is a third-party Delphi component (unit `Winamp`). It controls an external Winamp through the public Winamp window-message API. **[2.05]**

- It finds the player by window class `Winamp v1.x`. If no Winamp is running, it reads the Winamp path from the registry key `Software\CLASSES\Winamp.File\shell\Play\command` and starts it.
- A timer polls the window and status, and fires events on play, stop, pause, title change, and exit.
- Playing a track: if Winamp's current file differs or Winamp is stopped, the client loads the file and sends *play* (IPC_STARTPLAY / the play command).
- `stopmidi` sends *stop* when Winamp is playing or paused.
- `setmusicvolume left,right` maps to Winamp volume `(left + right) / 2 × 255` (IPC_SETVOLUME). The balance maps to Winamp panning.
- The component can also list the formats Winamp's input plugins accept (`winampGetInModule2`). In Winamp mode, music is effectively "whatever Winamp can play", MP3 included.

### GS1 sound commands in 2.05

| Command | Effect |
|---------|--------|
| `play file` | One-shot at the NPC's position (NPC x/y + half its image size). |
| `playlooped file` | Same, with the `+` loop prefix. |
| `stopsound file` | Stop a cached effect by file name. |
| `stopmidi` | Stop the current music (MCI or Winamp). |
| `setmusicvolume l,r` | MIDI-out volume (MCI) or Winamp volume and pan. |

## 2.17 / 2.22 / 2.31: BASS replaces DirectSound and Winamp

All three later clients import **`bass.dll`** with the same set of functions: init/start/free/update, sample load/play/stop/free, tracker music load/play/free, file streams, **URL streams**, stream length/position, channel attributes, and the **recording** API. `winmm` is still imported, now with `midiOutGetNumDevs` / `midiOutGetDevCapsA` added. **[2.17][2.22][2.31]**

| Area | 2.05 | 2.22 |
|------|------|------|
| Effects | DelphiX DirectSound wave list, 8-voice cap | BASS samples **[inf]** |
| Music files | MCI (MIDI) or Winamp (anything Winamp plays) | BASS streams and tracker modules. MIDI still via MCI **[inf]** |
| Internet radio | none | BASS URL streams, `radio` / `radiovolume` **[inf from names]** |
| Winamp | `usewinamp`, `TWinamp` | **removed**: no Winamp component, key, or window class |
| Volume options | none (only `setmusicvolume`) | `midivolume`, `mp3volume`, `radiovolume`, `sfxvolume`, `voicevolume` |
| Script access | `play`, `playlooped`, `stopsound`, `stopmidi`, `setmusicvolume` | same commands plus `musicpos` / `musiclen` (stream position and length) |
| Voice chat | none | microphone capture through BASS recording, `hvdi.dll` codec |

### Voice chat (2.22)

New options: `microon`, `microinputdevice`, `microactivatebyvolume`, `microactivationlevel`, `microactivatekey`, `voicecodec`, `voicevolume`. Status strings: "Could not initialize Microphone", "Microphone enabled", "Green when microphone activated". An `emoticonmicro.png` icon is shown over a talking player.

`hvdi.dll` is the HawkVoice voice library (exports `hvdiPacketEncode` / `Decode`, `VOX`, `AGC`, codec selection). The client captures with BASS, encodes with HawkVoice, and sends the voice packets over the network. **[2.22][inf for the transport]**

### `basswma.dll`

The 2.2.2 folder ships `basswma.dll` (the BASS WMA add-on), but its use depends on the version:

- **2.17.1** loads it at run time by name and uses `BASS_WMA_StreamCreateFile` / `StreamPlay` / `StreamFree`. **[2.17]**
- **2.22**, **2.31**, and GraalEditor 2.3.1.1 neither import nor name it. In those builds the DLL is a leftover and WMA music is not supported. **[2.22]**

## Open

- 2.22 extension-to-backend dispatch (which types go to samples, modules, or streams) needs the 2.22 sound routine traced.
- Exactly what 2.05 does after a missing sound file arrives from the server.
