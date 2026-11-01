# gif2mng

GIF to PNG or MNG. Banner date 2004-06-03. PE32, base 0x400000, entry 0x416558. Units `UGif` and `UMNG`, zlib 1.1.2.

- One frame → PNG.
- Two or more frames → MNG.
- `-b` snaps the palette to the seven Graal body slots and forces transparent index 2.

The converter does not invent a second palette; it rewrites the existing one to the body slots.

`level-tools-gaps/gif2mng.py` writes the frame rule above on synthetic frames. The seven slot RGB values are not listed here, so `-b` forces transparent index 2 and leaves the existing RGB entries unchanged. TERM's delay fields are not listed here either, so the writer does not emit TERM.
