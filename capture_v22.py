import sys, json
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://yckang91-sketch.github.io/strongpeople-v21-preview/"
OUT = "/workspace/downloads/site_v2/"
PREFIX = sys.argv[2] if len(sys.argv) > 2 else "preview_v22"

def scroll_to(pg, sel, off=0):
    pg.evaluate("""([sel, off]) => {
      const el = document.querySelector(sel);
      if (!el) return;
      window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - off, behavior: 'instant' });
    }""", [sel, off])

def audit(pg, label):
    d = pg.evaluate("""async () => {
      const step = innerHeight * 0.6;
      for (let y = 0; y < document.body.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 200)); }
      window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
      const imgs = [...document.images];
      let ldok = true; try { document.querySelectorAll('script[type="application/ld+json"]').forEach(s => JSON.parse(s.textContent)); } catch(e) { ldok = false; }
      const fr = document.querySelector('.sample-frame iframe');
      const v = document.getElementById('heroVideo');
      return {
        broken: imgs.filter(i => i.getAttribute('src') && !i.naturalWidth).map(i => i.src.split('/').pop()),
        imgCount: imgs.length,
        jsonld: ldok,
        txt19: document.body.innerText.includes('19,000') || document.body.innerHTML.includes('19,000'),
        tallySrc: fr ? (fr.getAttribute('src') || '') : 'NO_FRAME',
        tallyH: fr ? Math.round(fr.getBoundingClientRect().height) : 0,
        heroVideo: v ? {paused: v.paused, t: +(v.currentTime || 0).toFixed(2), rs: v.readyState, w: v.videoWidth, src: (v.currentSrc || '').split('/').pop()} : null,
        docW: document.documentElement.scrollWidth, innerW: innerWidth,
        h1: document.querySelector('h1') ? document.querySelector('h1').innerText.replace(/\\n/g, ' ') : null,
        sections: [...document.querySelectorAll('main>section')].map(s => s.id || s.className.split(' ')[0])
      };
    }""")
    print(f"[{label}]", json.dumps(d, ensure_ascii=False))
    return d

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--font-render-hinting=none", "--autoplay-policy=no-user-gesture-required"])
    logs = []
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("console", lambda m: logs.append(f"{m.type}:{m.text[:120]}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: logs.append("pageerror:" + str(e)[:160]))
    pg.on("response", lambda r: logs.append(f"HTTP{r.status}:{r.url.split('/')[-1][:40]}") if r.status >= 400 else None)
    pg.goto(URL, wait_until="load", timeout=60000)
    pg.wait_for_timeout(4000)
    pg.add_style_tag(content="html{scroll-behavior:auto !important}")
    d = audit(pg, "LIVE PC 1440x900")
    pg.wait_for_timeout(800); pg.screenshot(path=OUT + f"{PREFIX}_pc_01_hero.png")
    scroll_to(pg, '#work', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_02_work.png")
    pg.evaluate("window.scrollBy({top:900,behavior:'instant'})"); pg.wait_for_timeout(900); pg.screenshot(path=OUT + f"{PREFIX}_pc_03_work2.png")
    scroll_to(pg, '#process', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_04_process.png")
    scroll_to(pg, '#sample', 0); pg.wait_for_timeout(2600); pg.screenshot(path=OUT + f"{PREFIX}_pc_05_sample.png")
    scroll_to(pg, '#contact', 0); pg.wait_for_timeout(2200); pg.screenshot(path=OUT + f"{PREFIX}_pc_06_contact.png")
    # archive modal + card modal
    scroll_to(pg, '#archive', 0); pg.wait_for_timeout(600)
    pg.evaluate("document.querySelector('.marquee .track a').click()"); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT + f"{PREFIX}_pc_07_archive_modal.png")
    print("  archive modal:", pg.inner_text("#mTitle"), "/", pg.inner_text("#mKr"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    pg.click(".card[data-i='6']"); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT + f"{PREFIX}_pc_08_modal.png")
    print("  card modal:", pg.inner_text("#mTitle"), "/", pg.inner_text("#mKr"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    print("  console/network:", logs[:10])
    pg.close()

    # mobile: dsf=1 to avoid headless-shell iframe layout bug (see note in report)
    m = b.new_page(viewport={"width": 390, "height": 844})
    m.on("pageerror", lambda e: logs.append("mo-pageerror:" + str(e)[:160]))
    m.goto(URL, wait_until="load", timeout=60000); m.wait_for_timeout(4500)
    m.add_style_tag(content="html{scroll-behavior:auto !important}")
    dm = audit(m, "LIVE MO 390x844")
    m.screenshot(path=OUT + f"{PREFIX}_mo_01_hero.png")
    scroll_to(m, '#index', 0); m.wait_for_timeout(900); m.screenshot(path=OUT + f"{PREFIX}_mo_02_index.png")
    scroll_to(m, '#work', 0); m.wait_for_timeout(1000); m.screenshot(path=OUT + f"{PREFIX}_mo_03_work.png")
    scroll_to(m, '#process', 0); m.wait_for_timeout(900); m.screenshot(path=OUT + f"{PREFIX}_mo_04_process.png")
    scroll_to(m, '#sample', 0); m.wait_for_timeout(2600); m.screenshot(path=OUT + f"{PREFIX}_mo_05_sample.png")
    m.evaluate("window.scrollBy({top:700,behavior:'instant'})"); m.wait_for_timeout(900); m.screenshot(path=OUT + f"{PREFIX}_mo_06_sample2.png")
    scroll_to(m, '#contact', 0); m.wait_for_timeout(2000); m.screenshot(path=OUT + f"{PREFIX}_mo_07_contact.png")
    print("  mobile video:", dm["heroVideo"], "| tally:", dm["tallyH"])
    m.close()
    b.close()
print("live capture done")
