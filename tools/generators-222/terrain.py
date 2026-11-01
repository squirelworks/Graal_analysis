"""TerrainGenerator (Graal 2.22): plasma world of GLEVNW01 levels.

The window is a GUI. This module is the file it writes, not the window.
A level is 64 rows of tile 0, a 9×9 HEIGHTS block, and an edge LINK where a
neighbour exists. The gmap is the generator form (GENSEED, HEIGHTMAP,
RANDOMSEEDS). `seihai-core` reads the level board and skips these gmap keys.

The field is midpoint displacement on the control grid (one sample every 8
tiles, shared across level edges). The same seed repeats. It is not a
byte-identical replay of the Delphi window: that program was not run.
"""

from nwtext import (
    column_name,
    edge_links,
    heights_block,
    level_text,
    terrain_gmap,
)

STEP = 8


class DelphiRandom:
    """The Delphi LCG the generator was built with. Seed stays in 32 bits."""

    def __init__(self, seed):
        self.seed = int(seed) & 0xFFFFFFFF

    def unit(self):
        self.seed = (self.seed * 0x08088405 + 1) & 0xFFFFFFFF
        return (self.seed / 4294967296.0) * 2.0 - 1.0


def _covered(size):
    span = 1
    while span + 1 < size:
        span *= 2
    return span + 1


def plasma(width, height, seed, base, amplitude, chaos, even_borders):
    """Control-point heights, `width` by `height`, as whole numbers.

    `chaos` multiplies the displacement after each coarser step. With even
    borders the outer ring stays at `base`.
    """
    if width < 2 or height < 2:
        raise ValueError('plasma grid needs at least 2 by 2')
    span = _covered(max(width, height))
    rng = DelphiRandom(seed)
    field = [[int(base) for _ in range(span)] for _ in range(span)]
    if not even_borders:
        for corner in ((0, 0), (0, span - 1), (span - 1, 0), (span - 1, span - 1)):
            field[corner[1]][corner[0]] = int(round(base + rng.unit() * amplitude))
    step = span - 1
    amp = float(amplitude)
    while step > 1:
        half = step // 2
        for y in range(half, span, step):
            for x in range(half, span, step):
                if even_borders and _on_rim(x, y, span):
                    continue
                average = (
                    field[y - half][x - half] + field[y - half][x + half]
                    + field[y + half][x - half] + field[y + half][x + half]
                ) / 4.0
                field[y][x] = int(round(average + rng.unit() * amp))
        for y in range(0, span, half):
            shift = half if (y // half) % 2 == 0 else 0
            for x in range(shift, span, step):
                if even_borders and _on_rim(x, y, span):
                    field[y][x] = int(base)
                    continue
                samples = []
                for dx, dy in ((-half, 0), (half, 0), (0, -half), (0, half)):
                    sx, sy = x + dx, y + dy
                    if 0 <= sx < span and 0 <= sy < span:
                        samples.append(field[sy][sx])
                average = sum(samples) / float(len(samples))
                field[y][x] = int(round(average + rng.unit() * amp))
        amp *= chaos
        step = half
    if even_borders:
        for i in range(span):
            field[0][i] = int(base)
            field[span - 1][i] = int(base)
            field[i][0] = int(base)
            field[i][span - 1] = int(base)
    return [row[:width] for row in field[:height]]


def _on_rim(x, y, span):
    return x == 0 or y == 0 or x == span - 1 or y == span - 1


def control_size(levels_x, levels_y):
    return levels_x * STEP + 1, levels_y * STEP + 1


def generate(world, seed, width=2, height=2, base=0, amplitude=64, chaos=0.5,
             even_borders=False, islands=False, lev_amplitude=None, lev_chaos=None):
    """Return `{filename: text}` for the gmap and each level.

    `islands` forces even borders, which is what the Islands preset is for:
    a low rim around a displaced interior. `lev_amplitude` and `lev_chaos`
    are written as LEVHEIGHT and LEVCHAOS; they default to the map values.
    """
    if width < 1 or height < 1:
        raise ValueError('world size must be at least 1 by 1')
    if islands:
        even_borders = True
    if lev_amplitude is None:
        lev_amplitude = amplitude
    if lev_chaos is None:
        lev_chaos = chaos
    points_x, points_y = control_size(width, height)
    field = plasma(points_x, points_y, seed, base, amplitude, chaos, even_borders)
    names = [
        '%s%s%02d.nw' % (world, column_name(x), y)
        for y in range(height) for x in range(width)
    ]
    rng = DelphiRandom(seed ^ 0xA5A5)
    level_seeds = []
    files = {}
    blank = [0] * (64 * 64)
    for y in range(height):
        for x in range(width):
            level_seeds.append(rng.seed & 0x7FFFFFFF)
            rng.unit()
            window = [
                field[y * STEP + row][x * STEP:(x + 1) * STEP + 1]
                for row in range(STEP + 1)
            ]
            text = level_text(
                blank,
                links=edge_links(names, width, height, x, y),
                extra=heights_block(window),
            )
            files[names[y * width + x]] = text
    rows = [' '.join(str(value) for value in row) for row in field]
    files['%s.gmap' % world] = terrain_gmap(
        world, width, height, seed, base, even_borders, amplitude, chaos,
        lev_amplitude, lev_chaos, rows, level_seeds,
    )
    return files
