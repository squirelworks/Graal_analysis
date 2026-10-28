# Client asset tree (measured)

Date: 2026-10-14 (archived 2026-10-28)

Measured from the official client install. No decompile material.

## Tile sheets

| File | Size | Role |
|------|------|------|
| pics1.png | 2048×512 | Standard tiles, 128×32 of 16 px, 4096 ids |
| picso.png | 1024×512 | Offline tileset (type 1) |
| sprites.png | 128×452 | Sprite sheet |
| letters.png | — | Bitmap font |

Tile id `t` maps to `col = t % 128`, `row = t // 128`, source rect `(col*16, row*16, 16, 16)` on pics1.

## Tiledef

Offline line recovered from the tree:

```
picso.png,offlinetutorial,1,0,0
```

Format is `image,prefix,type[,x,y]`. Type 0 is the old Graal order (pics1). Type 1 is the new order.

## levels/ counts (files on disk)

| Dir | Files | Contents |
|-----|------:|----------|
| ganis/ | 93 | 86 .gani plus images |
| midis/ | 49 | music |
| heads/ | 35 | 33 png, 2 mng |
| weapons/ | 33 | weapon images, 2 txt |
| bomys/ | 29 | bomy images and ganis |
| emoticons/ | 29 | png and mng |
| webgifs/ | 26 | mostly png |
| backpals/ | 23 | background palettes |
| bodies/ | 20 | body images |
| images/ | 19 | misc images |
| smilies/ | 15 | |
| baddies/ | 10 | one sheet per baddy |
| shields/ | 7 | |
| swords/ | 6 | |
| npcs/ | 5 | script text |
| horses/ | 4 | |
| hats/ | 4 | |
| tutorial/ | 4 | |
| letters/ | 2 | blueletters, graal2002letters |
| snapshot/ | 2 | ss_arrow, ss_bomb |
| tiledefs/ | 1 | offline tiledef line |

Later work in `client-internals/client-assets.md` and the version-profile notes supersedes this snapshot where counts or mappings differ.
