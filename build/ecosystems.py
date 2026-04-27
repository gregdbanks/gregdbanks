"""Three stacked ecosystem panels, each representing a cluster of private repos.

Per user direction: name the ecosystem and what's inside, but never expose
individual private repo names or URLs. Reviewers see breadth without 404s.
"""
from __future__ import annotations
from pathlib import Path

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
import pixfont

W, H = 1200, 780
OUT = Path(__file__).parent.parent / "assets" / "ecosystems.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def panel(x, y, w, h, accent, body=PANEL, bw=3):
    out = []
    out.append(rect(x + 4, y + 4, w, h, SHADOW))
    out.append(rect(x, y, w, h, body))
    out.append(rect(x, y, w, bw, accent))
    out.append(rect(x, y + h - bw, w, bw, accent))
    out.append(rect(x, y, bw, h, accent))
    out.append(rect(x + w - bw, y, bw, h, accent))
    # corner chamfer
    out.append(rect(x, y, bw, bw, BG))
    out.append(rect(x + w - bw, y, bw, bw, BG))
    out.append(rect(x, y + h - bw, bw, bw, BG))
    out.append(rect(x + w - bw, y + h - bw, bw, bw, BG))
    return "".join(out)


def chip(x, y, label, accent, scale=2):
    """Inline pixel chip used for tech stack tags."""
    pad_x = 10
    text_w = pixfont.width(label, scale)
    w = text_w + pad_x * 2
    h = 7 * scale + 12
    out = [
        rect(x, y, w, h, SHADOW),
        rect(x, y, w, 2, accent),
        rect(x, y + h - 2, w, 2, accent),
        rect(x, y, 2, h, accent),
        rect(x + w - 2, y, 2, h, accent),
        rect(x, y, 2, 2, BG),
        rect(x + w - 2, y, 2, 2, BG),
        rect(x, y + h - 2, 2, 2, BG),
        rect(x + w - 2, y + h - 2, 2, 2, BG),
        pixfont.render(label, x + pad_x, y + 6, scale, INK),
    ]
    return "".join(out), w


def chips_row(x, y, items, accent, scale=2, gap=10):
    out = []
    cursor = x
    for label in items:
        body, w = chip(cursor, y, label, accent, scale)
        out.append(body)
        cursor += w + gap
    return "".join(out)


def icon_local_first(x, y):
    """Pixel illustration: stacked servers with a green LED."""
    s = 4
    grid = [
        "..............",
        ".PPPPPPPPPPPP.",   # P = panel/blue
        ".PXXXXXXXXXXP.",   # X = inset
        ".PXMMMMMMMMXP.",   # M = mint indicator strip
        ".PXXXXXXXXLXP.",   # L = LED
        ".PPPPPPPPPPPP.",
        "..............",
        ".PPPPPPPPPPPP.",
        ".PXXXXXXXXXXP.",
        ".PXMMMMMMMMXP.",
        ".PXXXXXXXLXXP.",
        ".PPPPPPPPPPPP.",
        "..............",
        ".PPPPPPPPPPPP.",
        ".PXXXXXXXXXXP.",
        ".PXMMMMMMMMXP.",
        ".PXXXXLXXXXXP.",
        ".PPPPPPPPPPPP.",
        "..............",
    ]
    cmap = {"P": PRIM, "X": "#10102A", "M": ACC2, "L": WARN}
    out = []
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            if ch in cmap:
                out.append(rect(x + rx * s, y + ry * s, s, s, cmap[ch]))
    # blinking LED overlay
    out.append(
        f'<rect x="{x + 8 * s + 4}" y="{y + 16 * s}" width="{s}" height="{s}" fill="{ACC2}">'
        f'<animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    return "".join(out)


def icon_pixel_craft(x, y):
    """Pixel illustration: a tiny tilemap with brush hovering."""
    s = 4
    # 14x14 tilemap, alternating
    grid = [
        ".GGGGGGGGGGGG.",   # G = grass mint
        ".GGGGSSGGGGGG.",
        ".GGSSSSSSGGGG.",   # S = stone (yellow)
        ".GGSWWWWSGGGG.",   # W = water blue
        ".GGSWWWWSGGSS.",
        ".GGSSSSSSGSSS.",
        ".GGGGGGGGGSSS.",
        ".GGGGFFFFGGGG.",   # F = flower (magenta)
        ".GGGGFFFFGGGG.",
        ".GGGGGGGGGGGG.",
        ".SSSSSSSSSSSSS",
        ".SBBBSSBBBSSSS",   # B = bridge dark
        ".SSSSSSSSSSSSS",
        ".GGGGGGGGGGGG.",
    ]
    cmap = {"G": ACC2, "S": WARN, "W": PRIM, "F": ACC1, "B": SHADOW}
    out = []
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            if ch in cmap:
                out.append(rect(x + rx * s, y + ry * s, s, s, cmap[ch]))
    # brush cursor — animated bob
    bx = x + 6 * s
    by = y - 4
    out.append(
        f'<g>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0; 0 -4; 0 0" dur="1.6s" repeatCount="indefinite"/>'
        + rect(bx, by, s, s * 4, ACC1)
        + rect(bx - s, by + s * 4, s * 3, s, ACC1)
        + rect(bx, by + s * 5, s, s, INK)
        + f'</g>'
    )
    return "".join(out)


def icon_ai(x, y):
    """Pixel illustration: a brain-circuit / core with orbiting nodes."""
    s = 4
    grid = [
        "...AAAAAAAA...",
        "..ABBBBBBBBA..",
        ".ABBCCCCCCBBA.",
        ".ABCCDDDDCCBA.",   # D = inner glow
        "ABCCDDIIDCCBA.",   # I = ink (pulse core)
        "ABCCDDIIDCCBA.",
        ".ABCCDDDDCCBA.",
        ".ABBCCCCCCBBA.",
        "..ABBBBBBBBA..",
        "...AAAAAAAA...",
        "..............",
        "..PPP....PPP..",
        "..PPP....PPP..",
        "..............",
    ]
    cmap = {"A": PRIM, "B": ACC1, "C": WARN, "D": ACC2, "I": INK, "P": ACC2}
    out = []
    for ry, row in enumerate(grid):
        for rx, ch in enumerate(row):
            if ch in cmap:
                out.append(rect(x + rx * s, y + ry * s, s, s, cmap[ch]))
    # pulsing core
    out.append(
        f'<rect x="{x + 6 * s}" y="{y + 4 * s}" width="{2 * s}" height="{2 * s}" fill="{INK}">'
        f'<animate attributeName="opacity" values="1;0.4;1" dur="1.8s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    return "".join(out)


def ecosystem(y, accent, code, name, blurb_lines, stack, icon_fn,
              repo_count_label):
    out = []
    px, py = 32, y
    pw, ph = W - 64, 200
    out.append(panel(px, py, pw, ph, accent))

    # numeric tag in corner
    out.append(rect(px + 14, py - 10, 80, 20, accent))
    out.append(pixfont.render(code, px + 22, py - 4, 2, BG))

    # icon block
    icon_box_x = px + 32
    icon_box_y = py + 32
    out.append(rect(icon_box_x - 8, icon_box_y - 8, 96, 96, "#0A0A18"))
    out.append(rect(icon_box_x - 8, icon_box_y - 8, 96, 2, accent))
    out.append(rect(icon_box_x - 8, icon_box_y + 86, 96, 2, accent))
    out.append(rect(icon_box_x - 8, icon_box_y - 8, 2, 96, accent))
    out.append(rect(icon_box_x + 86, icon_box_y - 8, 2, 96, accent))
    out.append(icon_fn(icon_box_x, icon_box_y))

    # title
    title_x = icon_box_x + 110
    out.append(pixfont.render(name, title_x, py + 24, 4, INK))
    out.append(rect(title_x, py + 60, pixfont.width(name, 4), 2, accent))

    # blurb
    for i, line in enumerate(blurb_lines):
        out.append(pixfont.render(line, title_x, py + 78 + i * 22, 2, ACC2))

    # repo count badge — far right
    badge_x = px + pw - 220
    badge_y = py + 24
    out.append(rect(badge_x, badge_y, 180, 28, "#0A0A18"))
    out.append(rect(badge_x, badge_y, 180, 2, WARN))
    out.append(rect(badge_x, badge_y + 26, 180, 2, WARN))
    out.append(rect(badge_x, badge_y, 2, 28, WARN))
    out.append(rect(badge_x + 178, badge_y, 2, 28, WARN))
    out.append(pixfont.render(repo_count_label, badge_x + 14, badge_y + 8, 2, WARN))

    # stack chips at bottom
    out.append(chips_row(title_x, py + 140, stack, accent, scale=2, gap=8))
    return "".join(out)


def build() -> str:
    out = [rect(0, 0, W, H, BG)]

    # title
    title = "ECOSYSTEMS"
    t_scale = 5
    tw = pixfont.width(title, t_scale)
    out.append(pixfont.render(title, (W - tw) // 2, 30, t_scale, INK))
    sub = "PRIVATE REPO CLUSTERS · UNDER CONSTANT FORGING"
    sw = pixfont.width(sub, 2)
    out.append(pixfont.render(sub, (W - sw) // 2, 30 + 7 * t_scale + 14, 2, ACC2))

    # 3 ecosystems
    out.append(ecosystem(
        y=120,
        accent=PRIM,
        code="01.SYS",
        name="LOCAL-FIRST DEV STACK",
        blurb_lines=[
            "PERSONAL CLOUD-OPS CONSOLE, OS-NATIVE SECRETS VAULT,",
            "DEV COMMAND CENTER, AND LOCAL TEST DASHBOARD.",
            "ALL DATA STAYS ON THE MACHINE.",
        ],
        stack=["TYPESCRIPT", "ELECTRON", "VITE", "REACT", "MAC KEYCHAIN"],
        icon_fn=icon_local_first,
        repo_count_label="6 REPOS",
    ))

    out.append(ecosystem(
        y=340,
        accent=ACC1,
        code="02.ART",
        name="PIXEL ART & GAME-CRAFT",
        blurb_lines=[
            "WYSIWYG TILEMAP EDITORS, VOXEL-FLOW TOOLING,",
            "AND RETRO-THEMED DESKTOP CONTROL PANELS.",
            "PIXEL-PERFECT GRIDS, NO ANTI-ALIAS COMPROMISES.",
        ],
        stack=["PHASER", "TYPESCRIPT", "CANVAS API", "ELECTRON"],
        icon_fn=icon_pixel_craft,
        repo_count_label="3 REPOS",
    ))

    out.append(ecosystem(
        y=560,
        accent=ACC2,
        code="03.LRN",
        name="STUDY & LEARNING TOOLS",
        blurb_lines=[
            "SELF-HOSTED LEARNING PLATFORM, SPACED-REPETITION",
            "FLASHCARD ENGINE, EXAM MICROSERVICE, AND PROGRESS",
            "TRACKING. BUILT TO OUTLAST A SUBSCRIPTION.",
        ],
        stack=["TYPESCRIPT", "NODE", "PYTHON", "MONGODB", "REACT"],
        icon_fn=icon_ai,
        repo_count_label="6 REPOS",
    ))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="Three private project ecosystems" '
        f'shape-rendering="crispEdges">'
        + "".join(out) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
