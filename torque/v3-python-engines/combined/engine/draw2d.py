"""Flat 2D grid.

Evidence: start2D() is eval'd by a client routine. GuiBitmapCtrl and
GuiShowImgCtrl are the blit-shaped controls in used.md. The cell value is
the uint16 from level.py. No texture atlas was recovered, so a tile is
drawn as three hex digits and the player as @.
"""

from __future__ import annotations

import math

from level import BOARD, Level


class Drawer:
    def __init__(self, view: int = 9) -> None:
        self.view = view
        self.started = False

    def start2d(self) -> None:
        self.started = True

    def frame(self, level: Level | None, px: float, py: float, facing: str,
              remotes: dict | None = None) -> str:
        if not self.started:
            return "(2D not started)"
        half = self.view // 2
        cx, cy = math.floor(px), math.floor(py)
        occupied: dict[tuple[int, int], int] = {}
        for player in (remotes or {}).values():
            if "x" not in player or "y" not in player:
                continue
            occupied[(math.floor(player["x"]), math.floor(player["y"]))] = player["id"]
        rows = ["2D %s player %.1f,%.1f facing %s" % (
            level.magic if level else "no-level", px, py, facing)]
        for y in range(cy - half, cy + half + 1):
            cells = []
            for x in range(cx - half, cx + half + 1):
                if x == cx and y == cy:
                    cells.append(" @ ")
                elif (x, y) in occupied:
                    cells.append("%03d" % (occupied[(x, y)] % 1000))
                elif level is None or not (0 <= x < BOARD and 0 <= y < BOARD):
                    cells.append("###")
                else:
                    cells.append("%03X" % (level.tile(x, y) or 0))
            rows.append(" ".join(cells))
        return "\n".join(rows)
