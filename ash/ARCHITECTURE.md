# 39ster 2.1 GServer — architecture

December 2006 open remake of the 1.39 Graal server, targeting Graal clients 2.*. Single-process Windows/POSIX C++ server. No script VM. No MySQL despite the readme. No `.nw` loader despite the stub.

## 1. System context

```
                    ┌────────────────────┐
   Graal 2.* player │  TCP :14822         │
   RC client        │  zlib frames        │──► win32Gserver.exe
                    └────────────────────┘
                              │
          ┌──────────────────┼───────────────────┐
          ▼                   ▼                   ▼
   data/** (maps,gifs)   accounts/<name>     Weapons.txt
   resolved by subdirs   save is a stub      INI catalog
```

External actors:

- **CLIENTPLAYER (0)** — game client. Login packet carries a scramble `key`. Every later inbound line drops one byte via LCG.
- **CLIENTRC (1)** — Remote Control client. Same framing, **no** scramble. RC opcodes 51–87 exist in the table; bodies are empty stubs.
- Filesystem only. Readme promised MySQL credentials; `loadAccount` hard-codes spawn.

## 2. Process and thread model

Two threads, shared heaps, no locks.

```
 main thread
 │
 ├─ listen on 14822 (non-blocking)
 ├─ accept loop (select 1 s)
 ├─ for each new connection: spawn player thread
 └─ every 1 s: gameTime++, idle-kick check (300 s), weapon list reload?

 player threads (one per connection)
 │
 ├─ mainLoop: recv → inflate frames → split lines → (descramble if PLAYER) → parseMessage
 └─ sendoutgoing on flush or buffer pressure
```

`maxPlayers` is 100 but never enforced. `playerIds` is a simple free-list.

## 3. Class graph (simplified)

```
CPlayer
 ├─ sock, type, key, iterator, id, accountname, nickname, version, levelname
 ├─ level* (CLevel*)
 ├─ sendbuff / outgoing
 └─ stats, weapons, openChests, enteredLevels, ...

CLevel
 ├─ filename, tiles[64*64], links, baddies, npcs, chests, signs
 ├─ LoadedMaps (static map)
 └─ load_graal() / animate()

CNpc / CBaddy / CWeapon (stubs or partial)
```

## 4. Data stores

- `data/` tree walked once at boot (`getSubDirs`). `getDataFile(name)` returns first match by basename.
- `accounts/<name>` — plain text, load is stubbed to spawn on `level13.graal`.
- `Weapons.txt` — INI-style catalog loaded into `weaponList`.

Default listen port: **14822**. Start map: **level13.graal**.

See ALGORITHMS.md for wire format, scramble, GCHAR, and GR-V1 details.
See OPCODE-MAP.md (already present) for the packet tables.
