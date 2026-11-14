# Saved passwords and the client's DES string cipher

Date: 2026-10-21

Traced from client 2.05 rev 2. Tags: **[2.05]** read from the client · **[test]** checked with `tools/file-formats/graaldes.py`.

## Warning for anyone holding old installs

The client stores account passwords in the registry under `HKEY_CURRENT_USER\Software\Graal\Client` (`password`, and `<account>:pass` per account). They are DES-encrypted with an 8-byte key that is the same in every copy of the client: `~2%$zsd^`. **[2.05]**

The same key and string form are already used by 1.3 test (Nov 1999): a value saved by 1.31/1.32 in a lab run decrypts with `graaldes.py`, and the key string is in every client from 1.3 test to 1.39 (`live-trace-early.md`). So the warning covers those old installs too.

That means anyone who can read the registry, or a `.reg` export or backup of that key, can recover the password with no secret at all. Treat these values as plain text. If an old machine, disk image or exported profile is shared, delete the values first, or tick "Don't save the passwords" in More Options (the client then deletes them on close).

## Cipher

- DES in ECB mode, standard tables, with one twist: **each key byte is bit-reversed** before the key schedule (bit 0 becomes bit 7). This is how the Acme Labs Java `DesCipher` handles keys, and the client's DES unit behaves the same. **[2.05]** **[test]**
- Equivalent: standard DES with the key `bitreverse(k[0]) … bitreverse(k[7])`.
- **Later clients keep the quirk (2026-11-06).** The libtomcrypt DES in the 4.04r2 `GraalEngine.dll` and the 6.03r7 Windows client, run in an emulator, gives `CEE55ACD2386B23F` for key `133457799BBCDFF1` and block `0123456789ABCDEF` (textbook DES: `85E813540F0AB405`), and matches "standard DES with bit-reversed key bytes" on every random pair tried. `graaldes.py` gives the same value. The real 6.03r7 and 4.20r8 clients both loaded an encrypted `.gpake` package built this way (`formats/gpak.md`). So the PLO 104 package keys, and very likely the `GRESCR01` script cache, need this DES too. **[bin]** **[test]**

## String format (48 characters)

Encrypt:
1. Truncate the plaintext to 23 bytes.
2. Build 24 bytes: `len`, the plaintext, then random padding bytes.
3. Encrypt as three DES blocks.
4. Write each of the 24 bytes as two characters: `(b >> 4) + 0x20`, `(b & 0x0F) + 0x20`.

Decrypt reverses this. Input shorter than 48 characters gives an empty string. The first decrypted byte is the length, and values of 0 or ≥ 24 give an empty string. **[2.05]**

Because the padding is random, the same password encrypts to a different string each time.

## Mac 4.20r6: same format, per-machine key (2026-11-12)

The Mac PowerPC 4.20r6 client keeps its settings in `~/.graal/.registry`, a plain-text
`key=value` file that stands in for the Windows registry key. It holds `accountname`,
`password` and one `<account>:pass` line per saved account (a colon, as on Windows). Each value
is `1` followed by the same 48-character string as above: length byte, password, random padding,
DES-ECB with bit-reversed key bytes. **[bin][lab]**

The key is not the fixed `~2%$zsd^`. The client starts from the 8 bytes `73 e4 7e b3 34 a7 4a 2b`
and, when it finds a primary Ethernet interface, XORs key bytes 2 to 7 with the six bytes of that
interface's hardware address and with `5d c4 2a 3f 60 dc`. With no primary interface the base key
is used as it is. So a saved password decrypts only with the same machine's hardware address, and
a copied `.registry` file moved to another Mac loses its passwords. A lab value decrypted to the
typed password with this key and `graaldes.GraalDES`; the 2.05 fixed key and normal key byte order
both gave garbage. **[bin][lab]** The same per-machine idea applies to Windows v4 (there with part
of the address and of the product id); see `protocol/pcid.md` for which interface counts as
primary on the Mac.

## Other uses of the same cipher

- The hidden listserver host: the server list frame builds a different 8-byte key and a 48-character ciphertext one character at a time. It decrypts to `<list-host-classic>`, port `14921`. **[2.05]** **[test]**
- The web-level cache uses the same DES routine with per-block keys. See `formats/gwebl001-cache.md`.

## Tool

`tools/file-formats/graaldes.py` (pure Python):

```
python3 graaldes.py '<48-char value>'
```

It implements `GraalDES` (block cipher), `string_decrypt` and `string_encrypt`. It reproduces the listserver string and round-trips its own output.
