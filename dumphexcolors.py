#!/usr/bin/env python3

from perdolingtools import paletbars, exp_svg
from collections import Counter
import re
import argparse

def extract_colors(infile):
    with open(infile, "r") as f:
        s = f.read()
        matches = re.findall("(#[0-9A-Fa-f]{6})", s)
        color_counter = Counter(matches)
        # return colors, numbers
        return list(zip(*color_counter.most_common()))


def export_palete_svg(palete, text=None, outimage='/tmp/paleteimg.svg'):

    cols = len(palete)
    BAR_WIDTH = 82
    BAR_WIDTH_GAP = 26
    BAR_HEIGHT = 50
    BAR_HEIGHT_GAP = 5
    BAR_X_OFF = BAR_WIDTH_GAP
    BAR_Y_OFF = 25
    i_width = cols * (BAR_WIDTH + BAR_WIDTH_GAP) + 2 * BAR_X_OFF
    i_height = BAR_HEIGHT + BAR_HEIGHT_GAP + BAR_Y_OFF * 2

    # (BAR_X_OFF + i * (BAR_WIDTH + BAR_WIDTH_GAP), BAR_Y_OFF,
    #  BAR_X_OFF + i * (BAR_WIDTH + BAR_WIDTH_GAP) + BAR_WIDTH,
    #  BAR_Y_OFF + BAR_HEIGHT), fill = c)

    if not text:
        text = palete

    bodys = "\n".join([f'\t<rect'\
                        f' x="{BAR_X_OFF + i * (BAR_WIDTH + BAR_WIDTH_GAP)}"' 
                        f' y="{BAR_Y_OFF}"'
                        f' width="{BAR_WIDTH}"'
                        f' height="{BAR_HEIGHT}"'
                        f' fill="{c}"/>'
                     for i, c in enumerate(palete)])
    text = "\n".join(
        [   f'\t<text x="{BAR_X_OFF + i * (BAR_WIDTH + BAR_WIDTH_GAP) + BAR_WIDTH // 2}"'
            f' y="{BAR_Y_OFF + BAR_HEIGHT + 3 * BAR_HEIGHT_GAP}"'
            f' text-anchor="middle">'
            f'{c}'
            f'</text>'
            for i, c in enumerate(text[:len(palete)])])

    svg_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    version="1.1" baseProfile="full"
    width="{i_width}" height="{i_height}"
    viewBox="0 0 {i_width} {i_height}">
{bodys}
{text}
</svg>"""

    with open(outimage, "w") as out:
        out.write(svg_str)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="dump all hex colors from file")
    parser.add_argument("--inputfile", "-i", type=str, help="some file to process")
    parser.add_argument("--outputimage", "-o", type=str, help='dump colors as svg', default='/tmp/palette.svg')
    parser.add_argument("--tostdo", "-s", help='dump colors to console', action="store_true")
    parser.add_argument("--count", "-c", help='dump colors with counts to console', action="store_true")
    args = parser.parse_args()

    colors, counts = extract_colors(args.inputfile)
    export_palete_svg(colors, outimage=args.outputimage)

    if args.count:
        print(" COLOR  │ COUNT\n────────┼────────")
        for color, num in zip(colors, counts):
            print(f"{color} │ {num}")

    elif args.tostdo:
        print(*colors, sep="\n")