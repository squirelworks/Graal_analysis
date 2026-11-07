# Graphics and sound packs (2026-11-01)

The Game Assets inventory (`archive/game-assets-2026-11-01.md`) lists the
archives under `/[Grok/Graal/Game Assets` and leaves the large graphics and
sound packs, plus three small RARs, as filenames. This note opens those.
Nothing from them is committed: no archives, images, or audio.

Evidence is a full file list of each archive, plus header samples (image
width and height, MIDI text events, a few ID3 tags). No program in the
archives was run. Official host names that show up inside a few filenames
are left out.

## heads.7z

`Graphics/heads.7z` is a solid 7-zip archive, 219,893,893 bytes, one LZMA
block. Uncompressed it is 273,472,670 bytes: 34,369 files and 2 folders.
Image timestamps run from 1997 to 2014. The heavy years are 2003 (6,327
files), 2004 (5,549), 2014 (5,473), and 2005 (4,575).

| Where | Files | What |
| --- | ---: | --- |
| `heads/heads/` | 34,366 | the loose images, plus one `.htm` and one `.pe4` |
| `heads/heads.rar` | 1 | RAR5, 115,588,316 bytes |
| `heads/prewipeheads.zip` | 1 | zip, 13,150,942 bytes |
| `heads/teikaro-vamps-head.gif` | 1 | one GIF outside the inner folder |

Extensions across the whole archive:

| Extension | Count |
| --- | ---: |
| `.png` | 26,117 |
| `.gif` | 7,308 |
| `.mng` | 922 |
| `.bmp` | 15 |
| `.jpg` | 2 |
| `.tif` | 1 |
| `.htm` | 1 |
| `.pe4` | 1 |
| `.rar` | 1 |
| `.zip` | 1 |

That is 34,365 files with an image extension. Five of them are 1 to 8 bytes
(a newline, or an 8-byte stub). Another 65 image-extension files are under
512 bytes. Of the image-extension files, the median size is 2,972 bytes
(10th percentile 1,749, 90th percentile 6,200). The largest, 445,814 bytes,
is named `.png` and is a 24-bit BMP.

`heads/heads.rar` is the same 34,366 names as the loose `heads/heads/`
folder, path for path. It does not add images. `prewipeheads.zip` is an
older tree, timestamps 2008–2009, 3,655 files (15,893,816 bytes
uncompressed): 3,563 `.png`, 52 `.mng`, 36 `.gif`, 2 `.jpg`, and 2 files
with no extension. 1,215 of those basenames also appear in the loose tree.

Names are player or author stems. On the image-extension files, 2,485 are
exactly `head` plus digits (`head100.gif`, `head632.gif`), 11,156 end in
`head`, 19,713 contain `head` elsewhere in the stem, and 1,005 do not
contain that word. 1,945 stems exist as both a `.gif` and a `.png`. A few
names use characters outside ASCII; those bytes are left as the archive
stored them.

Dimensions are a sample, not a census. Eighteen files taken at even steps
through the image list: 14 are 32×560. A second set picked to cover png,
gif, mng, bmp, jpg, and tif is the same strip, with the exceptions below.
The opened GIFs are a single image each, so the 560-pixel height is the
picture itself.

| Opened file | What the header says |
| --- | --- |
| `(T)-Flame-Head.png`, `head100.gif`, `head61.gif`, `bluerose-darkhead1.png`, `zeroghead3.gif`, `cloud-kainhead.bmp`, `zoehead3.jpg`, `Hydromethadoxkat.tif`, `catboy-darkmage-head.mng`, `teikaro-vamps-head.gif` | 32×560. PNG and BMP samples are indexed colour (palette 7 to 256). The JPEG and the TIFF are the same width and height. GIF87a or GIF89a, one image. |
| `cloud-head9-edited.png` | 32×560, indexed, 29 palette entries |
| `kaybehhead1.mng` | MNG, 36×560 |
| `pink-wierdo-head.png` | truecolour PNG, 29×508 |
| `katie-head29.png` | indexed PNG, 32×557 |
| one other PNG in the even spread | indexed PNG, 32×559 |
| `blue-monkey-head.png` | truecolour PNG, 41×618 |
| `ellens-magic-head.png` | BMP, 265×560, 24-bit |
| `sniperrifleleft.gif` | GIF, 84×22, one image |

The `.htm` (26,859 bytes) and `.pe4` (21,675 bytes) were not treated as
images. The `.pe4` header is a binary record and embeds a local Windows
path; that path is omitted.

## Graal File Pack.7z

`Graphics/Graal File Pack.7z` is 124,044,350 bytes (7-zip, LZMA with BCJ,
two solid blocks). Uncompressed it is 267,976,494 bytes: 49,619 files and
200 folders. Timestamps run from 1996 to 2013, with 17,604 files dated 2003
and 10,103 dated 2004.

Three top-level folders:

| Folder | Files | Layout |
| --- | ---: | --- |
| `levels/` | 48,631 | the asset folders below |
| `sounds/` | 880 | flat: 876 `.wav`, 2 `.mid`, 1 `.au`, 1 `.txt` |
| `npcs/` | 108 | `.txt` only |

`levels/` children, by file count:

| Folder | Files | Main extensions |
| --- | ---: | --- |
| `levels/heads` | 12,258 | png 7,888, gif 3,826, mng 527, bmp 12 |
| `levels/webgifs` | 11,292 | png 6,366, gif 4,588, mng 262, bmp 31, mid 18, txt 12 |
| `levels/heads2` | 7,542 | png 5,451, gif 1,784, mng 307 |
| `levels/ganis` | 7,388 | gani 7,353, plus a handful of png, gif, wav, mng |
| `levels/images` | 3,076 | 98 files in the folder, 2,978 more in 180 subfolders |
| `levels/shields` | 2,199 | png 1,236, gif 816, mng 140 |
| `levels/swords` | 1,640 | png 880, gif 732, mng 23 |
| `levels/bodies` | 1,238 | png 983, gif 235, mng 16 |
| `levels/hats` | 835 | png 796, gif 35 |
| `levels/bodies2` | 784 | png 636, gif 132, mng 16 |
| `levels/bomys` | 156 | png 109, gani 37, gif 10 |
| `levels/midis` | 134 | wav 71, mid 61 |
| `levels/npcs` | 37 | txt 33, plus one `.nw`, one `.exe`, two images |
| `levels/backpals` | 31 | png 23, gif 5, pe4 2, txt 1 |
| `levels/baddies` | 10 | png |
| `levels/horses` | 8 | gif 4, png 4 |
| `levels/letters` | 3 | png 2, gif 1 |

Extension totals for the whole archive: png 26,601, gif 13,007, gani 7,391,
mng 1,334, wav 950, txt 157, mid 81, bmp 49, pe4 17, jpg 10, nw 6, graal 3,
mp3 2, bat 2, and one each of psd, au, cur, jbf, log, tif, tmp, exe, and a
file with no extension.

Headers that were opened match those extensions. `levels/ganis/1_mace_walking.gani`
starts with `GANI0001` and a `SPRITE` line. A head GIF and a head BMP in
this pack are 32×560, the same strip as `heads.7z`. A shield MNG is
191×68. A webgif PNG is 48×48 indexed. `levels/midis/007variation1.mid` is
standard MIDI, format 1, 8 tracks, 192 ticks per quarter note.
`sounds/44magnum.wav` is a RIFF WAVE file. `sounds/kookabur.au` is a
Sun/NeXT `.snd` file, 26,160 bytes, 8 kHz, mono, mu-law (the same name and
size the inventory note measured inside `SFX.rar`). The 23 PNGs under
`levels/backpals` are the same count `client-internals/client-assets.md`
gives for a client `backpals/` folder. The 18 PNG names and byte sizes from
`backpals.rar` (below) all sit in that folder as well.

`levels/npcs/npcs.exe` (51,200 bytes) was not run. The `.txt` files under
`npcs/` and `levels/npcs/` were not read. The three `.graal` files and six
`.nw` files were counted by extension only.

## MIDI.rar

`Sounds/MIDI.rar` is a solid RAR4 archive, 236,891,607 bytes. The outer
archive has 116 files under `MIDI/`:

| Extension | Entries | Notes |
| --- | ---: | --- |
| `.mid` | 105 | 94 distinct names. Eleven names are stored twice, once at `MIDI/` and once under `MIDI/MIDI_GraalForums_Player_Made/`, with the same byte size both times |
| `.zip` | 8 | see below |
| `.mp3` | 3 | `g2k2_medieval-banquet.mp3` (3,812,751 bytes), `g2k2_two-kings-in-hadinland.mp3` (13,643,569), `pwn00bzer.mp3` (1,318,313) |

No `.kar` in the outer archive. Folders: 60 files directly in `MIDI/`,
41 in `MIDI/Stef_Collection/`, 15 in the player-made subfolder.

The eight zips unpack to 157 files: 48 `.mid`, 108 `.mp3`, 1 `.ogg`. Still
no `.kar`. `stef##.zip` is the same 41 names as `Stef_Collection`.
`soundtrack.zip` adds seven mid names that are not in the outer rar
(`gmaintheme.mid`, `gBar.mid`, `gdive.mid`, `gskit.mid`, `gdance.mid`,
`gencounter.mid`, `intro.mid`). `Graal MP3s.zip` is 203,293,878 bytes and
holds 102 mp3s. The other zips are one or two audio files each
(`DEvolution.zip`, `mainmusic.zip`, `More_songs_I_made.zip`,
`music_I_made.zip`, `dgn1-theme.zip`). The ogg is `varia_dgn1-theme.ogg`,
beside an mp3 of the same stem. None of the 108 inner mp3 names match the
three loose mp3s.

Counting a duplicated name once, the unpacked set is 101 `.mid` names
(94 outer + 7 soundtrack), 111 `.mp3` names, and 1 `.ogg`.

Opened MIDI headers and text events (a sample, not every file):

| File | Header | Text that was read |
| --- | --- | --- |
| `andor_theme2.mid` | format 1, 18 tracks, 48 ticks | a text event in Shift-JIS: fullwidth "ETERNAL WIND" and a short Japanese phrase. Track names include drums, guitar, melody |
| `armashop.mid` | format 1, 17 tracks, 384 ticks | no text or track-name event in the parse |
| `gene1.mid` | format 0, 1 track, 24 ticks | "Created by Square Wave(R), Swiftlet Algorithms, Port Blair, India" |
| `GrlMainO.mid` | format 1, 7 tracks, 384 ticks | copyright text "© 1998, 2001 by Peach." Track names are Guitar, Bass, Pads, Drums, Pan Flute |
| `medieval.mid` | format 1, 2 tracks, 960 ticks | track name "Track 1" |
| `nw-mood-fahren_glade.mid` | format 1, 7 tracks, 120 ticks | sequence title "untitled"; copyright text names Daniel Garzone, 2000. Same header shape as the small New World rar below |
| `Rainy Night.mid` | format 1, 8 tracks, 480 ticks | track names Lead Guitar, Acoustic Guitar, Strings, Piano, Rain |
| `stef3.mid` | format 1, 6 tracks, 192 ticks | track names Drums, Track7, Track8, Track9, Track10 |
| `TORERO-2.MID` | format 1, 13 tracks, 384 ticks | standard MIDI header |
| `zzzero-town-1.mid` | format 1, 3 tracks, 384 ticks | marker text from a sequencer (`DEVICE=GENERAL.MDV`) |
| `gmaintheme.mid` (inside `soundtrack.zip`) | format 1, 15 tracks, 192 ticks | track name "-Fine Leather Midis-"; text names Michael Land |
| `intro.mid` (same zip) | format 1, 17 tracks, 120 ticks | sequence name "Rollercoaster of Death"; a text line names Curse of Monkey Island and a 1997 LucasArts copyright |
| `gdance.mid`, `gdive.mid`, `gencounter.mid`, `gskit.mid` | format 1, 11 tracks, 120 ticks | first track names MKBONES, MKDIVE, mkwdtick, MKEND, then instrument names |
| `gBar.mid` | format 1, 3 tracks, 192 ticks | track name "Jojo"; text credits Michael Land, Peter McConnell, and Clint Bajakian, with a 1991 LucasArts copyright line |

Opened mp3s: `aiq_crypt.mp3` has an ID3 title "The Crypt" and artist "Ph8".
`pwn00bzer.mp3` has ID3 year 2019, encoder "LAME in FL Studio 20", tempo
140, and no title frame. `[r]Evolution.mp3` has year 2007 and encoder
"LAME in FL Studio 7", and no title frame. `armashop.mp3`, `jfhappy.mp3`,
and `mainmusic.mp3` start with an MPEG frame and have no ID3 tag.

## pets.rar, backpals.rar, New World MIDI

These three are the small archives the inventory note only had as RAR
header names. Each was extracted.

**`pets.rar`** (2,382 bytes, RAR4, solid). One file:
`pets/22 - BTsddue.png`, 2,194 bytes, dated 2019-01-30. It is an 8-bit
RGBA PNG, 64×64.

**`backpals.rar`** (16,460 bytes, RAR4, solid). Eighteen PNGs under
`backpals/`, every one indexed colour with a 256-entry palette.
`afirebackpal.png` and `duskpal.png` are 1×1 (`duskpal.png` also has a
256-byte transparency chunk). The other sixteen are small strips, about
36–56 pixels wide and 26–49 tall, each with a 225-byte transparency chunk:
`dusk1`–`dusk8`, `sunrise1`–`sunrise4`, `sunset1`–`sunset4`. Timestamps
are 2001-11-26 for `afirebackpal` and `dusk1`–`dusk3`, and 2014-04-23 for
the rest.

**`MIDI [Graal New World].rar`** (16,982 bytes, RAR4, solid). Twenty-one
`.mid` files and ten `.ini` files under `MIDI [NW]/`. Every opened MIDI is
format 1 with 120 ticks per quarter note. Dates inside the archive are
2001-10-09.

| Folder | MIDIs |
| --- | --- |
| `Battle/` | 2 (`NW-Battle-Battledance`, `NW-Battle-Metalgans_Revenge`) |
| `Mood/` | 6 |
| `Over/` | 3 |
| `Town/` | 5 |
| `Other/` | 2 |
| archive root | 3 (`Faded5.mid`, `newworld intro.mid`, `NW-Under-Ominous_Shadow.mid`) |

Each of Battle, Mood, Over, Town, and Other also has `dc.filelocations.ini`
and `dc.fileversions.ini`. The location file lists the mids in that folder
with a value of `*`. The version file lists the same names with a value of
1. The root mids are not in those lists.

Sequence titles that are set: "Victory is Ours!" (`NW-Mood-Victory_Is_Ours.mid`,
which also names Johnathan Williams next to Daniel Garzone), "Sunlight of
Joy", "Valgoth", and "NewWorld Intro". The other opened files use the
sequence title "untitled", and the filename is the name. A copyright text
event on these files names Daniel Garzone, 2000. Further track names are
instruments (Piano, Strings, Trumpets, Guitar, Percussion). Sizes run from
2,203 bytes (`NW-Mood-Martyrs_Blood.mid`) to 24,139 bytes
(`NW-Battle-Metalgans_Revenge.mid`). `newworld intro.mid` is format 1 with
17 tracks.

## What was checked

Full archive listings: `heads.7z` (including the inner RAR5 and the prewipe
zip), `Graal File Pack.7z`, `MIDI.rar` (including all eight inner zips),
`pets.rar`, `backpals.rar`, and `MIDI [Graal New World].rar`.

Headers opened: about two dozen head images from `heads.7z` (the table
above), one gani, one wav, one au, one mid, one head gif, one head bmp, one
shield mng, and one webgif png from the file pack, the single pet PNG, all
18 backpal PNGs, all 21 New World mids, and the MIDI files and mp3s named
in the MIDI section. NPC text and `npcs.exe` were left alone.
