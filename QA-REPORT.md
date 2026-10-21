# Zad — FontBakery QA report

Tool: FontBakery 1.1.0 · profile: `universal` · date: 21 October 2026  
Targets: 5 weights (`fonts/Zad-{Light,Regular,Medium,SemiBold,Bold}.ttf`).

Machine-readable summary: [`qa.json`](qa.json).

## Result

| Target    | FATAL | FAIL | WARN | PASS | SKIP |
| --------- | :---: | :--: | :--: | :--: | :--: |
| 5 weights |   0   |  15  |  30  | 355  | 172  |

> Earlier docs that claimed **0 FAIL** referred to an older 3-weight
> `check-opentype` run. The numbers above are the current 5-weight
> `universal` profile results.

### FAIL breakdown (15 = 3 checks × 5 weights)

| Check | Count | Source |
| ----- | :---: | ------ |
| `arabic_spacing_symbols` | 5 | Inherited from IBM Plex Sans Arabic (GDEF marks U+FBB2… with advance width) |
| `case_mapping` | 5 | Inherited — missing case pairs (e.g. U+0110↔U+0111) already absent upstream |
| `smart_dropout` | 5 | Inherited hinting / prep from IBM Plex masters |

### Fixes applied in this kit (build.py)

- `opentype/family/underline_thickness` — normalised `post.underlineThickness`
  / `underlinePosition` to Regular’s values (60 / −95) across all five weights.
- `no_mac_entries` — stopped writing Macintosh (platform 1) name records so the
  derivative matches upstream (which ships Windows-only names).

### Remaining WARN (30 = 6 checks × 5 weights, all upstream)

- `opentype/gdef_non_mark_chars`
- `arabic_high_hamza`
- `contour_count`
- `ligature_carets`
- `soft_hyphen`
- `valid_glyphnames`

None of these affect Arabic joining or mark positioning in practice. Resolving
them would mean editing IBM Plex outlines / GDEF, which this lightweight
rename/subset kit deliberately does not do.

### Shaping

Arabic joining, lam-alef ligatures, and tashkeel positions were verified with
HarfBuzz against the previous kit binaries after the metadata rebuild — glyph
ids, advances, and offsets match.

## Reproduce

```bash
pip install fontbakery
fontbakery check-universal fonts/Zad-*.ttf
```
