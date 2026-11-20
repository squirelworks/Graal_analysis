# File reads for Appendix E, thirteenth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[file]** (content hashes and RIFF headers of the held sound files,
and a search of the held folders and archives on the Mirae lab; no client run, no network).
Covers App. E#325 (the count) and E#101.

## The WAV census reconciled (E#325)

**Where the 255 came from.** The survey behind
[sound-files-6x.md](sound-files-6x.md) (its scripts and saved output, dated 2026-11-13) still
exists on the lab. Re-running its summary on that saved output gives exactly 255, but that figure
is not a content count and is not limited to 4.x to 6.x:

- it is unique by lower-cased file name and byte size;
- it covers every era the survey scanned: 2,836 `.wav` files, pre-4.x clients included.

**The gap.** `sounds/steps2.wav` (26,468 bytes) starts with an ID3 tag and has no RIFF/WAVE
header. It is in the 255, but the format and channel tallies only see files with a `fmt ` chunk,
so it is in neither. 255 = 254 RIFF files + 1 non-RIFF file. No other file was unreadable.

**Recount by content hash (SHA-256), over the survey's own file list:**

| Scope | Files | Unique by name and size | Unique by content | PCM | MPEG-in-WAV | IMA ADPCM | A-law | non-RIFF | mono | stereo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All eras (the survey's 255) | 2,836 | 255 | 233 | 203 | 20 | 6 | 3 | 1 | 194 | 38 |
| 4.x to 6.x sets only | 369 | 126 | 103 | 73 | 20 | 6 | 3 | 1 | 67 | 35 |

- **MPEG-in-WAV falls from 43 to 20.** In 5.00r7's `sounds` folder the piano notes are mostly the
  same bytes under up to three names (for example `eye_piano-c0`, `-c1` and `-c2`).
- **Name and size is not a safe key either way.** All-era PCM is 203 by content but 202 by name
  and size: three Linux 3.04 sounds (`bomb.wav`, `frog.wav`, `stonemove.wav`) exist as two
  different contents with the same name and size.
- Some survey files had moved since and were hashed through a copy with the same name and size.
  For 4.x to 6.x every such match was a single content; only those three Linux 3.04 files are
  ambiguous, which moves the all-era row by at most 3.
- The update packages hold no WAV payload on disk; their `FILE` lines add names, not files.

Distinct contents per 4.x to 6.x set (the sets overlap, so these do not add up to 103):

| Set | Distinct WAVs |
| --- | ---: |
| 4.04r2, 4.20r6, 4.20r8 (Windows, Mac, Linux) | 9 |
| 5.00r7 Windows | 83 |
| 5.12 and 5.2.4r3 Windows | 1 |
| 5.x Mac | 1 |
| 6.00r2 | 10 |
| 6.1.1.3 archive copy | 52 |
| 6.1.1.3 installed copy (as surveyed) | 68 |

**The installed 6.1.1.3 copy has grown since.** Its `sounds` folder now holds 114 WAVs against the
survey's 68; a recount of today's disk over the same 4.x to 6.x sets finds 151 distinct contents,
the extra ones all 6.1.1.3 sounds added after 2026-11-13. The dated survey-scope figure (103) is
the one the manual cites.

## The earlier type-0 mask export (E#101)

**Not found.** No mask export and no script that produced "3,195 non-blocking and 682 blocking
tiles" exists in any held folder or archive.

- Searched: every lab, scratch, research and intake folder and repository checkout on the Mirae
  lab, the older working-paper folders, the installed client, the dated archive drive, and the
  GwenTea2 intake (reviewed notes and the file indexes of the backup tarballs).
- By file name: mask, nowall, walk or walkable, tiletype, tiledef, collision, blocking, type0.
- By content: text files holding both 3195 (or 3,195) and 682.
- Every hit is the same sentence, in copies of `formats/tile-walk.md`, the manual's App. E and
  `docs/book/04-where-the-notes-disagree.md`. The sentence first appears in the commit "Expand
  tile walk and collision notes with observed rules" (2026-10-14), which adds no data file or
  script with it. The `ash/` and Ash notes hold no tile mask or allow list.

**The counts match none of the possible inputs.**

| Input | What it gives |
| --- | --- |
| The exact 11,500-byte `arrays.dat` (→ manual §3.5.3.1) | list 0 = 934, list 1 = 116, union 1,035 |
| The 4,096-entry `Type0` table of the GServer-v2 fork's tile types | 1,035 ids below type 20 and 3,061 at 20 or above |
| The `Type1` table of the same fork | 2,371 and 1,725, the type 1 and 2 grid already in `formats/tile-walk.md` |
| The 2.22 `pics1.png` (2048 x 512, 4,096 tiles) by pixels | 58 single-colour tiles, no fully transparent tile; nothing gives 3,877 or 3,195 |

3,195 + 682 = 3,877, which is 219 short of 4,096, and no inspected table or sheet leaves out 219
tiles. The figure has no recoverable source and is retired.

**Side finding.** The 1,035-value union of the `arrays.dat` lists equals the number of `Type0` ids
below 20 in the GServer-v2 fork's table. Only the counts were compared; whether the two sets
hold the same ids was not checked.
