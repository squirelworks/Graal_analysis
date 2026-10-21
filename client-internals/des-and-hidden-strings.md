# Hidden strings and 2.22 saved passwords (2.05, 2.22)

Date: 2026-10-21

Tags: **[2.05]** read from the 2.05 rev 2 binary · **[2.22]** read from the 2.22 binary · **[cap]** checked in the lab (`tools/lab-setup.md`) · **[inf]** inference.

## DES, saved passwords and the web cache (pointers)

The 2.05 DES routine (standard DES-ECB with each key byte bit-reversed), the 48-character string form and the 2.05 saved-password scheme are written up in `client-internals/saved-passwords.md`, and the web-level cache cipher in `formats/gwebl001-cache.md` (both added by PR #6). This note only adds the parts those files don't cover.

**2.22 saved passwords** **[2.22]**
- Same 48-character scheme as 2.05, with one change. A saved value of 49 characters starting with a marker character is decrypted with a second key held by the options form. Any other value is decrypted with the first key, so old saved passwords still load.
- New saves use the second key and the marker.
- The account name is also stored hidden, using the byte transform below.

## Hidden strings

**2.05 listserver host** **[2.05][cap]**
- Uses the DES string form from `saved-passwords.md`. The server-list form builds an 8-byte DES key (`2B 77 77 A7 B4 31 21 41`) and a 48-character ciphertext one `Chr()` at a time, so neither appears in the string table.
- It decrypts to `www.graalonline.com`. The port (`14921`) and the first packet text (`newmain`) are built the same way, as plain characters.

**2.22 transform** **[2.22][cap]**
- `dec(b) = (NOT b − 10) & 0xFF` and `enc(b) = NOT (b + 10)`.
- Used for:
  - the in-memory copy of the three listserver host names (`listserver.graal.in`, `.graal.cc`, `listserver.graalonline.biz`) and the port (`14922`)
  - the account name in the config
  - the account name before it goes into the game-server login packet
- The host names and port themselves are read at start-up from `arrays2.dat`, where they are plain text (checked against `arrays2.sig`). Only the copy held in memory is transformed, so a memory search for the plain names finds nothing. See `protocol/listserver.md`.

**2.22 version token** **[2.22]**
- The game-server login builds `GNW03014` one character at a time.
- On the wire the login line is: `GCHAR 5` (client type 5, gen 5), `GCHAR key`, the token, `GCHAR len` + account, `GCHAR len` + password. **[cap]**
- It is followed at once by id 37 (language) and id 39, a 10-byte value the client builds from two 32-bit globals. Its meaning is not traced. **[inf]**

## Notes for tool writers
- To redirect 2.05, a hosts entry for `www.graalonline.com` is enough.
- To redirect 2.22, hosts entries for the three `listserver.*` names are enough. It tries them in order. Editing `arrays2.dat` instead would have to get past the `arrays2.sig` check, which the lab did not test.
- None of these schemes protect anything. They only keep the strings out of a casual `strings` dump.
