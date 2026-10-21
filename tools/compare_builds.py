"""Compare two builds of Zad: per-table bytes, glyph outline hashes, and HarfBuzz shaping on a broad test set."""
import hashlib, itertools, sys, json
from fontTools.ttLib import TTFont
import uharfbuzz as hb
OLD, NEW = sys.argv[1], sys.argv[2]
W = ["Light", "Regular", "Medium", "SemiBold", "Bold"]
ar_letters = [chr(c) for c in range(0x0621, 0x064B)] + list("پچژکگیۀہےڈڑںٹھۓ")
tash = [chr(c) for c in range(0x064B, 0x0653)] + ["\u0670"]
texts = []
texts += ["بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "الحمد لله رب العالمين", "لا إله إلا الله محمد رسول الله", "نصٌّ عربيٌّ جميل — لا إله إلا الله",
          "مرحبًا بالعالم! Hello ١٢٣ ۴۵۶ گچپژ", "قَالَ رَسُولُ اللَّهِ ﷺ", "لأ لإ لآ لا ﻻ ﻷ", "سـ ـسـ ـس", "٠١٢٣٤٥٦٧٨٩ ۰۱۲۳۴۵۶۷۸۹ 0123456789 ٪ ٫ ٬ ؟ ، ؛",
          "خط زاد العربي: معلومات وكود تركيب ومعاينة", "فكرة Fekra 2026", "The quick brown fox jumps over the lazy dog. SPHINX OF BLACK QUARTZ, JUDGE MY VOW!",
          "Đ ĵ Ĉ ĉ ß Æ æ Œ œ ﬁ ﬂ — – … “quotes” ‘single’ € £ ¥ $ % & @ # → ←", "میں نے کہا کہ یہ کتاب بہت اچھی ہے", "این یک متن فارسی است با حروف گ چ پ ژ",
          "ٱلْكِتَٰبُ لَا رَيْبَ ۛ فِيهِ ۛ هُدًى لِّلْمُتَّقِينَ", "ـ" * 5, "a\u0301 e\u0300 o\u0308 n\u0303"]
texts += [a + b for a in ar_letters for b in ar_letters]            # every join pair
texts += [a + t for a in ar_letters for t in tash]                    # every letter + tashkeel
texts += ["ل" + a for a in "اأإآ"] + ["ب" + chr(c) + "ب" for c in range(0xFBB2, 0xFBC2)] + [chr(c) for c in range(0xFBB2, 0xFBC2)]
def cps(path): return sorted(TTFont(path).getBestCmap())
texts += [chr(c) for c in cps(f"{OLD}/Zad-Regular.ttf")]                # every codepoint alone
feats = [{}, {"liga": False}, {"kern": False}, {"mark": False, "mkmk": False}]
def shape(fontpath, text, f):
    blob = hb.Blob.from_file_path(fontpath); face = hb.Face(blob); font = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(font, buf, f)
    return [(i.codepoint, i.cluster, p.x_advance, p.y_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
report = {"weights": {}}
for w in W:
    o, n = f"{OLD}/Zad-{w}.ttf", f"{NEW}/Zad-{w}.ttf"
    fo, fn = TTFont(o), TTFont(n)
    tables = sorted(set(fo.keys()) | set(fn.keys()) - {"GlyphOrder"})
    changed = [t for t in tables if t != "GlyphOrder" and (t not in fo or t not in fn or fo.getTableData(t) != fn.getTableData(t))]
    go = fo.getGlyphOrder(); assert go == fn.getGlyphOrder()
    def gh(f, g): gl = f["glyf"][g]; gl.expand(f["glyf"]); return hashlib.sha256(f["glyf"][g].compile(f["glyf"])).hexdigest()
    outline_diff = [g for g in go if gh(fo, g) != gh(fn, g)]
    hmtx_diff = [g for g in go if fo["hmtx"][g] != fn["hmtx"][g]]
    sd = []; n_runs = 0
    for t in texts:
        for f in feats:
            n_runs += 1
            a, b = shape(o, t, f), shape(n, t, f)
            if a != b: sd.append((t, f))
    report["weights"][w] = {"glyphs": len(go), "changed_tables": changed, "outline_diffs": len(outline_diff), "hmtx_diffs": len(hmtx_diff), "shaping_runs": n_runs, "shaping_diffs": len(sd),
                            "diff_samples": [(" ".join(f"U+{ord(ch):04X}" for ch in t), f) for t, f in sd[:8]]}
    print(w, json.dumps(report["weights"][w], ensure_ascii=False))
print("texts", len(texts))
