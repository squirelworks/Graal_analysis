# Medium-term slice

Date: 2026-10-14

## Renderer
SDL2 is not available in this environment. `client/src/render/mod.rs` provides:
- `ascii_board` — 64×64 ASCII view (`#` wall, `.` passable, `P` player)
- `write_ppm` — raw PPM dump of the same view

A real SDL2/OpenGL path can replace this when the dependency is present.

## Listserver
`Connection::listserver_session` connects, sends the locked classic login line, and reads the reply as text. No decryption. Timeout is 5 seconds.

## GS1 interpreter
`Bytecode::execute` runs a minimal stack VM covering the OpenGS1 arithmetic, comparison, and jump opcodes. `Call` / `CmdCall` / array ops are no-ops until the command set is wired. Unit test covers `Push` + `Add`.
