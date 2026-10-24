# 2.05 rev2: other facts (derived)

- **Prop 10** is the bow image slot (pre-2.1 meaning), as in the existing prop table. No new meaning was found.
- **Swim state** is a client mode (10), not a prop. It is visible to others only through the animation.
- **Send helper** (also in 1.39): a message whose payload contains a newline is silently dropped, since the newline is the message terminator. The helper prefixes the id byte (id+32), adds the newline, queues, and flushes when the queue would pass 4095 bytes.
- **Disconnect on overload**: if more than 256 KiB (0x3ffff) of compressed output is pending (1.39), the client closes the link. The 2.05 figure was not checked.
- **Obfuscated attributes**: see `01-death-respawn.md`.
- **Respawn and CLAIMPKER** are explained in `01-death-respawn.md`.
