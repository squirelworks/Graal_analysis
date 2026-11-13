# Assets

## Level open · high

a client routine at an address reads 8 bytes.

| magic | next call |
| --- | --- |
| `GLEVNW01` | a client routine |
| `GR-V1.00` | a client routine with selector `0x0C`, then a client routine, a client routine |
| `GR-V1.01` | the same, plus a client routine and a client routine |
| `GR-V1.02`, `GR-V1.03` | the `GR-V1.01` path, and the first selector becomes `0x0D` |

`GSERVL01` is also tested at the start of a client routine.

a client routine splits the file into sections. Names compared, in the order the branches are written:

`BOARD`, `LINK`, `CHEST`, `SIGN`, `NPC`, `BADDY`, `HEIGHTS`, `REPLACENPCS` … `REPLACENPCSEND`.

## BOARD line · high

For a `BOARD` section with more than 4 tokens:

| token | use |
| --- | --- |
| 0 | x, must be `< 64` |
| 1 | y, must be in `0..63` |
| 2 | count of tiles, `x + count <= 64` |
| 4 | the tile text. Token 3 is not read here |

Each tile is two characters. a client routine returns the index of the character in the alphabet at file offset an address:

`0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`

That is 62 characters, then NUL. An unknown character aborts the run. The stored `uint16` is `(index1 << 6) + index2`, written at `(y * 64 + x) * 2` and growing by 2.

## Other files the image names · high on the name, low on order

| name | where |
| --- | --- |
| `offlinetutorial.gmap` | a client routine after the console line `start2D();` |
| `offlinetutorial_b-2.graal` | string only |
| `GRMAP001` | a client routine, 22 KB, not walked |
| `license/sig.graal`, `license/license.graal` | strings |
| `.nw` `.gani` `.txt` `.rtf` `.html` `.xml` `.cs` `.gs` `.arc` `.dat` | a client routine keeps these extensions when building a path. Others are dropped |
| `.gft` | a client routine skips names with this suffix before packet `0x17` |
| `wbow1.png` | inbound id 3 |
| `compudead.wav` | inbound id 5, value 9 |
| gani verbs `SCRIPTEND`, `ANIEND`, `WAIT`, `PLAYSOUND`, `ACTOR`, `FRAME` | a client routine |

a client routine calls a client routine with 7, then with 8, on each object in a list, then loads `offlinetutorial.gmap`, then a client routine with 0, then a client routine. That is the only ordered load that was read. It is the offline tutorial path, and it runs only when a client global is zero.

`.gani` is also referenced from a client routine and a client routine. Those bodies were not mapped to a call order.
