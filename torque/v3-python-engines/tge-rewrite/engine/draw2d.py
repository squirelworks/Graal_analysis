"""Flat 2D grid.

Evidence: start2D() is eval'd by a client routine. GuiBitmapCtrl and
GuiShowImgCtrl are the blit-shaped controls in used.md. The cell value is
the uint16 from level.py. No texture atlas was recovered, so a tile is
drawn as four hex digits and the player as @.
"""

from __future__ import annotations

from level import BOARD, Level


class Drawer:
    def __init__(self, view: int = 9) -> None:
        self.view = view
        self.started = False

    def start2d(self) -> None:
        self.started = True

    def frame(self, level: Level | None, px: int, py: int, facing: str) -> str:
        if not self.started:
            return "(2D not started)"
        half = self.view // 2
        rows = ["2D %s player %d,%d facing %s" % (
            level.magic if level else "no-level", px, py, facing)]
        for y in range(py - half, py + half + 1):
            cells = []
            for x in range(px - half, px + half + 1):
                if x == px and y == py:
                    cells.append(" @ ")
                elif level is None or not (0 <= x < BOARD and 0 <= y < BOARD):
                    cells.append("###")
                else:
                    cells.append("%03X" % (level.tile(x, y) or 0))
            rows.append(" ".join(cells))
        return "\n".join(rows)
