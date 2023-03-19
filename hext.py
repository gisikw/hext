#!/usr/bin/env python3

import svgwrite
import sys
import cairosvg
import yaml
from hextile import Hextile

with open("terrain.yml", 'r') as f:
    terrain_colors = yaml.safe_load(f)

def parse_hexmap_input(input_file):
    hexmap = []
    with open(input_file, 'r') as f:
        for line in f:
            tile = Hextile.parse(line.strip())
            if tile:
                hexmap.append(tile)
    return hexmap

def get_map_size(hexmap, size):
    max_row = max([h.row for h in hexmap]) + 1
    max_col = max([h.col for h in hexmap]) + 1
    hex_width = 2 * size
    hex_height = size * (3 ** 0.5)
    width = int(hex_width * max_col * 0.75 + hex_width * 0.25)
    height = int(hex_height * (max_row + 0.5))
    return width, height

def draw_hexmap_svg(hexmap, output_file, size=100):
    width, height = get_map_size(hexmap, size)
    dwg = svgwrite.Drawing(output_file, (width, height), debug=True)
    for tile in hexmap:
        x, y = tile.origin(size)
        hex_color = terrain_colors.get(tile.terrain, 'white')
        dwg.add(dwg.polygon(tile.vertices(size), fill=hex_color, stroke='black', stroke_width=2))
        if tile.label:
            font_size = 12
            dwg.add(dwg.text(tile.label, insert=tile.label_coord(size), text_anchor='middle', alignment_baseline='middle', font_size=f'{font_size}px', fill='none', stroke='white', stroke_width=4, stroke_linejoin='round', stroke_linecap='round'))
            dwg.add(dwg.text(tile.label, insert=tile.label_coord(size), text_anchor='middle', alignment_baseline='middle', font_size=f'{font_size}px', fill='black'))

    dwg.save()
    return output_file

def main(input_file):
    output_file_base = input_file.rsplit('.', 1)[0]
    svg_output_file = f'{output_file_base}.svg'
    png_output_file = f'{output_file_base}.png'

    hexmap = parse_hexmap_input(input_file)
    svg_output = draw_hexmap_svg(hexmap, svg_output_file)
    cairosvg.svg2png(url=svg_output, write_to=png_output_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: hext input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
