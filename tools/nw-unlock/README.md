# nw-unlock: New World bodies and shields for the 2.17.1, 2.22 and 2.31 clients

Background and evidence: [../../client-internals/newworld-mode-2x.md](../../client-internals/newworld-mode-2x.md).

`nwunlock.py` patches a copy of a 2.17.1, 2.22 or 2.31 Windows client so that, **only while the server has put
it in New World mode (id 177)**:

- a body is recoloured with 8 colour slots × 3 shades (palette entries *k*, *k* + 9, *k* + 18), as the 2001
  NewWorld betas do, instead of the classic 5 entries;
- SHIELD sprites use the GANI's rect as written, instead of rescaling it against a 38×20 sheet.

Without 177 the patched client runs the original code. Pure Python 3, no dependencies; everything is found by
byte pattern, and the tool refuses a file where a pattern is missing or ambiguous.

```
python3 nwunlock.py scan  Graal.exe
python3 nwunlock.py patch Graal.exe Graal-nw.exe [--colours] [--shield] [--bodycolors bodycolors.txt]
python3 test_nwunlock.py        # self-test on a synthetic PE
```

With neither `--colours` nor `--shield` both are applied. `--bodycolors` takes the 57-line `bodycolors.txt`
shipped with the NewWorld betas; without it the shades are 1.0, 0.9 and 0.8 of the client's own colours.

What it changes: one new code section (`.nwu`, under 400 bytes, shade tables included) and two jumps into it,
one at the body recolour loop and one after the SHIELD name compare. It does not touch the stored mode flag.

Notes:
- The patched exe's tamper-check value (PLI 39) changes. Use it on your own lab server only.
- The server must send COLORS as 8 bytes (player prop 13, NPC prop 19) once 177 is sent, and serve NW bodies,
  shields and GANIs. In the lab, `../probe/gen5probe.py` can inject both.
- Never commit a client binary, patched or not.
