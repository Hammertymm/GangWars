"""Capture market screen screenshots at common phone sizes."""
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_market_screens"
PORT = 8765

SCENARIOS = [
    ("01_default", "Default market", None),
    ("02_held", "Held goods (BUY|SELL)", {"inventory": {"moonshine": 3, "cigars": 12, "diamonds": 1}}),
    ("03_dead", "Unavailable good", {"prices": {"furcoats": None}}),
]

SIZES = [
    ("iphone-se", 360, 640),
    ("iphone-14", 390, 844),
    ("pro-max", 430, 932),
]


def start_server():
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(  # noqa: E731
        *args, directory=str(ROOT), **kwargs
    )
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def seed_save(page, patch):
    page.evaluate(
        """(patch) => {
          const KEY = 'gw:save';
          let raw = localStorage.getItem(KEY);
          if (!raw) return false;
          const s = JSON.parse(raw);
          if (patch.inventory) Object.assign(s.inventory, patch.inventory);
          if (patch.prices) Object.assign(s.prices, patch.prices);
          localStorage.setItem(KEY, JSON.stringify(s));
          return true;
        }""",
        patch,
    )


def open_market(page):
    page.goto(f"http://127.0.0.1:{PORT}/gangwars.html", wait_until="networkidle")
    page.evaluate("localStorage.setItem('gw:tutorialDone', '1')")
    page.wait_for_selector("#new", timeout=15000)
    page.click("#new")
    page.wait_for_selector(".market-play", timeout=15000)
    if page.locator("#tutorial-overlay").count():
        page.click("#tskip")
        page.wait_for_selector(".market-play", timeout=15000)
    page.wait_for_timeout(400)


def reopen_from_save(page):
    page.goto(f"http://127.0.0.1:{PORT}/gangwars.html", wait_until="networkidle")
    page.evaluate("localStorage.setItem('gw:tutorialDone', '1')")
    page.wait_for_selector("#cont:not([disabled])", timeout=15000)
    page.click("#cont")
    page.wait_for_selector(".market-play", timeout=15000)
    if page.locator("#tutorial-overlay").count():
        page.click("#tskip")
        page.wait_for_selector(".market-play", timeout=15000)
    page.wait_for_timeout(400)


def main():
    OUT.mkdir(exist_ok=True)
    meta = []
    httpd = start_server()
    time.sleep(0.3)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for sc_id, sc_label, patch in SCENARIOS:
                for size_id, w, h in SIZES:
                    context = browser.new_context(
                        viewport={"width": w, "height": h},
                        device_scale_factor=2,
                        is_mobile=True,
                        has_touch=True,
                    )
                    page = context.new_page()
                    if patch is None:
                        open_market(page)
                    else:
                        open_market(page)
                        seed_save(page, patch)
                        reopen_from_save(page)

                    out = OUT / f"{sc_id}_{size_id}.png"
                    page.locator("#crt").screenshot(path=str(out))
                    meta.append(
                        {
                            "file": out.name,
                            "scenario": sc_label,
                            "size": f"{w}x{h}",
                        }
                    )
                    context.close()

            # Composite contact sheet for quick viewing
            sheet = browser.new_page(viewport={"width": 1400, "height": 2200})
            tiles = []
            for sc_id, _, _ in SCENARIOS:
                row = []
                for size_id, _, _ in SIZES:
                    row.append(str(OUT / f"{sc_id}_{size_id}.png").replace("\\", "/"))
                tiles.append(row)
            html = ["<html><body style='margin:0;background:#111;color:#ccc;font:12px monospace'>"]
            html.append("<h1 style='padding:12px'>Gang Wars — Market screen previews</h1>")
            for i, (sc_id, sc_label, _) in enumerate(SCENARIOS):
                html.append(f"<h2 style='padding:0 12px'>{sc_label}</h2>")
                html.append("<div style='display:flex;gap:8px;padding:0 12px 16px'>")
                for j, (_, w, h) in enumerate(SIZES):
                    html.append(
                        f"<div><div>{w}×{h}</div>"
                        f"<img src='file:///{tiles[i][j]}' style='width:260px;border:1px solid #444'></div>"
                    )
                html.append("</div>")
            html.append("</body></html>")
            sheet.set_content("".join(html), wait_until="load")
            sheet.wait_for_timeout(500)
            sheet.screenshot(path=str(OUT / "00_contact_sheet.png"), full_page=True)
            sheet.close()
            browser.close()
    finally:
        httpd.shutdown()

    (OUT / "manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {len(meta)} screenshots to {OUT}")


if __name__ == "__main__":
    main()
