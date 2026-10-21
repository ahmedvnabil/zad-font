# Zad — FontBakery QA report

Tool: FontBakery 1.1.0 · profile: `universal` · date: 21 October 2026  
Targets: 5 weights (`fonts/Zad-{Light,Regular,Medium,SemiBold,Bold}.ttf`).

Machine-readable summary: [`qa.json`](qa.json).

## Result

| Target    | FATAL | FAIL | WARN | PASS | SKIP |
| --------- | :---: | :--: | :--: | :--: | :--: |
| 5 weights |   0   |  10  |  30  | 360  | 172  |

> Earlier docs that claimed **0 FAIL** referred to an older 3-weight
> `check-opentype` run. The numbers above are the current 5-weight
> `universal` profile results.

### FAIL breakdown (10 = 2 checks × 5 weights, both inherited)

| Check | Count | Why it is not fixed |
| ----- | :---: | ------------------- |
| `arabic_spacing_symbols` | 5 | Upstream classes U+FBB2–U+FBC1 as GDEF marks **and** draws them with a zero advance. Re-classing them as base glyphs (tested) only turns this into 5 × `base_has_width` FAIL; a real fix needs new advance widths, i.e. a spacing/design change. |
| `case_mapping` | 5 | U+0110 Đ ships without U+0111 đ, and U+0135 ĵ without U+0134 Ĵ (already absent upstream). Fixing needs new glyphs (đ needs a newly drawn stroke). |

Before this change: 15 FAIL (the two above + `smart_dropout` × 5).

### Fixes applied in this kit (build.py)

- `smart_dropout` — prepend TrueType smart dropout control (`PUSHW 511, SCANCTRL, PUSHB 4, SCANTYPE`)
  to the inherited `prep` program. It only stops pixels from dropping out at tiny sizes; outlines,
  metrics and the rest of the hinting program are unchanged.
- `opentype/family/underline_thickness` — normalised `post.underlineThickness`
  / `underlinePosition` to Regular’s values (60 / −95) across all five weights.
- `no_mac_entries` — stopped writing Macintosh (platform 1) name records so the
  derivative matches upstream (which ships Windows-only names).

### Verification of the smart-dropout rebuild

`tools/compare_builds.py <old fonts dir> fonts` compared every weight against the previous build:
only `head.checkSumAdjustment` and `prep` differ; all glyph outline hashes and `hmtx` entries are
identical; HarfBuzz shaping (glyph ids, clusters, advances, offsets) is identical for 4,814 strings ×
4 feature settings (default, no `liga`, no `kern`, no `mark`/`mkmk`): every Arabic letter pair,
every letter + tashkeel, Lam-Alef forms, Quranic text with small high marks, Persian/Urdu, Arabic and
Latin digits, Latin text, the Arabic spacing symbols, and every encoded codepoint on its own.

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
