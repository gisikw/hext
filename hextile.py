import re
from dataclasses import dataclass

LABEL_VERTICAL_OFFSET = -8

@dataclass(frozen=True)
class Hextile:
    row: int
    col: int
    terrain: str
    label: str

    def parse(line):
        match = re.match(r'(\d{2})(\d{2})\s+(\w+)\s*(\".*\")?', line.strip())
        if match:
            col, row, terrain, label = match.groups()
            return Hextile(row=int(row), col=int(col), terrain=terrain, label=label.strip('"') if label else None)

    def origin(self, size):
        hex_width = 2 * size
        hex_height = size * (3 ** 0.5)
        x = self.col * hex_width * 0.75
        y = self.row * hex_height + 0.5 * hex_height * (self.col % 2)
        return x, y

    def label_coord(self, size):
        x, y = self.origin(size)
        return x, y + size * (5/6) + LABEL_VERTICAL_OFFSET

    def vertices(self, size):
        x, y = self.origin(size)
        return [
            (x + size * p[0], y - size * p[1])
            for p in [
                (1.0, 0.0),
                (0.5, 0.8660254037844386),
                (-0.5, 0.8660254037844386),
                (-1.0, 0.0),
                (-0.5, -0.8660254037844386),
                (0.5, -0.8660254037844386),
            ]
        ]
