# Python Standard Library
import base64
import hashlib
import time
from pathlib import Path

# Third-Party Libraries
from playwright.sync_api import sync_playwright

JS_image_finder = open("image_finder.js", mode="r", encoding="utf-8").read()


def fetch_captcha(page) -> bytes:
    page.goto(
        "https://ensap.gouv.fr",
        wait_until="networkidle",
        timeout=30000,
    )
    page.wait_for_selector("ensap-captcha", timeout=10000)
    captcha_element = page.query_selector("ensap-captcha")

    if not captcha_element:
        raise RuntimeError("CAPTCHA element not found")

    image_data = page.evaluate(JS_image_finder)

    if not image_data or not image_data.get("src"):
        raise RuntimeError("No image found in CAPTCHA element")

    src = image_data["src"]
    assert src.startswith("data:image/png;base64,")
    base64_data = src.split(",")[1].strip()
    image_bytes = base64.b64decode(base64_data)
    return image_bytes


def download_ensap_captchas(num_captchas) -> None:
    """Download CAPTCHA images from ensap.gouv.fr"""

    output_dir = Path("./captchas")
    output_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"Downloading {num_captchas} CAPTCHA images...")

        for i in range(num_captchas):
            print(f"[{i + 1}/{num_captchas}]")

            try:
                captcha_binary = fetch_captcha(page)
            except Exception as e:
                print(f"Error fetching CAPTCHA: {e}")
                captcha_binary = None
                continue
            
            hash_digest = hashlib.sha256(captcha_binary).hexdigest()
            filename = f"{hash_digest}.png"
            filepath = output_dir / filename
            filepath.write_bytes(captcha_binary)

            time.sleep(0.0) # Throttle

        browser.close()


if __name__ == "__main__":
    import sys
    num_to_download = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    download_ensap_captchas(num_to_download)
