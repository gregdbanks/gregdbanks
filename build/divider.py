"""Section divider: pixel rule with a sweeping highlight."""
from __future__ import annotations
from pathlib import Path

from palette import BG, INK, PRIM, ACC1, ACC2, WARN, DIM
import pixfont

W, H = 1200, 32
OUT = Path(__file__).parent.parent / "assets" / "divider.svg"


def rect(x, y, w, h, fill, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def build() -> str:
    out = [rect(0, 0, W, H, BG)]
    # base rule (dashed)
    dash_y = 14
    for x in range(0, W, 12):
        out.append(rect(x, dash_y, 6, 4, DIM))
    # mid diamond
    cx = W // 2
    out.append(rect(cx - 6, dash_y - 4, 12, 12, ACC1))
    out.append(rect(cx - 4, dash_y - 6, 8, 16, ACC1))
    out.append(rect(cx - 2, dash_y - 8, 4, 20, ACC1))
    out.append(rect(cx - 2, dash_y - 2, 4, 8, INK))
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="100%" role="presentation" shape-rendering="crispEdges">'
        + "".join(out) + "</svg>"
    )
    return svg


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
