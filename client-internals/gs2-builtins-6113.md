# Built-in names in unpacked 6.1.1.3 and 6.0.3.7

Static read of both listings, set against `npc-library/preagonal-gs2.md`.
Nothing was run. The opcode case list stays in `client-internals/gs2-6113.md`.
No case in that dispatcher was tied to one of the names below. [bin]

## Math names

Both images store one run of eighteen names:

`pi`, `sqrt2`, `sqrt1_2`, `abs`, `atan`, `atan2`, `ceil`, `cos`, `floor`,
`log`, `max`, `min`, `pow`, `random`, `round`, `sin`, `sqrt`, `tan`.

In 6.1.1.3 the next packed runs are the key names (`up`, `down`, `enter`,
`escape`, and the rest of that run) and the movie-clip names
(`gotoandplay`, `gotoandstop`, `attachmovie`, `stop`). 6.0.3.7 has the
same eighteen math names and has `gotoandplay`. [bin]

## Against Preagonal

Preagonal's compiler turns these names into their own opcodes rather than
a call by name: `sin`, `cos`, `arctan`, `abs`, `exp`, `log`, `random`,
`min`, `max`, `vecx`, `vecy`, `char`, `pow`, `getangle`, `getdir`,
`arraylen`, `sarraylen`, `waitfor`, `sleep`, `setarray`, `makevar`,
`format`, and the string and list methods it names (`trim`, `length`,
`pos`, `starts`, `ends`, `tokenize`, `size`, `clear`, `add`, `delete`,
`insert`, `remove`, `replace`). [doc] (`npc-library/preagonal-gs2.md`)

Of that list, these images contain the names `abs`, `cos`, `log`, `max`,
`min`, `pow`, `random`, `sin`, `format`, and a plaintext `sleep`. They do
not contain `arctan`, `exp`, `vecx`, `vecy`, `char`, `getangle`, `getdir`,
`arraylen`, `sarraylen`, `waitfor`, `setarray`, `makevar`, `trim`,
`length`, `pos`, `starts`, `ends`, `tokenize`, `size`, `clear`, `add`,
`delete`, `insert`, `remove`, or `replace` as their own identifiers.

The math run also has names that list does not: `pi`, `sqrt2`,
`sqrt1_2`, `atan`, `atan2`, `ceil`, `floor`, `round`, `sqrt`, `tan`.
Those ten are in both images.

`format` is a name in both images. It was not matched to a dispatcher
case. The case numbers themselves are in `client-internals/gs2-6113.md`.

## Commands, and where the builds differ

Both images contain the command run that includes `showimg`, `hide`,
`echo`, `move`, `say`, `sleep` (the plaintext one), and `setzoomeffect`.
The whole run is not copied out here.

Names present in 6.0.3.7 and not in 6.1.1.3, from the decoded identifier
set: `putcomp`, `putnewcomp`.

Names present in 6.1.1.3 and not in 6.0.3.7 include `setprotocol`,
`sendraw`, `senddata`, the `tclient_*` methods, and the cipher names
`aes_encrypt`, `aes_decrypt`, `des_encrypt`, `des_decrypt`, `rc4_cipher`,
`rsa_encrypt`, `rsa_decrypt`, `rsa_sign`, `rsa_verify`, and `sha256`.
The `tclient_*` list is the receive-method table, not repeated here.
