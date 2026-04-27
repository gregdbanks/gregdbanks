"""JRPG-style status panel: portrait, stats, bars, blinking cursor."""
from __future__ import annotations
from pathlib import Path

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
import pixfont

W, H = 880, 380
OUT = Path(__file__).parent.parent / "assets" / "player-card.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def panel(x, y, w, h, border=PRIM, body=PANEL, bw=4):
    out = []
    out.append(rect(x, y, w, h, body))
    out.append(rect(x, y, w, bw, border))
    out.append(rect(x, y + h - bw, w, bw, border))
    out.append(rect(x, y, bw, h, border))
    out.append(rect(x + w - bw, y, bw, h, border))
    # corner pixels (chamfer)
    out.append(rect(x, y, bw, bw, BG))
    out.append(rect(x + w - bw, y, bw, bw, BG))
    out.append(rect(x, y + h - bw, bw, bw, BG))
    out.append(rect(x + w - bw, y + h - bw, bw, bw, BG))
    out.append(rect(x + bw, y + bw, bw, bw, border))
    out.append(rect(x + w - 2 * bw, y + bw, bw, bw, border))
    out.append(rect(x + bw, y + h - 2 * bw, bw, bw, border))
    out.append(rect(x + w - 2 * bw, y + h - 2 * bw, bw, bw, border))
    return "".join(out)


def stat_bar(x, y, w, h, pct, fill, label, value, label_color=INK):
    """A labeled progress bar in retro RPG style."""
    out = []
    # label above
    out.append(pixfont.render(label, x, y - 14, 2, label_color))
    # value (right-aligned-ish above bar)
    val_w = pixfont.width(value, 2)
    out.append(pixfont.render(value, x + w - val_w, y - 14, 2, INK))
    # bar housing
    out.append(rect(x, y, w, h, SHADOW))
    out.append(rect(x + 2, y + 2, w - 4, h - 4, DIM))
    # fill segments — pixel-segmented like classic JRPG bars
    seg_w = 6
    gap = 2
    inner_w = w - 8
    fill_px = int(inner_w * pct / 100)
    n_segs = fill_px // (seg_w + gap)
    for i in range(n_segs):
        out.append(rect(x + 4 + i * (seg_w + gap), y + 4, seg_w, h - 8, fill))
    # tip highlight
    if n_segs:
        tip_x = x + 4 + (n_segs - 1) * (seg_w + gap)
        out.append(rect(tip_x, y + 4, 2, h - 8, INK, opacity="0.55"))
    return "".join(out)


def portrait(x, y, scale=6):
    """Greg's logo, slightly pixelated. 31x32 grid extracted from his GitHub
    avatar (hair + round glasses silhouette). '#' = ink pixel, '.' = transparent
    so the underlying panel shows through."""
    grid = [
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
    out = []
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            if ch == "#":
                out.append(rect(x + rx * scale, y + ry * scale, scale, scale, INK))
    return "".join(out)


def stat_row(x, y, label, value, label_color=ACC2, value_color=INK):
    out = []
    out.append(pixfont.render(label, x, y, 2, label_color))
    lw = pixfont.width(label, 2)
    out.append(pixfont.render(value, x + lw + 16, y, 2, value_color))
    return "".join(out)


def blink_cursor(x, y, scale=2):
    """Animated blinking square cursor."""
    return (
        f'<rect x="{x}" y="{y}" width="{5 * scale}" height="{7 * scale}" fill="{ACC2}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1.0s" repeatCount="indefinite"/>'
        f'</rect>'
    )


def heartbeat_dot(x, y, color):
    return (
        f'<rect x="{x}" y="{y}" width="8" height="8" fill="{color}">'
        f'<animate attributeName="opacity" values="0.3;1;0.3" dur="1.4s" repeatCount="indefinite"/>'
        f'</rect>'
    )


def build() -> str:
    out = [rect(0, 0, W, H, BG)]

    # Outer bevel — double-frame for chunky retro window
    out.append(panel(8, 8, W - 16, H - 16, PRIM, PANEL, 4))
    out.append(panel(20, 20, W - 40, H - 40, ACC1, PANEL, 2))

    # Header bar — "STATUS" tab
    tab_w = 220
    tab_x = 32
    tab_y = 12
    out.append(rect(tab_x, tab_y, tab_w, 22, PRIM))
    out.append(rect(tab_x + 2, tab_y + 2, tab_w - 4, 18, BG))
    out.append(pixfont.render("--  STATUS  --", tab_x + 22, tab_y + 5, 2, INK))

    # Portrait box — Greg's logo, slightly pixelated
    px, py = 36, 50
    pw, ph = 220, 250
    out.append(panel(px, py, pw, ph, ACC1, SHADOW, 3))
    out.append(rect(px + 8, py + 8, pw - 16, ph - 16, PANEL))
    # The grid is 31w x 32h. At scale 6 → 186x192. Center inside the inset.
    inner_w, inner_h = pw - 16, ph - 16
    logo_w, logo_h = 31 * 6, 32 * 6
    lx = px + 8 + (inner_w - logo_w) // 2
    ly = py + 8 + (inner_h - logo_h) // 2
    out.append(portrait(lx, ly, scale=6))
    # corner LED
    out.append(heartbeat_dot(px + pw - 18, py + 10, ACC2))

    # Right column: stats
    sx = px + pw + 28
    sy = 60

    # Name and bio
    out.append(pixfont.render("NAME", sx, sy, 2, ACC2))
    out.append(pixfont.render("GREG BANKS", sx + 80, sy, 3, INK))

    out.append(pixfont.render("CLASS", sx, sy + 36, 2, ACC2))
    out.append(pixfont.render("FULL-STACK ENGINEER", sx + 80, sy + 36, 2, WARN))

    out.append(pixfont.render("GUILD", sx, sy + 64, 2, ACC2))
    out.append(pixfont.render("@FLOGISTIX  ·  OKC", sx + 80, sy + 64, 2, INK))

    out.append(pixfont.render("LV", sx, sy + 92, 2, ACC2))
    out.append(pixfont.render("47", sx + 40, sy + 92, 3, WARN))
    out.append(pixfont.render("9-YR JOURNEY", sx + 110, sy + 92, 2, INK))

    # Bars
    bars_y = sy + 132
    bars_w = W - sx - 40
    out.append(stat_bar(sx, bars_y, bars_w, 16, 92, ACC1,
                        "HP / SHIP-CRAFT", "92 / 100"))
    out.append(stat_bar(sx, bars_y + 46, bars_w, 16, 80, WARN,
                        "MP / DEEP FOCUS", "80 / 100"))
    out.append(stat_bar(sx, bars_y + 92, bars_w, 16, 71, ACC2,
                        "EXP / NEXT TIER", "71%"))

    # Inventory strip — three little icons (laptop, controller, coffee)
    inv_y = py + ph + 16
    # commented out: keep card tight, action lives in next assets
    # left blank to avoid clutter

    # Footer cursor blink
    out.append(pixfont.render("- READY", 36, H - 38, 2, INK))
    out.append(blink_cursor(36 + pixfont.width("- READY", 2) + 10, H - 38, 2))

    out.append(pixfont.render("PRESS  - SELECT  TO CONNECT", W - 380, H - 38, 2, ACC2))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="Player status card for Greg Banks" '
        f'shape-rendering="crispEdges">'
        + "".join(out) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
