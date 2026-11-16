# Official GS2 segment-3 strings: Latin-1 (one sample + client text path)

Date: 2026-11-16. Tags: **[cap]** for the official-body string table; **[file]** for shipped language packs; **[bin]** for focus-client text APIs.

Leads-only. No third-party code. Bodies, keys and names stay private.

## Official segment-3 bytes

Across the **19** official 6.113-era bodies, high bytes (`0x80`–`0xFF`) appear in segment 3 of **1 / 19** bodies. **[cap]**

That sample stores the French word *Français* as `Fran` + byte **`0xE7`** + `ais`. Under Latin-1 / Windows-1252 letter mapping, `0xE7` is **ç**. A UTF-8 encoding of the same character would be the two-byte sequence `C3 A7`, which is **not** what the table holds. **[cap]**

So for this non-ASCII string, official bytecode uses **single-byte Latin-1-compatible** storage, not UTF-8. The sample is sparse (one string) but decisive against UTF-8 for that hit. Do not over-generalise beyond the held hit until more non-ASCII official strings appear. **[cap]**

## Classic UI language packs (supporting)

Delphi-era French language packs on hand store Western European letters as single high bytes (for example `0xE9` for é) with **no** plausible UTF-8 multi-byte sequences. The C1 range `0x80`–`0x9F` appears mainly as **`0x92`** (Windows-1252 curly apostrophe). For letters such as ç / é, CP1252 and ISO-8859-1 agree. **[file]**

Torque-era French stubs checked here are ASCII-only and add no non-ASCII evidence. **[file]**

## Focus client text path (5.00r7 / 6.03r7)

Stock Windows **5.00r7** and unpacked **6.03r7** images sit on an **ANSI / ACP** text path: ANSI GDI text APIs and ACP query helpers are present; no `UTF-8` / `UTF8` literal was found in the scanned 5.00r7 engine strings. **[bin]**

On a Western European Windows ACP (1252), high bytes in the Latin-1 letter range draw as the expected glyphs — the same bytes official bytecode stores for *Français*. **[bin][inf]**

## Still open

- Live on-screen fixture: inject / play a GS2 `showtext` (or sign) with segment-3 byte `0xE7` on **5.00r7** and a **6.x** build and confirm the glyph. **[lab]**
- Exact code-page argument on every wide-char conversion along the GS2 string→draw path. **[bin]**
- Non-Western ACP installs (out of Western focus; do not assume ACP == Latin-1 globally).
