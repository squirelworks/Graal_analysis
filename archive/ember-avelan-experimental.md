# Archival notes: Ember / Avelan experimental work

**Status:** Decommissioned 2026-10-28. These notes preserve prior attempts to understand and walk the Graal environment outside the main analysis corpus. Raw assets and full source trees are archived separately.

## Drive archive

A complete zip of the experimental project is stored on Google Drive:

- Path: `/[Grok/[Projects/Graal Enigma Playerworld.zip`
- File ID: `1Zqyp3ECN8dP-dk6jBjqfRQ728_PZzbgY`
- Link: https://drive.google.com/file/d/1Zqyp3ECN8dP-dk6jBjqfRQ728_PZzbgY/view

The zip contains Ember series sources, the Avelan 10×10 world, tileset variants, the tiledef plugin, stitched overworld maps, and documentation written against those trees.

## What the experiments were

### Ember series (React top-down walker)

A minimal client that loads GLEVNW01 `.nw` and GR-V1 `.graal` boards, walks them, and follows doors. No NPC scripts, no combat, no socket.

- Ember / Ember2 / Ember3.1: progressive addition of the pics1 type-0 mask, tileset upload, and a fly toggle that ignores the mask.
- Start level for the later builds: `avg-05.nw` at 10.5, 56.5.
- Save key used by Ember3.1: `ember31-avelan-v1`.
- Docs written against Ember3.1 live in the archive under `Ember3.3/Documentation` (the request was for 3.3; no 3.3 source tree existed).

Key level-format observations confirmed or refined here (already present in the main corpus):

- Boards are 64×64.
- Text `.nw` uses the `A-Za-z0-9+/` alphabet; pair = `hi * 64 + lo`.
- Edge links use `-1` on the free axis.
- Door arrival for the house south door to `egk-10` is resolved by looking back rather than trusting `nx, ny`.

### Avelan (original 10×10 overworld)

100 GLEVNW01 levels named `av{a–j}-{01–10}.nw`. Landmarks:

- Halebridge — `avg-05` (start)
- Saltwharf — `avf-09`
- Westmere — `avd-06`
- Highcairn — `avf-03`
- Cinderholm — `avi-08`
- Greywater — `avg-06`

Useful as a clean, self-contained test world for offline walkers and future level-editor fixtures.

### Tilesets and the blocking mask

All sheets are 2048×512, 16×16, 128×32 = 4096 cells. Index = `y * 128 + x`.

- `eg_tiles.png` — original Enigma pics1.
- Identity remake and Koyo Isles themed variants.
- Emberhold series (`em_tiles` through `em_tiles4.png`): art that follows the type-0 mask (walls on 22, grates on 20, water 11, lava 12, chairs 3, beds 4/5).

**Blocking is not in the pixels.** The mask is a 4096-byte `types.bin`:

- Body cannot enter type 20 (throw-through) or 22 (blocking).
- A throw cannot enter 22; it can enter 20.
- Other types (0, water 11, lava 12, chairs 3, beds 4/5, …) are enterable.
- Feet cell is `floor(px / 16)`, `floor(py / 16)`.

The tiledef plugin (SKILL.md + assets + `tiletype.py`) is included in the archive. Do not treat the client line `pics1.png,,0` as the mask.

### Enigma overworld

25×25 grid (`eg{a-y}-{01-25}`, 625 levels). Player start house is `onlinestartlocal.graal`, which doors onto `egk-10.graal`. Stitched maps (original and remake tileset) and the level-name grid are in the zip. The full life-size 25600×25600 stitch is also present as row strips.

## Relation to this repository

These experiments were exploratory walkers and art passes. They do not add new protocol facts or decompile material. The format notes they produced have already been folded into the main corpus (levels, tile types, door resolution). The archive exists so later work (especially Seihai level-editor expansion) can pull clean test levels, a known-good mask, and the tileset variants without reconstructing them.

## Suggested use for Seihai

- Drop `avg-05.nw` (and the rest of Avelan) into an assets folder for offline editor and walker tests.
- Use `types.bin` as a fixture when validating tiledef / arrays.dat loaders.
- The Emberhold tilesets are drop-in 2048×512 sheets that already respect the mask.

No further maintenance is planned for the Ember trees themselves.
