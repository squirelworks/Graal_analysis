# arrays.dat, arrays2.dat and the .sig files

Date: 2026-10-21

From client 2.05 rev 2 (traced), clients 2.17, 2.22 and 2.31 (disassembly of the load and check path), and the files in a 2.22 install. Tags: **[2.05]** · **[2.17]** · **[2.22]** · **[2.31]** · **[test]** · **[inf]** inferred.

## Summary

| File | Holds | Signed | Checked by |
|------|-------|--------|------------|
| `arrays.dat` | 25 built-in tile and sprite tables | no | nobody. The client quits with "File not found" if it is missing. **[2.05]** |
| `arrays2.dat` | Listserver hosts, port and URLs, one per line | `arrays2.sig` | 2.22 (traced), 2.17 and 2.31 (same code) |
| `graal.sig` | Signature over the client exe itself | | 2.22 (traced), 2.17 and 2.31 (same code) |

2.05 has no signature check at all. It doesn't reference `arrays2.dat`, `graal.sig` or `arrays2.sig`. **[2.05]**

## arrays.dat

Big-endian 32-bit integers. Each array starts with a header word: **[2.05]**

```
header = (kind << 16) | count
kind 0: count int32 values follow
kind 1: count nested arrays follow (each with its own header)
```

The client reads exactly 25 arrays in a fixed order into 25 globals at startup. The 2.22 file (11,500 bytes) parses to exactly 25 arrays with nothing left over. **[test]**

| # | Shape | Content (where usage was traced) |
|---|-------|----------------------------------|
| 0 | 934 ints, max 4089 | Tile ids. With array 1, the legacy walkability test: in the old tile mode, a tile counts as blocking unless it is in array 0 or array 1. **[2.05]** |
| 1 | 116 ints | Tile ids, second list for that test |
| 2 | 133 ints | Tile ids (use not traced) |
| 3 | 76 ints | Tile ids (use not traced) |
| 4 | 40 ints | Tile ids (use not traced) |
| 5, 6 | 4 ints each | Single 2×2 tile blocks (708–711, 724–727) (use not traced) |
| 7 | 79 ints | Tile ids. The legacy tile-type lookup maps a tile's position in this list to 4 classes (positions 0–11, 12–19, 20–62, 63+). The newer tile-type path returns types 6–9 for the same 4 classes. **[2.05]** |
| 8 | 4 lists, one per facing | Ledge tiles (tile type 21): a ledge jump needs the tile to be in the list for the player's facing. See `client-internals/ledges-push-pull.md` **[2.05]** |
| 9–12, 14, 15 | small nested lists of 2×2 tile groups | Used by level-object code (9 to 12: cut and lift, see Seihai's `cut-and-lift.md`) |
| 16 | 2 × 2×2 blocks | Stone blocks: entry 0 pushable, entry 1 pullable. See `client-internals/ledges-push-pull.md` **[2.05]** |
| 13 | 4 ints | One 2×2 tile block, used with array 14 |
| 17 | 124 × 4 | Packed records used by the horse object **[2.05]** |
| 18 | nested | Use not traced |
| 19 | nested | Used by the leap object **[2.05]** |
| 20, 22, 23 | nested | Used by the baddy AI object **[2.05]** |
| 21 | 4 × 4 | Packed values (use not traced in detail) |
| 24 | 356 ints, packed | Used by the item, bomb and extras objects **[2.05]** |

All tile ids index the 4096-tile `pics1` sheet. Mapping every table to a gameplay rule needs more tracing, and isn't needed to load the file.

## arrays2.dat

Plain text, CRLF lines. The 2.22 client needs at least 5 lines. Lines are numbered from 0. **[2.22]**

| Line | Use |
|------|-----|
| 0 | Main listserver host |
| 1 | Listserver port |
| 2 | Web host, joined into a URL template **[inf]** |
| 3 | Registration page URL |
| 4 | Translation service URL |
| 5, 6 | Fallback listserver hosts (optional) |

The Graal Reborn copy points at `listserver.graal.in` port 14922, with `listserver.graal.cc` and `listserver.graalonline.biz` as fallbacks. **[test]**

## The signatures

Both `.sig` files are 128 bytes, the size of an RSA-1024 signature. **[test]** The check runs at startup: **[2.22]**

1. The client builds a 1024-bit RSA public key from an obfuscated hex string assembled one character at a time in code. Each decoded byte is `not(b) - 10`.
2. It verifies `graal.sig` against **its own exe file**, then `arrays2.sig` against `arrays2.dat`. The verifier is an RSA crypto component configured with a SHA-1 signing digest and a PKCS#1 encryption scheme. **[inf]** That's from the component's class and property names. No signature has been verified yet, so the exact algorithm is not confirmed.
3. On any failure it shows "The Graal execution file is corrupted. Please check for viruses or other programs that manipulate…" and exits.

2.17, 2.22 and 2.31 embed the same two obfuscated key strings and the same error text. **[2.17]** **[2.22]** **[2.31]**

Open: checking the shipped signatures by hand against the decoded key with exponents 3, 17 and 65537 did not reproduce PKCS#1 padding, so the key encoding (exponent, byte order, or which of the two strings is used) is not pinned down yet.

### The Graal Reborn 2.22 exe has the check disabled

The Reborn `Graal_222.exe` was rebuilt on the same day its `arrays2.dat` was edited. In its RSA verify routine, the three conditional branches that raise the verify error are rewritten as unconditional jumps, so verification always passes. The 2.17 and 2.31 exes have the original conditional branches. **[2.22]** **[2.17]** **[2.31]**

That's why the Reborn client runs with a modified `arrays2.dat` and an old `arrays2.sig`, and with a modified exe and the old `graal.sig`. An unpatched 2.17, 2.22 or 2.31 client would refuse both. **[inf]**

Practical upshot: pointing an unpatched 2.17+ client at another listserver means patching the exe, as Reborn did. Editing `arrays2.dat` alone fails the signature. 2.05 has no such file. Its listserver host is the DES-hidden string in `client-internals/saved-passwords.md`.
