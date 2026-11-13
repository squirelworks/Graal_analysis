"""64 by 64 BOARD loader.

Evidence: teardown assets.md, a client routine and a client routine
. Alphabet at file offset 5536006.
"""

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BOARD = 64
MAGICS = ("GLEVNW01", "GR-V1.00", "GR-V1.01", "GR-V1.02", "GR-V1.03")


class Level:
    def __init__(self) -> None:
        self.magic = ""
        self.tiles = [0] * (BOARD * BOARD)
        self.sections: list[str] = []

    def load(self, text: str) -> None:
        self.magic = text[:8]
        if self.magic not in MAGICS:
            raise ValueError("header %r is not accepted by a client routine" % self.magic)
        self.tiles = [0] * (BOARD * BOARD)
        self.sections = []
        for line in text.splitlines():
            parts = line.split()
            if not parts:
                continue
            self.sections.append(parts[0])
            if parts[0] == "BOARD" and len(parts) >= 6:
                self._board(int(parts[1]), int(parts[2]), int(parts[3]), parts[5])

    def _board(self, x: int, y: int, width: int, data: str) -> None:
        if not (x < BOARD and 0 <= y < BOARD and width > 0 and x + width <= BOARD):
            return
        if len(data) < width * 2:
            return
        for n in range(width):
            a = ALPHABET.find(data[n * 2])
            b = ALPHABET.find(data[n * 2 + 1])
            if a < 0 or b < 0:
                break
            self.tiles[y * BOARD + x + n] = (a << 6) + b

    def tile(self, x: int, y: int) -> int | None:
        if 0 <= x < BOARD and 0 <= y < BOARD:
            return self.tiles[y * BOARD + x]
        return None
