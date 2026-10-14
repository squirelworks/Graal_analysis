# gif2mng

GIF to PNG or MNG. Banner date 2004-06-03. PE32, base 0x400000, entry 0x416558. Units `UGif` and `UMNG`, zlib 1.1.2.

- One frame → PNG.
- Two or more frames → MNG.
- `-b` snaps the palette to the seven Graal body slots and forces transparent index 2.

The converter does not invent a second palette; it rewrites the existing one to the body slots.
