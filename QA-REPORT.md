# Zad — FontBakery QA report

Tool: FontBakery 1.1.0 · profile: `check-opentype` · date: 12 June 2026
Targets: 3 weights (`fonts/Zad-{Regular,Medium,Bold}.ttf`).

## Result

| Target          | FATAL | FAIL | WARN | PASS |
| --------------- | :---: | :--: | :--: | :--: |
| 3 weights       |   0   |  0   |  1   |  88  |

**No FAIL or FATAL.**

### Fix applied

- `opentype/family/underline_thickness` — normalised `post.underlineThickness`
  / `underlinePosition` to be identical across the three weights (the upstream
  IBM Plex masters used slightly different values per weight).

### Remaining WARN (upstream)

- `opentype/gdef_non_mark_chars` — a few glyphs are classed as marks in the
  GDEF table while having advance width. This is inherited from **IBM Plex Sans
  Arabic** (Zad's source) and does not affect shaping in practice; resolving it
  would require editing the upstream GDEF.

### Environmental note

`opentype/italic_angle` ERROR is a missing-dependency artifact in this sandbox
(`beziers` / `opentype-sanitizer` unavailable), not a font defect.

## Reproduce

```bash
pip install fontbakery
fontbakery check-opentype fonts/Zad-*.ttf
```
