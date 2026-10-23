"""Open the DAKboard screen in a headless browser and save a 1920x1080 PNG."""
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

URL = os.environ.get("DAKBOARD_URL", "").strip()
if not URL:
    sys.exit("DAKBOARD_URL secret is missing (Settings > Secrets and variables > Actions).")

OUT = pathlib.Path("out")
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 1920, "height": 1080},
        timezone_id="America/Chicago",
    )
    page.goto(URL, wait_until="networkidle", timeout=60_000)
    page.wait_for_timeout(8_000)  # let photos, weather and calendar finish drawing
    page.screenshot(path=str(OUT / "dakboard.png"))
    browser.close()

(OUT / ".nojekyll").touch()
print("Saved out/dakboard.png")
