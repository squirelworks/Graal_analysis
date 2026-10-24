# Links: decimals, negative arrivals, destination names

Counts over the 139 distinct files: 338 links in 136 files (`Z3-V1.03` 207, `Z3-V1.04` 131).

## Decimals

- `Z3-V1.03` links are written with decimal points: 167 of 207 have a decimal arrival, 124 have a decimal x, y, width or height (47 of the 85 `Z3-V1.03` files). Geometry is whole tiles with a `.0` ending; arrivals are often half tiles (171 links have a fractional arrival, 79 in `1.03`, 92 in `1.04`).
- `Z3-V1.04` links have no decimal geometry (0 of 131) but 92 have a decimal arrival.
- All three loaders read six floating-point numbers (the Java source with `parseDouble`-style reads, 1st Graal and 1.39 with string-to-float). A reader that parses integers drops these links.
- No destination name contains a space (0 of 338), so splitting the first token off is safe for these files. `formats/level-binary.md` says tokens before the last 6 are rejoined for GR-V1; the Delphi clients take the destination up to the first space.

## Negative arrivals

- 67 links have a negative x arrival and 85 a negative y arrival (151 links in all; one has both). `Z3-V1.03` and `.04` both use them.
- Rule, from the Java source and 1st Graal: a negative arrival coordinate is a flag meaning "keep the player's own coordinate on that axis". Both set a "constant" flag from `< 0` and use the player's position otherwise.
- The same appears in `GR-V1` links: 805 of 5381 distinct links in the same builds have a negative arrival. That the 2.x clients read it the same way is inferred, not traced.

## Destination extensions

- `Z3-V1.03` links name `.zelda` (205) or `.editor` (2) files. `Z3-V1.04` links name `.graal` (76) or `.zelda` (54), or `.editor` (1).
- The extension in a link therefore differs between builds that name their levels `.graal` and builds that name them `.zelda`; the loader sees the magic only (see 03).
