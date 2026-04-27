# /build — SVG generators for the profile

Every asset under `/assets` is hand-authored from these scripts. Re-run any
file to regenerate its SVG. Palette and pixel font are shared.

```sh
cd build
python3 banner.py
python3 player_card.py
python3 skill_tree.py
python3 ecosystems.py
python3 cartridges.py
python3 divider.py
python3 footer.py
```

Or all at once:

```sh
cd build && for f in banner player_card skill_tree ecosystems cartridges divider footer; do python3 ${f}.py; done
```

## Files

| File | Purpose |
|---|---|
| `palette.py` | Locked NES-inspired color palette |
| `pixfont.py` | 5×7 hand-drawn pixel font + render helpers |
| `banner.py` | Hero banner with animated walking sprite + skyline |
| `player_card.py` | JRPG-style status panel |
| `skill_tree.py` | Skill constellation: 4 branches around a core |
| `ecosystems.py` | Three private project clusters |
| `cartridges.py` | Public OSS repos as 8-bit cartridges |
| `divider.py` | Section divider with sweeping highlight |
| `footer.py` | Press-START contact panel |

## Conventions

- All SVGs use `shape-rendering="crispEdges"` for pixel fidelity
- Animations use SMIL (works inside `<img>` tags on GitHub)
- `viewBox` is virtual pixels; physical scale comes from `width="100%"` on the
  `<img>` tag in the README
