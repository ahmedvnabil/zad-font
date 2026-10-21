# Zad

> **Zad** — a clean, open-source Arabic web font.
> 5 weights · `woff2` + `ttf` · SIL Open Font License 1.1 · zero dependencies.

<p>
  <a href="LICENSE"><img alt="License: OFL 1.1" src="https://img.shields.io/badge/license-SIL%20OFL%201.1-black?style=flat-square"></a>
  <img alt="Weights: 5" src="https://img.shields.io/badge/weights-5-black?style=flat-square">
  <img alt="Format: woff2 + ttf" src="https://img.shields.io/badge/format-woff2%20%2B%20ttf-black?style=flat-square">
  <img alt="Glyphs: 1652–1657" src="https://img.shields.io/badge/glyphs-1%2C652%E2%80%931%2C657-black?style=flat-square">
  <a href="QA-REPORT.md"><img alt="FontBakery: 0 FATAL · 10 FAIL (inherited)" src="https://img.shields.io/badge/FontBakery-0%20FATAL%20%C2%B7%2010%20FAIL%20(inherited)-orange?style=flat-square"></a>
  <a href="#mcp-server--للـai-agents"><img alt="MCP server" src="https://img.shields.io/badge/MCP-server-black?style=flat-square"></a>
</p>

**Live landing page →** https://zadfont.zad.tools/

---

## ما هو Zad؟

**Zad** فونت عربي نضيف، نسخة خفيفة ومُعاد تسميتها من **IBM Plex Sans Arabic**
(مرخّص تحت SIL Open Font License 1.1). جاهز تحطه في أي موقع وتستخدمه على طول.

- **5 أوزان:** Light (300) · Regular (400) · Medium (500) · SemiBold (600) · Bold (700)
- **الصيغة:** `woff2` (مضغوط، ~67–71KB لكل وزن) + `ttf` لسطح المكتب (~215–224KB)
- **المحارف:** 1,657 (Light/Regular) · 1,652 (Medium/SemiBold/Bold)
- **النصوص:** عربي + لاتيني + أرقام (عربية ولاتينية) + علامات ترقيم
- **الوصل والتشكيل:** سليم 100% (متحقَّق منه بـ HarfBuzz — نفس محرك المتصفحات)
- **اعتماديات:** صفر — ملف CSS + فولدر خطوط، يشتغل في أي مكان.

---

## Install — التركيب

### Option A · Self-host (recommended)

انسخ فولدر `zad-font/` كامل (المهم: `fonts/` + `zad.css`)، وضيف في الـ`<head>`:

```html
<link rel="stylesheet" href="zad-font/zad.css">
```

وبعدها استخدمه في الـCSS:

```css
body {
  font-family: 'Zad', sans-serif;   /* أو: var(--font-zad) */
}

h1 { font-weight: 700; }     /* Bold     */
.lead { font-weight: 600; }  /* SemiBold */
.label { font-weight: 500; } /* Medium   */
p { font-weight: 400; }      /* Regular  */
.faint { font-weight: 300; } /* Light    */
```

> `zad.css` بيعرّف كمان متغيّر جاهز فيه fallback آمن:
> `--font-zad: "Zad", "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, "Noto Sans Arabic", sans-serif;`

### Option B · Use via CDN — الاستخدام عبر CDN (jsDelivr)

مش عايز ترفع ملفات؟ jsDelivr بيخدم الملفات مباشرة من الريبو ده على GitHub.
*No hosting needed: jsDelivr serves the files straight from this GitHub repo.*

**1 · سطر CSS واحد / one CSS line** (`zad.css` فيه الأوزان الخمسة بمسارات نسبية، فالـCDN بيجيب الـ`woff2` من نفس الـref):

```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<!-- pinned (recommended for production) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/zad.css">
<!-- or always the newest commit on main -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@main/zad.css">
```

```css
body { font-family: var(--font-zad); }   /* أو: 'Zad', sans-serif */
```

**2 · `@font-face` بنفسك / your own `@font-face`** (لو عايز وزن أو اتنين بس — only the weights you use):

```css
@font-face {
  font-family: "Zad";
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  src: url("https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-Regular.woff2") format("woff2");
}
@font-face {
  font-family: "Zad";
  font-weight: 700;
  font-style: normal;
  font-display: swap;
  src: url("https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-Bold.woff2") format("woff2");
}
```

**3 · روابط `woff2` مباشرة / direct `woff2` URLs**

| الوزن · Weight | `font-weight` | URL |
|---|---|---|
| Light | 300 | https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-Light.woff2 |
| Regular | 400 | https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-Regular.woff2 |
| Medium | 500 | https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-Medium.woff2 |
| SemiBold | 600 | https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-SemiBold.woff2 |
| Bold | 700 | https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@3966299/fonts/Zad-Bold.woff2 |

(`.ttf` على نفس المسار — same path with `.ttf` for desktop/design apps.)

**أختار أنهي ref؟ / Which ref should I use?**

- **`@<commit>` (زي `@3966299`) — للإنتاج / for production.** الملفات مش هتتغيّر أبداً، وjsDelivr بيكاشها للأبد. *Immutable: the files never change under you and are cached permanently.*
- **`@main`** — دايماً آخر نسخة على `main`. ممكن تتأخر لحد 12 ساعة بعد أي تحديث (كاش jsDelivr للفروع)، وممكن تتغيّر من غير ما تاخد بالك. *Always the newest build on `main`; jsDelivr caches branches for up to 12 h, and the files can change without notice. Good for prototypes.*
- **`@v1.0.0` / `@latest`** — `@latest` بيروح لآخر tag، وهو حالياً `v1.0.0` (البناء الأول، قبل تصحيحات الـmetadata والـsmart dropout). *`@latest` resolves to the newest git tag, currently `v1.0.0` (the first build, before the metadata/smart-dropout fixes). Prefer a commit or `@main` until a newer tag is published.*

> بعد ما الـcommits دي تتعمل merge في `main`، `@main` هيخدم نفس الملفات اللي في `@3966299`.
> *Once this branch is merged, `@main` serves the same files as `@3966299`.*

### Option C · Tailwind

```js
// tailwind.config
theme: { extend: { fontFamily: { zad: ['Zad', 'sans-serif'] } } }
```

```html
<body class="font-zad">…</body>
```

---

## محتويات الفولدر

```
zad-font/
├── index.html        ← اللاندنج بيج (GitHub Pages)
├── zad.css           ← @font-face للأوزان الخمسة (font-display: swap)
├── fonts/
│   ├── Zad-Light.woff2     + Zad-Light.ttf
│   ├── Zad-Regular.woff2   + Zad-Regular.ttf
│   ├── Zad-Medium.woff2    + Zad-Medium.ttf
│   ├── Zad-SemiBold.woff2  + Zad-SemiBold.ttf
│   └── Zad-Bold.woff2      + Zad-Bold.ttf
├── proof/
│   ├── specimen-proof.png  ← proof مولّد من الخطوط نفسها
│   └── specimen-proof.svg
├── build.py          ← السكربت اللي بنى الكِت
├── OFL.txt / LICENSE ← الرخصة (لازمة تفضل مع الفونت)
├── FONTLOG.txt       ← سجل التغييرات
├── QA-REPORT.md      ← تقرير فحص FontBakery
├── qa.json           ← نتيجة FontBakery (machine-readable)
├── originality.json  ← بيان الاشتقاق من IBM Plex Sans Arabic
├── README.md
└── _src/             ← الأصل (مش محتاجها للويب — للبناء فقط)
    └── IBMPlexSansArabic-*.ttf
```

---

## إعادة البناء / Reproducible build

فولدر `_src/` فيه ملفات IBM Plex Sans Arabic الأصلية (النسخة الرسمية من Google
Fonts تحت OFL). يعني `python build.py` بيشتغل على طول ويطلّع **`fonts/*.ttf`
و`fonts/*.woff2`** مع بعض من نفس الـsubset (متّسقين تماماً، نفس البايتات في كل
بناء).

```bash
# مطلوب مرة واحدة:
pip install fonttools brotli

python build.py        # يبني fonts/*.ttf + fonts/*.woff2 من _src/
```

عايز تضيف وزن جديد أو تشيل وزن؟ عدّل `WEIGHTS` في [`build.py`](build.py).
لإضافة وزن، نزّل ملف الـttf المقابل من Google Fonts
(`ofl/ibmplexsansarabic/IBMPlexSansArabic-<Weight>.ttf`) إلى `_src/`.

---

## فحص الجودة — QA

تقرير FontBakery الكامل في [`QA-REPORT.md`](QA-REPORT.md):

FontBakery 1.1.0 · profile `universal` · الأوزان الخمسة:

| Target    | FATAL | FAIL | WARN | PASS |
| --------- | :---: | :--: | :--: | :--: |
| 5 weights |   0   |  10  |  30  | 360  |

- **الـ10 FAIL** = فحصين × 5 أوزان، **متوارثين من IBM Plex Sans Arabic** ومحتاجين تعديل في التصميم نفسه:
  `arabic_spacing_symbols` (رموز U+FBB2–FBC1 مرسومة بعرض صفر) · `case_mapping` (Đ من غير đ، وĵ من غير Ĵ).
- **الـ30 WARN** = 6 فحوصات × 5 أوزان، متوارثة برضه (GDEF، ligature carets، أسماء الجليفات…).
- اتصلّح في `build.py`: `smart_dropout` (إضافة smart dropout control لجدول `prep`)، و`underline_thickness` (توحيد قيم الـunderline)، و`no_mac_entries`.
- اتأكدنا إن الرسم والتشكيل ماتغيّروش: نفس hashes لكل الجليفات ونفس نتيجة HarfBuzz لـ4,814 نص × 4 إعدادات × 5 أوزان (`tools/compare_builds.py`).
- الوصل والتشكيل اتحقق منهم بـ HarfBuzz (نفس محرك المتصفحات) — مفيش أي FAIL بيأثر على التشكيل.

> The 10 remaining FAILs and 30 WARNs are inherited from upstream IBM Plex Sans Arabic
> outlines/GDEF; fixing them would require design changes (new advance widths or new glyphs).
> `smart_dropout` (5 FAILs) was fixed in `build.py` without touching outlines or shaping. Older docs claiming
> "0 FAIL" referred to an earlier 3-weight `check-opentype` run.

---

## MCP server — للـAI agents

فيه **MCP server** شغّال أونلاين يخلّي أي AI agent (Cursor، Claude، VS Code…) يعرف كل حاجة عن Zad،
ويطلّع كود التركيب جاهز، ويعمل preview لأي نص، وكمان **يولّد خطوط مشتقة** من خطوط مفتوحة.

A live **MCP server** lets AI agents read Zad's metadata, get install snippets, preview text,
and **generate derived fonts** from open-source sources.

- **URL:** `https://fekra-zad-font.marsaplatform.com/mcp` (Streamable HTTP · بدون مصادقة / no auth)
- **صفحة المشروع / Project page:** https://spaces.marsaplatform.com/s/sp2rdwbuyb/

**الأدوات (11) / Tools:**

| Tool | الوظيفة / Purpose |
| ---- | ----------------- |
| `get_font_info` | معلومات الخط والأوزان · font & weight metadata |
| `get_install_snippet` | كود التركيب (HTML / CSS / Tailwind / Next.js / Vite) |
| `get_font_files` | لينكات ملفات woff2 / ttf |
| `get_css` | محتوى `zad.css` |
| `check_text_support` | يتأكد إن كل حرف في النص موجود في الخط |
| `preview_text` | لينك preview لنص بأي وزن |
| `list_source_fonts` | الخطوط المصدر المتاحة للتوليد (OFL) |
| `generate_font` | يولّد خط مشتق (subset / عرض / تباعد / وزن / دمج عربي+لاتيني) |
| `get_generated_font` | تفاصيل وملفات خط اتولّد |
| `preview_generated_font` | preview لخط اتولّد |
| `get_font_css` | CSS `@font-face` لخط اتولّد |

> الخطوط اللي بتتولّد **مشتقة** تحت SIL OFL 1.1، ومينفعش تستخدم الـReserved Font Name بتاع المصدر.
> Generated fonts are **OFL derivatives** and must not use a source's Reserved Font Name.

**Cursor / Claude Desktop (`mcp.json`):**

```json
{
  "mcpServers": {
    "zad-font": {
      "url": "https://fekra-zad-font.marsaplatform.com/mcp"
    }
  }
}
```

**عميل بيدعم stdio بس / stdio-only clients (`npx mcp-remote`):**

```json
{
  "mcpServers": {
    "zad-font": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://fekra-zad-font.marsaplatform.com/mcp"]
    }
  }
}
```

---

## ملاحظات

- **الفونت نفسه (`fonts/` + `zad.css`) صفر اعتماديات** — لا JS ولا build، يشتغل في أي موقع.
- **`index.html` (اللاندنج بيج) بيستخدم Tailwind Play CDN + Alpine.js** للعرض فقط
  (أدوات تطوير، مش للإنتاج). صفحة العرض مش جزء من اللي بتنشره — بتنشر `fonts/` و
  `zad.css` بس.
- الخطوط **قابلة لإعادة الإنتاج** (deterministic) ومتحقَّق من تطابق الـGPOS
  (مواضع التشكيل) مع الأصل، مش بس شكل الحروف.

---

## الرخصة — License (مهم تقراها)

Zad مبني على **IBM Plex Sans Arabic** © IBM Corp.، تحت **SIL Open Font License 1.1**.
ده **مسموح قانونياً** بشرط:

1. ✅ الاسم الجديد **ميحتويش** الاسم المحجوز `"Plex"` — و"Zad" مالهوش علاقة بيه.
2. ✅ تشحن `OFL.txt` (أو `LICENSE`) مع الفونت — موجود.
3. ✅ الفونت المعدَّل يفضل تحت OFL.
4. ❌ ممنوع تبيع الفونت لوحده.

تقدر تستخدمه في أي عدد مواقع — شخصية أو تجارية — مجاناً.

> Zad is a renamed/subset derivative of [IBM Plex Sans Arabic](https://github.com/IBM/plex),
> distributed under the [SIL Open Font License 1.1](LICENSE). It does **not** use
> the Reserved Font Name "Plex". You may use it in any number of websites —
> personal or commercial — free of charge.

**حامل حقوق النسخة المعدّلة / Maintainer of this derivative:** Ahmed Morsy ([@ahmedvnabil](https://github.com/ahmedvnabil)).

---

## Credits

- Source: [IBM Plex Sans Arabic](https://github.com/IBM/plex) © IBM Corp. (SIL OFL 1.1)
- Tooling: [fontTools](https://github.com/fonttools/fonttools), [Brotli](https://github.com/google/brotli)
- QA: [FontBakery](https://github.com/fonttools/fontbakery)
