import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8932"
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":900})
    pg.on("requestfailed", lambda r: print("FAILED:", r.url[:110], "|", r.failure) if "cloudfront" in r.url or ".mp4" in r.url else None)
    pg.on("response", lambda r: print("RESP:", r.status, r.url[:110]) if ".mp4" in r.url else None)
    pg.on("console", lambda m: print("console:", m.type, m.text[:200]))
    pg.goto(BASE, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(5000)

    print("\n--- video state (t+5s) ---")
    print(pg.evaluate("""(() => { const v = document.getElementById('heroVideo');
        return {rs:v.readyState, ns:v.networkState, t:v.currentTime, paused:v.paused,
                err: v.error ? (v.error.code+' '+v.error.message) : null}; })()"""))

    print("\n--- scroll debug ---")
    pg.evaluate("__lenis.scrollTo(1530, {duration:0.1})")
    for i in range(4):
        pg.wait_for_timeout(1000)
        st = pg.evaluate("""(() => {
            const pins = window.ScrollTrigger.getAll().filter(s=>s.pin);
            const p = pins[0];
            return {scrollY: Math.round(window.scrollY),
                    pinStart: p ? Math.round(p.start) : null,
                    pinEnd: p ? Math.round(p.end) : null,
                    pinProgress: p ? +p.progress.toFixed(3) : null,
                    lenisTarget: window.__lenis ? Math.round(window.__lenis.targetScroll ?? -1) : -1,
                    lenisActual: window.__lenis ? Math.round(window.__lenis.animatedScroll ?? -1) : -1};
        })()""")
        print(i, st)
    b.close()
