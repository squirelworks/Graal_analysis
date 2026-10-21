# DES, saved passwords and hidden strings (2.05, 2.22)

Date: 2026-10-21

Tags: **[2.05]** read from the 2.05 rev 2 binary · **[2.22]** read from the 2.22 binary · **[cap]** checked in the lab (`tools/lab-setup.md`) · **[inf]** inference.

## The DES class **[2.05]**

2.05 has a `DesCipher` class that does standard DES in ECB mode on 8-byte blocks. One detail matters: **each key byte is bit-reversed before key setup**, as in the old Java `DesCipher` ports. With an unmodified DES library, reverse the bits of every key byte first. This was confirmed by decrypting the hidden listserver string below. **[2.05][cap]**

Three uses are built on it.

### 1. Short strings (48-char text form)
- **Encrypt:**
  1. Cut the string to 23 characters.
  2. Write a length byte, then the characters.
  3. Fill the rest of the 24-byte buffer with `Random` bytes.
  4. DES-encrypt the three blocks.
  5. Write each byte as two characters, `(hi nibble)+0x20` and `(lo nibble)+0x20`. The output is always 48 printable characters.
- **Decrypt:** needs at least 48 characters. It reverses the steps and returns `length` characters. A length of 24 or more gives an empty string.

### 2. Files (web-level cache)
Used for the `GWEBL001` web-level cache.
- **Layout:**
  1. The plaintext is padded with `\n` to a multiple of 8.
  2. A 32-bit length (`len + 8`) is written.
  3. Each 8-byte block is DES-encrypted with **its own key**: 8 bytes from the Delphi RTL `Random(256)`.
  4. An 8-byte checksum (bytewise sums of the plaintext) follows.
- **How the key stream is seeded:** the reader sets `RandSeed = 0x4A80B38 × (product of the level-name bytes)` (mod 2^32) before reading. The key stream depends only on the level name, so anyone with the name can decrypt the file. The full format and a decoder belong in the formats notes. **[2.05]**

### 3. The hidden listserver address
See below.

## Saved passwords

**2.05** **[2.05]**
- Unless `dontsavepasswords=1`, the options writer stores the account name in clear and the password as a 48-character DES string, under section `Client`, keys `accountname` and `password`.
- A second copy goes under `<account>:pass`.
- The key is the constant `~2%$zsd^`, compiled into the client. Any saved password can be decrypted by anyone who has the client. Treat old config stores as plain text.

**2.22** **[2.22]**
- Same scheme, with one change. A saved value of 49 characters starting with a marker character is decrypted with a second key held by the options form. Any other value is decrypted with the first key, so old saved passwords still load.
- New saves use the second key and the marker.
- The account name is also stored hidden, using the byte transform below.

## Hidden strings

**2.05 listserver host** **[2.05][cap]**
- The server-list form builds an 8-byte DES key (`2B 77 77 A7 B4 31 21 41`) and a 48-character ciphertext one `Chr()` at a time, so neither appears in the string table.
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
