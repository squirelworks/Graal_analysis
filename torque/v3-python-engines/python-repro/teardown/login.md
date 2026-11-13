# Login

## Game server · high on the bytes, medium on the two string fields

a client routine at an address.

1. Require a non-empty host at a client global and a positive port at a client global.
2. Print `Connecting to the game server...`.
3. a client routine sets the first-record flag and calls a client routine, which joins host and port with `":"` and hands that string to a client routine. The numeric port is not a constant in this function.
4. Continue only if `connection+0x1c` is non-zero and the byte at `connection+0x1c + 0xa8` is zero. Then print `Done.`.

First record, id `5`. Because `+0x18` is 1, the wire line is:

| offset | bytes |
| --- | --- |
| 0 | `0x25` (`5 + 0x20`) |
| 1 | `(connection+0x13) + 0x20` |
| 2 | `G3D28015` |
| 10 | `len(A) + 0x20`, then string A |
| after A | `len(B) + 0x20`, then string B |
| end | `0x0A` |

A is the string at a client field. B is the string object a client global. Neither global is a literal in this function. They are length-prefixed with the short-string rule. Confidence high on the layout, low on the English names of A and B.

Second record, id `0x25` (37), wire `0x45`. The first-record flag is already clear, so there is no extra byte. The payload is the string object a client global, then `0x0A`. What that string holds was not recovered.

a client routine then pushes the buffer to the socket.

If `noudp` and a client global are both zero, a client routine opens a UDP socket. `fixedport` selects the port argument: 0, or `fixedudpport` when the flag is set. `socket(2, 2, 0)` is `AF_INET` / `SOCK_DGRAM`. That socket is not the login stream.

## Server lister · high

a client routine at an address. Host a client global, port a client global. The label string is `server lister`.

| order | id | wire | payload |
| --- | --- | --- | --- |
| 1 | 7 | `0x27` | `G3D30123newmain`. First record, so the extra `+0x13` byte is present |
| 2 | 1 | `0x21` | `gchar(len C) + C + gchar(len B) + B` |

C is a client global. B is the same a client global used by the game login. `vtable+0x10` is called after each of these two sends.

## Expected reply · low

No function matches a login-accept literal and then branches. The next parser that consumes server bytes for a player is a client routine, and it only accepts logical ids 0–10. A line whose first byte is outside `0x20`–`0x2A` stops that parser. There is no recovered “login ok” opcode.
