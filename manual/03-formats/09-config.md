<!-- manual: kind=reference status=draft -->
# 3.9 Config and dat files

The client keeps its settings in `graalconfig.txt` next to the executable and its login details in the registry. This chapter gives both as 2.05 rev 2 reads and writes them, checked against a real `graalconfig.txt` written by 2.22, which uses the same keys in the same order [2.05][2.22] (client-internals/graalconfig-reference.md). The table files `arrays.dat` and `arrays2.dat` are in → §3.5.

> Status: draft. 2.05 is traced and 2.22 compared; the keys of 3.x and later clients are unmeasured.

## 3.9.1 Where settings live

| Store | Location | Holds | Source |
| --- | --- | --- | --- |
| `graalconfig.txt` | next to the executable | every option on the More Options and Player List Options dialogs, the head, language, font, joystick and key bindings | [2.05] (client-internals/graalconfig-reference.md#where-settings-live) |
| registry | `HKEY_CURRENT_USER\Software\Graal\Client` | `nickname`, `accountname`, `password`, and one `<account>:pass` value per account | [2.05] (client-internals/graalconfig-reference.md#where-settings-live) |

## 3.9.2 graalconfig.txt file rules

| Rule | Detail | Source |
| --- | --- | --- |
| form | a plain `key=value` list; key lookup is case-insensitive and order does not matter on read | [2.05] (client-internals/graalconfig-reference.md#where-settings-live) |
| read | once, when the options form is created at startup | [2.05] (client-internals/graalconfig-reference.md#when-it-is-read-and-written) |
| written | in full every time the More Options or Player List Options dialog closes, every key in the fixed order of §3.9.3; hand-added keys are lost on the next save | [2.05] (client-internals/graalconfig-reference.md#when-it-is-read-and-written) |
| missing file | the built-in defaults stay, and `language` is set to the English name of the Windows user locale (for example `English` or `German`) | [2.05] (client-internals/graalconfig-reference.md#when-it-is-read-and-written) |
| boolean | `true` when the lowercased value is exactly `true`, anything else `false`; written as `true` or `false` | [2.05] (client-internals/graalconfig-reference.md#value-parsing) |
| missing boolean | reads as `false`, not as the default; a partial file therefore switches off `musicon`, `soundfxon`, `saveimages`, `nohtmlimages` and `joystickon` | [2.05] (client-internals/graalconfig-reference.md#value-parsing) |
| integer | converted as decimal; a conversion error, an empty value or a missing key keeps the default | [2.05] (client-internals/graalconfig-reference.md#value-parsing) |
| string | used only when non-empty | [2.05] (client-internals/graalconfig-reference.md#value-parsing) |

## 3.9.3 Keys in file order (2.05)

MO is the More Options dialog and PL the Player List Options dialog; labels are the dialog captions as the client spells them. [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order)

| Key | Type | Default | Dialog label | Effect | Source |
| --- | --- | --- | --- | --- | --- |
| `waitvertical` | bool | false | MO "Wait for vertical blank (slower but smoother)" | vsync on flip | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `musicon` | bool | true | MO "Music support" | turning it off stops the music player | [2.05][inf] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `usewinamp` | bool | false | MO "Use WinAmp for music" | music goes through Winamp (→ §3.10.3) | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `soundfxon` | bool | true | MO "Sound FX's enabled" | sound effects | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `reversestereo` | bool | false | MO "Reverse stereo channels" | swaps channels | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `saveimages` | bool | true | MO "Save downloaded images (to \levels\webgifs)" | turning it on writes the images already in memory to disk | [2.05][inf] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `dontsavepms` | bool | false | PL "Don't save PMs/Profiles" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `compabilitydraw` | bool | false | MO "Draw in compatibility mode (very slow)" | spelling as in the client | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `nodecompressionerror` | bool | false | MO "Don't show decompression errors" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `head1`, then `head` | string | `Fung Si Yun` | none | read in that order, so `head` wins; only `head=` is written; the 2.22 file still holds the default | [2.05][2.22] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `joystickon` | bool | true | MO "Joystick support" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `nodirectinput` | bool | false | MO "Don't use DirectInput" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `joyselected` (also reads `joyselected1`) | string | `(none)` | Controls frame | `(none)`, `Joystick1` or `Joystick2` | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `keyset_<action>_joystickbutton` | string | per action | Controls frame | one of `Joy_Up`, `Joy_Down`, `Joy_Left`, `Joy_Right`, `Button1` to `Button12` | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `keyset_<action>_key0` to `_key2` | string | per action | Controls frame | three key slots per action, by key name (`Up`, `Num 8`, `Space`, `Tab` …); empty means unbound | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `language` | string | `English` | Connect frame language box | interface language | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `font` | string | `Tempus Sans ITC` | MO "Font:" | chat and name font; the 2.22 folder ships this font file | [2.05][2.22] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `fontsize` | int | 24 | MO "Size:" | font size | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `fixedport` | bool | false | MO "Use fixed port for data packages:" | fixes the UDP port | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `fixedudpport` | int | 14899 | MO port box | used when `fixedport` is true | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `noudp` | bool | false | MO "Don't use UDP for data packages" | changing the UDP options restarts the UDP socket (→ §2.9) | [2.05][inf] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `nomassmessages` | bool | false | PL "Ignore mass messages" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `nohtmlinpms` | bool | false | PL "Don't use HTML for PMs" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `limitnicknames` | bool | false | MO "Limit the lenght of nicknames to" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `nicknamelimit` | int | 50 | MO length box | the limit | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `dontconnectlevels` | bool | false | MO "Don't connect levels" | turning it on drops the cached neighbour levels | [2.05][inf] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `notoalls` | bool | false | MO "Ignore toalls" | turning it on also clears the toall history | [2.05][inf] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `nohtmlimages` | bool | true | PL "No images in PMs" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `sortplayersbyname` | bool | false | PL "Playerlist: sort by nickname" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `dontloadlistheads` | bool | false | MO "Don't load heads for the playerlist / map" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `dontsavepasswords` | bool | false | MO "Don't save the passwords" | see §3.9.5 | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `dontusedirectx7` | bool | false | MO "Don't use DirectX7" | as labelled | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| `fullscreenmode` | string | `1024x768` | MO "Fullscreen mode:" | one of `640x480`, `800x600`, `1024x768`, `1280x1024`, `1600x1200`; any other value keeps the default | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |

## 3.9.4 Key bindings

| Rule | Detail | Source |
| --- | --- | --- |
| position | the joystick and key block is written right after `head=` | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| actions | 11, in file order: `up`, `left`, `down`, `right`, `item`, `attack`, `action`, `map`, `switchtochat`, `itemlist`, `pause` | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| duplicate key | a key name already bound earlier in the file is treated as `-` (unbound), so one key cannot drive two slots | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| rebinding | binding a key that another slot holds moves it, and the other slot gets the old key | [2.05] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| default joystick buttons | in action order: `Joy_Up`, `Joy_Left`, `Joy_Down`, `Joy_Right`, `Button1` to `Button5`, `Button9`, `Button10`; the 2.22 file matches | [2.05][2.22] (client-internals/graalconfig-reference.md#keys-in-file-order) |
| 2.22 default keys | arrows or IJKL, D, S or space, A, M, Tab, Q and P | [doc] (client-internals/config-and-input.md#update-2026-10-21-205-vs-222-graalconfig) |
| key names | 2.05 holds only the bare prefix `keyset_` as a string, so it probably builds the binding key names at run time | [inf] (client-internals/config-and-input.md#update-2026-10-21-205-vs-222-graalconfig) |

## 3.9.5 Registry values

| Value | Read | Written | Source |
| --- | --- | --- | --- |
| `nickname` | at startup | when the dialogs close | [2.05] (client-internals/graalconfig-reference.md#registry-values) |
| `accountname` | at startup; a comma list whose first entry is the current account | when the dialogs close | [2.05] (client-internals/graalconfig-reference.md#registry-values) |
| `password` | at startup, decrypted | when the dialogs close, unless `dontsavepasswords` is true | [2.05] (client-internals/graalconfig-reference.md#registry-values) |
| `<account>:pass` | at startup for the current account, and again when the account box changes | as `password` | [2.05] (client-internals/graalconfig-reference.md#registry-values) |

| Rule | Detail | Source |
| --- | --- | --- |
| clearing | when More Options closes with "Don't save the passwords" ticked, the client deletes `password` and every value whose name ends in `:pass` from the key | [2.05] (client-internals/graalconfig-reference.md#registry-values) |
| encryption | password values are encrypted with a fixed DES key, the literal that older notes called a password mask | [2.05] (client-internals/graalconfig-reference.md#registry-values); [2.05] (client-internals/config-and-input.md#graalconfigtxt) |

## 3.9.6 Keys by build

| Key or group | 2.05 | 2.22 | Source |
| --- | --- | --- | --- |
| the keys of §3.9.3 | read and written | present, same order | [2.05][2.22] (client-internals/graalconfig-reference.md) |
| `automapping`, the `micro*` and `voice*` voice-chat keys, `midivolume`, `mp3volume`, `radiovolume`, `sfxvolume`, `startinfullscreen`, `quickplayerworlds` | n/a | present | [2.05][doc] (client-internals/config-and-input.md#update-2026-10-21-205-vs-222-graalconfig) |
| `noudp` | default false | `noudp=true` in the compared file | [2.05][doc] (client-internals/config-and-input.md#update-2026-10-21-205-vs-222-graalconfig) |
| total | about 29 keys in the string table | 86 keys in the compared file | [2.05][doc] (client-internals/config-and-input.md#update-2026-10-21-205-vs-222-graalconfig) |
| `serveraddr`, `loadcolorsfromserver`, `gamemode` | not read or written | unmeasured | [2.05] (client-internals/graalconfig-reference.md#keys-in-older-notes-that-205-does-not-read) |

The three keys in the last row come from an older public key list [2.05] (client-internals/graalconfig-reference.md#keys-in-older-notes-that-205-does-not-read). The static survey places them in earlier clients, not later ones: `gamemode` from 1.1 to 1.41, `serveraddr` from 1.21 to 1.39, `loadcolorsfromserver` from 1.21 to NewMain [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys).

### 3.9.6.1 Plain key strings added and dropped, 1998 to 2.31

From 1.38 some keys are built one character at a time, so a build can read a key that is missing here; three-letter fragments such as `ekv` are such keys [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys).

| Build | Added | Dropped | Source |
| --- | --- | --- | --- |
| 6th Graal | `joystickon`, `musicon`, `reversestereo`, `soundfxon`, `waitvertical` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 8th Graal | `saveimages` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.1 | `editnickname`, `gamemode` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.21 | `accountname`, `loadcolorsfromserver`, `password`, `serveraddr`, `serverport` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.28 beta 2 | `compabilitydraw`, `externalchat`, `language`, `nodecompressionerror` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.3 test | `font`, `fontsize` | `accountname`, `password` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.31 | `fixedport`, `fixedudpport`, `noudp` | `editnickname` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.32 | `nomassmessages` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.33 | `nodirectinput` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.35 | `nohtmlinpms` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.36 | `limitnicknames`, `nicknamelimit` | `serverport` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.38 | | `externalchat` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.39 | `dontconnectlevels`, `dontloadlistheads`, `nohtmlimages`, `notoalls`, `sortplayersbyname` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.41 rev 1 | `dontsavepasswords`, `fullscreenmode`, `usewinamp` | `serveraddr` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| NewMain 1.42 | `dontsavepms`, `dontusedirectx7`, `head`, `joyselected` | `gamemode` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.00 | | `loadcolorsfromserver` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.1 test 2 | `startinfullscreen` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.17.1 | `automapping`, the `micro*` and `voice*` keys, `midivolume`, `mp3volume`, `quickplayerworlds`, `radiovolume`, `sfxvolume` | `musicon`, `soundfxon`, `usewinamp` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.31 | `cachefilenames` | | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |

## 3.9.7 Dropped files

| Rule | Detail | Source |
| --- | --- | --- |
| gate | a file dragged onto the client window is handled only when an internal flag is set, the same flag that enables the editor drop target | [live] (client-internals/config-and-input.md#drop-files) |
| `.txt` | spawns a script NPC | [live] (client-internals/config-and-input.md#drop-files) |
| `.gif`, `.png`, `.mng` | spawn an image NPC | [live] (client-internals/config-and-input.md#drop-files) |
| anything else | loaded as a level | [live] (client-internals/config-and-input.md#drop-files) |
| joystick | the device is activated when an internal bit is set; the WinMM joystick identifier is stored apart from the main window object | [live] (client-internals/config-and-input.md#device-path) |
