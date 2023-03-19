import re
import yaml
from dataclasses import dataclass

with open("terrain.yml", 'r') as f:
    terrain_colors = yaml.safe_load(f)

LABEL_VERTICAL_OFFSET = -8

@dataclass(frozen=True)
class Hextile:
    row: int
    col: int
    terrain: str = None
    label: str = None

    def parse(line):
        match = re.match(r'(\d{2})(\d{2})\s+(\w+)\s*(\".*\")?', line)
        if match:
            col, row, terrain, label = match.groups()
            return Hextile(row=int(row), col=int(col), terrain=terrain, label=label.strip('"') if label else None)

    def origin(self, size):
        hex_width = 2 * size
        hex_height = size * (3 ** 0.5)
        x = self.col * hex_width * 0.75
        y = self.row * hex_height + 0.5 * hex_height * (self.col % 2)
        return x, y

    def midpoint(self, other, size):
        x, y = self.origin(size)
        x2, y2 = other.origin(size)
        return ((x + x2) / 2, (y + y2) / 2)

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

    def draw(self, dwg, size):
        hex_color = terrain_colors.get(self.terrain, 'white')
        dwg.add(dwg.polygon(self.vertices(size), fill=hex_color, stroke='black', stroke_width=2))
        if self.label:
            font_size = 12
            dwg.add(dwg.text(self.label, insert=self.label_coord(size), text_anchor='middle', alignment_baseline='middle', font_size=f'{font_size}px', fill='none', stroke='white', stroke_width=4, stroke_linejoin='round', stroke_linecap='round'))
            dwg.add(dwg.text(self.label, insert=self.label_coord(size), text_anchor='middle', alignment_baseline='middle', font_size=f'{font_size}px', fill='black'))
