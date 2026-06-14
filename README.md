# Zad

> **Zad** — a clean, open-source Arabic web font.
> 5 weights · `woff2` + `ttf` · SIL Open Font License 1.1 · zero dependencies.

<p>
  <a href="LICENSE"><img alt="License: OFL 1.1" src="https://img.shields.io/badge/license-SIL%20OFL%201.1-black?style=flat-square"></a>
  <img alt="Weights: 5" src="https://img.shields.io/badge/weights-5-black?style=flat-square">
  <img alt="Format: woff2 + ttf" src="https://img.shields.io/badge/format-woff2%20%2B%20ttf-black?style=flat-square">
  <img alt="Glyphs: 1657" src="https://img.shields.io/badge/glyphs-1%2C657-black?style=flat-square">
  <img alt="QA: FontBakery" src="https://img.shields.io/badge/QA-FontBakery%20%E2%9C%93-2da44e?style=flat-square">
</p>

**Live landing page →** https://zadfont.zad.tools/

---

## ما هو Zad؟

**Zad** فونت عربي نضيف، نسخة خفيفة ومُعاد تسميتها من **IBM Plex Sans Arabic**
(مرخّص تحت SIL Open Font License 1.1). جاهز تحطه في أي موقع وتستخدمه على طول.

- **5 أوزان:** Light (300) · Regular (400) · Medium (500) · SemiBold (600) · Bold (700)
- **الصيغة:** `woff2` (مضغوط، ~67KB لكل وزن) + `ttf` لسطح المكتب
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
> `--font-zad: "Zad", "Segoe UI", system-ui, "Noto Sans Arabic", sans-serif;`

### Option B · CDN one-liner (jsDelivr)

عايز تشغّله بدون رفع ملفات؟ سطر واحد:

```html
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/ahmedvnabil/zad-font@latest/zad.css">
```

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

| Target    | FATAL | FAIL | WARN | PASS |
| --------- | :---: | :--: | :--: | :--: |
| 5 weights |   0   |  0   |  1   |  88  |

الوصل والتشكيل اتحقق منهم بـ HarfBuzz (نفس محرك التشكيل اللي بتستخدمه المتصفحات).
الـWARN الوحيد متوارث من ملفات IBM Plex الأصلية ومش بيأثر على التشكيل.

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

**حامل حقوق النسخة المعدّلة / Maintainer of this derivative:** Ahmed Morsy.

---

## Credits

- Source: [IBM Plex Sans Arabic](https://github.com/IBM/plex) © IBM Corp. (SIL OFL 1.1)
- Tooling: [fontTools](https://github.com/fonttools/fonttools), [Brotli](https://github.com/google/brotli)
- QA: [FontBakery](https://github.com/fonttools/fontbakery)
