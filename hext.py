#!/usr/bin/env python3

import svgwrite
import re
import sys
import cairosvg
import yaml

LABEL_BOTTOM_PADDING = 4

with open("terrain.yml", 'r') as f:
    terrain_colors = yaml.safe_load(f)

def parse_hexmap_input(input_file):
    hexmap = []
    with open(input_file, 'r') as f:
        for line in f:
            match = re.match(r'(\d{2})(\d{2})\s+(\w+)\s*(\".*\")?', line.strip())
            if match:
                col, row, terrain, label = match.groups()
                hexmap.append((int(row), int(col), terrain, label.strip('"') if label else None))
    return hexmap

def hex_to_pixel(size, row, col):
    hex_width = 2 * size
    hex_height = size * (3 ** 0.5)
    
    x = col * hex_width * 0.75
    y = row * hex_height + 0.5 * hex_height * (col % 2)
    return x, y

def hex_points(size, x, y):
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

def draw_hexmap_svg(hexmap, output_file, size=100):
    max_row = max([h[0] for h in hexmap]) + 1
    max_col = max([h[1] for h in hexmap]) + 1

    hex_width = 2 * size
    hex_height = size * (3 ** 0.5)

    width = int(hex_width * max_col * 0.75 + hex_width * 0.25)
    height = int(hex_height * (max_row + 0.5))

    dwg = svgwrite.Drawing(output_file, (width, height), debug=True)

    for row, col, terrain, label in hexmap:
        x, y = hex_to_pixel(size, row, col)
        hex_color = terrain_colors.get(terrain, 'white')

        dwg.add(dwg.polygon(hex_points(size, x, y), fill=hex_color, stroke='black', stroke_width=2))

        if label:
            label_x = x
            label_y = y + size * (5/6) - LABEL_BOTTOM_PADDING
            font_size = 12
            dwg.add(dwg.text(label, insert=(label_x, label_y), text_anchor='middle', alignment_baseline='middle', font_size=f'{font_size}px', fill='none', stroke='white', stroke_width=4, stroke_linejoin='round', stroke_linecap='round'))
            dwg.add(dwg.text(label, insert=(label_x, label_y), text_anchor='middle', alignment_baseline='middle', font_size=f'{font_size}px', fill='black'))

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
