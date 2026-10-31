# MSK — Cherry-Blossom SaaS Landing

A single-file, zero-build landing page for "benchmarking your AI staff", themed as an
anime-watercolor cherry-blossom valley. One `index.html`, inline `<style>` + `<script>`,
no local assets: every image/video loads from CloudFront, scripts from cdnjs/unpkg,
fonts from Google Fonts.

Recreated from the free **Petalyx** prompt template on [motionsites.ai](https://motionsites.ai/),
rebranded to **MSK** (wordmark in the nav, animated M·S·K monogram in the footer).

> Repo name is `petalyx` for historical reasons — the page itself is fully MSK-branded.

## Quick start

```bash
python -m http.server 8932   # then open http://localhost:8932
# or just double-click index.html — everything is CDN-based
```

## Stack

- Vanilla HTML/CSS/JS in ONE file (~35 KB)
- GSAP 3.12.5 + ScrollTrigger (cdnjs) — pinning, scrubs, word reveals, footer SVG timeline
- Lenis 1.1.13 (unpkg) — smooth scrolling, driven by GSAP's ticker
- Inter Tight (Google Fonts)
- Graceful degradation: if GSAP/Lenis fail to load (or `prefers-reduced-motion`), the page
  renders fully static — counters filled, footer monogram shown, nothing hidden behind JS.

## Scenes

1. **Intro** — the white page starts at 90% scale with rounded corners over a blurred
   cherry-blossom backdrop, then grows to full screen.
2. **Hero** — pill nav (MSK · Start for $0), drifting pastel clouds, word-by-word blur
   headline reveal, looping valley video in the lower 72% fading into white sky,
   flickering frosted-glass squares.
3. **Stats** (pinned on desktop) — counters scrub to 40% / 300+ / 99.2% / 99.2% while the
   cherry tree rises behind the lime ticket cards; a frosted band blurs it behind the
   logo row (slack · zapier · Dropbox · HubSpot · Notion).
4. **Human-in-the-loop** — 3-panel hover accordion with giant olive/green/lime numbers;
   inactive panels show clipped numbers, the active one reveals title + copy + mini cloud.
5. **CTA** — frosted white-to-clear card over the moonlit valley with 18 falling petals.
6. **Footer** — three dots bounce, fade, then M·S·K stroke-draw themselves as a ring
   draws around them (SVG dashoffset timeline).

## Re-theming checklist

1. **Brand** — search `MSK` (nav, footer aria-label, favicon data-URI, copyright).
   The footer monogram letters are three `.fL` paths in the footer SVG — replace the
   `d` attributes to spell different initials.
2. **Colors** — edit `:root` tokens: `--olive #4d6a10`, `--green #6f9a0c`, `--lime #b4cd52`,
   `--pill #e7efcf`.
3. **Copy** — all text is inline English; buttons say `Start for $0`.
4. **Assets** — six CloudFront URLs (in their tags):
   - HERO_VIDEO (mp4, 1080p loop): `hf_20261021_093331_...mp4`
   - HERO_POSTER (also the blurred intro backdrop): `hf_20261021_093215_b7826239...png`
   - CLOUD_A / CLOUD_B (transparent clouds): `hf_20261021_093216_44218665...png` / `hf_20261021_093215_0f37c0c3...png`
   - TREE (cherry trees on grass base): `hf_20261021_093215_95f11900...png`
   - NIGHT (21:9 moonlit valley, CTA): `hf_20261021_093217_cc690198...png`
5. **Stats** — each `.card` has `data-to` / `data-dec` / `data-suf`.
6. **Logos** — `.logos` spans in `#stats` (SVGs inline).

## HEVC video note ⚠

The provided hero MP4 is **H.265/HEVC** (`hvc1`). iPhones/iPads and most modern
Windows/macOS machines play it natively; some Android/Chrome/Firefox setups cannot.
The page ships a watchdog: if the video can't start within 6 s, the hero falls back to
the poster image with a slow **Ken-Burns drift**, so the hero never looks dead.
(To guarantee motion everywhere, re-encode the MP4 to H.264 and swap the `src`.)

## Hosting (mainland China)

Don't use Vercel (blocked in China). This file is a static single page — deploy to
**Tencent EdgeOne Pages** (free), Gitee Pages, or any static host.

## QA

Headless-Edge Playwright suite in `qa/` (`C:\Python314\python.exe qa/qa.py`, serve on :8932):
0 console/page errors, 0 horizontal overflow at 1440×900 and 390×844, counters scrub to
40% / 300+ / 99.2% / 99.2% under pin, hover-accordion switches panels, footer monogram
timeline completes (dots → M·S·K draw → ring). Screenshots in `qa/shots/`.

Gotcha for QA scripts: don't read `offsetTop` of a ScrollTrigger-pinned element (returns 0
while pinned) — read the pin's `start`/`end` off `ScrollTrigger.getAll()` instead.
