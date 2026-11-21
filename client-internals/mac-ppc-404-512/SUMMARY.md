# Mac PPC 4.04r2 / 4.20r6 / 5.12: step rule and PLO sets (static read, 2026-11-13)

Address-free summary. Static disassembly only; no client was run.

## Gen-5 frame cipher step rule

Every routine read has the same shape, in both directions (encode and decode):
- type 2 (raw): steps = min((len + 3) >> 2, 12); a partial last group is XORed.
- types 4 (zlib) and 6 (bz2): steps = min(len >> 2, 4), which is **round down**; a partial last group is left as is.
- LCG `it = it * 0x08088405 + key`, XOR with the iterator's little-endian bytes.
- Compression choice: plaintext > 4095 → bz2, > 47 → zlib, else raw.

| Build | Compressed-body step | Source |
|---|---|---|
| Mac 4.20r6 (G3D27076) | **round down**, encode and decode | read directly |
| Windows 4.04r2 (G3D17026) | **not read**: no genuine Windows 4.04r2 engine was available for this read. The installer labelled "4.04r2 Windows" is byte-identical to the 4.20r8 Windows exe (Thinstall-packed). The nearest evidence is **round down**: Linux 4.04r2 (same release) and Windows 4.20r8 `GraalEngine.dll` both round down in encode and decode. | proxy |
| Mac 4.04r2, Mac 5.12 | round down (re-confirmed) | read directly |
| Windows 5.12 | round down (calibration; matches seihai) | read directly |

The two rules differ only for a compressed body under 16 bytes with len % 4 != 0. The plaintext compression threshold does not by itself establish compressed-body length or whether traffic exercises that difference. This static read is not a discriminating capture or runtime-acceptance result.

The original report's recommendation to update the consumer's Mac `gen5_round_down` rows is historical implementation advice, not evidence that current code still omits those rows. Check current profiles before repeating that work. The exact Windows 4.04r2 engine's static rule remains unproven here; sibling results do not replace that read.

## PLO ids handled (server → client)

- **Mac 4.04r2 (G3D18026), 97 ids:** 0–25, 27–40, 42, 43, 45–49, 67, 68, 69, 74, 75, 82, 84, 100, 101, 102, 104, 105, 106, 131–134, 150, 151, 153–156, 165, 166, 168–176, 178–187, 189, 190, 191, 193, 194, 195. One switch (bound 195); 100 is a switch case; there is no 107 or 108.
- **Mac 4.20r6 (G3D27076), 99 ids:** Mac 4.04r2 + 107, 108 (100 and 108 are tested before a 97-case switch). This equals seihai's existing row.
- **Mac 5.12 (G3D15097), 101 ids:** Mac 4.20r6 + 140, 197 (a 99-case switch with bound 197, plus 100 and 108 tested before it).

Differences from the Windows sets that seihai borrows today:
- Mac 4.04r2 vs Windows 4.04r2 (98): Mac **lacks 41**.
- Mac 5.12 vs Windows 5.12 (100): Mac **lacks 41** and **adds 100 and 108**.

No Windows switch was re-read in this study: the intended Windows 4.04r2 input was unavailable for that read, and Windows 5.12 stayed as the consumer recorded it. This is a dated study boundary, not a current inventory of all retained inputs.
