# Graal Character Designer and GChar

Date: 2026-11-01

GCD 1.2.7 (November 1999, Andrew Bridges / Bruges) and GChar 1.0 release CA, the same author. Both are Delphi windows for classic character looks. Neither image imports a socket library. **[bin][doc]**

`chrfile.py` parses the character line.

## Files they read

Both expect a Graal folder that contains `headsconfig.txt`, `levels\heads\`, `levels\gifs\` and `levels\webgifs\`. If `headsconfig.txt` is missing they say so and stop. GCD also looks for `Graal.exe` under the usual install folders and, failing that, asks the operator to type the folder. **[bin]**

GChar reads `GChar.ini` from its own folder: `drawmethod` (1 or 2), `headmode` (1 or 2) and `graaldir` (the folder the operator set). The command `/setdraw 1` or `/setdraw 2` writes the draw method and shows `Draw Mode Set to 1` or the matching line for 2. Draw mode 2 is the default. Head mode 1 is a head number. Head mode 2 is a gif name with no `.gif`, looked up under `levels\heads` and `levels\webgifs`, or a file the operator picks. The readme says a typed name is not checked beyond being a gif, and that a head with no number is not one the server has. **[doc][file][bin]**

On startup each tool looks for `*.chi` in the Graal folder, adds characters that are not already in the list, and renames those files to `*.chr` so the next run does not add them again. GChar warns and skips a CHI whose name is already present; the operator has to open it and use Save to Graal. **[doc]**

`GCD.dat` and `GChar.dat` are small binary scratch files (the GChar readme mentions a fix for that file being corrupted). They are not the character format. **[file]**

## The character line

A `.chr` or `.chi` file is one text line. Every sample in both archives has this shape: **[file]**

```
CHR:1.00Blade=head189.gif,male,black,black,gray,gray,red
```

`CHR:1.00`, the name, `=`, the head gif, sex (`male` or `female`), and five colour names. The file does not label the five colours. Sample names include black, gray, red, yellow, darkblue, cynober, brown, green, purple, lightblue, darkgreen, orange, darkred, darkpurple, white, lightgray, pink and lightgreen. Two samples are `female` (Anna, Sarah). Several files whose names say Girl are stored as `male`; the head gif is doing the work. **[file]**

## What the operator sees, and what is never sent

Buttons along the bottom set the colours. A box on the right is the head. Buttons on the left turn the preview. Name sets the name. Save to Graal writes the character into the client's list. Save to file writes `.chr` or `.chi`. Open reads a file. Load reads one back from the Graal list. Snapshot writes a bmp of the current view. Manage deletes, reorders and renames list entries. **[doc]**

Nothing is sent. There is no list login, no account, and no URL request in the import table. The readme's contact line is a mailbox on the official site; the programs do not open it. **[bin][doc]**
