"""5x7 pixel font, hand-drawn. Authentic NES-era proportions.

Glyphs are strings of '.' and 'O' rows; 'O' becomes a square <rect>.
Renders at any scale via render(text, x, y, scale, color).

Only uppercase + digits + common punctuation. Lowercase is folded to
uppercase for retro consistency.
"""
from textwrap import dedent

GLYPH_W = 5
GLYPH_H = 7

# fmt: off
_GLYPHS = {
    "A": ".OOO.\nO...O\nO...O\nOOOOO\nO...O\nO...O\nO...O",
    "B": "OOOO.\nO...O\nO...O\nOOOO.\nO...O\nO...O\nOOOO.",
    "C": ".OOOO\nO....\nO....\nO....\nO....\nO....\n.OOOO",
    "D": "OOOO.\nO...O\nO...O\nO...O\nO...O\nO...O\nOOOO.",
    "E": "OOOOO\nO....\nO....\nOOOO.\nO....\nO....\nOOOOO",
    "F": "OOOOO\nO....\nO....\nOOOO.\nO....\nO....\nO....",
    "G": ".OOOO\nO....\nO....\nO..OO\nO...O\nO...O\n.OOO.",
    "H": "O...O\nO...O\nO...O\nOOOOO\nO...O\nO...O\nO...O",
    "I": ".OOO.\n..O..\n..O..\n..O..\n..O..\n..O..\n.OOO.",
    "J": "..OOO\n...O.\n...O.\n...O.\n...O.\nO..O.\n.OO..",
    "K": "O...O\nO..O.\nO.O..\nOO...\nO.O..\nO..O.\nO...O",
    "L": "O....\nO....\nO....\nO....\nO....\nO....\nOOOOO",
    "M": "O...O\nOO.OO\nO.O.O\nO.O.O\nO...O\nO...O\nO...O",
    "N": "O...O\nOO..O\nO.O.O\nO.O.O\nO.O.O\nO..OO\nO...O",
    "O": ".OOO.\nO...O\nO...O\nO...O\nO...O\nO...O\n.OOO.",
    "P": "OOOO.\nO...O\nO...O\nOOOO.\nO....\nO....\nO....",
    "Q": ".OOO.\nO...O\nO...O\nO...O\nO.O.O\nO..OO\n.OOOO",
    "R": "OOOO.\nO...O\nO...O\nOOOO.\nO.O..\nO..O.\nO...O",
    "S": ".OOOO\nO....\nO....\n.OOO.\n....O\n....O\nOOOO.",
    "T": "OOOOO\n..O..\n..O..\n..O..\n..O..\n..O..\n..O..",
    "U": "O...O\nO...O\nO...O\nO...O\nO...O\nO...O\n.OOO.",
    "V": "O...O\nO...O\nO...O\nO...O\nO...O\n.O.O.\n..O..",
    "W": "O...O\nO...O\nO...O\nO.O.O\nO.O.O\nOO.OO\nO...O",
    "X": "O...O\nO...O\n.O.O.\n..O..\n.O.O.\nO...O\nO...O",
    "Y": "O...O\nO...O\n.O.O.\n..O..\n..O..\n..O..\n..O..",
    "Z": "OOOOO\n....O\n...O.\n..O..\n.O...\nO....\nOOOOO",
    "0": ".OOO.\nO...O\nO..OO\nO.O.O\nOO..O\nO...O\n.OOO.",
    "1": "..O..\n.OO..\nO.O..\n..O..\n..O..\n..O..\nOOOOO",
    "2": ".OOO.\nO...O\n....O\n...O.\n..O..\n.O...\nOOOOO",
    "3": ".OOO.\nO...O\n....O\n..OO.\n....O\nO...O\n.OOO.",
    "4": "...O.\n..OO.\n.O.O.\nO..O.\nOOOOO\n...O.\n...O.",
    "5": "OOOOO\nO....\nOOOO.\n....O\n....O\nO...O\n.OOO.",
    "6": ".OOO.\nO....\nO....\nOOOO.\nO...O\nO...O\n.OOO.",
    "7": "OOOOO\n....O\n...O.\n..O..\n.O...\n.O...\n.O...",
    "8": ".OOO.\nO...O\nO...O\n.OOO.\nO...O\nO...O\n.OOO.",
    "9": ".OOO.\nO...O\nO...O\n.OOOO\n....O\n....O\n.OOO.",
    " ": ".....\n.....\n.....\n.....\n.....\n.....\n.....",
    ".": ".....\n.....\n.....\n.....\n.....\n.....\n..OO.",
    ",": ".....\n.....\n.....\n.....\n.....\n..OO.\n..O..",
    ":": ".....\n.....\n..O..\n.....\n..O..\n.....\n.....",
    "/": "....O\n....O\n...O.\n..O..\n.O...\nO....\nO....",
    "-": ".....\n.....\n.....\nOOOOO\n.....\n.....\n.....",
    "_": ".....\n.....\n.....\n.....\n.....\n.....\nOOOOO",
    "+": ".....\n..O..\n..O..\nOOOOO\n..O..\n..O..\n.....",
    "·": ".....\n.....\n.....\n..O..\n.....\n.....\n.....",
    "@": ".OOO.\nO...O\nO.OOO\nO.O.O\nO.OOO\nO....\n.OOO.",
    "!": "..O..\n..O..\n..O..\n..O..\n..O..\n.....\n..O..",
    "?": ".OOO.\nO...O\n....O\n..OO.\n..O..\n.....\n..O..",
    "#": ".O.O.\n.O.O.\nOOOOO\n.O.O.\nOOOOO\n.O.O.\n.O.O.",
    "<": "....O\n...O.\n..O..\n.O...\n..O..\n...O.\n....O",
    ">": "O....\n.O...\n..O..\n...O.\n..O..\n.O...\nO....",
    "[": ".OOO.\n.O...\n.O...\n.O...\n.O...\n.O...\n.OOO.",
    "]": ".OOO.\n...O.\n...O.\n...O.\n...O.\n...O.\n.OOO.",
    "(": "..OO.\n.O...\n.O...\n.O...\n.O...\n.O...\n..OO.",
    ")": ".OO..\n...O.\n...O.\n...O.\n...O.\n...O.\n.OO..",
    "*": ".....\n.O.O.\n..O..\nOOOOO\n..O..\n.O.O.\n.....",
    "=": ".....\nOOOOO\n.....\nOOOOO\n.....\n.....\n.....",
    "'": "..O..\n..O..\n.....\n.....\n.....\n.....\n.....",
    "\"": ".O.O.\n.O.O.\n.....\n.....\n.....\n.....\n.....",
    "&": ".OO..\nO..O.\nO.O..\n.O...\nO.O.O\nO..O.\n.OO.O",
    "%": "OO..O\nOO.O.\n...O.\n..O..\n.O...\n.O.OO\nO..OO",
    "$": "..O..\n.OOOO\nO.O..\n.OOO.\n..O.O\nOOOO.\n..O..",
    "|": "..O..\n..O..\n..O..\n..O..\n..O..\n..O..\n..O..",
}
# fmt: on


def width(text: str, scale: int = 1, tracking: int = 1) -> int:
    """Pixel width of a rendered string."""
    if not text:
        return 0
    chars = len(text)
    return chars * GLYPH_W * scale + (chars - 1) * tracking * scale


def render(text: str, x: int, y: int, scale: int = 1, color: str = "#F8F8F2",
           tracking: int = 1) -> str:
    """Return SVG fragment placing `text` at (x, y) at the given scale."""
    out = []
    cursor = x
    for ch in text.upper():
        if ch == "\n":
            continue
        glyph = _GLYPHS.get(ch, _GLYPHS["?"])
        for row, line in enumerate(glyph.split("\n")):
            for col, cell in enumerate(line):
                if cell == "O":
                    out.append(
                        f'<rect x="{cursor + col * scale}" '
                        f'y="{y + row * scale}" '
                        f'width="{scale}" height="{scale}" fill="{color}"/>'
                    )
        cursor += (GLYPH_W + tracking) * scale
    return "".join(out)


def render_centered(text: str, cx: int, y: int, scale: int = 1,
                    color: str = "#F8F8F2", tracking: int = 1) -> str:
    w = width(text, scale, tracking)
    return render(text, cx - w // 2, y, scale, color, tracking)


__all__ = ["render", "render_centered", "width", "GLYPH_W", "GLYPH_H"]
