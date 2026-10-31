# Graal3D files

Date: 2026-10-21

## `graal3dconfig.txt` (client)

`key=value` lines, read at start and written back when settings change:

| Key | Shipped value | Meaning |
|---|---|---|
| `serveraddr` | `<graal3d-default-host>` | Server host or IP (the connect window default is the loopback address) |
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

One account per `\n`-terminated line, in the protocol's `+32` text codec. Confirmed byte for byte in the lab, and a hand-written file is accepted. **[cap]**

```
str(name) str(password) str(saved props) c(flags) c(0) c(0) c(0) c(0) c(0) c(0) c(0)
```

For example, a fresh administrator account `alice` / `pw1` is `%alice#pw1 &` followed by seven spaces and `\n`.

- **saved props** is the player's prop run (the same encoding as packet 1): props 1–14, 16 and 17, no 0 or 15. It is empty until the player first leaves. It is written back when a bound player leaves or is edited, and applied on the next login (positions, chat text and nickname included).
- **flags**: bit 0 = Load only, bits 1–3 = rights level (0 No rights, 1 Graalian Police, 2 Trusted Admin, 3 Administrator), bit 4 = Blocked.
- **The seven trailing bytes** are the empty count-prefixed lists inherited from the 2D account record. The reader accepts lists there, but no Graal3D prop or packet fills them.
- The server rewrites the file whenever an account changes, not only at shutdown.

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
