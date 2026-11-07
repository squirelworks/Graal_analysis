<!-- manual: kind=front status=draft -->
# Appendix D. Glossary

Short definitions of the terms the manual uses, each with the section that defines it. A glossary entry adds no fact of its own. Where a term has several meanings in the notes, the entry lists the meanings and points to where each one applies.

> Status: draft.

| Term | Meaning | Defined in |
| --- | --- | --- |
| 1st Graal … 15th Graal | early 1998–1999 Delphi builds named by archive order | → §1.1.1 |
| `ADDITFLAGS` | a bit field in the player props | → §2.6.2 |
| admin level | the 0–3 rights value in an account record (Graal3D: No rights, Graalian Police, Trusted Admin, Administrator) | → §5.4, → §9.2.4 |
| allowed versions | the server's list of version tokens it lets log in | → §5.4 |
| archive name | the name of the archive a build was found in, such as `graal121` | → §0.9 |
| arrays.dat, arrays2.dat | client data files holding the tile allow lists and other tables | → §3.5.3, → §3.5.4 |
| arrival | the `newx`/`newy` text of a link; a number, `playerx`/`playery`, or one of those with an offset | → §3.1.3, → App. E#601 |
| baddy | a level opponent with a type and three verse lines; `BDPROP` props | → §3.1, → §2.6.5 |
| BDPROP | a baddy prop id | → §2.6.5, → App. B |
| BigData events | the two Torque events that carry Graal text and scripts over the 3D connection | → §10.5.3 |
| `bigmap.txt` | the text world map of older builds and generators: one row per line of quoted level names | → §3.2.5, → §11.3.4 |
| board | one level's tile grid | → §0.8, → §3.1 |
| board modify | a message that changes a rectangle of board tiles | → §2.4.5, → §2.5.3 |
| build | one client executable by release name and revision, such as `2.05 rev 2` | → §0.9, → §1.1 |
| build tag | an evidence tag naming the build a claim was read from, such as `[2.05]` | → App. G.2 |
| `CHR:1.00` | the one-line character file of the Character Designer and GChar | → §11.7 |
| class table | the list of class names and ids in a Torque connect accept, a Graal change from 3.153 on | → §10.3.3 |
| client type | the login type value that selects a server code path (0, 4, 5, 6) | → §0.9, → §2.3 |
| control-NPC | an `editnpc*.txt` script that drives the built-in editor | → §11.6.1 |
| DSO | compiled TorqueScript, file version 33 in the 3.x clients | → §10.4 |
| encryption generation | the transport scheme 1–6, in the GServer-v2 numbering | → §0.9, → §2.2.1 |
| era | a heading aid grouping builds; never a scope for a fact | → §0.9 |
| frame | one transport unit carrying one or more messages | → §0.7, → §2.1.4 |
| GANI | the text animation format, `GANI0001` sprite mode and `GANI0002` movie mode | → §3.3 |
| `GameObject` | the 3D object class of the 4.20r6 and 5.12 clients | → §10.5.2 |
| GCHAR, GSHORT, GINT3–5, GSTRING | Graal's printable integer and string encodings, short names `c`, `s`, `i3`–`i5`, `str` | → §0.6, → §2.1.1 |
| `GDUNG001` | the DungeonGenerator options file | → §11.3.3 |
| gen 3 insertion | the per-message byte the generation-3 client inserts | → §2.2.2 |
| `GENERATED` | a gmap key whose meaning depends on the writer: a level name, a flag, or absent | → §3.2.3 |
| GLEVNW01 | the text level format (`.nw`) | → §3.1.3 |
| gmap, GRMAP001 | a world map naming a grid of level files | → §3.2 |
| GOBJSET01 | the stamp-set format the editors use | → §3.4 |
| GR-V1 | the binary `.graal` level family, 1.00 to 1.04 | → §3.1.2 |
| `GR3DV002` | the version string of the February 2000 Graal3D client | → §9.1.2 |
| Graal3D | either the February 2000 DirectX program or the Torque 3D side of 3.x–5.12; the manual says which | → §9, → §10 |
| GraalEditor | the standalone level editor from 2.3 | → §11.1 |
| GraalShop | the GANI editor | → §11.2 |
| GS1 | the original NPC scripting language, interpreted from text | → §8.1 |
| GS2 | the later scripting language, compiled to bytecode | → §8.3, → §8.4 |
| GServer13 | the 1999 game server | → §5.1 |
| GServer-v2 | the open-source server used as `[srv]` reference behaviour | → §5.3 |
| guest login | the clients' built-in guest account | → §0.10 |
| GWEBL001 | the encrypted web-level cache format | → §3.8 |
| half-tile | 8 px; the unit of most 2D coordinate fields | → §0.8 |
| `HEIGHTS` | a 9 × 9 height block in a level file; distinct from a gmap's `HEIGHTMAP` | → §3.1.2.7, → App. E#606 |
| leader | the player picked to run level-local actions for a level | → §2.9.3, → §9.1.3 |
| level-format generation | the level file family and revision | → §0.9, → §1.5 |
| listserver | the directory server a client asks for the server list | → §6 |
| load only | an account flag: the session is not tied to the record and may be shared | → §5.4, → §9.2.4 |
| logical id | the decimal message id used in this manual; the wire byte is the id + `0x20` | → §0.7 |
| message | one id, its payload and, in most generations, a `\n` terminator | → §0.7, → §2.1.2 |
| mission phases | the Torque `MissionStartPhaseN` steps after a 3D connect | → §10.3.6 |
| NC, NPC Control | the staff client for an NPC server | → §7.2, → §11.5 |
| NewMain, NewWorld | the 2000–2001 builds of the New World line | → §1.1 |
| NPC server | the server-side host for NPC scripts | → §7 |
| NPCPROP | an NPC prop id | → §2.6.4, → App. B |
| offline mode | single-player play without a server | → §4.8 |
| PLI | a client-to-server message, names `PLI_*` | → §0.7, → §2.4, → App. A |
| PLO | a server-to-client message, names `PLO_*` | → §0.7, → §2.5, → App. A |
| PLPROP | a player prop id | → §2.6.2, → App. B |
| predefined NPC | a `defnpc*.txt` script with `#EDIT` parameters, placed from the editor palette | → §11.6.1 |
| prop stream | a run of prop id and value pairs in one message | → §2.6.1 |
| raw data | the escape that carries a binary payload behind `PLO_RAWDATA` | → §2.1.3 |
| RC, RemoteControl | the staff client for a game server | → §7.1, → §11.5 |
| server-defined protocol | the 6.11 scheme in which a connector script defines the transport | → §2.10 |
| sign alphabet | the code table used for sign text in binary levels | → §3.6 |
| stamp | a predefined tile object from a GOBJSET01 set | → §3.4, → §11.6.4 |
| tick | one step of a client's game loop; its length is per build | → §0.8, → §4.1 |
| tile | one board cell, 16 px on a side | → §0.8 |
| tile definition | a line `image,prefix,type,x,y` swapping the tile sheet for levels whose name starts with a prefix | → §11.6.4 |
| tile type | the per-tile value from the type table that decides walls and water | → §3.5.2 |
| TGE, Torque | GarageGames' Torque Game Engine, the base of the 3.x–5.12 clients | → §10.1 |
| UDP id | a message on the peer-to-peer UDP channel | → §0.7, → §2.9.4 |
| unmeasured | a table cell value meaning no build was measured | → §0.4 |
| version token | the login version string a build sends, such as `GNW03081` | → §0.9, → §1.2 |
| warp field | a link created from an editor selection | → §11.6.4 |
| wire byte | the byte on the wire for a GCHAR id, the logical id + `0x20` | → §0.7 |
| Zelda Online | the 1997–1998 Java precursor and its `.zelda` (Z3-V1) levels | → §1.1.1, → §3.1.1 |
