# 39ster 2.1 — engineering blueprint

## Source tree

```
39ster's 2.1 Gserver/
  win32Gserver.sln
  win32Gserver/          ← compile unit
    main.cpp / main.h
    sockets.cpp / sockets.h
    tools.cpp / tools.h
    ini.cpp / ini.h
    player.cpp / player.h
    level.cpp / level.h
    npc.cpp / npc.h
    includes.h
    zlib.h  zconf.h
  debug/                 ← runtime cwd of the shipped exe
    win32Gserver.exe
    zlib1.dll
    Weapons.txt
    readme.txt
    developmentlog.txt
    accounts/<name>
    data/
      Levels/            .graal maps + weapon scripts as .txt
      gifs/  ganis/  charset/
      tempnpcs/
```

`getSubDirs("data/")` walks every subdirectory once at boot and stores full paths in `subdirs`. `getDataFile(name)` returns the first existing `subdir + name`. Maps are requested by basename (`level13.graal`), not by relative path.

## File ownership

| File | Lines (approx) | Owns |
|---|---|---|
| `includes.h` | 6 | WIN32 vs libc |
| `main.cpp` | 259 | port 14822, accept, 1s tick, idle 300s, `gameTime`, weapons INI, `getDataFile` |
| `sockets.cpp` | 111 | `tcplisten`/`tcpaccept`/`setsync`/`tcpReceive`/`tcpSend` |
| `tools.cpp` | 465 | `CList` growth +5, `CBuffer` GCHAR codec, file load/save |
| `ini.cpp` | 95 | `[section]` / `key=value` / `#` comments |
| `player.h` | 423 | 89 client ops, server ops, player props, `CPlayer` |
| `player.cpp` | 1401 | `msgFuncs`, scramble, login, warp, file/weapon send, props |
| `level.cpp` | 451 | GR-V1 decoder, sections, animate, baddy props |
| `npc.cpp` | 176 | NPC ctor + prop getters; `setProperties` almost empty |

## Wire frame blueprint

```
TCP stream
┌───────────────┬──────────────────────────┐
│ len u16 BE │ zlib payload  (len bytes)    │  repeated
└───────────────┴──────────────────────────┘

inflated payload = newline-separated messages
```

Login line (first message, **not** scrambled):

```
type:u8_gchar
[key:u8_gchar]               only if type == CLIENTPLAYER
version: 7 bytes (player) or 8 bytes (RC)   raw
mystery: 1 raw byte          skipped
namelen:u8_gchar  name:raw
passlen:u8_gchar  pass:raw
```

Later PLAYER line after descramble: `opcode:u8_gchar    payload…`

## Server → client special ops (not in the named enum)

| Byte | Role | Payload |
|---|---|---|
| 100 | announced length | GCHAR-int32 of the following packet size |
| 101 | raw board | 4096 native `short` tiles |
| 102 | file blob | GCHAR-int64 mtime, GCHAR-len, name, raw bytes |

Full runtime layout, login/presence blueprint, known holes, and remaining details are in the Drive archive under `Ash/BLUEPRINT.md`.
