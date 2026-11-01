# Game Assets folder (2026-11-01)

Inventory of the owner's Google Drive folder "Game Assets"
(https://drive.google.com/drive/folders/1TGSRLwXwRpSPKG9KFWvuMYGpovM_XJGD),
created 2026-11-01. Nothing from the folder is committed here: no zips, images,
sounds, levels, or website copies.

Evidence is a static read of Drive listings, plus headers from a few small
archives. Multi-megabyte world trees and the multi-hundred-megabyte packs were
not downloaded. No binary was run. Official host names that appear inside a
couple of old pages are left out of this note.

The folder has three children:

| Child | What it is |
| --- | --- |
| Game Assets | `Graphics/` and `Sounds/` |
| Playerworlds | 35 folders: 33 named worlds, plus archived servers and level dumps |
| Websites | 15 website archives and a folder of 12 screenshots |

## Sounds

`Sounds/` is three archives, not loose files.

| Archive | Size | Opened |
| --- | --- | --- |
| `SFX.rar` | 1.2 MB | yes |
| `MIDI [Graal New World].rar` | 17 KB | header only |
| `MIDI.rar` | 227 MB | no |

`SFX.rar` (files dated 2001–2003) lists 126 `.wav`, 2 `.mid`, and 1 `.au`,
under an `SFX/` directory. Uncompressed wav sizes run from 794 bytes to 63 KB
(median about 13 KB): 16 under 5 KB, 64 from 5 to 20 KB, 35 from 20 to 50 KB,
11 at 50 KB or more. Names are short action words (`axe.wav`, `bomb.wav`,
`chest.wav`, `closedoor.wav`) plus numbered instrument takes (`flute1`–`flute8`,
`guitar1`–`guitar8`, `drums1`–`drums4`).

Opened samples: `axe.wav` is a 1,506-byte RIFF WAVE file; `sandbox.mid` starts
with the standard MIDI header; `kookabur.au` starts with the Sun audio header
(26 KB).

The 17 KB New World MIDI archive is a RAR. Its header names
`MIDI [NW]\Other\dc.filelocations.ini`. The rest of that archive was not
listed. The 227 MB `MIDI.rar` was not opened.

## Graphics

`Graphics/` is 27 archives (24 RAR, 3 are 7z or a second RAR part). Names
follow the usual client folders: `backpals`, `Baddies`, `body`, `bomb1`,
`bomb2`, `Bomy`, `Fonts`, `Gani`, `GUI`, `hats`, `heads`, `horses`, `letters`,
`pets`, `shields`, `sprites`, `state`, `swords`, `Tiles`, `Wings`, plus
loading screens, emotion images, computer backgrounds, and templates. Sizes
run from `pets.rar` at 2 KB up to `heads.7z` at 210 MB and `Graal File Pack.7z`
at 118 MB. Those two, and `Graal File Pack.part2.rar` (25 MB), were not
opened.

Opened or header-checked:

| Archive | What was checked |
| --- | --- |
| `Gani.rar` (1.5 MB) | full listing |
| `Tiles.rar` (572 KB) | full listing, two PNGs measured |
| `SFX.rar` | see Sounds |
| `pets.rar` (2 KB) | RAR header names one PNG |
| `backpals.rar` (16 KB) | RAR header names PNG palettes |

`Gani.rar` is one flat `Gani/` directory, 2,646 files, about 16 MB
uncompressed: 2,464 `.gani`, 123 `.png`, 54 `.gif`, 2 `.mng`, 2 `.zip`, and
one file with no extension. Gani sizes run from 20 bytes to 55 KB (median
about 7 KB). Names are lowercase effect and pose stems
(`arrow.gani`, `akuma-effect-charme.gani`, `amsel_sten-walk.gani`), often
`world_or_author` plus `idle` / `walk` / `fire`.

Two text shapes showed up. The smallest files that were opened
(`era_parksign.gani` and five siblings, all under 200 bytes) start with
`GANI0001`, then `SPRITE`, `SINGLEDIRECTION` or `DEFAULTHEAD` / `DEFAULTBODY`,
then `ANI` / `ANIEND`. A mid-size sample was mixed: some of those also start
with `GANI0001`, and others (`arrow.gani`, `axe2.gani`) start at `SPRITE`
with no version line. This note does not claim a ratio for all 2,464 files.

`Tiles.rar` holds five images: `pics1.png` (162 KB), `pics1format.png`,
`1IMp0kk.png`, `angel_tile-template.png`, and `pics1d_legion.gif` (231 KB).
The two PNGs that were measured are both 512 pixels tall and wider than they
are a square tile sheet: `pics1.png` is 1856×512, `angel_tile-template.png`
is 1952×512. That `pics1.png` is not the 2048×512 client sheet described in
`client-internals/client-assets.md`.

`pets.rar` names `pets\22 - BTsddue.png`. `backpals.rar` names
`backpals\afirebackpal.png` and `backpals\dusk1.png`. The same palette names
also sit inside the level dump below, as PNGs of about 1–10 KB. The other
graphics archives were not opened; their formats are only the archive names.

## Levels

Loose level files are not at the top of Playerworlds. They sit inside RAR
dumps.

`# Level Dumps #` has two folders. "Graal - Level Dumps" is 20 small RARs
(hundreds of bytes up to `alkarenhyralt_levels.rar` at 669 KB), named for a
place or a date (`9-06-2000.rar`, `elftown.rar`, `partyhall.rar`). "Graal
New World - Level Dumps" is 17 RARs (`3dcube.rar` at 1 KB through
`Agret Levels and scripts.rar` at 2 MB). Only `alkarenhyralt_levels.rar` was
unpacked.

That dump is 82 files: 34 `.nw`, 16 `.graal`, 20 `.png`, 7 `.gif`, plus one
each of `.txt`, `.zip`, `.ini`, `.bmp`, and `.log`. Of the level files that
extracted:

| Magic | Where |
| --- | --- |
| `GLEVNW01` | 29 `.nw` files |
| `GR-V1.03` | 16 `.graal` files |
| `GR-V1.03` | 5 `.nw` files (the extension is not the magic) |

An opened `GLEVNW01` file (`ak_aa-01.nw`, and a police `.nw` in the same dump)
is text: the magic, then 64 `BOARD` rows, then `LINK`, `SIGN`, and `NPC` /
`NPCEND` blocks. The police file has 4 links, 1 sign, and 6 NPC blocks.
`formats/grv1-decoder` read `asas.graal` as `GR-V1.03` with no links, baddies,
NPCs, chests, or signs, and `andormine.graal` (from the Andor archive below)
as `GR-V1.03` with 2 links and 40 NPCs. No `Z3-V1` magic turned up in the
files that were opened. Sign text and NPC scripts were not copied.

## Playerworlds

The 33 named world folders, and the ones opened under archived servers, are
dated RAR (sometimes 7z or zip) packs, not loose trees. Examples that were
listed but not unpacked: Enigma (five RARs, 2002–2005, one of them
"levelsonly"), Doomsday (five RARs, 2001–2003, up to 28 MB), Era (eight
archives, including a 90 MB and a 164 MB levels-and-images pack), Classic
(eleven RARs, 2000–2009, plus a 524 KB iPhone-overworld RAR), Zelda Online
(three RARs: `Zelda Online.rar` 49 KB, `Zelda.rar` 948 KB, `zolevels.rar`
49 KB), Unix Graal (one 15 MB RAR). `# Archived Servers #` is 87 folders in
one listing (no further page), from an offline-games folder through Zerati.
The one archived folder that was opened (Chaos Continuum) is a single RAR.
The offline-games folder is 14 RARs, one of them 265 MB. Those large packs
were not downloaded.

What a pack actually contains depends on which archive it is. Three were
listed all the way through:

**Andor, 21 July 2002** (`Andor [2002-07-21].rar`, 1.6 MB, 532 files). One
flat `Andor/` directory holds 409 `.graal` and 93 `.nw` (502 levels), plus
`bocotest.gmap`, one `.gani` is outside that directory, three `.mng`, one
`.mid` (46 KB), one `.wav`, and PNGs. There is no separate NPC or weapons
tree; a level named `andor_npcarea.graal` is still a level file. Screenshots
and a `Takino/` set of ghost PNGs sit beside the world. `bocotest.gmap` is
text `GRMAP001`, `WIDTH 3`, `HEIGHT 3`, `GENERATED` pointing at an `.nw`
name, then the usual generator keys (`GENSEED`, `GENBASE`,
`GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`,
`MAPIMG`) and `HEIGHTMAP` / `RANDOMSEEDS` blocks. `andormine.graal` is
`GR-V1.03`. `ak_aa-01.nw` is `GLEVNW01` with 64 `BOARD` rows and one NPC
block.

**Era without levels** (`Era_No_Levels_5_19_2019.rar`, 108 KB, 42 files).
Three script folders, all `.txt`: `weapons/` (command, options, and event
scripts), `NPCS/` (control, staff, shop, SQL), and `classes/` (`func_*.txt`).
No levels, gmaps, or ganis in this particular archive. A separate Era backup
on Drive is 90 MB and was not opened, so this file is not the whole world.

**Graal 2002 client zip** (`graal2002v22.zip`, 960 KB, dated December 2001).
Nine `GRMAP001` files under `levels/maps/` (`main` 40×40, `caverns` 16×16,
`mines` 2×2, and six others), plus `loadgmaps.txt` naming those nine, plus
`Graal_2002v22.exe` (1.7 MB). The executable was not run. This zip has maps,
not the level bodies.

Other shapes seen only as listings: Zone is `sounds.rar`, an assets RAR, an
iPhone RAR, and a `Zone Files` folder of two image RARs, `zone_ganis.rar`
(298 KB), `Zone_GMAP.rar` (2 KB), and `zone_gui.rar`. The gmap RAR's header
names `zone_ad.gmap` and `zone_platform.gmap`; it was not extracted. Graal2001
is several multi-megabyte level archives plus a 9 KB `graal2001classes.zip`
and two loose text files (a 427-line GS1 bomy script and a one-page 2001
letter; neither is copied). Its New World subfolder also has `music1.mid`
(6 KB, not opened), `npccontrol.txt`, `npcserverdoc.txt`, `RemoteControl-NW.exe`
(not run), and one JPEG. The NPC-server note describes a program that logs
into the 2001 game server like a player, loads levels and NPCs, and runs
scripts on a tenth-of-a-second loop, with a `//#CLIENTSIDE` split for drawing
and music. The NPC-control note is five lines about who may connect; the
host it names is omitted here.

## Old websites

`Websites/` is 15 RARs plus `Websites Screenshots/` (12 PNGs, 65 KB to 2.4 MB).
The screenshots were not opened. From the filenames they are captures of
Armageddon (2010), Coasta De Agua (2000), Elven Lands (2001), a 2001 intro
page and main page, a 2019 Adventure page, a 2010 Reborn page, two topsite
listings, a fansite before it changed hands, a holiday news page, and a
ministry-themed page.

Archives that were opened:

**Doomsday, October 2001** (98 KB, 13 files). Four HTML pages, all titled
"Welcome to Doomsday Online", plus a start-message RTF with the same title,
event and map images, and a map zip. The pages are a mini-site: an index
that says a newer Doomsday is in progress, a download page that tells the
reader to unzip a map into the maps folder, a short events list, and a
numbered rules list. The start message says this mini-site stands in for a
plain start message.

**Game Boy demo site, snapshot dated 22 September 1999** (110 KB, 28 files).
Titles that were read: "Graal Gameboy", "Graal Gameboy - Downloads",
"Graal Gameboy - Email List", "Graal Gameboy - News", "Graal Gameboy -
Screen Shots", "Graal Gameboy - Production Team", and a tiny "Sorry" page.
Images are a logo, a cartridge picture, and numbered screenshots. The pages
document the demo: news, downloads, how to order, the team, and pictures.

**Community site, 5 January 1999** (57 KB). The front page is titled
"Graal-Online". Other real pages are "Graal-Online: BBS", "Graal-Online:
Chat", and "Galen's Weak Apology". Many companion files are Internet Archive
shells titled "Internet Archive Wayback Machine", or a 404 page, so this
rar is a saved mirror of the front page plus BBS and chat, not a full site
copy. One chat page contains an address; it is not repeated here.

**November 2001 site source** (634 KB, 105 files: 45 `.php`, 28 `.inc`,
22 `.htm`, plus shtml/html). Opened pages have no useful `<title>` (the
header file's title is the PHP variable for the site name). From the file
names the tree is accounts (signup, age check, conduct, license), a guild
control panel, a shop, a download page, and admin. `index.php` is a story
list. One account page names an official host; that host is not written
here. A 5 MB file saved as `.htm` is a classic remote-control log and was
not read. Files whose names are an IP ban list and an fstab note were not
opened.

Header-only, not extracted: a 20 KB Chaos Continuum site from November 1999
names `index1.html` and `download_gif.html`; a 24 KB ODiUM v4 site from
March 2002 names `index.html.html` (the extension is doubled in the archive).

Not opened, filename and size only: a classic-community flash intro (30 KB),
that community's forums dump (52 MB), a Dragon world site-and-server archive
(18 MB, 2014–2017), a guild vault site (177 KB, 2004), a 2023 construction
site (5.7 MB), a Game Boy site is the one opened above, a kingdoms library
site (4.8 MB, 1998–2006), an NPC website (59 MB, 2003), a forum SQL dump
(225 KB, 2006), and a 2019 developer-site archive (3.1 MB).

## Verified against filenames only

Checked by opening bytes or a full archive listing: `SFX.rar`, `Gani.rar`,
`Tiles.rar` (two PNG sizes), the alkaren level dump, the Andor 2002 RAR
(including one gmap and two level headers), the Era script-only RAR, the
2002 gmap zip, the Doomsday, Game Boy, 1999 community, and November 2001
website archives (titles and file names, not full page text), plus
`npcserverdoc.txt` and `npccontrol.txt`.

Checked only as a RAR header name: `pets.rar`, `backpals.rar`, the small
New World MIDI rar, `Zone_GMAP.rar`, the Chaos Continuum site, the ODiUM
site.

Seen as Drive names and sizes only: the other graphics packs (including
`heads.7z` and both file-pack parts), `MIDI.rar`, the large world and
archived-server RARs, the Zelda Online RARs, the level-dump RARs other than
alkaren, the 12 website screenshots, and the website RARs listed as not
opened above.
