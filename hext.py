#!/usr/bin/env python3

import svgwrite
import sys
import cairosvg
from hextile import Hextile
from path import Path

def parse_hexmap_input(input_file):
    hexmap = []
    paths = []
    with open(input_file, 'r') as f:
        for line in f:
            tile = Hextile.parse(line.strip())
            if tile:
                hexmap.append(tile)
            else:
                path = Path.parse(line.strip())
                if path:
                    paths.append(path)
    return hexmap, paths

def get_map_size(hexmap, size):
    max_row = max([h.row for h in hexmap]) + 1
    max_col = max([h.col for h in hexmap]) + 1
    hex_width = 2 * size
    hex_height = size * (3 ** 0.5)
    width = int(hex_width * max_col * 0.75 + hex_width * 0.25)
    height = int(hex_height * (max_row + 0.5))
    return width, height

def draw_hexmap_svg(hexmap, paths, output_file, size=100):
    width, height = get_map_size(hexmap, size)
    dwg = svgwrite.Drawing(output_file, (width, height), debug=True)
    for tile in hexmap:
        tile.draw(dwg, size)
    for path in paths:
        path.draw(dwg, size)
    dwg.save()
    return output_file

def main(input_file):
    output_file_base = input_file.rsplit('.', 1)[0]
    svg_output_file = f'{output_file_base}.svg'
    png_output_file = f'{output_file_base}.png'

    hexmap, paths = parse_hexmap_input(input_file)
    svg_output = draw_hexmap_svg(hexmap, paths, svg_output_file)
    cairosvg.svg2png(url=svg_output, write_to=png_output_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: hext input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
