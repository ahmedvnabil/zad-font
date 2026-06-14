#!/usr/bin/env python3
"""
Zad font kit builder.

Takes the original IBM Plex Sans Arabic weights (SIL OFL 1.1) from ./_src,
subsets them to Arabic + Latin + digits + punctuation while preserving ALL
OpenType layout features (so Arabic joining/shaping stays intact), renames the
font internally to "Zad", and writes compressed .woff2 files to ./fonts.

OFL compliance:
  - The new name "Zad" does NOT contain the Reserved Font Name "Plex".
  - The original copyright + OFL license notices are preserved in the name table.
  - A modification notice is appended to the copyright record.
  - OFL.txt is shipped alongside the fonts.

Re-run after editing WEIGHTS to change which weights are bundled.

Requires: fonttools, brotli  (pip install fonttools brotli)
"""
from __future__ import annotations

import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
NEW_FAMILY = "Zad"
VENDOR_ID = "ZAD "  # 4 chars, OS/2 achVendID
DERIVATIVE_HOLDER = "Ahmed Morsy"  # copyright holder of the Zad derivative
DERIVATIVE_YEAR = "2026"

HERE = Path(__file__).resolve().parent
SRC = HERE / "_src"
OUT = HERE / "fonts"

# weight name (matches _src/IBMPlexSansArabic-<name>.ttf)  ->  (usWeightClass, is_bold)
WEIGHTS = {
    "Light": (300, False),
    "Regular": (400, False),
    "Medium": (500, False),
    "SemiBold": (600, False),
    "Bold": (700, True),
}

# Unicode ranges to keep. The subsetter only keeps codepoints actually present
# in the font, so over-specifying is harmless. Layout features are kept in full
# (layout_features = ['*']) which is what preserves Arabic contextual shaping.
UNICODE_RANGES = [
    (0x0000, 0x00FF),  # Basic Latin + Latin-1 Supplement
    (0x0100, 0x017F),  # Latin Extended-A
    (0x0180, 0x024F),  # Latin Extended-B
    (0x02B0, 0x02FF),  # Spacing modifier letters
    (0x0300, 0x036F),  # Combining diacritics
    (0x0600, 0x06FF),  # Arabic
    (0x0750, 0x077F),  # Arabic Supplement
    (0x08A0, 0x08FF),  # Arabic Extended-A
    (0x2000, 0x206F),  # General Punctuation (smart quotes, dashes, etc.)
    (0x2070, 0x209F),  # Super/subscripts
    (0x20A0, 0x20CF),  # Currency symbols
    (0x2190, 0x21FF),  # Arrows
    (0x2200, 0x22FF),  # Mathematical operators
    (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
    (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
]


def unicode_set() -> set[int]:
    out: set[int] = set()
    for lo, hi in UNICODE_RANGES:
        out.update(range(lo, hi + 1))
    return out


RESERVED_NAME = "Plex"  # IBM's Reserved Font Name

# Identity records that DEFINE the font's name — these must never carry the
# reserved name. We overwrite all of them in rename().
IDENTITY_IDS = {1, 2, 3, 4, 6, 16, 17}
# Marketing / trademark records the subsetter inherits verbatim. OFL forbids
# carrying the reserved name in the derivative, so any of these that still
# mention "Plex" are dropped. Attribution records (copyright/license/designer)
# are intentionally NOT here — naming the source "IBM Plex Sans Arabic" is
# required attribution, which the reserved-name clause explicitly permits.
MARKETING_IDS = {7, 10, 19}  # trademark, description, sample text


def set_name(font: TTFont, name_id: int, value: str) -> None:
    """Set a name record for both Windows (3,1,0x409) and Mac (1,0,0)."""
    name = font["name"]
    name.setName(value, name_id, 3, 1, 0x409)
    name.setName(value, name_id, 1, 0, 0)


def purge_reserved_name(font: TTFont) -> list[int]:
    """Drop inherited marketing records that still carry the Reserved Font Name.

    Only MARKETING_IDS are touched. Identity records are already rewritten to
    "Zad"; attribution records (copyright/license/designer) legitimately keep
    the "IBM Plex Sans Arabic" reference and are left intact.
    Returns the list of dropped name IDs (for reporting).
    """
    name = font["name"]
    dropped = []
    kept = []
    for rec in name.names:
        try:
            text = rec.toUnicode()
        except Exception:
            kept.append(rec)
            continue
        if rec.nameID in MARKETING_IDS and RESERVED_NAME.lower() in text.lower():
            dropped.append(rec.nameID)
        else:
            kept.append(rec)
    name.names = kept
    return sorted(set(dropped))


def rename(font: TTFont, weight_name: str, weight_class: int, is_bold: bool) -> None:
    """Rewrite the name table + weight metadata to the Zad family."""
    name = font["name"]

    # Preserve original copyright (id 0) and append a modification notice.
    original_copyright = ""
    rec = name.getName(0, 3, 1, 0x409) or name.getName(0, 1, 0, 0)
    if rec:
        original_copyright = rec.toUnicode()
    mod_notice = (
        f"{original_copyright} "
        f'"{NEW_FAMILY}" derivative Copyright {DERIVATIVE_YEAR} {DERIVATIVE_HOLDER}. '
        f"{NEW_FAMILY} is a renamed/subset derivative of IBM Plex Sans Arabic, "
        "distributed under the SIL Open Font License 1.1. "
        'It does not use the Reserved Font Name "Plex".'
    ).strip()
    set_name(font, 0, mod_notice)

    # RIBBI-safe naming: Medium is not part of Regular/Bold/Italic/BoldItalic,
    # so it gets its own legacy family "Zad Medium" while modern apps group it
    # under the typographic family "Zad" via name IDs 16/17.
    if is_bold:
        legacy_family, legacy_sub = NEW_FAMILY, "Bold"
    elif weight_name == "Regular":
        legacy_family, legacy_sub = NEW_FAMILY, "Regular"
    else:
        legacy_family, legacy_sub = f"{NEW_FAMILY} {weight_name}", "Regular"

    full_name = f"{NEW_FAMILY} {weight_name}"
    ps_name = f"{NEW_FAMILY}-{weight_name}".replace(" ", "")

    set_name(font, 1, legacy_family)              # Family
    set_name(font, 2, legacy_sub)                 # Subfamily
    set_name(font, 3, f"1.000;{VENDOR_ID.strip()};{ps_name}")  # Unique ID
    set_name(font, 4, full_name)                  # Full name
    set_name(font, 6, ps_name)                    # PostScript name
    set_name(font, 16, NEW_FAMILY)                # Typographic Family
    set_name(font, 17, weight_name)               # Typographic Subfamily

    # Weight / style flags
    os2 = font["OS/2"]
    os2.usWeightClass = weight_class
    os2.achVendID = VENDOR_ID
    head = font["head"]

    # fsSelection: bit0=italic, bit5=bold, bit6=regular
    fs = os2.fsSelection
    fs &= ~(1 << 0)   # clear italic
    if is_bold:
        fs |= (1 << 5)        # bold
        fs &= ~(1 << 6)       # clear regular
        head.macStyle |= 0x01  # bold
    else:
        fs &= ~(1 << 5)       # clear bold
        fs |= (1 << 6)        # regular
        head.macStyle &= ~0x01
    os2.fsSelection = fs


def build_weight(weight_name: str, weight_class: int, is_bold: bool) -> dict:
    src = SRC / f"IBMPlexSansArabic-{weight_name}.ttf"
    if not src.exists():
        sys.exit(f"ERROR: missing source font {src}")

    # recalcTimestamp=False keeps head.modified stable → reproducible output.
    font = TTFont(src, recalcTimestamp=False)
    before_glyphs = font["maxp"].numGlyphs

    # --- subset (keep all layout features → Arabic shaping survives) ---------
    options = Options()
    options.layout_features = ["*"]   # CRITICAL for Arabic joining/ligatures
    options.name_IDs = ["*"]
    options.glyph_names = True         # keep names so shaping can be verified
    options.notdef_outline = True
    options.recommended_glyphs = True
    options.drop_tables = ["DSIG"]     # our edits invalidate the signature
    options.recalc_bounds = True
    options.recalc_timestamp = False

    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=unicode_set())
    subsetter.subset(font)
    after_glyphs = font["maxp"].numGlyphs

    # --- rename to Zad -------------------------------------------------------
    rename(font, weight_name, weight_class, is_bold)

    # --- strip any name record that still carries the reserved name ----------
    dropped = purge_reserved_name(font)

    # --- write desktop .ttf + web .woff2 (both from the same subset) ---------
    OUT.mkdir(parents=True, exist_ok=True)
    ttf_path = OUT / f"{NEW_FAMILY}-{weight_name}.ttf"
    font.flavor = None
    font.save(ttf_path)

    out_path = OUT / f"{NEW_FAMILY}-{weight_name}.woff2"
    font.flavor = "woff2"
    font.save(out_path)

    return {
        "weight": weight_name,
        "class": weight_class,
        "glyphs_before": before_glyphs,
        "glyphs_after": after_glyphs,
        "dropped_name_ids": dropped,
        "out": out_path,
        "ttf": ttf_path,
        "kb": out_path.stat().st_size / 1024,
    }


def main() -> None:
    print(f"Building '{NEW_FAMILY}' from {SRC}\n")
    results = []
    for wname, (wclass, is_bold) in WEIGHTS.items():
        r = build_weight(wname, wclass, is_bold)
        results.append(r)
        dropped = (
            f"  dropped 'Plex' name IDs {r['dropped_name_ids']}"
            if r["dropped_name_ids"]
            else "  (no reserved-name records)"
        )
        print(
            f"  {r['weight']:8} w{r['class']}  "
            f"glyphs {r['glyphs_before']}→{r['glyphs_after']}  "
            f"{r['kb']:6.1f} KB  →  {r['out'].name}{dropped}"
        )
    total = sum(r["kb"] for r in results)
    print(f"\nDone. {len(results)} weights, {total:.1f} KB total in {OUT}")


if __name__ == "__main__":
    main()
