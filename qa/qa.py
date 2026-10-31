import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8932"
OUT = "C:/Users/Mohammed Shehzad/AppData/Local/Temp/petalyx-qa"

def check_overflow(page):
    return page.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")

def snap(page, name):
    page.screenshot(path=f"{OUT}/{name}.png")
    print("shot:", name)

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel="msedge", headless=True)
    errors = []

    # ---------- desktop ----------
    pg = browser.new_page(viewport={"width":1440,"height":900})
    pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    pg.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    pg.goto(BASE, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(4500)
    snap(pg, "02-hero")

    video = pg.evaluate("(() => { const v = document.getElementById('heroVideo'); return {rs: v.readyState, t: v.currentTime, fb: v.parentElement.classList.contains('no-video')}; })()")
    print("video:", video)

    # stats pin — scroll using real pin start/end
    pg.evaluate("""(() => {
        const p = window.ScrollTrigger.getAll().find(s => s.pin);
        window.__lenis.scrollTo(p.start + (p.end - p.start) * 0.55, {duration:0.01});
    })()""")
    pg.wait_for_timeout(2500)
    snap(pg, "03-stats-mid")
    print("counters mid:", pg.evaluate("[...document.querySelectorAll('.card b')].map(b=>b.textContent)"))

    pg.evaluate("""(() => {
        const p = window.ScrollTrigger.getAll().find(s => s.pin);
        window.__lenis.scrollTo(p.start + (p.end - p.start) * 0.95, {duration:0.01});
    })()""")
    pg.wait_for_timeout(2500)
    snap(pg, "04-stats-end")
    print("counters end:", pg.evaluate("[...document.querySelectorAll('.card b')].map(b=>b.textContent)"))
    print("tree yPercent:", pg.evaluate("gsap.getProperty('#tree','yPercent')"))

    # loop + hover panel 2
    pg.evaluate("__lenis.scrollTo(document.querySelector('#loop').getBoundingClientRect().top + window.scrollY + 200, {duration:0.01})")
    pg.wait_for_timeout(1500)
    box = pg.locator(".panel").nth(1).bounding_box()
    pg.mouse.move(box["x"]+box["width"]/2, box["y"]+box["height"]/2)
    pg.wait_for_timeout(1600)
    snap(pg, "05-loop-panel2")
    print("active panel:", pg.evaluate("document.querySelector('.panel.is-active').getAttribute('aria-label')"))
    # cta
    pg.evaluate("__lenis.scrollTo(document.querySelector('#cta').getBoundingClientRect().top + window.scrollY + window.innerHeight*0.5, {duration:0.01})")
    pg.wait_for_timeout(1800)
    snap(pg, "06-cta")

    # footer
    pg.evaluate("__lenis.scrollTo(document.body.scrollHeight, {duration:0.01})")
    pg.wait_for_timeout(1800)
    snap(pg, "07-footer")
    print("ring offset:", pg.evaluate("getComputedStyle(document.getElementById('fRing')).strokeDashoffset"),
          "| letters offset:", pg.evaluate("[...document.querySelectorAll('.fL')].map(e=>getComputedStyle(e).strokeDashoffset).join(',')"))

    d = check_overflow(pg)
    print("desktop overflow:", d, "OK" if d["sw"] <= d["iw"] else "FAIL")
    pg.close()

    # ---------- mobile ----------
    pm = browser.new_page(viewport={"width":390,"height":844}, is_mobile=True, has_touch=True)
    pm.on("pageerror", lambda e: errors.append(f"m pageerror: {e}"))
    pm.on("console", lambda m: errors.append(f"m console.{m.type}: {m.text}") if m.type == "error" else None)
    pm.goto(BASE, wait_until="domcontentloaded", timeout=60000)
    pm.wait_for_timeout(4500)
    snap(pm, "08-m-hero")
    pm.evaluate("window.__lenis.scrollTo(document.querySelector('#stats').getBoundingClientRect().top + window.scrollY + 300, {duration:0.01})")
    pm.wait_for_timeout(2200)
    snap(pm, "09-m-stats")
    print("m counters:", pm.evaluate("[...document.querySelectorAll('.card b')].map(b=>b.textContent)"))
    pm.evaluate("window.__lenis.scrollTo(document.querySelector('#loop').getBoundingClientRect().top + window.scrollY + 150, {duration:0.01})")
    pm.wait_for_timeout(1600)
    snap(pm, "10-m-loop")
    pm.evaluate("window.__lenis.scrollTo(document.querySelector('#cta').getBoundingClientRect().top + window.scrollY + 200, {duration:0.01})")
    pm.wait_for_timeout(1800)
    snap(pm, "11-m-cta")
    pm.evaluate("window.__lenis.scrollTo(document.body.scrollHeight, {duration:0.01})")
    pm.wait_for_timeout(1600)
    snap(pm, "12-m-footer")
    m = check_overflow(pm)
    print("mobile overflow:", m, "OK" if m["sw"] <= m["iw"] else "FAIL")
    pm.close()
    browser.close()

    print("\nERRORS:" if errors else "\nNO CONSOLE/PAGE ERRORS")
    for e in errors[:20]:
        print(" -", e)
