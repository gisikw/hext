import re
from dataclasses import dataclass
from hext.hextile import Hextile

@dataclass(frozen=True)
class Path:
    hexes: list
    style: str

    def parse(line):
        match = re.match(r'(\d{4}(?:-\d{4})+)\s+(\w+)', line)
        if match:
            sequence, style = match.groups()
            return Path(hexes=[Hextile(col=int(coord[0:2]),row=int(coord[2:4])) for coord in sequence.split('-')], style=style)

    def draw(self, dwg, size):
        if len(self.hexes) < 2:
            return

        hex_path = []

        start_hex = self.hexes[0]
        hex_path.extend(['M', start_hex.origin(size)])
        hex_path.extend(['L', start_hex.midpoint(self.hexes[1], size)])

        for index in range(1, len(self.hexes) - 1):
            current_hex = self.hexes[index]
            exit_point = current_hex.midpoint(self.hexes[index + 1], size)
            hex_path.extend(['Q', current_hex.origin(size), exit_point])

        hex_path.extend(['L', self.hexes[-1].origin(size)])

        style = {
            'stroke': self.style,
            'stroke_width': 4,
            'fill': 'none'
        }

        dwg.add(dwg.path(hex_path, **style))
