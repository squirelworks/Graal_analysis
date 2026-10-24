# 09 In-game options

Snapshots read: Graal_analysis `8da6800` (`client-internals/graalconfig-reference.md`, `config-and-input.md`), Seihai `06aacfd` (`settings.rs`, `bin/main.rs`).

## What it is
The 2.05 client has a **More Options** dialog, a **Player List Options** dialog and a **Controls** frame. All of them read and write one text file, `graalconfig.txt` (`key=value`, case-insensitive keys, rewritten in full with every key in fixed order whenever either dialog closes). Nothing goes over the network. Registry values hold the nickname, account list and (encrypted) passwords.

### Parse rules (matter for a compatible reader) **[2.05]**
- Booleans are true only if the lower-cased value is exactly `true`; a **missing** boolean reads as false.
- Integers: parse error keeps the default. Strings: used only if non-empty.
- Key binding: a key already bound earlier in the file becomes unbound; binding a key held elsewhere swaps it.

### Keys (file order, default)
`waitvertical` false, `musicon` true, `usewinamp` false, `soundfxon` true, `reversestereo` false, `saveimages` true, `dontsavepms` false, `compabilitydraw` false (spelling as in the client), `nodecompressionerror` false, `head` (default `Fung Si Yun`), `joystickon` true, `nodirectinput` false, `joyselected`, `keyset_<action>_joystickbutton`, `keyset_<action>_key0..2`, `language` (English), `font` (Tempus Sans ITC), `fontsize` 24, `fixedport` false, `fixedudpport` 14899, `noudp` false, `nomassmessages` false, `nohtmlinpms` false, `limitnicknames` false, `nicknamelimit` 50, `dontconnectlevels` false, `notoalls` false, `nohtmlimages` true, `sortplayersbyname` false, `dontloadlistheads` false, `dontsavepasswords` false, `dontusedirectx7` false, `fullscreenmode` 1024x768.
Actions with three key slots: up, left, down, right, item, attack, action, map, switchtochat, itemlist, pause. The per-action default keys for 2.05 are not listed in the notes; the fixed keys of 1.37 were arrows or IJKL, D item, S or Space attack, A action, M map, Q item list, P pause, Tab chat (`versions-133-139.md`). Default joystick buttons are in `graalconfig-reference.md`.
Later clients add `midivolume`, `mp3volume`, `radiovolume`, `sfxvolume`, `voicevolume`, and an Audio/Microphone tab (2.17+).

### What the options change at run time
`musicon`/`soundfxon`/`reversestereo` (01); `noudp`/`fixedport`/`fixedudpport` (07); `nomassmessages`, `notoalls`, `nohtmlinpms`, `nohtmlimages`, `sortplayersbyname`, `dontloadlistheads` (14, player list); `dontconnectlevels` stops neighbour-level preloading (06); `limitnicknames` truncates displayed nicknames; `saveimages`; `language`.

## Seihai today
- `settings.rs` is Seihai's own launcher file (assets path, account, password, version, last server, listserver, offline flag). It is **not** `graalconfig.txt`. It stores the account password in the settings file; note that 2.05 encrypts saved passwords and has `dontsavepasswords`. Decide with the user before keeping plaintext.
- `bin/main.rs` has fixed keys (arrows move, A/Space interact, Enter chat, F2/F3/F4/F5/F9/F12 dev actions, PageUp/Down scroll). No options screen. The launcher `gui.rs` (egui) picks assets and server.

## Steps for Claude
1. Add `options.rs`: a struct with the keys above, `load_graalconfig(path)` implementing the parse rules, `save_graalconfig(path)` writing all keys in order. Keep Seihai-specific keys in `settings.rs`.
2. Round-trip test: parse a 2.05-style file with a missing boolean and assert the false-on-missing behaviour; write and re-read.
3. Key map: a table from action to up to three key names; implement the "already bound is unbound" load rule. Replace the hard-coded keys in `main.rs` with lookups.
4. In-game screen: an egui or framebuffer window opened with F1 (original key) listing music, sound, reverse stereo, UDP options, nickname limit, no-toalls, player-list sort. Apply without restart where easy.
5. Wire only options whose feature exists (sound after 01, UDP after 07, gmap after 06). Others are stored and written back unchanged.
6. Optionally read an existing `graalconfig.txt` from the assets folder as defaults.

## How to test
- Pure unit tests (file parse/write). No lab needed.
- Compare against a real file written by the 2.22 client in the lab (the notes say 2.22 uses the same keys in the same order).

## NEEDS
nothing.
