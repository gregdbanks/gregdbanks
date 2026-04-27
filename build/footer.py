"""Footer: 'PRESS START TO CONNECT' marquee + contact chips."""
from __future__ import annotations
from pathlib import Path

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM, PANEL, SHADOW
import pixfont

W, H = 1200, 280
OUT = Path(__file__).parent.parent / "assets" / "footer.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def chip(x, y, label, accent, scale=2):
    pad = 14
    text_w = pixfont.width(label, scale)
    w = text_w + pad * 2
    h = 7 * scale + 14
    out = [
        rect(x + 3, y + 3, w, h, SHADOW),
        rect(x, y, w, h, PANEL),
        rect(x, y, w, 2, accent),
        rect(x, y + h - 2, w, 2, accent),
        rect(x, y, 2, h, accent),
        rect(x + w - 2, y, 2, h, accent),
        rect(x, y, 2, 2, BG),
        rect(x + w - 2, y, 2, 2, BG),
        rect(x, y + h - 2, 2, 2, BG),
        rect(x + w - 2, y + h - 2, 2, 2, BG),
        pixfont.render(label, x + pad, y + 7, scale, INK),
    ]
    return "".join(out), w


def chips_centered_row(cy, items, gap=20):
    # measure
    sizes = []
    for label, accent in items:
        text_w = pixfont.width(label, 2)
        w = text_w + 28
        sizes.append((label, accent, w))
    total = sum(w for _, _, w in sizes) + gap * (len(sizes) - 1)
    x = (W - total) // 2
    y = cy - 14
    out = []
    for label, accent, w in sizes:
        body, _ = chip(x, y, label, accent, 2)
        out.append(body)
        x += w + gap
    return "".join(out)


def build() -> str:
    out = [rect(0, 0, W, H, BG)]

    # decorative top border
    for i in range(W // 12):
        x = i * 12
        out.append(rect(x, 0, 6, 4, ACC1 if i % 6 == 0 else DIM))

    # PRESS [START] TO CONNECT — central marquee
    line1 = "- PRESS [START] -"
    s1 = 5
    w1 = pixfont.width(line1, s1)
    y1 = 40
    # shadow + body
    out.append(pixfont.render(line1, (W - w1) // 2 + 3, y1 + 3, s1, SHADOW))
    out.append(pixfont.render(line1, (W - w1) // 2, y1, s1, INK))

    # blinking glow underlay
    out.append(
        f'<g opacity="0">'
        f'<animate attributeName="opacity" values="0;0.45;0" dur="2.4s" repeatCount="indefinite"/>'
        + pixfont.render(line1, (W - w1) // 2, y1, s1, ACC2)
        + f'</g>'
    )

    line2 = "TO CONTINUE THE JOURNEY"
    s2 = 3
    w2 = pixfont.width(line2, s2)
    y2 = y1 + 7 * s1 + 16
    out.append(pixfont.render(line2, (W - w2) // 2, y2, s2, ACC2))

    # chips
    chips_y = y2 + 7 * s2 + 36
    out.append(chips_centered_row(chips_y, [
        ("@GREGDBANKS", ACC1),
        ("STUDY.COFFEE", PRIM),
        ("OPEN TO COLLABS", ACC2),
    ]))

    # animated walking sprite re-used: simple bobbing dots
    dots_y = chips_y + 50
    for i in range(7):
        cx = (W // 2) - 60 + i * 20
        out.append(
            f'<rect x="{cx}" y="{dots_y}" width="6" height="6" fill="{ACC1 if i % 2 == 0 else WARN}">'
            f'<animate attributeName="opacity" values="0.2;1;0.2" dur="1.6s" '
            f'begin="{i * 0.15}s" repeatCount="indefinite"/>'
            f'</rect>'
        )

    # decorative bottom signature bar
    sig_y = H - 36
    sig = "// MADE WITH PIXEL LOVE IN OKLAHOMA CITY"
    sw = pixfont.width(sig, 2)
    out.append(rect((W - sw) // 2 - 18, sig_y - 4, sw + 36, 28, PANEL))
    out.append(rect((W - sw) // 2 - 18, sig_y - 4, sw + 36, 2, PRIM))
    out.append(rect((W - sw) // 2 - 18, sig_y + 22, sw + 36, 2, PRIM))
    out.append(pixfont.render(sig, (W - sw) // 2, sig_y + 6, 2, ACC2))

    # decorative bottom border
    for i in range(W // 12):
        x = i * 12
        out.append(rect(x, H - 4, 6, 4, ACC1 if i % 6 == 0 else DIM))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="img" aria-label="Press start to connect — contact chips" '
        f'shape-rendering="crispEdges">'
        + "".join(out) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
