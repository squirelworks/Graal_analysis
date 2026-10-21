# Client 2.05 rev 2 architecture

Date: 2026-10-21

Build: `GNW03081`, the "2002ver9" leak build in GServer's `versions.txt`. Delphi (Borland), DelphiX (DirectDraw/DirectSound/DirectInput), zlib 1.1.2. Derived from the class list and behavior of the 2.05 binary. Names only, no code. Tag: **[2.05]** unless marked.

## Networking classes

| Class | Parent | Role |
|-------|--------|------|
| `TGraalClient` | TObject | socket, out buffer, zlib flush, u16be frame |
| `TServerListClient` | TGraalClient | listserver link: base send (no cipher), receive handles ids 0 and 1 |
| `TAdventureClient` | TGraalClient | game link: gen-3 insertion on send, a receive jump table that handles 59 ids, login builder |
| `TWebClient` | TObject | HTTP (web levels / `openurl`) [inf] |
| `TAdventureServer` | TObject | local or offline server stand-in [inf] |

The game socket keeps the gen-3 iterator, the key, and a "first message sent" flag in the client object. Disconnecting resets the server name to `Offline`. Messages are buffered and flushed at 0x1000 bytes. The client drops the link if 256 KB is queued. A UDP socket handles peer-to-peer traffic (`protocol/udp-p2p.md`).

## Game model

| Class | Parent | Notes |
|-------|--------|-------|
| `TAdventure` | TDXForm | main window and game loop |
| `TAdventureLevel`, `TBoard`, `TBoardModify` | TObject | level, 64×64 board, pending board changes |
| `TLevelObject` | TDrawableObject | base for drawable level objects |
| `TAdventureExtra`, `TAdventureLeap`, `TAdventureBomb`, `TAdventureExplosion`, `TAdventureBall`, `TAdventureFlying`, `TAdventureCarry` | TLevelObject | items, leaps, bombs, explosions, fireballs, arrows, carried objects [inf from names] |
| `TServerPlayer` | TLevelObject | networked character. `TPlayer` (self) and `TEditorNPC` derive from it |
| `TComputer` | TSurfaceOwner | baddy ("compu") |
| `TAdventureHorse` | TSurfaceOwner | horse or boat |
| `TDisplayedNPCImg`, `TTempWeaponImg` | — | `showimg` overlays, weapon icons |
| `TAdventureWeapon` | TObject | weapon (name, image, GS1 script) |
| `TTileDef`, `TTempTile` | TObject | `addtiledef` and temporary tile overrides |
| `TGraalMap` | TObject | big-map / minimap overlay [inf] |
| `TGraalAni`, `TGraalAniStep`, `TGraalAniPart`, `TGraalAniSprite`, `TGraalAniSound` | TObject | GANI model (see `formats/gani.txt`) |
| `TCachedStream` | TObject | file cache [inf] |

## Script engine

`TAdventureCommand`, `TAdventureOperation`, and `TAdventureVariable` are the parse-tree nodes, with `TArray`, `TInteger`, `TDouble`, and `TStringPosList` as values. Execution is a recursive tree walk. See `npc-library/gs1-reference-205.md`.

## UI forms

`TConnectFrame`, `TReconnectFrame`, `TServerListFrame`, `TLoadLevel`, `TServerMessage`, `TShortMessage`, `TPlayerList`, `TPlayerListOptions`, `TProfileEdit`, `TOptions`, `TMoreOptions`, `TLinkList`, `TLinkOptions`, `TShowCodes`, `TPersonAction`, `TChestEdit`, `TDebuggerFrame`. The editor and the client are **one executable** in 2.05: link, chest, and NPC editing forms are built in. They split into separate programs at 2.3 (see `version-tokens.md`).

## Other formats seen in 2.05

- **GWEBL001**: a web-level cache file. It starts with the magic `GWEBL001`, then GSTRING fields and a GSHORT version that is checked against the client. The client also computes a running product hash over a key string, seeded with `0x04A80B38`. **[2.05]** The field list is not fully traced.
- A Delphi DES cipher class (`UDesCipher`) is linked in. It is not the game wire codec. It protects the saved passwords, the hidden listserver host (`www.graalonline.com`, port 14921, list `newmain`), and the `GWEBL001` web-level cache. **[2.05]**
- Image decoders: GIF (`TGifAnimation`), MNG (`TMNGAnimation`), JPEG. MNG animation fits with `gif2mng`.

## Level magics accepted
`GLEVNW01`, `GR-V1.00`–`GR-V1.03`, `Z3-V1.03`, `Z3-V1.04`. No `GR-V1.04`. A `GRMAP001` reader is also present (with the generated-map and `HEIGHTS` keys), but no static caller was found; see `formats/gmap.md`.
