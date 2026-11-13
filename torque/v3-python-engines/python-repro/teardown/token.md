# Token

## Game session · high

a client routine at an address, immediately after the literal `Done.`.

The function appends eight one-character strings, in order, onto one buffer:

`G` `3` `D` `2` `8` `0` `1` `5`

That is `G3D28015`. It is not a single C string in the file. `G3D03014` is not built.

It is sent as the front of packet id `5` (wire byte `0x25`) on the game connection. See `login.md`. The send is a client routine(connection, 5, buffer)` at an address.

## Server lister · high

a client routine at an address builds a second string the same way:

`G` `3` `D` `3` `0` `1` `2` `3` `n` `e` `w` `m` `a` `i` `n`

That is `G3D30123newmain`. It is packet id `7` (wire `0x27`) on the lister connection, not on the game connection. The call is the vtable slot at `+0x0C` with immediate `7`, at an address.

`getVersionString` is only registered as a console command in a client routine. Its return text was not read. The product version in the plist is not this token.
