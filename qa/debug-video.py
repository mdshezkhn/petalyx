import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8932"
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="msedge", headless=True)
    pg = b.new_page(viewport={"width":1440,"height":900})
    pg.on("requestfailed", lambda r: print("FAILED:", r.url[-30:], r.failure) if ".mp4" in r.url else None)
    pg.on("response", lambda r: print("RESP:", r.status, r.url[-30:], r.headers.get("content-length","?")) if ".mp4" in r.url else None)
    pg.goto(BASE, wait_until="domcontentloaded", timeout=60000)
    for i in range(10):
        pg.wait_for_timeout(2000)
        st = pg.evaluate("(() => { const v=document.getElementById('heroVideo'); return {rs:v.readyState, t:+v.currentTime.toFixed(2), paused:v.paused, err:v.error?v.error.code:null}; })()")
        print(f"t+{(i+1)*2}s", st)
        if st["t"] > 0.5: break
    b.close()
