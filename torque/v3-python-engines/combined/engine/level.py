"""64 by 64 level.

BOARD tiles use the alphabet at file offset 5536006.
SIGN, CHEST, NPC, LINK and BADDY are the section names a client routine compares.
Their field order is the GLEVNW01 record shape from the v2 study
(squirelworks/Graal_analysis formats/glevnw01.txt). The Mac image names
the sections and does not, in the notes we have, spell these fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def _number(text: str) -> bool:
    try:
        float(text)
    except ValueError:
        return False
    return True


def _index(char: str) -> int:
    found = ALPHABET.find(char)
    if found >= 0:
        return found
    if char == "+":
        return 62
    if char == "/":
        return 63
    return -1
BOARD = 64
MAGICS = ("GLEVNW01", "GSERVL01", "GR-V1.00", "GR-V1.01", "GR-V1.02", "GR-V1.03")


def encode_tile(tile: int) -> str:
    """Mac alphabet is 62 characters. Index 62 and 63 are '+' and '/', the
    tail of the GLEVNW01 alphabet in the v2 study, so a tile the 62-character
    string cannot spell still round-trips in this file.
    """
    def one(index: int) -> str:
        if index < len(ALPHABET):
            return ALPHABET[index]
        return "+/"[index - len(ALPHABET)]

    return one((tile >> 6) & 63) + one(tile & 63)


@dataclass
class Sign:
    x: int
    y: int
    text: str


@dataclass
class Chest:
    x: int
    y: int
    item: str
    sign: int
    opened: bool = False


@dataclass
class Npc:
    image: str
    x: float
    y: float
    script: str


@dataclass
class Link:
    dest: str
    x: int
    y: int
    width: int
    height: int
    newx: str
    newy: str


@dataclass
class Baddy:
    x: str
    y: str
    kind: str
    body: str


class Level:
    def __init__(self) -> None:
        self.magic = ""
        self.tiles = [0] * (BOARD * BOARD)
        self.sections: list[str] = []
        self.signs: list[Sign] = []
        self.chests: list[Chest] = []
        self.npcs: list[Npc] = []
        self.links: list[Link] = []
        self.baddies: list[Baddy] = []
        self.raw_blocks: list[str] = field(default_factory=list)

    def load(self, text: str) -> None:
        self.magic = text[:8]
        if self.magic not in MAGICS:
            raise ValueError("header %r is not accepted by a client routine" % self.magic)
        self.tiles = [0] * (BOARD * BOARD)
        self.sections = []
        self.signs = []
        self.chests = []
        self.npcs = []
        self.links = []
        self.baddies = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            parts = lines[i].split()
            if not parts:
                i += 1
                continue
            word = parts[0]
            self.sections.append(word)
            if word == "BOARD" and len(parts) >= 6:
                self._board(int(parts[1]), int(parts[2]), int(parts[3]), parts[5])
            elif word == "LINK" and len(parts) >= 8:
                self.links.append(Link(parts[1], int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]), parts[6], parts[7]))
            elif word == "CHEST" and len(parts) >= 5:
                self.chests.append(Chest(int(parts[1]), int(parts[2]), parts[3], int(parts[4])))
            elif word == "SIGN" and len(parts) >= 3:
                x, y = int(parts[1]), int(parts[2])
                body: list[str] = []
                i += 1
                while i < len(lines) and lines[i].strip() != "SIGNEND":
                    body.append(lines[i])
                    i += 1
                self.signs.append(Sign(x, y, "\n".join(body)))
            elif word == "NPC" and len(parts) >= 4:
                if _number(parts[1]) and _number(parts[2]):
                    self.npcs.append(Npc(parts[3], float(parts[1]), float(parts[2]), ""))
                else:
                    image, x, y = parts[1], float(parts[2]), float(parts[3])
                    body = []
                    i += 1
                    while i < len(lines) and lines[i].strip() != "NPCEND":
                        body.append(lines[i])
                        i += 1
                    self.npcs.append(Npc(image, x, y, "\n".join(body)))
            elif word == "BADDY" and len(parts) >= 4:
                body = []
                i += 1
                while i < len(lines) and lines[i].strip() != "BADDYEND":
                    body.append(lines[i])
                    i += 1
                self.baddies.append(Baddy(parts[1], parts[2], parts[3], "\n".join(body)))
            i += 1

    def _board(self, x: int, y: int, width: int, data: str) -> None:
        if not (x < BOARD and 0 <= y < BOARD and width > 0 and x + width <= BOARD):
            return
        if len(data) < width * 2:
            return
        for n in range(width):
            a = _index(data[n * 2])
            b = _index(data[n * 2 + 1])
            if a < 0 or b < 0:
                break
            self.tiles[y * BOARD + x + n] = (a << 6) + b

    def tile(self, x: int, y: int) -> int | None:
        if 0 <= x < BOARD and 0 <= y < BOARD:
            return self.tiles[y * BOARD + x]
        return None

    def put(self, x: int, y: int, tile: int) -> None:
        if self.tile(x, y) is not None:
            self.tiles[y * BOARD + x] = tile & 0xFFF

    def save(self) -> str:
        """Write GLEVNW01 with the Mac alphabet, so this client can read it back."""
        lines = ["GLEVNW01"]
        for y in range(BOARD):
            row = "".join(encode_tile(self.tiles[y * BOARD + x]) for x in range(BOARD))
            if set(row) != {"0"}:
                lines.append("BOARD 0 %d 64 0 %s" % (y, row))
        for link in self.links:
            lines.append("LINK %s %d %d %d %d %s %s" % (
                link.dest, link.x, link.y, link.width, link.height, link.newx, link.newy))
        for chest in self.chests:
            lines.append("CHEST %d %d %s %d" % (chest.x, chest.y, chest.item, chest.sign))
        for sign in self.signs:
            lines.append("SIGN %d %d" % (sign.x, sign.y))
            if sign.text:
                lines.append(sign.text)
            lines.append("SIGNEND")
        for npc in self.npcs:
            lines.append("NPC %s %s %s" % (npc.image, npc.x, npc.y))
            if npc.script:
                lines.append(npc.script)
            lines.append("NPCEND")
        for baddy in self.baddies:
            lines.append("BADDY %s %s %s" % (baddy.x, baddy.y, baddy.kind))
            if baddy.body:
                lines.append(baddy.body)
            lines.append("BADDYEND")
        return "\n".join(lines) + "\n"
