"""Public repos as 8-bit game cartridges, 3x2 grid."""
from __future__ import annotations
from pathlib import Path

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
import pixfont

W, H = 1200, 860
OUT = Path(__file__).parent.parent / "assets" / "cartridges.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def chip(x, y, label, accent, scale=2):
    pad_x = 8
    text_w = pixfont.width(label, scale)
    w = text_w + pad_x * 2
    h = 7 * scale + 10
    out = [
        rect(x, y, w, 2, accent),
        rect(x, y + h - 2, w, 2, accent),
        rect(x, y, 2, h, accent),
        rect(x + w - 2, y, 2, h, accent),
        rect(x, y, 2, 2, BG),
        rect(x + w - 2, y, 2, 2, BG),
        rect(x, y + h - 2, 2, 2, BG),
        rect(x + w - 2, y + h - 2, 2, 2, BG),
        pixfont.render(label, x + pad_x, y + 5, scale, INK),
    ]
    return "".join(out), w


def cartridge_shell(x, y, w, h, accent):
    """Authentic NES cartridge silhouette: top label, body, two notches."""
    out = []
    # Drop shadow
    out.append(rect(x + 5, y + 5, w, h, SHADOW))

    # Outer body
    out.append(rect(x, y, w, h, "#1a1a30"))
    # Frame
    out.append(rect(x, y, w, 3, accent))
    out.append(rect(x, y + h - 3, w, 3, accent))
    out.append(rect(x, y, 3, h, accent))
    out.append(rect(x + w - 3, y, 3, h, accent))
    # Corner chamfer
    out.append(rect(x, y, 3, 3, BG))
    out.append(rect(x + w - 3, y, 3, 3, BG))
    out.append(rect(x, y + h - 3, 3, 3, BG))
    out.append(rect(x + w - 3, y + h - 3, 3, 3, BG))

    # Top notches (cartridge handle indents)
    notch_w, notch_h = 24, 8
    out.append(rect(x + 30, y, notch_w, notch_h, BG))
    out.append(rect(x + w - 30 - notch_w, y, notch_w, notch_h, BG))

    # Label band — top third
    label_y = y + 10
    label_h = 60
    out.append(rect(x + 14, label_y, w - 28, label_h, accent))
    out.append(rect(x + 14, label_y, w - 28, 2, INK, opacity="0.20"))
    return "".join(out), label_y, label_h


def screen(x, y, w, h, accent):
    """Inner pixel 'screenshot' frame area."""
    out = []
    out.append(rect(x, y, w, h, "#08081A"))
    out.append(rect(x, y, w, 2, accent))
    out.append(rect(x, y + h - 2, w, 2, accent))
    out.append(rect(x, y, 2, h, accent))
    out.append(rect(x + w - 2, y, 2, h, accent))
    return "".join(out)


def screen_voxflow(x, y, w, h):
    """Tiny waveform, like dictation."""
    s = 4
    out = []
    # Microphone icon top-left
    mx, my = x + 12, y + 12
    out += [rect(mx, my, 8, 16, ACC1), rect(mx + 2, my + 4, 4, 8, INK),
            rect(mx - 4, my + 16, 16, 4, ACC1), rect(mx + 2, my + 20, 4, 6, ACC1)]
    # Waveform bars (animated)
    bars = [10, 30, 18, 50, 22, 40, 14, 36, 24, 12, 28, 18, 32, 16]
    for i, bh in enumerate(bars):
        bx = x + 36 + i * 8
        by = y + h // 2 - bh // 2
        out.append(
            f'<rect x="{bx}" y="{by}" width="4" height="{bh}" fill="{ACC2}">'
            f'<animate attributeName="height" values="{bh};{bh//2};{bh}" '
            f'dur="{0.4 + (i % 5) * 0.1:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{by};{by + bh//4};{by}" '
            f'dur="{0.4 + (i % 5) * 0.1:.1f}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    # Cursor caret
    out.append(
        f'<rect x="{x + w - 16}" y="{y + h - 24}" width="3" height="14" fill="{INK}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="0.7s" repeatCount="indefinite"/>'
        f'</rect>'
    )
    return "".join(out)


def screen_perf(x, y, w, h):
    """A line chart showing perf gains."""
    out = []
    # axes
    ax_x, ax_y = x + 16, y + 16
    aw, ah = w - 32, h - 32
    out.append(rect(ax_x, ax_y + ah, aw, 2, INK))
    out.append(rect(ax_x, ax_y, 2, ah, INK))
    # gridlines
    for i in range(1, 4):
        gy = ax_y + (ah * i // 4)
        for gx in range(ax_x + 8, ax_x + aw, 12):
            out.append(rect(gx, gy, 4, 1, DIM))
    # before line (descending zigzag, magenta)
    pts_before = [(0.05, 0.25), (0.20, 0.30), (0.35, 0.45), (0.50, 0.55),
                  (0.65, 0.65), (0.80, 0.78), (0.95, 0.85)]
    pts_after = [(0.05, 0.20), (0.20, 0.18), (0.35, 0.20), (0.50, 0.22),
                 (0.65, 0.20), (0.80, 0.21), (0.95, 0.22)]
    def plot(pts, color):
        rs = []
        for i in range(len(pts) - 1):
            x1 = ax_x + int(pts[i][0] * aw)
            y1 = ax_y + int(pts[i][1] * ah)
            x2 = ax_x + int(pts[i + 1][0] * aw)
            y2 = ax_y + int(pts[i + 1][1] * ah)
            rs.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{color}" stroke-width="3"/>'
            )
        for px, py in pts:
            cx = ax_x + int(px * aw) - 3
            cy = ax_y + int(py * ah) - 3
            rs.append(rect(cx, cy, 6, 6, color))
        return "".join(rs)
    out.append(plot(pts_before, ACC1))
    out.append(plot(pts_after, ACC2))
    # legend
    out.append(rect(x + w - 88, y + 12, 8, 4, ACC1))
    out.append(pixfont.render("BEFORE", x + w - 76, y + 10, 1, INK))
    out.append(rect(x + w - 88, y + 24, 8, 4, ACC2))
    out.append(pixfont.render("AFTER", x + w - 76, y + 22, 1, INK))
    # animated bouncing dot on after-line
    out.append(
        f'<circle cx="{ax_x + 30}" cy="{ax_y + int(0.20 * ah)}" r="4" fill="{INK}">'
        f'<animate attributeName="cx" values="{ax_x + 30};{ax_x + aw - 20};{ax_x + 30}" '
        f'dur="3s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    return "".join(out)


def screen_mindmap(x, y, w, h):
    """A small constellation of nodes connected by lines."""
    nodes = [(40, 30), (90, 70), (40, 110), (140, 40), (170, 90), (130, 120)]
    out = []
    for i, (a, b) in enumerate([(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (1, 4)]):
        n1 = (x + nodes[a][0], y + nodes[a][1])
        n2 = (x + nodes[b][0], y + nodes[b][1])
        out.append(
            f'<line x1="{n1[0]}" y1="{n1[1]}" x2="{n2[0]}" y2="{n2[1]}" '
            f'stroke="{PRIM}" stroke-width="2" opacity="0.6"/>'
        )
    colors = [ACC1, WARN, ACC2, PRIM, ACC1, WARN]
    for (nx, ny), c in zip(nodes, colors):
        absx, absy = x + nx - 8, y + ny - 8
        out += [rect(absx, absy, 16, 16, SHADOW),
                rect(absx + 2, absy + 2, 12, 12, c),
                rect(absx + 4, absy + 4, 8, 8, INK)]
        out.append(
            f'<rect x="{absx + 2}" y="{absy + 2}" width="12" height="12" fill="{c}">'
            f'<animate attributeName="opacity" values="1;0.6;1" dur="2s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    return "".join(out)


def screen_react_patterns(x, y, w, h):
    """A do/don't comparison: red X panel and green check panel."""
    out = []
    # Don't panel
    out += [rect(x + 12, y + 12, 88, h - 24, "#1A0A18"),
            rect(x + 12, y + 12, 88, 2, ACC1),
            rect(x + 12, y + h - 14, 88, 2, ACC1),
            rect(x + 12, y + 12, 2, h - 24, ACC1),
            rect(x + 98, y + 12, 2, h - 24, ACC1)]
    # X mark
    cx, cy = x + 56, y + h // 2
    for d in range(-12, 13, 4):
        out.append(rect(cx + d - 2, cy + d - 2, 4, 4, ACC1))
        out.append(rect(cx + d - 2, cy - d - 2, 4, 4, ACC1))
    # arrow
    out += [rect(x + 110, y + h // 2 - 2, 30, 4, INK),
            rect(x + 138, y + h // 2 - 6, 4, 12, INK),
            rect(x + 134, y + h // 2 - 4, 4, 8, INK)]
    # Do panel
    px = x + 152
    out += [rect(px, y + 12, 88, h - 24, "#0A1A0F"),
            rect(px, y + 12, 88, 2, ACC2),
            rect(px, y + h - 14, 88, 2, ACC2),
            rect(px, y + 12, 2, h - 24, ACC2),
            rect(px + 86, y + 12, 2, h - 24, ACC2)]
    # Check mark
    ccx, ccy = px + 44, y + h // 2 + 4
    for i, (dx, dy) in enumerate([(-12, -4), (-8, 0), (-4, 4), (0, 0),
                                   (4, -4), (8, -8), (12, -12)]):
        out.append(rect(ccx + dx - 2, ccy + dy - 2, 4, 4, ACC2))
    return "".join(out)


def screen_rusty(x, y, w, h):
    """Terminal output of a todo list."""
    out = []
    # Terminal frame
    out += [rect(x + 8, y + 8, w - 16, h - 16, "#0a0a14"),
            rect(x + 8, y + 8, w - 16, 14, "#202040"),
            rect(x + 14, y + 12, 4, 4, ACC1),
            rect(x + 22, y + 12, 4, 4, WARN),
            rect(x + 30, y + 12, 4, 4, ACC2)]
    # Prompt + items
    items = [("$", "RUSTY ADD CODE", INK),
             ("[X]", "FORGE PIXEL ART", ACC2),
             ("[X]", "DEPLOY VOXFLOW", ACC2),
             ("[ ]", "SHIP STUDY-BUDDY", WARN),
             ("[ ]", "WRITE BLOG POST", DIM)]
    for i, (mark, text, color) in enumerate(items):
        ty = y + 30 + i * 20
        out.append(pixfont.render(mark, x + 16, ty, 2, color))
        out.append(pixfont.render(text, x + 16 + pixfont.width(mark, 2) + 8, ty, 2, color))
    return "".join(out)


def screen_pwa(x, y, w, h):
    """Phone outline showing offline-capable PWA."""
    out = []
    # Phone
    pw_, ph_ = 70, h - 24
    px = x + (w - pw_) // 2
    py = y + 12
    out += [rect(px, py, pw_, ph_, "#16162A"),
            rect(px, py, pw_, 3, INK),
            rect(px, py + ph_ - 3, pw_, 3, INK),
            rect(px, py, 3, ph_, INK),
            rect(px + pw_ - 3, py, 3, ph_, INK)]
    # Screen
    out += [rect(px + 8, py + 12, pw_ - 16, ph_ - 28, "#08081A")]
    # Cards
    for i in range(3):
        cy = py + 18 + i * 22
        out += [rect(px + 12, cy, pw_ - 24, 16, ACC1 if i == 0 else PRIM)]
    # Offline cloud icon corner
    out += [rect(x + w - 38, y + 14, 24, 14, ACC2),
            rect(x + w - 30, y + 10, 14, 8, ACC2)]
    # diagonal slash through cloud (offline)
    for d in range(8):
        out.append(rect(x + w - 36 + d * 2, y + 28 - d * 2, 2, 2, ACC1))
    return "".join(out)


def cartridge(x, y, w, h, name, lang, blurb, accent, screen_fn):
    out = []
    shell, label_y, label_h = cartridge_shell(x, y, w, h, accent)
    out.append(shell)
    # Repo name on label
    name_scale = 3
    name_w = pixfont.width(name, name_scale)
    out.append(pixfont.render(name, x + (w - name_w) // 2,
                              label_y + (label_h - 7 * name_scale) // 2,
                              name_scale, BG))

    # Screen below label
    sx = x + 14
    sy = label_y + label_h + 12
    sw = w - 28
    sh = 130
    out.append(screen(sx, sy, sw, sh, accent))
    # Render screen content into the screen area
    out.append(screen_fn(sx, sy, sw, sh))

    # Lang chip
    chip_body, _ = chip(x + 14, sy + sh + 10, lang, accent, scale=2)
    out.append(chip_body)

    # Blurb
    blurb_y = sy + sh + 44
    for i, line in enumerate(blurb):
        out.append(pixfont.render(line, x + 14, blurb_y + i * 18, 2, ACC2))

    # bottom barcode strip
    barcode_y = y + h - 18
    bx = x + 14
    bw_ = w - 28
    out.append(rect(bx, barcode_y, bw_, 4, "#0a0a14"))
    import random
    rng = random.Random(hash(name) & 0xFFFF)
    cursor = bx + 2
    while cursor < bx + bw_ - 2:
        seg_w = rng.choice([2, 2, 4, 2, 6])
        if rng.random() > 0.4:
            out.append(rect(cursor, barcode_y, seg_w, 4, INK))
        cursor += seg_w + 1
    return "".join(out)


def build() -> str:
    out = [rect(0, 0, W, H, BG)]

    # title
    title = "PUBLIC CARTRIDGES"
    t_scale = 5
    tw = pixfont.width(title, t_scale)
    out.append(pixfont.render(title, (W - tw) // 2, 30, t_scale, INK))
    sub = "OPEN-SOURCE PROJECTS · PRESS START TO PLAY"
    sw = pixfont.width(sub, 2)
    out.append(pixfont.render(sub, (W - sw) // 2, 30 + 7 * t_scale + 14, 2, ACC2))

    # 3x2 grid
    cart_w, cart_h = 360, 340
    gap = 30
    grid_w = cart_w * 3 + gap * 2
    start_x = (W - grid_w) // 2
    start_y = 130

    cells = [
        # row 1
        ("VOXFLOW", "TYPESCRIPT", [
            "HOLD OPT. TALK. RELEASE.",
            "LOCAL WHISPER, 500MS LATENCY.",
            "MIT-LICENSED, NO CLOUD.",
        ], ACC1, screen_voxflow),
        ("REACT-PERF", "JAVASCRIPT", [
            "WORKED EXAMPLES OF MEMO,",
            "USECALLBACK, AND VIRTUALIZATION",
            "ON A 10K-ROW LIST.",
        ], PRIM, screen_perf),
        ("MIND-MAP", "TYPESCRIPT", [
            "VISUAL CONCEPT NETWORK",
            "FOR STUDYING. OFFLINE-FIRST,",
            "BROWSER-LOCAL STORAGE.",
        ], ACC2, screen_mindmap),
        # row 2
        ("RUSTY", "RUST", [
            "TINY CLI TODO IN RUST.",
            "FILE-BACKED, ZERO DEPS.",
            "FIRST RUST COMMIT, KEPT CLEAN.",
        ], WARN, screen_rusty),
        ("REACT.PATTERNS", "MARKDOWN", [
            "TOP REACT ANTI-PATTERNS",
            "WITH SIDE-BY-SIDE EXAMPLES.",
            "USED AS TEAM REFERENCE.",
        ], ACC1, screen_react_patterns),
        ("GB-CRA-PWA", "JAVASCRIPT", [
            "CREATE-REACT-APP + PWA",
            "SHELL DEMO. OFFLINE-FIRST",
            "BLOG ARCHITECTURE.",
        ], PRIM, screen_pwa),
    ]

    for i, (name, lang, blurb, accent, screen_fn) in enumerate(cells):
        col = i % 3
        row = i // 3
        x = start_x + col * (cart_w + gap)
        y = start_y + row * (cart_h + gap)
        out.append(cartridge(x, y, cart_w, cart_h, name, lang, blurb, accent, screen_fn))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="Public open-source projects as game cartridges" '
        f'shape-rendering="crispEdges">'
        + "".join(out) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
