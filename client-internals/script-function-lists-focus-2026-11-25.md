# `-listscriptfunctions` on the focus clients (G066, 2026-11-25)

Each focus client was started once under Wine with `-listscriptfunctions`, in the loopback-only lab VM with no servers running. The lists stay in the lab; this note records what the switch does, the format, the counts and the differences between builds. **[lab]**

| Build | Client |
|---|---|
| 4.20r8 | `Graal4.exe` with the stock engine |
| 5.00r7 | unpacked `Graal.exe`, the lab's licence-check-patched engine, signed licence in place |
| 5.12 | packed `Graal.exe` |
| 6.037 | `graal603.exe` |

## What the switch does

The same on all four builds: no window, no dialog, nothing on the console and no network. The client writes one file, `scriptfunctions_client.txt` (ASCII, CRLF), into its own folder and exits by itself within ten seconds. It was the only file created in the client tree.

| Build | Lines | Bytes |
|---|---|---|
| 4.20r8 | 2 152 | 73 099 |
| 5.00r7 | 2 305 | 82 125 |
| 5.12 | 2 331 | 83 805 |
| 6.037 | 2 281 | 110 716 |

## Format

Two top-level sections: `Global:` (global settings, variables and functions) and `TGraalVar:` (members of the base script object). Under `TGraalVar:` there is one block per object type, `  ClassName (Parent):`, with its members indented four spaces. Each entry is one line: a variable as `name - type [(read only)] [- description]`, a function as `name(arg types) [- returns type] [- description]`. From 4.20r8:

```
  $pref::audio::choosenvoicecodec - integer
  getascii(str) - returns integer
  timevar3 - float (read only) - synchronized time which works on both server- and client-side, precision is milliseconds, only available for Graal3D right now
  ActionMap (TGraalVar):
    bind(str, str, str)
```

## Counts

Unique (owner, name) pairs, overloads counted once; owners are `Global`, `TGraalVar` and each object type.

| Build | Entries | Functions | Variables | Owners | Global functions | Global variables |
|---|---|---|---|---|---|---|
| 4.20r8 | 1 988 | 667 | 1 014 | 37 | 252 | 117 |
| 5.00r7 | 2 131 | 706 | 1 089 | 37 | 247 | 130 |
| 5.12 | 2 155 | 713 | 1 105 | 37 | 254 | 137 |
| 6.037 | 2 132 | 807 | 929 | 33 | 298 | 127 |

## Differences between builds

**4.20r8 → 5.00r7:** entries +153 / −39, functions +69 / −30.

- Added, for example: `copystrings`, `escapestring`, `findnearestplayer(s)`, `findpathinarray`, `getdesktopresolution`, `getfilemodtime`, `getloginaccountname`, `isclassloaded`, `isfullscreenmode`, `loadclass`, `loadtranslation`, `rungarbagecollector`, `setspritesimage`, `setstatusimage`, `startrecordvideo`, `stoprecordvideo`, `stopmusic`.
- Removed: the 4.x launcher hooks `adventure_*` (`adventure_installgraal`, `_openserverlist`, `_quit`, `_reconnect`, `_setaccountname`, `_setnickname`, `_setpassword`, `_startofflinemode` and others).
- Object types: `MovieClip` added, `TFlashInstance` removed.

**5.00r7 → 5.12:** entries +24 / −1, functions +8 / −1. Added: `findplayerbycommunityname`, `getmusicfilename`, `gettileset`, `gettilesettype`, `ismusicplaying`, `issoundplaying`, `switchtoopengl`, `TGraalVar.clearemptyvars`. Removed: `TDrawableObject.toweapons`. Object types unchanged.

**5.12 → 6.037:** entries +521 / −603, functions +268 / −174.

- Added, for example: `adddnsentry`, `clearemptyglobalvars`, `convertlatintoutf8`, `convertutf8tolatin`, `converttimetostring`, `decompressfile`, `deletefile`, `downloadfiletofolder`, `escapefilename`, `fileupdateignore`, `findplayer2`, `formattimestring`, `freeallresources`, `getcallstack`, `getdownloadprogress`, `getmemoryusage`, `getplayerlisticons`, `getpremiumoption`.
- Removed: mostly the Torque/Graal3D object types and their methods (`ActionMap.bind`, `DTSAniThread.play`, `GameMovementList.move3d`, `GameShape.getanimation` and so on).
- Object types added: `GuiAccordionEntry`, `GuiSlideShowEntry`, `Stage`, `TCallStackEntry`, `TControlBinding`, `TGUIAnimation`, `TRTMPStream`, `TTileAnimation`, `TTileImageMap`, `TTileMap`, `TTileMapLayer`, `TTileMapObject`, `TWindow`.
- Object types removed: `ActionMap`, `DTSAniThread`, `GameMovementInterpolate`, `GameMovementList`, `GameShape`, `MRandomGenerator`, `SimObject`, `TGraalAniPart`, `TGraalAniSound`, `TGraalAniSprite`, `TGraalAniStep`, `TGraalSpriteAttachment`, `TMovementRigid`, `TParticle`, `TShapeMaterial`, `TShowImg_Values`, `Terraformer`.

## Against the wiki client page

The 2008-09-22 archived copy of the wiki's `Creation/Dev/Script/Client` page lists 176 function names in its Functions section. (The "90 client functions" in the [wiki cross-check](graal-wiki-crosscheck-2026-11-11.md) came from another page or revision.) **[doc]**

| Build | Wiki names in the build's global functions | Wiki only | Build only |
|---|---|---|---|
| 4.20r8 | 174 | 2 (`findweaponnpc`, `savelog2`) | 78 |
| 5.00r7 | 173 | 3 (+ `updateratings`) | 74 |
| 5.12 | 173 | 3 | 81 |
| 6.037 | 158 | 18 | 140 |

The 2008 page is evidently a dump from a 4.20r8–5.12-era build [inf]. The names missing on 6.037 are the Graal3D functions 6.x dropped (`get3dobjectat`, `lightscene`, `setfogcolors`, `setskyband*`, `setsuncolors`, `setterrainrendermode`, `synctimeofday` and others), plus `requestfiledeletion`, `requestfilerename`, `requestfilesmove` and `setmap`.

Across the four builds there are 356 distinct global function names; 286 of them appear somewhere in this repository as `name(`.
