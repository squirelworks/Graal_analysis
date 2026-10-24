# 01 Sound and music

Snapshots read: Graal_analysis `8da6800` (main), Seihai `06aacfd` (main, 2026-10-24 03:23 JST).
Tags: **[2.05]** read from the 2.05 client, **[srv]** GServer-v2 source, **[cap]** lab capture, **[inf]** inferred.

## What it is
There is **no sound packet**. Sound is purely client-side and is triggered by four things:
- GS1 commands `play`, `playlooped`, `stopsound`, `stopmidi`, `setmusicvolume`.
- GANI `PLAYSOUND name x y` lines (the sound belongs to a frame).
- Built-in events: item pickup, bomb, sword, arrow, baddy death, chest, jump, etc.
- Config switches `musicon`, `soundfxon`, `reversestereo`, `usewinamp` (see 09).

The only network part is fetching a missing sound: the client sends `PLI_WANTFILE` (23) and the server answers with `PLO_FILE` (102) via `TPlayer::msgPLI_WANTFILE` / `sendFile`. File transfer is already in Seihai.

2.05 built-in effect names (the client plays these without any NPC): arrow, arrowon, axe, bomb, chest, compudead, crush, extra, fire, frog, horse2, item, item2, jump, lift, lift2, nextpage, put, steps, stonemove, sword, swordon, thunder, water (all `.wav`). **[2.05]**

## Exact client behaviour (from `client-internals/sound-and-music.md`) **[2.05]**
1. One entry point takes (file, level offset x/y, x, y). A leading `+` means loop and is stripped.
2. A missing file while online triggers WANTFILE; the sound plays on a later trigger.
3. Listener = player at (x+1.5, y+2). A sound from a neighbouring gmap level is shifted by 64 tiles. Pan = (soundx - listenerx) * 150, clamped to ±10000, negated by `reversestereo`. Volume = attenuation growing with distance on both axes, floored at -10000 (hundredths of a dB).
4. `.wav` goes to the effect path (only if `soundfxon`); anything else goes to the music path (only if `musicon`).
5. At most 8 effects play at once; a 9th is dropped. Effects are cached by file name. Leaving a level stops looped effects.
6. MIDI music loops until `stopmidi` or another track. `setmusicvolume l,r` is 0..1 each.
7. 2.17+ clients use BASS (effects, tracker modules, streams, URL radio). Same GS1 commands plus `musicpos`/`musiclen`. **[2.17][2.22]**

## Seihai today
- `assets/gani.rs` parses `PLAYSOUND` into `GaniFrame.sound` (a name only). Nothing plays it.
- No audio dependency in `Cargo.toml` (only flate2, bzip2, minifb, eframe/egui).
- GS1 command table in `scripting/gs1.rs` lists the sound commands by opcode but there is no executor for them.

## Steps for Claude
1. Add a `sound` module with a trait `SoundOut { play(name, pan, vol, looped), stop(name), stop_all_loops() }` and a null implementation, so the rest compiles and tests without a device.
2. Write a small WAV reader (PCM 8/16-bit, mono/stereo; the 2.05 files are plain PCM). Cache decoded buffers by lower-cased base name.
3. Implement the mixing rules above: 8-voice cap, pan and volume from listener distance, `+` loop prefix, `reversestereo` flag.
4. Real backend behind a cargo feature (for example `rodio` or `cpal`) so the default build stays dependency-light. Ask the user before adding the crate.
5. Wire three triggers: GANI frame `sound` when a frame is first shown, the GS1 `play` family in `offline/mod.rs` and `scripting`, and a short fixed list of built-in events (sword swing, bomb, item pickup, chest).
6. Missing file: call the existing `send_wantfile`, then retry on the next trigger.
7. Music: play only formats you can decode (WAV, later OGG/MP3). Do not try to emulate MIDI; log "music skipped: midi" and carry on. This is a design call for the user.

## How to test
- Unit tests with a recording `SoundOut` mock: feed a gani with `PLAYSOUND`, check calls, the 8-voice cap, pan sign and the loop prefix.
- Lab: the lab gserver world has a `sounds` folder; log in with Seihai, walk, and request a sound file with WANTFILE to see the `PLO_FILE` path (private display only).

## NEEDS
nothing for `.wav` effects. (MIDI/MP3 backend choice is a design decision, not missing research. The exact 2.22 extension-to-backend dispatch is only needed if you want BASS parity.)
