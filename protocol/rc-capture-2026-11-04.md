# RC player admin on the wire: a real 2004 RC against a GServer-v2 fork

Date: 2026-11-04. Tags: [cap] for what the capture shows. Names of ids are the
GServer-v2 names that the Seihai capture viewer prints.

## Setup

- RC: `RemoteControl.exe` from the Graal Reborn folder (2004), token `GSERV024`, under Wine 9 (32-bit prefix).
- Target: a real 2.22 client logged in as player id 3, on the start level.
- Game server: the Seihai project's GPL GServer-v2 fork (`seihai-gserver-v2`, commit `f585ca6`), lab world, account `labrc` on the staff list.
- Listserver: `seihai-listserver` (Rust, `main` of 2026-11-04).
- Everything ran on one host, in a private network namespace with only loopback. Addresses and ports are written here as `<gserver-ip>` and `<gserver-port>`.
- Decoded with `seihai capture show <pcap> --version 2.22 --raw`. The pcap is private to the project; it holds only a lab password.

Notation: `c` is one byte = value + 32; `s` is 2 bytes, `i3` 3 bytes and `i5` 5 bytes, 7 bits per byte, high first, each byte + 32. `str` is a `c` length then that many bytes. `rest` is the rest of the message. CSV is Graal's tokenized text: each line quoted when it needs it, lines joined by commas.

Each layout below was seen in one session, with the values given.

## RC list from the listserver

| Dir | Message | Layout | Seen |
| --- | --- | --- | --- |
| C→S | handshake | client id 5, empty token, empty list name | id 5 |
| C→S | login | `str account`, `str password` | account `labrc` |
| S→C | id 0 list | `c count`; per server `c 8` (field count), then 8 × `str`: name, language, description, URL, version, players, address, port | 1 server; name `H My Server`, language `English`, URL empty, players `1` |
| S→C | id 4 | text, for an unknown account | `Account does not exist.` |

The RC lists the name and the player count, and shows the id 4 text in a message box. The `H ` at the start of the name is the lab listserver's type tag.

## After the RC login

Server → RC, in this order: 25 SIGNATURE, 194 CLEARWEAPONS, 74 RC_CHAT three times, 190 SERVERLISTCONNECTED (empty), 47 STAFFGUILDS (comma list), 180 STATUSLIST, 103 RC_MAXUPLOADFILESIZE, 55 ADDPLAYER for each player online, then 74 RC_CHAT `Currently online: ...`.

| Id | Layout | Seen |
| ---: | --- | --- |
| 103 RC_MAXUPLOADFILESIZE | `i5` bytes | 20971520 (20 MiB) |
| 55 ADDPLAYER | `s player id`, `str account`, then props as id + value | id 3, `test1`, prop 20 CURLEVEL `onlinestartlocal.nw`, then more props |

The RC then sent its own 2 PLAYERPROPS twice, and the server answered with 9.

## Player props

| Dir | Id | Layout |
| --- | ---: | --- |
| C→S | 73 RC_PLAYERPROPSGET2 | `s player id` |
| S→C | 72 RC_PLAYERPROPSGET | `s player id`, `str account`, `str world`, `c n`, n bytes of props (id + value), tail |
| C→S | 76 RC_PLAYERPROPSSET2 | `str account`, `str world`, `c n`, n bytes of props, tail, then one more byte (0) |

The tail is the same both ways: `s 0`, `s 0`, `c weapon count`, `str` per weapon. Seen weapons: `bomb`, `bow`, `-gr_movement`. Both `s` values were 0, so which one counts flags and which counts opened chests has not been seen. The extra last byte of 76 was 0 and has no known meaning.

The world was `main`. The props block was 144 bytes from the server and 125 from the RC.

| Prop | Server sent | RC sent back |
| ---: | --- | --- |
| 0 NICKNAME | `Lab222rc` | not sent |
| 1, 2 | max power 3, power 6 (half hearts) | same |
| 3 | `i3` 0, then 7 after the edit | 7 (the only value changed in the dialog: gralats 0 → 7) |
| 4, 5, 6 | arrows 10, bombs 5, glove 1 | same |
| 8, 9 | sword (power + 30, `sword1.png`), shield (power + 10, `shield1.png`) | same |
| 10, 11 | gani `idle`; head (length + 100, `head0.png`) | same |
| 13, 15, 16, 18, 20 | colours (5 bytes), x 60 and y 61 (half tiles), status 20, level `onlinestartlocal.nw` | same |
| 21, 22, 23 | not sent | one byte each, 0 |
| 26 | one byte, 0 | same |
| 27, 28, 29 | `i3` 0, `i3` 0, `i3` 475 (the dialog's kills 0, deaths 0, online seconds 475) | same, 29 sent as 0 |
| 30 | `i5` (the dialog's last IP) | not sent |
| 32 | one byte, 52, then 55 on the second read (the dialog's AP) | 52 |
| 34 | account `test1` | not sent |
| 35 | body `body.png` | same |
| 36 | `i3` = rating × 512 + deviation (1500, 350) | not sent |

The server logged that the RC set the player's attributes, and the second read showed gralats 7.

## Rights

| Dir | Id | Layout | Seen |
| --- | ---: | --- | --- |
| C→S | 83 RC_PLAYERRIGHTSGET | account as `rest` | `test1` |
| S→C | 62 RC_PLAYERRIGHTSGET | `str account`, `i5 rights`, `str IP range`, `s n` + n bytes of folder rights | rights 0, `0.0.0.0`, empty |
| C→S | 84 RC_PLAYERRIGHTSSET | same layout as 62 | rights 513, `0.0.0.0`, 13 bytes `"rw levels/*"` |

In this one session, the rights bits followed the order of the dialog's check boxes from bit 0: "Warpto x y" (1) and "Admin message" (512) give 513.

The RC sends the folder lines as CSV, so a line with a space is quoted. On the second read the fork returned `rw levels/*` (11 bytes, no quotes), and the RC showed it as two lines, `rw` and `levels/*`.

## Comments

| Dir | Id | Layout | Seen |
| --- | ---: | --- | --- |
| C→S | 85 RC_PLAYERCOMMENTSGET | account as `rest` | `test1` |
| S→C | 63 RC_PLAYERCOMMENTSGET | `str account`, comments as CSV (`rest`) | empty; after the set `"lab comment one","line two"` |
| C→S | 86 RC_PLAYERCOMMENTSSET | `str account`, comments as CSV (`rest`) | `"lab comment one","line two"` |

Each line of the dialog's text box is one CSV item. The comments came back unchanged.

## Ban

This RC's player menu has Edit Ban only. That is the account ban on this server; there is no ban by IP or computer id.

| Dir | Id | Layout | Seen |
| --- | ---: | --- | --- |
| C→S | 87 RC_PLAYERBANGET | account as `rest` | `test1` |
| S→C | 64 RC_PLAYERBANGET | `str account`, `c banned`, reason (`rest`) | not banned, empty reason |
| C→S | 88 RC_PLAYERBANSET | `str account`, `c banned`, reason as CSV (`rest`) | banned 1, `"lab ban reason"` |

After 88 for a player who was online, the fork wrote the ban to the account file. Then it used a full CPU core and sent nothing more to either connection, and it did not answer two later 87. Its process stayed up and its port still accepted connections. This was seen once.

## Ids against the static read

The 2004 row of the static id read lists 84, 86 and 88 but not 83, 85 or 87, and that read counts only constant ids. On the wire this RC sent 83, 85 and 87 as well, together with 73 and 76.
