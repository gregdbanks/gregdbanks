"""Skill constellation: 4 branches radiating from a central core, pulsing nodes."""
from __future__ import annotations
from pathlib import Path
import math

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
import pixfont

W, H = 1200, 560
OUT = Path(__file__).parent.parent / "assets" / "skill-tree.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def chip(cx, cy, label, accent=PRIM, w=None):
    """Pixel-frame chip with label."""
    pad = 14
    text_w = pixfont.width(label, 2)
    w = w or text_w + pad * 2
    h = 32
    x = cx - w // 2
    y = cy - h // 2
    parts = []
    # backplate shadow
    parts.append(rect(x + 3, y + 3, w, h, SHADOW))
    parts.append(rect(x, y, w, h, PANEL))
    # frame
    parts.append(rect(x, y, w, 2, accent))
    parts.append(rect(x, y + h - 2, w, 2, accent))
    parts.append(rect(x, y, 2, h, accent))
    parts.append(rect(x + w - 2, y, 2, h, accent))
    # corner notches (chamfer)
    parts.append(rect(x, y, 2, 2, BG))
    parts.append(rect(x + w - 2, y, 2, 2, BG))
    parts.append(rect(x, y + h - 2, 2, 2, BG))
    parts.append(rect(x + w - 2, y + h - 2, 2, 2, BG))
    # label
    parts.append(pixfont.render(label, x + (w - text_w) // 2, y + 9, 2, INK))
    return "".join(parts), (x, y, w, h)


def pulse_line(x1, y1, x2, y2, color, dur=2.4, delay=0.0):
    """Dashed line that 'flows' between core and chip via stroke-dashoffset animation."""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="2" stroke-dasharray="4 6" opacity="0.55">'
        f'<animate attributeName="stroke-dashoffset" from="0" to="-40" '
        f'dur="{dur}s" repeatCount="indefinite" begin="{delay}s"/>'
        f'</line>'
    )


def core(cx, cy):
    """The central pixel sigil."""
    s = 4
    # 9x9 plus shape
    grid = [
        "...AAA...",
        "..ABBBA..",
        ".ABBCBBA.",
        "ABBCDCBBA",
        "ABBDIDCBA",
        "ABBCDCBBA",
        ".ABBCBBA.",
        "..ABBBA..",
        "...AAA...",
    ]
    cmap = {"A": PRIM, "B": ACC1, "C": WARN, "D": ACC2, "I": INK}
    out = []
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            if ch in cmap:
                out.append(rect(cx - 18 + rx * s, cy - 18 + ry * s, s, s, cmap[ch]))
    # outer ring sparks
    for angle_deg, color in [(0, ACC2), (90, WARN), (180, ACC1), (270, PRIM)]:
        rad = math.radians(angle_deg)
        sx = cx + int(math.cos(rad) * 32) - 4
        sy = cy + int(math.sin(rad) * 32) - 4
        out.append(
            f'<rect x="{sx}" y="{sy}" width="8" height="8" fill="{color}">'
            f'<animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    return "".join(out)


def heading(cx, y, text, color):
    text_w = pixfont.width(text, 3)
    out = [pixfont.render(text, cx - text_w // 2, y, 3, color)]
    # underline rule with notches
    out.append(rect(cx - text_w // 2 - 12, y + 24, text_w + 24, 2, color))
    return "".join(out)


def column(cx, header_y, header, header_color, items, link_color):
    """Render a vertical column header + chips, all linked to center core."""
    out = [heading(cx, header_y, header, header_color)]
    chips = []
    item_y = header_y + 60
    for label in items:
        body, (x, y, w, h) = chip(cx, item_y, label, accent=link_color)
        chips.append((x + w // 2, y + h // 2, body))
        item_y += 56
    return out, chips


def build() -> str:
    out = [rect(0, 0, W, H, BG)]

    # title
    title = "SKILL CONSTELLATION"
    t_scale = 4
    tw = pixfont.width(title, t_scale)
    out.append(pixfont.render(title, (W - tw) // 2, 30, t_scale, INK))
    # rule
    out.append(rect((W - tw) // 2 - 32, 30 + 7 * t_scale + 12, tw + 64, 2, PRIM))

    # subtitle
    sub = "FOUR BRANCHES · ONE STACK"
    sw = pixfont.width(sub, 2)
    out.append(pixfont.render(sub, (W - sw) // 2, 30 + 7 * t_scale + 24, 2, ACC2))

    # central core
    cx, cy = W // 2, 350
    # background halo (radial-feel with concentric rects)
    for r, op in [(110, 0.06), (80, 0.10), (50, 0.16)]:
        out.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PRIM}" opacity="{op}"/>'
        )

    # 4 columns
    col_xs = [180, 480, 760, 1040]
    columns_def = [
        ("LANGUAGES", ACC1, PRIM, ["TYPESCRIPT", "JAVASCRIPT", "PYTHON", "RUST"]),
        ("FRONT-END", PRIM, ACC1, ["REACT", "VITE", "PHASER", "ELECTRON"]),
        ("BACK-END", WARN, WARN, ["NODE.JS", "EXPRESS", "MONGODB", "JWT"]),
        ("PLATFORM & AI", ACC2, ACC2, ["AWS", "VERCEL", "GH ACTIONS", "CLAUDE / MCP"]),
    ]

    column_chips = []
    for col_x, (header, header_color, link_color, items) in zip(col_xs, columns_def):
        col_out, chips = column(col_x, 130, header, header_color, items, link_color)
        out.extend(col_out)
        column_chips.append((col_x, chips, link_color))

    # Draw connection lines (behind chips), then chips on top
    line_layer = []
    chip_layer = []
    for i, (col_x, chips, color) in enumerate(column_chips):
        for j, (chx, chy, body) in enumerate(chips):
            line_layer.append(pulse_line(cx, cy, chx, chy, color, dur=2.0 + j * 0.3,
                                         delay=i * 0.4 + j * 0.1))
            chip_layer.append(body)
    out.extend(line_layer)

    # central core sits between lines and chips
    out.append(core(cx, cy))

    out.extend(chip_layer)

    # corner stamps
    stamp = "// ALWAYS LEARNING"
    out.append(pixfont.render(stamp, 32, H - 36, 2, DIM))
    stamp2 = "GREG.SH/STACK"
    sw2 = pixfont.width(stamp2, 2)
    out.append(pixfont.render(stamp2, W - 32 - sw2, H - 36, 2, DIM))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="Skill constellation: languages, front-end, back-end, platform" '
        f'shape-rendering="crispEdges">'
        + "".join(out) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
