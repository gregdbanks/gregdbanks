"""Hero banner: title, animated walking sprite, parallax skyline + stars."""
from __future__ import annotations
import random
from pathlib import Path

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
import pixfont


W, H = 1200, 320
OUT = Path(__file__).parent.parent / "assets" / "banner.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def starfield(seed: int = 7) -> str:
    """80 stars across the upper canvas with staggered twinkle."""
    rng = random.Random(seed)
    out = []
    for i in range(90):
        x = rng.randint(0, W - 4)
        y = rng.randint(8, 180)
        size = rng.choice([2, 2, 2, 4])  # mostly small
        color = rng.choice([INK, INK, INK, ACC2, PRIM])
        delay = rng.uniform(0, 4)
        dur = rng.uniform(2.4, 5.5)
        opacity_min = rng.choice([0.1, 0.15, 0.2, 0.3])
        out.append(
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}" opacity="{opacity_min}">'
            f'<animate attributeName="opacity" values="{opacity_min};1;{opacity_min}" '
            f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    return "".join(out)


def moon() -> str:
    """Pixel crescent moon, top-right."""
    cx, cy, r = 1080, 70, 32
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{INK}" opacity="0.92"/>']
    out.append(f'<circle cx="{cx + 14}" cy="{cy - 6}" r="{r - 2}" fill="{BG}"/>')
    # craters
    for dx, dy, rr in [(-10, 6, 3), (-4, 14, 2), (-14, -8, 2)]:
        out.append(f'<rect x="{cx + dx}" y="{cy + dy}" width="{rr * 2}" height="{rr * 2}" fill="{DIM}" opacity="0.7"/>')
    return "".join(out)


def skyline() -> str:
    """Pixel city silhouette baseline at y=220, mid-distance."""
    out = []
    # back row (further, dimmer) — devon tower-ish
    back = [
        # (x, w, h)
        (40, 30, 36), (78, 18, 24), (104, 26, 50), (138, 14, 30),
        (160, 22, 42), (188, 30, 60), (224, 16, 28), (246, 28, 38),
        (282, 18, 22), (306, 24, 46), (336, 14, 26), (360, 32, 70),  # central spire
        (398, 18, 30), (422, 26, 44), (456, 14, 22), (478, 30, 56),
        (514, 18, 34), (538, 24, 42), (568, 14, 26), (590, 32, 64),
        (628, 18, 28), (652, 26, 50), (686, 16, 30), (708, 22, 38),
        (738, 30, 58), (774, 18, 30), (798, 26, 46), (832, 14, 22),
        (854, 28, 52), (888, 18, 36), (912, 24, 40), (944, 16, 28),
        (966, 32, 64), (1004, 18, 30), (1028, 26, 48), (1062, 14, 22),
        (1084, 30, 54), (1120, 18, 32), (1144, 26, 46),
    ]
    for x, w, h in back:
        out.append(rect(x, 256 - h, w, h, DIM))
        # window pattern (1 in 3)
        for wy in range(256 - h + 6, 252, 8):
            for wx in range(x + 4, x + w - 3, 6):
                if (wx + wy) % 16 == 0:
                    out.append(rect(wx, wy, 2, 2, WARN, opacity="0.55"))

    # tallest spire — antenna with blinking aircraft light
    out.append(rect(376, 156, 4, 30, DIM))
    out.append(
        f'<rect x="374" y="150" width="8" height="6" fill="{ACC1}">'
        f'<animate attributeName="opacity" values="0.2;1;0.2" dur="1.8s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    # ground line
    out.append(rect(0, 256, W, 4, PANEL))
    out.append(rect(0, 260, W, 60, BG))
    return "".join(out)


def cloud(x_start: int, y: int, dur: float, palette: str = INK, opacity: float = 0.18) -> str:
    """A pixel cloud drifting across at constant speed."""
    pixels = [
        (4, 2), (6, 2), (8, 2), (10, 2), (12, 2),
        (2, 4), (4, 4), (6, 4), (8, 4), (10, 4), (12, 4), (14, 4),
        (0, 6), (2, 6), (4, 6), (6, 6), (8, 6), (10, 6), (12, 6), (14, 6), (16, 6),
        (2, 8), (4, 8), (6, 8), (8, 8), (10, 8), (12, 8), (14, 8),
    ]
    s = 4
    parts = [f'<g transform="translate({x_start} {y})" opacity="{opacity}">']
    for px, py in pixels:
        parts.append(rect(px * s, py * s, s, s, palette))
    parts.append(
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="{-100} {y}" to="{W + 100} {y}" dur="{dur}s" repeatCount="indefinite"/>'
    )
    parts.append('</g>')
    return "".join(parts)


def sprite() -> str:
    """Pixelated logo head + casual-dev body with hands-in-pockets pose."""
    from avatar import GRID as HEAD
    from sprite_options import BODY_DEV_ARMS_B as BODY
    s = 2  # scale
    cmap = {
        "#": INK,      # head + neck (parchment)
        "B": ACC2,     # t-shirt (wheat)
        "A": DIM,      # jeans (smoke)
        "S": SHADOW,   # shoes
        "H": INK,      # hands (parchment)
    }
    out = ['<g id="sprite-art">']
    for ry, row in enumerate(HEAD):
        for rx, ch in enumerate(row):
            if ch == "#":
                out.append(rect(rx * s, ry * s, s, s, INK))
    head_h = len(HEAD)
    for ry, row in enumerate(BODY):
        for rx, ch in enumerate(row):
            color = cmap.get(ch)
            if color:
                out.append(rect(rx * s, (ry + head_h) * s, s, s, color))
    out.append('</g>')
    return "".join(out)


def walking_sprite() -> str:
    """Sprite walking left-to-right with vertical bob.
    Sprite is 31x48 grid * 2px = 62x96. Feet land near ground line at y=256.
    """
    spawn_y = 256 - 48 * 2  # top so feet sit on ground
    return (
        f'<g transform="translate(-70 {spawn_y})">'
        f'  <animateTransform attributeName="transform" type="translate" '
        f'  values="-70 {spawn_y}; {W + 10} {spawn_y}" dur="22s" repeatCount="indefinite"/>'
        f'  <g>'
        f'    <animateTransform attributeName="transform" type="translate" '
        f'    values="0 0; 0 -3; 0 0; 0 -3; 0 0" dur="0.7s" repeatCount="indefinite"/>'
        f'    {sprite()}'
        f'  </g>'
        f'</g>'
    )


def title_block() -> str:
    """The GREG BANKS marquee + tagline, with frame and shadow."""
    out = []
    # title shadow + main
    title = "GREG BANKS"
    scale = 7
    tw = pixfont.width(title, scale)
    tx = (W - tw) // 2
    ty = 60
    # back glow (mint)
    out.append(pixfont.render(title, tx + 4, ty + 4, scale, SHADOW))
    out.append(pixfont.render(title, tx + 2, ty + 2, scale, ACC1))
    out.append(pixfont.render(title, tx, ty, scale, INK))

    # subtle scan-shimmer: a lighter copy that fades in/out
    out.append(
        f'<g opacity="0.0">'
        f'<animate attributeName="opacity" values="0;0.45;0" dur="3.2s" repeatCount="indefinite"/>'
        + pixfont.render(title, tx, ty, scale, ACC2)
        + f'</g>'
    )

    # tagline
    sub = "DAD · DEVELOPER · OKLAHOMA CITY"
    sscale = 3
    sw = pixfont.width(sub, sscale)
    sx = (W - sw) // 2
    sy = ty + 7 * scale + 18
    # underline rule
    out.append(rect(sx - 24, sy - 10, sw + 48, 2, PRIM))
    out.append(pixfont.render(sub, sx, sy, sscale, ACC2))
    out.append(rect(sx - 24, sy + 7 * sscale + 6, sw + 48, 2, PRIM))

    # corner brackets
    bracket_pad = 18
    bx0, by0 = sx - 40, ty - 12
    bx1, by1 = sx + sw + 40, sy + 7 * sscale + 14
    L_ = 18
    bw = 3
    # top-left
    out.append(rect(bx0, by0, L_, bw, WARN))
    out.append(rect(bx0, by0, bw, L_, WARN))
    # top-right
    out.append(rect(bx1 - L_, by0, L_, bw, WARN))
    out.append(rect(bx1 - bw, by0, bw, L_, WARN))
    # bottom-left
    out.append(rect(bx0, by1 - bw, L_, bw, WARN))
    out.append(rect(bx0, by1 - L_, bw, L_, WARN))
    # bottom-right
    out.append(rect(bx1 - L_, by1 - bw, L_, bw, WARN))
    out.append(rect(bx1 - bw, by1 - L_, bw, L_, WARN))
    return "".join(out)


def coin_counter() -> str:
    """Top-left HUD showing contribution count, like an arcade score panel."""
    x, y = 24, 24
    out = [rect(x - 6, y - 6, 250, 36, PANEL),
           rect(x - 6, y - 6, 250, 2, PRIM),
           rect(x - 6, y + 28, 250, 2, PRIM),
           rect(x - 6, y - 6, 2, 36, PRIM),
           rect(x + 244 - 2, y - 6, 2, 36, PRIM)]
    # animated coin
    coin_x, coin_y = x + 4, y + 4
    out.append(
        f'<g transform="translate({coin_x} {coin_y})">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="{coin_x} {coin_y}; {coin_x} {coin_y - 2}; {coin_x} {coin_y}" '
        f'dur="0.6s" repeatCount="indefinite"/>'
        + rect(2, 2, 12, 12, WARN)
        + rect(4, 0, 8, 16, WARN)
        + rect(0, 4, 16, 8, WARN)
        + rect(6, 4, 4, 8, BG)
        + f'</g>'
    )
    out.append(pixfont.render("CONTRIBS X 5173", x + 30, y + 4, 2, INK))
    return "".join(out)


def hud_top_right() -> str:
    """Top-right HUD: 'P1 · 1CC' arcade-style player tag."""
    x, y = W - 24 - 220, 24
    out = [rect(x, y - 6, 220, 36, PANEL),
           rect(x, y - 6, 220, 2, ACC1),
           rect(x, y + 28, 220, 2, ACC1),
           rect(x, y - 6, 2, 36, ACC1),
           rect(x + 218, y - 6, 2, 36, ACC1)]
    out.append(pixfont.render("P1   READY", x + 14, y + 4, 2, INK))
    # blinker
    out.append(
        f'<rect x="{x + 200}" y="{y + 4}" width="10" height="14" fill="{ACC2}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="0.9s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    return "".join(out)


def build() -> str:
    body = []
    # hard background
    body.append(rect(0, 0, W, H, BG))

    # vertical gradient hint via 3 bands in palette
    body.append(rect(0, 0, W, 80, "#0B0B16"))
    body.append(rect(0, 80, W, 100, "#0F0F1B"))
    body.append(rect(0, 180, W, 80, "#13132A"))

    # parallax stars
    body.append(starfield())
    body.append(moon())

    # parallax clouds
    body.append(cloud(100, 36, 70, INK, 0.10))
    body.append(cloud(420, 80, 95, INK, 0.07))
    body.append(cloud(800, 24, 110, ACC2, 0.06))

    # skyline
    body.append(skyline())

    # title
    body.append(title_block())

    # walking sprite at horizon
    body.append(walking_sprite())

    # HUD
    body.append(coin_counter())
    body.append(hud_top_right())

    # Outer pixel border (4 corners only — keeps it light)
    bw = 4
    out_l = 24
    body.append(rect(out_l, out_l, 28, bw, PRIM))
    body.append(rect(out_l, out_l, bw, 28, PRIM))
    body.append(rect(W - out_l - 28, out_l, 28, bw, PRIM))
    body.append(rect(W - out_l - bw, out_l, bw, 28, PRIM))
    body.append(rect(out_l, H - out_l - bw, 28, bw, PRIM))
    body.append(rect(out_l, H - out_l - 28, bw, 28, PRIM))
    body.append(rect(W - out_l - 28, H - out_l - bw, 28, bw, PRIM))
    body.append(rect(W - out_l - bw, H - out_l - 28, bw, 28, PRIM))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="Greg Banks — Dad, Developer, Oklahoma City" '
        f'shape-rendering="crispEdges" style="background:{BG}">'
        + "".join(body)
        + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
