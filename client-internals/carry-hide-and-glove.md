# Hiding under a carried object, and the glove (2.05)

Date: 2026-10-29. Read from the 2.05 rev 2 client; tile lists from the 2.22 install's `arrays.dat`. **[2.05]** unless tagged. No addresses or decompiler text. Key slots are graalconfig's: D is the item key, S attack, A action.

## Hiding (mode 14)

* **D while carrying** a bush, a light stone, a black stone or an NPC hides the player under it. The carry sprites that allow it are 261 (bush), 263 (light stone) and 239 (black stone). A pot (265) or a sign (267): D does nothing.
* **D again**, or **A**, comes out: the player goes back to carrying (`carrystill`). Out from under a bush (not an NPC) the client starts break effect 0 (the leaves) at `(x + 0.5, y + 1)`.
* **S** throws, from hiding too.
* **Poses.** `hiddenstill` standing, `hidden` walking. The walk routine applies a factor of 0.2 while hidden, most likely the speed (not tested). **[inf]**
* **Hits.** The hit gate refuses hits on a hidden player unless a player byte that was not traced is set.
* **Wire.** `hiddenstill` is animation step 24, sprite 18 (as `carrystill`); `hidden` is steps 25 to 28, sprites 19, 20, 19, 18. STATUS gets bit 0x02. The carry sprite prop does not change.
* Not traced: the pose shown on stopping while hidden (most likely `hiddenstill`).

## Glove power and the lift table

* The lift routine reads the tile at the A key's facing point and tries the first **glove + 2** entries of `arrays.dat` array 11 (lift tiles; array 12 holds what each leaves behind). All four tiles must match.
* Array 11 in the 2.22 file: bush 2/3/18/19, sign 512/513/528/529, **pot** 684/685/700/701, light stone 34/35/50/51, black stone 990/991/1006/1007. The carry sprites in the same order are 261, 267, 265, 263, 239.
* Every player starts at **glove 1** (bush, sign, pot). The `glove1` item raises the power to at least 2 (adds the light stone), `glove2` to at least 3 (the black stone). GServer agrees: its default account has `GLOVEP 1` and its glove items set 2 and 3. **[srv]**
* Online the power is player prop 6 (GLOVEPOWER).
* An NPC is lifted only when its script set `canbecarried` (command 41, cleared by 42), at the same point and with no glove check. It leaves the level's NPC list and is carried. No packet goes out for it.
