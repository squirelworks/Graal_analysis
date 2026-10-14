# Medium-term expansion

Date: 2026-10-14

## Renderer
- `ascii_board` — full board, direction character for the player (`v < > ^`)
- `ascii_camera` — window centered on the player, out-of-bounds as space
- `write_ppm` — 64×64 PPM, walls dark, water blue, player red
- Tile characters: `#` wall, `~` water, `.` passable

SDL2 remains unavailable. These are the offline view until a graphics dependency is added.

## Listserver / net
- `Connection::listserver_session` — connect, classic login, read reply
- `Connection::send_walk` — short walk frame
- `parse_server_list` — provisional line filter (skips `GNW*` lines)

No decryption. List framing is still provisional.

## GS1
- Arithmetic, comparison, jump opcodes execute
- `Commands` registry with offline stubs: `message`/`say`, `setimg`, `move`
- `CmdCall` dispatches into the registry
- `Bytecode::execute_with` accepts a custom registry

`Call`, array ops, and most GS1 commands remain no-ops.

## Separation
Raw decompiles stay in `/shdecompiling/`. This note is cleaned. Client code is in `/seihai/`.
