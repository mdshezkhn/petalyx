# Petalyx — Cherry-Blossom SaaS Landing (China Edition)

A single-file, zero-build landing page for "benchmarking your AI staff", themed as an
anime-watercolor cherry-blossom valley — restyled with Chinese design taste for a
Chinese audience. One `index.html`, inline `<style>` + `<script>`, no local assets:
every image/video loads from CloudFront, scripts from cdnjs/unpkg, fonts from Google Fonts.

Recreated from the free **Petalyx** prompt template on [motionsites.ai](https://motionsites.ai/).

## Quick start

```bash
python -m http.server 8932   # then open http://localhost:8932
# or just double-click index.html — everything is CDN-based
```

## Stack

- Vanilla HTML/CSS/JS in ONE file (~36 KB)
- GSAP 3.12.5 + ScrollTrigger (cdnjs) — pinning, scrubs, word reveals, footer SVG timeline
- Lenis 1.1.13 (unpkg) — smooth scrolling, driven by GSAP's ticker
- Noto Serif SC (思源宋体) for Chinese headings + Inter Tight for Latin (Google Fonts)
- Graceful degradation: if GSAP/Lenis fail to load (or `prefers-reduced-motion`), the page
  renders fully static — content is never hidden behind JS.

## The Chinese design layer (中国风)

| Element | Where | Notes |
|---|---|---|
| Songti serif headings | all `.zh-serif` headings | `Noto Serif SC` with Songti/STSong/SimSun fallbacks (Google Fonts is blocked in mainland China — system fallbacks keep the look) |
| Vermilion seal 印章 | hero inscription + footer copyright | 朱砂红 `#c8402f`, rotated 篮印-style square stamp with 「樱」 |
| Vertical inscription 题跋 | hero right edge | 「落樱成诗 · 静待花开」 in `writing-mode: vertical-rl` — the handscroll-painting convention |
| Bilingual headlines | hero/stats/loop/CTA | Chinese primary, English sub-caption in tracked uppercase |
| Chinese brand logos | stats section | 微信 · 钉钉 · 飞书 · 华为云 · 金山文档 (swap for your real customers) |
| Chinese idiom copy | CTA | 「真金白银」plays on 一寸光阴一寸金 for the "every hour is gold" line |
| CJK-aware word split | JS splitter | Chinese headlines reveal **per character**, Latin per word |

All copy is in the HTML — search for `衡量`, `工单`, `真金白银` etc. and replace.

## Re-theming checklist

1. **Colors** — edit `:root` tokens: `--olive #4d6a10`, `--green #6f9a0c`, `--lime #b4cd52`,
   `--pill #e7efcf`, seal red `--seal #c8402f`.
2. **Copy** — all text is inline; buttons say `免费开始`.
3. **Assets** — six CloudFront URLs (constants at top of their tags):
   - HERO_VIDEO (mp4, 1080p loop): `hf_20261021_093331_...mp4`
   - HERO_POSTER (also the blurred intro backdrop): `hf_20261021_093215_b7826239...png`
   - CLOUD_A / CLOUD_B (transparent clouds): `hf_20261021_093216_44218665...png` / `hf_20261021_093215_0f37c0c3...png`
   - TREE (cherry trees on grass base): `hf_20261021_093215_95f11900...png`
   - NIGHT (21:9 moonlit valley, CTA): `hf_20261021_093217_cc690198...png`
4. **Stats** — each `.card` has `data-to` / `data-dec` / `data-suf`.
5. **Logos** — `.logos` spans in `#stats`.

## HEVC video note ⚠

The provided hero MP4 is **H.265/HEVC** (`hvc1`). iPhones/iPads and most modern
Windows/macOS machines play it natively; some Android/Chrome/Firefox setups cannot.
The page ships a watchdog: if the video can't start within 6 s, the hero falls back to
the poster image with a slow **Ken-Burns drift**, so the hero never looks dead.
(To guarantee motion everywhere, re-encode the MP4 to H.264 and swap the `src`.)

## Hosting (mainland China)

Don't use Vercel (blocked in China). This file is a static single page — deploy to
**Tencent EdgeOne Pages** (free), Gitee Pages, or any static host. Note Google Fonts is
intermittent in the mainland; the CJK font falls back to system Songti gracefully.

## QA

Headless-Edge Playwright suite in `qa/` (`C:\Python314\python.exe qa/qa.py`, serve on :8932):
0 console/page errors, 0 horizontal overflow at 1440×900 and 390×844, counters scrub to
40% / 300+ / 99.2% / 99.2% under pin, hover-accordion switches panels, footer logo
timeline completes (dots → mark → ring), petals/parallax verified via screenshots in `qa/shots/`.

## Credits

- Layout/motion spec: MotionSites "Petalyx" free prompt (motionsites.ai)
- Imagery: MotionSites Petalyx asset set (CloudFront-hosted)
