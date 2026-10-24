# Link arrivals are not only numbers or playerx/playery

`level-binary.md` lists a link as `dest x y w h newx newy` and the notes allow `playerx` / `playery` for the arrival. In the archive the last two fields hold, over 18,710 coordinate fields:

| Form | Count |
|------|-------|
| plain number (integers and half tiles such as `24.5`) | 12035 |
| `playerx` / `playery` | 6652 |
| `playerx` or `playery` followed by a signed number (`playery+10`, `playerx-15`, `playery-1.5`, `playerx+15`) | 21 (in 14 levels) |
| a stray non-numeric word (one level wrote two such words) | 2 |

Open: whether the stock client evaluates the offset, reads it as a number (0), or takes only the keyword. No capture shows it. The two level names that end in neither `.graal` nor `.nw` (`.enigma` 10, none 2) are also unexplained.

Link destination extensions: `.graal` 9203, `.nw` 140, `.enigma` 10, none 2.
