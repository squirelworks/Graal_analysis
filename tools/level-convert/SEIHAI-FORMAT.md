# SEIHAI01 package

Date: 2026-11-01

Tag: **[inf]**. This is a future container for the Seihai toolchain. It is not a
historical Graal format. A 2.22 client does not read it, and it is not in a
client string table. Do not rename it to `.graal` or `.nw` and expect a client
to open it.

The level generations stop at GLEVNW01 and GRMAP001. This wrapper only holds
one of those files so a later tool can carry either without pretending the
bytes are a new board encoding.

## Layout

Text header, then the payload bytes exactly:

```
SEIHAI01
kind nw
bytes <N>
<N bytes>
```

`kind` is `nw` or `gmap`.

| kind | Payload |
| --- | --- |
| `nw` | One GLEVNW01 level, the on-disk text from `formats/glevnw01.txt`. |
| `gmap` | One GRMAP001 map, the text from `formats/gmap.md`. |

- The first line is the eight-character version `SEIHAI01`. A later container
  would use a new first line.
- `bytes` is the payload length in decimal. The payload starts on the byte
  after that line's newline. There is no compression and no extra checksum.
- A file shorter than the declared length is truncated. Bytes after the
  payload are rejected.
- `kind nw` must start with `GLEVNW01`. `kind gmap` must start with `GRMAP001`.

`tools/level-convert/convert.py` writes a level into `kind nw` (a `.graal` or
`.zelda` source is converted to GLEVNW01 first, because that text can carry
the NPC and chest sections a `.zelda` file does not have). It writes a
directory or a `.gmap` into `kind gmap`. Reading the package back yields the
same payload bytes.
