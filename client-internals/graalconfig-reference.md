# graalconfig.txt and registry reference (client 2.05)

Date: 2026-10-21

Traced from the 2.05 rev 2 options reader and writer, the More Options and Player List Options dialogs, and their form resources. Checked against a real `graalconfig.txt` written by the 2.22 client, which uses the same keys in the same order. Tags: **[2.05]** read from the client · **[2.22]** seen in a 2.22 file · **[inf]** inferred.

## Where settings live

| Store | Location | Holds |
|-------|----------|-------|
| `graalconfig.txt` | Next to the exe | Every option on the More Options and Player List Options dialogs, the head, language, font, joystick and key bindings |
| Registry | `HKEY_CURRENT_USER\Software\Graal\Client` | `nickname`, `accountname`, `password`, and one `<account>:pass` value per account |

The file is a plain `key=value` list, read with Delphi `TStringList.Values`. Key lookup is case-insensitive, and order doesn't matter on read. **[2.05]**

## When it is read and written

- **Read** once, when the options form is created at startup. **[2.05]**
- **Written** in full every time the More Options or Player List Options dialog closes. The writer always emits every key in the fixed order below, so hand edits that add other keys are lost on the next save. **[2.05]**
- **If the file is missing**, the client keeps its built-in defaults and sets `language` to the English name of the Windows user locale (for example `English` or `German`). **[2.05]**

## Value parsing

| Kind | Rule | Pitfall |
|------|------|---------|
| Boolean | `true` when the value, lowercased, is exactly `true`. Anything else is `false`. Written as `true` / `false`. | A **missing** boolean key reads as `false`, not as the default. A partial file therefore switches off the options that default to on: `musicon`, `soundfxon`, `saveimages`, `nohtmlimages`, `joystickon`. |
| Integer | `StrToInt`. A conversion error is caught and the default is kept. | An empty or missing integer key keeps the default. |
| String | Used only when non-empty. | |

## Keys, in file order

UI labels are the dialog captions. MO = More Options, PL = Player List Options.

| Key | Type | Default | UI | Effect |
|-----|------|---------|----|--------|
| `waitvertical` | bool | false | MO "Wait for vertical blank (slower but smoother)" | Vsync on flip |
| `musicon` | bool | true | MO "Music support" | Turning it off stops the music player **[inf]** |
| `usewinamp` | bool | false | MO "Use WinAmp for music" | Music goes through Winamp |
| `soundfxon` | bool | true | MO "Sound FX's enabled" | |
| `reversestereo` | bool | false | MO "Reverse stereo channels" | |
| `saveimages` | bool | true | MO "Save downloaded images (to \levels\webgifs)" | Turning it on writes the images already in memory to disk **[inf]** |
| `dontsavepms` | bool | false | PL "Don't save PMs/Profiles" | |
| `compabilitydraw` | bool | false | MO "Draw in compatibility mode (very slow)" | Spelling as in the client |
| `nodecompressionerror` | bool | false | MO "Don't show decompression errors" | |
| `head1`, then `head` | string | `Fung Si Yun` | none | Read in that order, so `head` wins. Only `head=` is written. The default value is a literal in the client. **[2.05]** The 2.22 file still holds it. **[2.22]** |
| `joystickon` | bool | true | MO "Joystick support" | |
| `nodirectinput` | bool | false | MO "Don't use DirectInput" | |
| `joyselected` (also reads `joyselected1`) | string | `(none)` | Controls frame | `(none)`, `Joystick1` or `Joystick2` |
| `keyset_<action>_joystickbutton` | string | per action | Controls frame | One of `Joy_Up`, `Joy_Down`, `Joy_Left`, `Joy_Right`, `Button1`…`Button12` |
| `keyset_<action>_key0` … `_key2` | string | per action | Controls frame | Three key slots per action, by key name (`Up`, `Num 8`, `Space`, `Tab`, …). Empty means unbound. |
| `language` | string | `English` | Connect frame language box | |
| `font` | string | `Tempus Sans ITC` | MO "Font:" | Chat and name font. The 2.22 folder ships this font file. |
| `fontsize` | int | 24 | MO "Size:" | |
| `fixedport` | bool | false | MO "Use fixed port for data packages:" | |
| `fixedudpport` | int | 14899 | MO port box | Used when `fixedport` is true |
| `noudp` | bool | false | MO "Don't use UDP for data packages" | Changing the UDP options restarts the UDP socket **[inf]** |
| `nomassmessages` | bool | false | PL "Ignore mass messages" | |
| `nohtmlinpms` | bool | false | PL "Don't use HTML for PMs" | |
| `limitnicknames` | bool | false | MO "Limit the lenght of nicknames to" | |
| `nicknamelimit` | int | 50 | MO length box | |
| `dontconnectlevels` | bool | false | MO "Don't connect levels" | Turning it on drops the cached neighbour levels **[inf]** |
| `notoalls` | bool | false | MO "Ignore toalls" | Turning it on also clears the toall history **[inf]** |
| `nohtmlimages` | bool | true | PL "No images in PMs" | |
| `sortplayersbyname` | bool | false | PL "Playerlist: sort by nickname" | |
| `dontloadlistheads` | bool | false | MO "Don't load heads for the playerlist / map" | |
| `dontsavepasswords` | bool | false | MO "Don't save the passwords" | See below |
| `dontusedirectx7` | bool | false | MO "Don't use DirectX7" | |
| `fullscreenmode` | string | `1024x768` | MO "Fullscreen mode:" | One of `640x480`, `800x600`, `1024x768`, `1280x1024`, `1600x1200`. Any other value keeps the default resolution. |

The joystick and key block is written right after `head=`. The 11 actions, in file order, are `up`, `left`, `down`, `right`, `item`, `attack`, `action`, `map`, `switchtochat`, `itemlist`, `pause`. **[2.05]**

Key binding rules on load: **[2.05]**
- A key name that is already bound earlier in the file is treated as `-` (unbound), so one key can't drive two slots.
- Binding a key that another slot already holds moves it, and the other slot gets the old key.

Default joystick buttons, in action order: `Joy_Up`, `Joy_Left`, `Joy_Down`, `Joy_Right`, `Button1`…`Button5`, `Button9`, `Button10`. **[2.05]** The 2.22 file matches. **[2.22]**

## Keys in older notes that 2.05 does not read

`serveraddr`, `loadcolorsfromserver` and `gamemode` (listed in `config-and-input.md`) are not read or written by 2.05. If they exist, they belong to later clients. **[2.05]**

## Registry values

| Value under `HKCU\Software\Graal\Client` | Read | Written |
|------------------------------------------|------|---------|
| `nickname` | At startup | When the dialogs close |
| `accountname` | At startup. It is a comma list, and the first entry is the current account. | When the dialogs close |
| `password` | At startup, decrypted | When the dialogs close, unless `dontsavepasswords` is true |
| `<account>:pass` | At startup for the current account, and again when the account box changes | Same as `password` |

When the More Options dialog closes with "Don't save the passwords" ticked, the client deletes `password` and every value whose name ends in `:pass` from that key. **[2.05]**

Password values are encrypted with a fixed key. See `saved-passwords.md`.
