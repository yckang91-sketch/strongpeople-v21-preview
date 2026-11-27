import sys, json
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "https://yckang91-sketch.github.io/strongpeople-v21-preview/"
OUT = "/workspace/downloads/site_v2/"
PREFIX = sys.argv[2] if len(sys.argv) > 2 else "preview_v30"

def scroll_to(pg, sel, off=0):
    pg.evaluate("""([sel, off]) => {
      const el = document.querySelector(sel);
      if (!el) return;
      window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - off, behavior: 'instant' });
    }""", [sel, off])

def audit(pg, label):
    d = pg.evaluate("""async () => {
      const step = innerHeight * 0.6;
      for (let y = 0; y < document.body.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 180)); }
      window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 500));
      const imgs = [...document.images];
      let ldok = true; let ldmsg = '';
      try { document.querySelectorAll('script[type="application/ld+json"]').forEach(s => JSON.parse(s.textContent)); }
      catch(e) { ldok = false; ldmsg = String(e).slice(0,120); }
      const fr = document.querySelector('.sample-frame iframe');
      const v = document.getElementById('heroVideo');
      const fv = document.querySelector('.plate--07 video');
      const ldj = JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent);
      const org = ldj['@graph'].find(n => n['@type'] && String(n['@type']).includes('Organization'));
      const offers = (org.hasOfferCatalog.itemListElement || []).map(o => o.itemOffered.name);
      const bodyHTML = document.body.innerHTML;
      const bad = ['19,000','3,000+','그느드','삭제불가','스타터','풀퍼널','tel:180090014','20만 원','30만 원']
        .filter(s => bodyHTML.includes(s));
      return {
        broken: imgs.filter(i => i.getAttribute('src') && !i.naturalWidth).map(i => i.src.split('/').pop()),
        imgCount: imgs.length,
        jsonld: ldok, jsonldErr: ldmsg,
        offerCount: offers.length, offers,
        forbidden: bad,
        tallySrc: fr ? (fr.getAttribute('src') || '') : 'NO_FRAME',
        tallyH: fr ? Math.round(fr.getBoundingClientRect().height) : 0,
        heroVideo: v ? {paused: v.paused, t: +(v.currentTime || 0).toFixed(2), rs: v.readyState, w: v.videoWidth, src: (v.currentSrc || '').split('/').pop()} : null,
        filmVideo: fv ? {paused: fv.paused, t: +(fv.currentTime || 0).toFixed(2), rs: fv.readyState} : null,
        docW: document.documentElement.scrollWidth, innerW: innerWidth,
        overflow: document.documentElement.scrollWidth - innerWidth,
        h1: document.querySelector('h1') ? document.querySelector('h1').innerText.replace(/\\n/g, ' ').slice(0,160) : null,
        sections: [...document.querySelectorAll('main section')].map(s => s.id || s.className.split(' ')[0]),
        channels: document.querySelectorAll('.channels li').length,
        plates: document.querySelectorAll('.plate-btn').length,
        rows: document.querySelectorAll('.idx-row').length,
        fontSerif: getComputedStyle(document.querySelector('.lb-title')).fontFamily,
        fontKR: getComputedStyle(document.body).fontFamily
      };
    }""")
    print(f"[{label}]", json.dumps(d, ensure_ascii=False, indent=1))
    return d

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--font-render-hinting=none", "--autoplay-policy=no-user-gesture-required"])
    logs = []
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("console", lambda m: logs.append(f"{m.type}:{m.text[:140]}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: logs.append("pageerror:" + str(e)[:200]))
    pg.on("response", lambda r: logs.append(f"HTTP{r.status}:{r.url.split('/')[-1][:50]}") if r.status >= 400 else None)
    pg.goto(URL, wait_until="load", timeout=60000)
    pg.wait_for_timeout(4000)
    pg.add_style_tag(content="html{scroll-behavior:auto !important}")
    d = audit(pg, "PC 1440x900")
    pg.wait_for_timeout(900); pg.screenshot(path=OUT + f"{PREFIX}_pc_01_hero.png")
    scroll_to(pg, '#chain', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_02_chain.png")
    scroll_to(pg, '#lookbook', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_03_lookbook_head.png")
    scroll_to(pg, '.chapter:nth-of-type(1) .cover', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_04_ch1_cover.png")
    scroll_to(pg, '.chapter:nth-of-type(1) .plates', 0); pg.wait_for_timeout(1400); pg.screenshot(path=OUT + f"{PREFIX}_pc_05_ch1_plates.png")
    pg.evaluate("window.scrollBy({top:950,behavior:'instant'})"); pg.wait_for_timeout(1000); pg.screenshot(path=OUT + f"{PREFIX}_pc_06_ch1_plates2.png")
    scroll_to(pg, '.chapter:nth-of-type(2) .cover', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_07_ch2_cover.png")
    scroll_to(pg, '.chapter:nth-of-type(2) .plates', 0); pg.wait_for_timeout(1600); pg.screenshot(path=OUT + f"{PREFIX}_pc_08_ch2_plates.png")
    scroll_to(pg, '.chapter:nth-of-type(3) .cover', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_09_ch3_cover.png")
    scroll_to(pg, '.chapter:nth-of-type(3) .plates', 0); pg.wait_for_timeout(2000); pg.screenshot(path=OUT + f"{PREFIX}_pc_10_ch3_plates.png")
    scroll_to(pg, '#owned', 0); pg.wait_for_timeout(1200); pg.screenshot(path=OUT + f"{PREFIX}_pc_11_owned.png")
    pg.evaluate("window.scrollBy({top:900,behavior:'instant'})"); pg.wait_for_timeout(1000); pg.screenshot(path=OUT + f"{PREFIX}_pc_12_owned2.png")
    scroll_to(pg, '#index', 0); pg.wait_for_timeout(1000); pg.screenshot(path=OUT + f"{PREFIX}_pc_13_index.png")
    scroll_to(pg, '#process', 0); pg.wait_for_timeout(1000); pg.screenshot(path=OUT + f"{PREFIX}_pc_14_process.png")
    scroll_to(pg, '#faq', 0); pg.wait_for_timeout(1000); pg.screenshot(path=OUT + f"{PREFIX}_pc_15_faq.png")
    scroll_to(pg, '#sample', 0); pg.wait_for_timeout(3000); pg.screenshot(path=OUT + f"{PREFIX}_pc_16_sample.png")
    scroll_to(pg, '#contact', 0); pg.wait_for_timeout(2400); pg.screenshot(path=OUT + f"{PREFIX}_pc_17_contact.png")
    # modals
    scroll_to(pg, '.chapter:nth-of-type(1) .plates', 0); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('.plate-btn')[0].click()"); pg.wait_for_timeout(1000)
    pg.screenshot(path=OUT + f"{PREFIX}_pc_18_modal.png")
    print("  plate modal:", pg.inner_text("#mTitle"), "/", pg.inner_text("#mKr"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
    scroll_to(pg, '#index', 0); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('.idx-row')[3].click()"); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT + f"{PREFIX}_pc_19_idx_modal.png")
    print("  idx modal:", pg.inner_text("#mTitle"), "/", pg.inner_text("#mKr"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    print("  console/network:", logs[:12])
    pg.close()

    m = b.new_page(viewport={"width": 390, "height": 844})
    m.on("pageerror", lambda e: logs.append("mo-pageerror:" + str(e)[:200]))
    m.goto(URL, wait_until="load", timeout=60000); m.wait_for_timeout(4500)
    m.add_style_tag(content="html{scroll-behavior:auto !important}")
    dm = audit(m, "MO 390x844")
    m.screenshot(path=OUT + f"{PREFIX}_mo_01_hero.png")
    scroll_to(m, '#chain', 0); m.wait_for_timeout(1000); m.screenshot(path=OUT + f"{PREFIX}_mo_02_chain.png")
    scroll_to(m, '.chapter:nth-of-type(1) .cover', 0); m.wait_for_timeout(1000); m.screenshot(path=OUT + f"{PREFIX}_mo_03_ch1_cover.png")
    scroll_to(m, '.chapter:nth-of-type(1) .plates', 0); m.wait_for_timeout(1400); m.screenshot(path=OUT + f"{PREFIX}_mo_04_ch1_plates.png")
    scroll_to(m, '#owned', 0); m.wait_for_timeout(1000); m.screenshot(path=OUT + f"{PREFIX}_mo_05_owned.png")
    scroll_to(m, '#index', 0); m.wait_for_timeout(900); m.screenshot(path=OUT + f"{PREFIX}_mo_06_index.png")
    scroll_to(m, '#process', 0); m.wait_for_timeout(900); m.screenshot(path=OUT + f"{PREFIX}_mo_07_process.png")
    scroll_to(m, '#sample', 0); m.wait_for_timeout(2600); m.screenshot(path=OUT + f"{PREFIX}_mo_08_sample.png")
    scroll_to(m, '#contact', 0); m.wait_for_timeout(2000); m.screenshot(path=OUT + f"{PREFIX}_mo_09_contact.png")
    m.evaluate("document.getElementById('menuBtn').click()"); m.wait_for_timeout(900)
    m.screenshot(path=OUT + f"{PREFIX}_mo_10_menu.png")
    print("  mobile video:", dm["heroVideo"], "| tally:", dm["tallyH"], "| overflow:", dm["overflow"])
    m.close()
    b.close()
print("capture done")
