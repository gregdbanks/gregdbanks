"""Three sprite variants — same head (the pixelated logo), different bodies.
Renders each to a standalone PNG so the user can pick before committing.
"""
from __future__ import annotations
from pathlib import Path

from PIL import Image

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
from avatar import GRID as HEAD_GRID, hex_to_rgb


# Each body grid is 31 wide so it matches the head width.
# Letters: '#' = ink (parchment), 'B' = body primary, 'A' = body accent,
# 'S' = boots/shadow, 'T' = trim (warm), '.' = transparent.

# Variant 1 — JRPG hero. Tunic, belt, boots, sword glint at the side.
BODY_HERO = [
    "..............###..............",
    "..............###..............",
    ".........BBBBBBBBBBBBB.........",
    ".......BBBBBBBBBBBBBBBBB.......",
    "......BBBBBBBBBBBBBBBBBBB......",
    "......BBBBBABBBBBABBBBBBB......",
    "......BBBBBABBBBBABBBBBBB......",
    ".....BBBBBBBBBBBBBBBBBBBBB.....",
    ".....TTTTTTTTTTTTTTTTTTTTT.....",
    ".....BBBBBBBBBBBBBBBBBBBBB.....",
    "......BBBBBBBBBBBBBBBBBBB......",
    "......BBBBB.......BBBBBB.......",
    ".....BBBBB.........BBBBB.......",
    ".....BBBB...........BBBB.......",
    ".....SSSS...........SSSS.......",
    "....SSSSSS.........SSSSSS......",
]

# Variant 2 — Casual developer. T-shirt + jeans, hands in pockets.
BODY_DEV = [
    "..............###..............",
    ".............#####.............",
    "..........BBBBBBBBBBB..........",
    ".........BBBBBBBBBBBBB.........",
    "........BBBBBBBBBBBBBBB........",
    "........BBBBBBBBBBBBBBB........",
    "........BBBBBBBBBBBBBBB........",
    "........BBBBBBBBBBBBBBB........",
    "........BBBBBBBBBBBBBBB........",
    "........BBBBBBBBBBBBBBB........",
    ".........AAAAAAAAAAAAA.........",
    ".........AAAAA.AAAAAAA.........",
    ".........AAAA...AAAAAA.........",
    ".........AAAA...AAAAAA.........",
    ".........AAAA...AAAAAA.........",
    "........SSSSS...SSSSSSS........",
]

# Variant 3 — Heroic / armored. Cape behind, pauldrons, chest plate.
BODY_KNIGHT = [
    "..............###..............",
    "..............###..............",
    "....AAAA..BBBBBBBBBBB..AAAA....",
    "...AAAAA.BBBBBBBBBBBBB.AAAAA...",
    "..AAAAAABBBBBBBBBBBBBBBAAAAAA..",
    "..AAAAAABBBBBTTTTTBBBBBAAAAAA..",
    "..AAAAAABBBBTTTTTTTBBBBAAAAAA..",
    "...AAAA.BBBBBBTTTBBBBBB.AAAA...",
    "...AAAA.BBBBBBBBBBBBBBB.AAAA...",
    "....AAA.TTTTTTTTTTTTTTT.AAA....",
    "....AAA.BBBBBBBBBBBBBBB.AAA....",
    ".....AA.BBBBB.....BBBBB.AA.....",
    ".....AA.BBBBB.....BBBBB.AA.....",
    "........BBBB.......BBBB........",
    "........SSSS.......SSSS........",
    ".......SSSSSS.....SSSSSS.......",
]


def hex_rgba(h: str, a: int = 255) -> tuple[int, int, int, int]:
    return (*hex_to_rgb(h), a)


def render_sprite(body_grid: list[str], colors: dict[str, str], out_path: Path,
                  scale: int = 9, bg: str = BG) -> None:
    head_h = len(HEAD_GRID)
    head_w = len(HEAD_GRID[0])
    body_h = len(body_grid)
    grid_h = head_h + body_h
    grid_w = head_w

    # Add side margin so corners don't hug the canvas.
    margin = 2
    canvas_w = (grid_w + margin * 2) * scale
    canvas_h = (grid_h + margin * 2) * scale

    img = Image.new("RGBA", (canvas_w, canvas_h), hex_rgba(bg))
    px = img.load()

    cmap_head = {"#": hex_rgba(INK)}
    cmap_body = {k: hex_rgba(v) for k, v in colors.items()}
    cmap_body["#"] = hex_rgba(INK)  # neck flows from head ink

    def paint(grid, y_off):
        for ry, row in enumerate(grid):
            for rx, ch in enumerate(row):
                color = cmap_head.get(ch) if grid is HEAD_GRID else cmap_body.get(ch)
                if not color:
                    continue
                x0 = (rx + margin) * scale
                y0 = (ry + y_off + margin) * scale
                for dy in range(scale):
                    for dx in range(scale):
                        px[x0 + dx, y0 + dy] = color

    paint(HEAD_GRID, 0)
    paint(body_grid, head_h)

    img.save(out_path)


PRESETS = {
    "hero": {
        "grid": BODY_HERO,
        "colors": {"B": PRIM, "A": ACC2, "S": SHADOW, "T": WARN},
    },
    "dev": {
        "grid": BODY_DEV,
        "colors": {"B": ACC2, "A": DIM, "S": SHADOW},
    },
    "knight": {
        "grid": BODY_KNIGHT,
        "colors": {"B": PRIM, "A": ACC1, "T": WARN, "S": SHADOW},
    },
}


if __name__ == "__main__":
    desktop = Path("/Users/gregbanks/Desktop")
    assets = Path(__file__).parent.parent / "assets"
    for name, cfg in PRESETS.items():
        out = desktop / f"sprite-{name}.png"
        render_sprite(cfg["grid"], cfg["colors"], out)
        also = assets / f"sprite-{name}.png"
        render_sprite(cfg["grid"], cfg["colors"], also)
        print(f"wrote {out}")
