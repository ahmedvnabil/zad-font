"""Build the README artwork in assets/readme/ from the Zad fonts themselves.

Text is shaped with HarfBuzz (real Arabic joining) and written as outlined <path>s, so the SVGs
render identically on GitHub (which blocks web fonts inside <img> SVGs). Animations are CSS
@keyframes inside each SVG and are switched off under prefers-reduced-motion (the final state is
the default state, so a static render shows the finished artwork).

    pip install fonttools uharfbuzz
    python tools/readme_assets.py
    npx -y svgo@3 --config tools/svgo.config.cjs -f assets/readme   # optional, ~50% smaller
"""
import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "readme")
WEIGHTS = [("Light", 300), ("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700)]
THEMES = {
    "light": dict(bg="#faf7f2", card="#f1ece2", ink="#14201c", soft="#5b6b64", accent="#145a49", line="#ddd5c6"),
    "dark": dict(bg="#0d1411", card="#15201b", ink="#f1ece2", soft="#9fb0a8", accent="#e0b45c", line="#26352e"),
}

class Face:
    def __init__(self, style):
        path = os.path.join(ROOT, "fonts", f"Zad-{style}.ttf")
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        self.upem = self.tt["head"].unitsPerEm
        self.hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(path)))
        self.cache = {}

    def shape(self, text, rtl=None):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        if rtl is not None: buf.direction = "rtl" if rtl else "ltr"
        hb.shape(self.hbfont, buf, {"kern": True, "liga": True})
        x, out = 0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):   # visual order, left to right
            out.append((self.order[info.codepoint], x + pos.x_offset, pos.y_offset, info.cluster))
            x += pos.x_advance
        return out, x

    def outline(self, name, dx, dy, scale, ox, oy):
        """Glyph path in output pixels (y flipped), rounded to 0.1 px."""
        pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        self.gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, ox + dx * scale, oy - dy * scale)))
        return pen.getCommands()

    def text_paths(self, text, size, x, y, anchor="start", rtl=None, per_glyph=False):
        glyphs, adv = self.shape(text, rtl)
        s = size / self.upem; w = adv * s
        x0 = x - w if anchor == "end" else x - w / 2 if anchor == "middle" else x
        parts = [self.outline(n, gx, gy, s, x0, y) for n, gx, gy, _ in glyphs]
        return (parts if per_glyph else "".join(p for p in parts if p)), w

FACES = {st: Face(st) for st, _ in WEIGHTS}
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

def svg(w, h, css, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
            f"<title>{title}</title><style>{css}{RM}</style>{body}</svg>")

def write(name, data):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f: f.write(data)
    print(f"{name:28s} {len(data.encode()) / 1024:6.1f} KB")

def hero(t):
    W, H = 1280, 420
    bold, reg = FACES["Bold"], FACES["Regular"]
    letters, _ = bold.text_paths("زاد", 210, W / 2, 196, "middle", per_glyph=True)
    ar, _ = reg.text_paths("خط عربي نظيف ومفتوح المصدر للويب", 34, W / 2, 330, "middle")
    en, _ = reg.text_paths("Open-source Arabic web font  ·  5 weights  ·  SIL OFL 1.1", 21, W / 2, 374, "middle", rtl=False)
    css = (f".l{{fill:{t['ink']};animation:up .9s cubic-bezier(.2,.7,.2,1) backwards}}"
           ".l1{animation-delay:.1s}.l2{animation-delay:.3s}.l3{animation-delay:.5s}"
           f".ar{{fill:{t['ink']};animation:fade 1s .9s backwards}}.en{{fill:{t['soft']};animation:fade 1s 1.2s backwards}}"
           f".u{{fill:none;stroke:{t['accent']};stroke-width:4;stroke-linecap:round;stroke-dasharray:240;animation:draw 1.2s .7s cubic-bezier(.6,0,.2,1) backwards}}"
           f".d{{fill:{t['accent']};animation:fade .6s 1.6s backwards}}"
           "@keyframes up{from{opacity:0;transform:translateY(28px)}}@keyframes fade{from{opacity:0}}@keyframes draw{from{stroke-dashoffset:240}}")
    # HarfBuzz returns RTL glyphs in visual order (left to right), so the first letter ز is the rightmost: animate right to left
    order = list(range(len(letters)))[::-1]
    g = "".join(f'<path class="l l{order.index(i) + 1}" d="{p}"/>' for i, p in enumerate(letters) if p)
    body = (f'<rect width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>'
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="none" stroke="{t["line"]}"/>'
            f"{g}<path class=\"u\" d=\"M{W / 2 - 120} 272H{W / 2 + 120}\"/>"
            f'<circle class="d" cx="{W / 2 + 140}" cy="272" r="5"/><circle class="d" cx="{W / 2 - 140}" cy="272" r="5"/>'
            f'<path class="ar" d="{ar}"/><path class="en" d="{en}"/>')
    return svg(W, H, css, body, "Zad — خط عربي نظيف ومفتوح المصدر للويب")

SAMPLE = "زاد خط عربي واضح ومريح للقراءة على الشاشات"

def weights(t):
    W, row, top = 1280, 92, 36
    H = top * 2 + row * len(WEIGHTS) - 20
    reg = FACES["Regular"]; body = [f'<rect width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>',
                                    f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="none" stroke="{t["line"]}"/>']
    css = (f".s{{fill:{t['ink']};animation:in .8s cubic-bezier(.2,.7,.2,1) backwards}}.m{{fill:{t['soft']}}}"
           f".n{{fill:{t['accent']}}}.r{{stroke:{t['line']}}}"
           + "".join(f".w{i}{{animation-delay:{.12 * i:.2f}s}}" for i in range(len(WEIGHTS)))
           + "@keyframes in{from{opacity:0;transform:translateX(-24px)}}")
    for i, (st, wt) in enumerate(WEIGHTS):
        y = top + i * row + 52
        name, _ = reg.text_paths(st, 22, 48, y - 12, rtl=False)
        num, _ = reg.text_paths(str(wt), 18, 48, y + 16, rtl=False)
        sample, _ = FACES[st].text_paths(SAMPLE, 40, W - 48, y + 4, "end")
        body.append(f'<path class="m" d="{name}"/><path class="n" d="{num}"/><path class="s w{i}" d="{sample}"/>')
        if i: body.append(f'<path class="r" d="M48 {y - row + 30}H{W - 48}"/>')
    return svg(W, H, css, "".join(body), "Zad weights: Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700")

# (letter, label) — each panel shows one contextual form, forced with ZWJ (U+200D)
LETTERS = ["ع", "ه", "ك", "ب"]
FORMS = [("Isolated", "منفصل", "{}"), ("Initial", "أول", "{}\u200d"), ("Medial", "وسط", "\u200d{}\u200d"), ("Final", "آخر", "\u200d{}")]

def forms(t):
    W, H, n = 1280, 330, len(FORMS)
    pw, gap, x0 = 272, 24, 48
    bold, reg = FACES["SemiBold"], FACES["Regular"]
    body = [f'<rect width="{W}" height="{H}" rx="24" fill="{t["bg"]}"/>',
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="23" fill="none" stroke="{t["line"]}"/>']
    cyc = 3 * len(LETTERS)   # seconds per full cycle (3 s per letter)
    css = (f".p{{fill:{t['card']}}}.g{{fill:{t['ink']}}}.m{{fill:{t['soft']}}}.a{{fill:{t['accent']}}}"
           f".c{{opacity:0;animation:cy {cyc}s infinite}}.c0{{opacity:1}}"
           + "".join(f".c{i}{{animation-delay:{3 * i - 3 * len(LETTERS) if i else 0}s}}" for i in range(len(LETTERS)))
           + f"@keyframes cy{{0%{{opacity:0}}3%,22%{{opacity:1}}25%,100%{{opacity:0}}}}")
    # panels are laid out right to left (Arabic reading order): Isolated is the rightmost
    for k, (en, ar, _) in enumerate(FORMS):
        px = W - x0 - (k + 1) * pw - k * gap
        body.append(f'<rect class="p" x="{px}" y="40" width="{pw}" height="250" rx="18"/>')
        lab, _ = reg.text_paths(ar, 24, px + pw - 24, 82, "end")
        le, _ = reg.text_paths(en, 18, px + 24, 80, rtl=False)
        body.append(f'<path class="a" d="{lab}"/><path class="m" d="{le}"/>')
    for i, ch in enumerate(LETTERS):
        g = []
        for k, (_, _, fmt) in enumerate(FORMS):
            px = W - x0 - (k + 1) * pw - k * gap
            d, _ = bold.text_paths(fmt.format(ch), 150, px + pw / 2, 240, "middle")
            g.append(f'<path class="g" d="{d}"/>')
        body.append(f'<g class="c c{i}">{"".join(g)}</g>')
    return svg(W, H, css, "".join(body), "Arabic contextual forms in Zad: isolated, initial, medial, final")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, t in THEMES.items():
        write(f"hero-{name}.svg", hero(t))
        write(f"weights-{name}.svg", weights(t))
        write(f"forms-{name}.svg", forms(t))
