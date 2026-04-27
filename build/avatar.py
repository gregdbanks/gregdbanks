"""Generate a 460x460 PNG avatar from the pixelated logo grid in player_card.

GitHub user avatars cap at 460x460 and are displayed as a circle, so the grid
is centered with breathing room and a transparent background. Output: PNG that
the user uploads via Settings -> Profile -> Edit on the picture.
"""
from __future__ import annotations
from pathlib import Path

from PIL import Image

from palette import BG, INK


GRID = [
    ".............##................",
    "..........####...###...........",
    ".........#####..####...........",
    ".......############............",
    "......####################.....",
    "......####################.....",
    ".....####################......",
    "....#######################....",
    "..#.########################...",
    ".############################..",
    ".#############################.",
    ".#############################.",
    ".##############################",
    "###############################",
    "###############################",
    "###############################",
    "##########..........###########",
    "#######................########",
    "#####....................######",
    "####......................#####",
    "###........................####",
    "###.........................###",
    "##.....####........####.....##.",
    "##...##...##......##...##...##.",
    "##...#......#....#......#...##.",
    ".#..#.......######.......#...#.",
    "...##........####........###...",
    "...##........#..#........##....",
    "....#........#..##.......#.....",
    ".....#......#....#......##.....",
    ".....##....##.....#....##......",
    ".......####........#####.......",
]

GRID_W = len(GRID[0])  # 31
GRID_H = len(GRID)      # 32
SCALE = 11              # 32 * 11 = 352 px — fits inside GitHub's circle crop
CANVAS = 460            # GitHub avatar cap
OUT = Path(__file__).parent.parent / "assets" / "avatar.png"


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def build(background: tuple[int, int, int, int]) -> Image.Image:
    img = Image.new("RGBA", (CANVAS, CANVAS), background)
    pixels = img.load()
    ink = (*hex_to_rgb(INK), 255)

    # Center the grid horizontally and vertically.
    grid_px_w = GRID_W * SCALE
    grid_px_h = GRID_H * SCALE
    off_x = (CANVAS - grid_px_w) // 2
    off_y = (CANVAS - grid_px_h) // 2

    for ry, row in enumerate(GRID):
        for rx, ch in enumerate(row):
            if ch != "#":
                continue
            x0 = off_x + rx * SCALE
            y0 = off_y + ry * SCALE
            for dy in range(SCALE):
                for dx in range(SCALE):
                    pixels[x0 + dx, y0 + dy] = ink
    return img


def build_svg(background: str | None) -> str:
    """SVG version — vector, infinitely scalable, for non-GitHub-avatar uses."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {GRID_W} {GRID_H}" '
        f'width="460" height="460" shape-rendering="crispEdges">'
    ]
    if background:
        parts.append(f'<rect width="{GRID_W}" height="{GRID_H}" fill="{background}"/>')
    for ry, row in enumerate(GRID):
        for rx, ch in enumerate(row):
            if ch == "#":
                parts.append(f'<rect x="{rx}" y="{ry}" width="1" height="1" fill="{INK}"/>')
    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)

    bg = (*hex_to_rgb(BG), 255)
    build(bg).save(OUT)
    transparent_png = OUT.with_name("avatar-transparent.png")
    build((0, 0, 0, 0)).save(transparent_png)

    svg_solid = OUT.with_name("avatar.svg")
    svg_solid.write_text(build_svg(BG), encoding="utf-8")
    svg_transparent = OUT.with_name("avatar-transparent.svg")
    svg_transparent.write_text(build_svg(None), encoding="utf-8")

    for p in (OUT, transparent_png, svg_solid, svg_transparent):
        print(f"wrote {p} ({p.stat().st_size} bytes)")
