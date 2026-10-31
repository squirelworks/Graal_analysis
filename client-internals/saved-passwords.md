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

## String format (48 characters)

Encrypt:
1. Truncate the plaintext to 23 bytes.
2. Build 24 bytes: `len`, the plaintext, then random padding bytes.
3. Encrypt as three DES blocks.
4. Write each of the 24 bytes as two characters: `(b >> 4) + 0x20`, `(b & 0x0F) + 0x20`.

Decrypt reverses this. Input shorter than 48 characters gives an empty string. The first decrypted byte is the length, and values of 0 or ≥ 24 give an empty string. **[2.05]**

Because the padding is random, the same password encrypts to a different string each time.

## Other uses of the same cipher

- The hidden listserver host: the server list frame builds a different 8-byte key and a 48-character ciphertext one character at a time. It decrypts to `<list-host-classic>`, port `14921`. **[2.05]** **[test]**
- The web-level cache uses the same DES routine with per-block keys. See `formats/gwebl001-cache.md`.

## Tool

`tools/file-formats/graaldes.py` (pure Python):

```
python3 graaldes.py '<48-char value>'
```

It implements `GraalDES` (block cipher), `string_decrypt` and `string_encrypt`. It reproduces the listserver string and round-trips its own output.
