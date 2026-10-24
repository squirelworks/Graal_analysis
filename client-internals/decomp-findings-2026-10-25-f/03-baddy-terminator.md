# Baddy section: only a first byte >= 0x80 ends it

Two levels have a baddy at x = 0 (one at (0, 0), one at (0, 62) in a row of 16 baddies spaced 4 tiles apart ending with x = 60). `level-binary-client.md` says the section ends at a first byte of 0x80 or more; that is right. The reference decoder `formats/grv1-decoder/grv1.py` also stops at x = 0, which loses the x = 0 baddy and any after it (3 baddies in these two files) and then reads the rest of the baddy bytes as NPC lines, so NPC counts are wrong in those two files (26 against 25, 12 against 10 on the NPC count).

Corpus baddy totals: 902 baddies in 99 levels; types 0 to 9 all occur. A record's three bytes can be 0x0A or 0x00; the reader must look for the line end only after the first three bytes.
