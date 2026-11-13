"""Local actions a 2.05 client performs, from squirelworks/Graal_analysis.

The Mac v3 image registers doA, doS, doD, setChat, openServerList and
connectToSelectedServer. It does not, in the notes we have, show these
tile tables. The tables are the 2.05 / 2.22 study:

- carry-hide-and-glove.md and board-respawn.md: lift entries and leftovers
- decomp-findings-2026-10-25-l/03-cut-lift-chest.md: A tries lift first;
  a chest is the closed 2x2 1784 1785 / 1800 1801, opened to 829 830 / 845 846
- sign-panel.md: three lines a page; the map key closes the panel
- decomp-findings-2026-10-25-e/01-request-lists.md: a missing name is asked
  once, and at most four names go out together

Glove power starts at 1, so the first three lift entries work (bush, sign,
pot). The stone is the fourth entry and needs glove 2. A throw does not
write the board. Clients do not regrow a lifted object.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from level import Level

# (name, four tiles top-left, top-right, bottom-left, bottom-right, leftover, carry sprite)
LIFTS = (
    ("bush", (2, 3, 18, 19), (677, 678, 693, 694), 261),
    ("sign", (512, 513, 528, 529), (1802, 1803, 1818, 1819), 267),
    ("pot", (684, 685, 700, 701), (1770, 1771, 1786, 1787), 265),
    ("stone", (34, 35, 50, 51), (1834, 1835, 1850, 1851), 263),
    ("blackstone", (990, 991, 1006, 1007), (1834, 1835, 1850, 1851), 239),
)
HIDE_SPRITES = {261, 263, 239}
CLOSED_CHEST = (1784, 1785, 1800, 1801)
OPEN_CHEST = (829, 830, 845, 846)
DELTAS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


@dataclass
class Carry:
    name: str
    sprite: int
    hidden: bool = False


class FileStore:
    """PLI_WANTFILE queue. The send itself waits on the session cipher."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.wanted: list[str] = []
        self.settled: set[str] = set()

    def request(self, name: str) -> str:
        path = self.root / name
        if path.is_file() or name in self.settled:
            return "have %s" % name
        if name in self.wanted:
            return "waiting %s" % name
        self.wanted.append(name)
        if self.wanted.index(name) < 4:
            return "ask %s" % name
        return "queued %s" % name

    def write(self, name: str, data: bytes) -> str:
        dest = self.root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        if name in self.wanted:
            self.wanted.remove(name)
        self.settled.add(name)
        return "stored %s" % name


class LocalPlay:
    def __init__(self) -> None:
        self.glove = 1
        self.carry: Carry | None = None
        self.reading: list[str] | None = None
        self.page = 0
        self.editing = False
        self.server_list_open = False
        self.player_list_open = False
        self.selected_server = ""
        self.servers: list[str] = []
        self.rows: list[dict] = []
        self.selected_row: dict | None = None
        self.host = ""
        self.port: int | None = None
        self.players: list[str] = []
        self.chat = ""
        self.last = ""
        self.files = FileStore(Path(__file__).resolve().parent / "store")

    def status(self) -> list[str]:
        lines = []
        if self.carry is not None:
            state = "hidden" if self.carry.hidden else "carrying"
            lines.append("%s %s" % (state, self.carry.name))
        if self.reading is not None:
            start = self.page * 3
            lines.append("sign:")
            lines.extend(self.reading[start:start + 3] or ["(end)"])
        if self.chat:
            lines.append("chat: %s" % self.chat)
        if self.editing:
            lines.append("editor")
        if self.server_list_open:
            lines.append("servers: %s" % (", ".join(self.servers) or "(none)"))
            if self.selected_server:
                lines.append("selected: %s" % self.selected_server)
        if self.player_list_open:
            lines.append("players: %s" % (", ".join(self.players) or "(none)"))
        if self.last:
            lines.append(self.last)
        return lines

    def hidden_scale(self) -> float:
        """2.05 multiplies the walk by 0.2 while hidden. 0.5 * 0.2 is 0.1."""
        if self.carry is not None and self.carry.hidden:
            return 0.2
        return 1.0

    def do_a(self, level: Level | None, x: float, y: float, facing: str) -> str:
        if self.reading is not None:
            return self._turn_page()
        if self.carry is not None and self.carry.hidden:
            name = self.carry.name
            self.carry.hidden = False
            self.last = "out from under %s" % name
            return self.last
        if level is None:
            self.last = "doA"
            return self.last
        px, py = _probe(x, y, facing)
        lifted = self._lift(level, px, py)
        if lifted:
            return lifted
        opened = self._chest(level, px, py)
        if opened:
            return opened
        return self._sign(level, px, py)

    def do_s(self) -> str:
        if self.reading is not None:
            return self._turn_page()
        if self.carry is None:
            self.last = "doS"
            return self.last
        name = self.carry.name
        self.carry = None
        self.last = "throw %s" % name
        return self.last

    def do_d(self) -> str:
        if self.reading is not None:
            return self._turn_page()
        if self.carry is None or self.carry.sprite not in HIDE_SPRITES:
            self.last = "doD"
            return self.last
        self.carry.hidden = not self.carry.hidden
        self.last = "hide" if self.carry.hidden else "unhide"
        return self.last

    def do_m(self) -> str:
        if self.reading is not None:
            self.reading = None
            self.last = "sign closed"
            return self.last
        self.last = "doM"
        return self.last

    def _turn_page(self) -> str:
        assert self.reading is not None
        self.page += 1
        if self.page * 3 >= len(self.reading):
            self.reading = None
            self.last = "sign closed"
        else:
            self.last = "sign page %d" % (self.page + 1)
        return self.last

    def _lift(self, level: Level, px: int, py: int) -> str:
        limit = self.glove + 2
        for name, tiles, leaves, sprite in LIFTS[:limit]:
            origin = _match(level, px, py, tiles)
            if origin is None:
                continue
            ox, oy = origin
            _paint(level, ox, oy, leaves)
            self.carry = Carry(name, sprite)
            self.last = "lift %s" % name
            return self.last
        return ""

    def _chest(self, level: Level, px: int, py: int) -> str:
        origin = _match(level, px, py, CLOSED_CHEST)
        if origin is not None:
            _paint(level, origin[0], origin[1], OPEN_CHEST)
            self.last = "open chest"
            return self.last
        for chest in level.chests:
            if chest.opened or chest.x != px or chest.y != py:
                continue
            chest.opened = True
            self.last = "open chest %s" % chest.item
            if chest.sign >= 0 and chest.sign < len(level.signs):
                self._show(level.signs[chest.sign].text)
            return self.last
        return ""

    def _sign(self, level: Level, px: int, py: int) -> str:
        for sign in level.signs:
            if sign.x == px and sign.y == py and not (sign.x == 0 and sign.y == 0):
                self._show(sign.text)
                self.last = "read sign"
                return self.last
        self.last = "doA"
        return self.last

    def _show(self, text: str) -> None:
        self.reading = text.split("\n") if text else [""]
        self.page = 0


def _probe(x: float, y: float, facing: str) -> tuple[int, int]:
    dx, dy = DELTAS.get(facing, (0, 1))
    return math.floor(x) + dx, math.floor(y) + dy


def _match(level: Level, px: int, py: int, tiles: tuple[int, int, int, int]) -> tuple[int, int] | None:
    here = level.tile(px, py)
    offsets = ((0, 0), (1, 0), (0, 1), (1, 1))
    for index, (ox, oy) in enumerate(offsets):
        if here != tiles[index]:
            continue
        left, top = px - ox, py - oy
        if all(level.tile(left + ax, top + ay) == tiles[n] for n, (ax, ay) in enumerate(offsets)):
            return left, top
    return None


def _paint(level: Level, x: int, y: int, tiles: tuple[int, int, int, int]) -> None:
    level.put(x, y, tiles[0])
    level.put(x + 1, y, tiles[1])
    level.put(x, y + 1, tiles[2])
    level.put(x + 1, y + 1, tiles[3])
