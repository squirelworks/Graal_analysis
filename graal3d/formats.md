# Graal3D files

Date: 2026-10-21

## `graal3dconfig.txt` (client)

`key=value` lines, read at start and written back when settings change:

| Key | Shipped value | Meaning |
|---|---|---|
| `serveraddr` | `213.105.185.114` | Server host or IP (the connect window default is `127.0.0.1`) |
| `serverport` | `14901` | TCP port |
| `fixedport` | `false` | Bind the UDP socket to `fixedudpport` instead of a random port |
| `fixedudpport` | `14898` | |
| `noudp` | `false` | No UDP socket. Position and chat then go only through the server. |
| `bodyx` | `body.x` | Body mesh (prop 6) |
| `headx` | `head.x` | Head mesh (prop 7) |
| `bodytex` | `body.bmp` | Body texture (prop 8) |
| `armcolor` | `0xFF0000` | Prop 10 |
| `shoecolor` | `0x800000` | Prop 11 |
| `handcolor` | `0xFDCC47` | Prop 17 |

The reader also accepts `accountname` and `password`.

The client resolves host names once per run and keeps the name → address pairs in a small cache.

## Registry (client)

`HKCU\Software\Graal3D`, section `Client`: `nickname`, `accountname`, `password`.

The password is stored as 48 printable characters, two per byte, giving 24 bytes. Those are three DES blocks under a fixed 8-character key built into the exe. Decrypted, byte 0 is the length and the password follows. This is obfuscation, not protection. It uses the same `DesCipher` class that later 2D clients use to hide their list-server host.

## `serverconfig.txt` (server)

`serverport=14901`.

## `accounts.txt` (server)

One account per `\n`-terminated line, in the protocol's `+32` text codec:

```
str(name) str(password) str(saved props) c(flags) <inherited lists>
```

- **saved props** is the player's prop stream (the same encoding as packet 1, for the props the server keeps). It is written back when a player bound to the account leaves or is edited, and applied on login.
- **flags**: bit 0 = shared account (not bound to the session), bits 1–3 = admin level 0–3, bit 4 = disabled. The server UI calls the levels Administrator and Police.
- **inherited lists**: the 2D account record ends in count-prefixed string lists. The 3D server still reads and writes them, but no Graal3D prop or packet fills them.

`TServerAccount` is the same size as in the 2D `GServer13.exe`, so the record layout is very likely shared. The two files have not been byte-compared.

## `guilds\guild<name>.txt` (server)

A nickname `nick (Name)` keeps its `(Name)` tag only if this file exists and lists the player's account (one per line). This works the same as in the 2D server.

## Levels (`levels\*.x` on the server)

A level is a **DirectX retained-mode `.x` text file** (`xof 0302txt 0064`). `startlevel.x` is the server's start level and `level1.x` is the client's default. The two shipped files hold the same scene and differ only in whitespace (`level1.x` has CRLF line ends and trailing spaces, `startlevel.x` has LF line ends):

- One 139-vertex mesh named `obj`, with a material list and texture coordinates.
- Nine materials: `grasstex`, `waytex`, `stonestex`, `walltex`, `towertex`, `platformtex`, `cloudstex`, `plainblue`, `plaingray`.
- Textures referenced by file name: `grass.bmp`, `way.bmp`, `stones.bmp`, `wall.bmp`, `tower.bmp`, `platform.bmp`, `clouds.bmp`.

The server caches each level's text and sends it inline in packet 0 (`\n` written as `§`). The client saves the text to disk under the level name and loads it with Direct3D RM. **Textures are not transferred**: the BMPs a level names must already be in the client folder. There is no tile layer, NPC or link data. A level change is a change of prop 14.

## Player model (client)

Eight `.x` meshes (`xof 0303txt 0032`), each with one mesh, normals, texture coordinates and a material:

| File | Notes |
|---|---|
| `body.x` | Textured with `body.bmp` (128×128, 24-bit; `body1.bmp` is an alternative) |
| `head.x` | Three materials, textured with `man.bmp` (64×64) |
| `armright.x`, `armleft.x` | Coloured by prop 10 |
| `handright.x`, `handleft.x` | Coloured by prop 17 |
| `footright.x`, `footleft.x` | Coloured by prop 11 |

The body and head mesh and texture names travel as props 6–9, so a player can point them at other files present on every client. Colours are 24-bit RGB set as material colours at runtime. Prop 5 is passed to the model's animation object; it is most likely the animation frame.

## Textures

Plain Windows BMPs: 24-bit for `body.bmp`, `body1.bmp`, `grass.bmp`, `tower.bmp`, `man.bmp` and `logo.bmp`; 8-bit RLE for `clouds.bmp` (256×256), `platform.bmp`, `stones.bmp`, `wall.bmp` and `way.bmp`. Most are 128×128.
