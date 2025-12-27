# Python Standard Library
import asyncio
import base64
import hashlib
from pathlib import Path
import sys

# Third-Party Libraries
from playwright.async_api import async_playwright

JS_image_finder = open("image_finder.js", mode="r", encoding="utf-8").read()


async def fetch_captcha(page) -> bytes:
    await page.goto(
        "https://ensap.gouv.fr",
        wait_until="networkidle",
        timeout=30000,
    )
    await page.wait_for_selector("ensap-captcha", timeout=10000)
    captcha_element = await page.query_selector("ensap-captcha")

    if not captcha_element:
        raise RuntimeError("CAPTCHA element not found")

    image_data = await page.evaluate(JS_image_finder)

    if not image_data or not image_data.get("src"):
        raise RuntimeError("No image found in CAPTCHA element")

    src = image_data["src"]
    assert src.startswith("data:image/png;base64,")
    base64_data = src.split(",")[1].strip()
    image_bytes = base64.b64decode(base64_data)
    return image_bytes


async def download_ensap_captchas(num_captchas) -> None:
    """Download CAPTCHA images from ensap.gouv.fr"""

    output_dir = Path("./captchas")
    output_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        print(f"Downloading {num_captchas} CAPTCHA images...")

        semaphore = asyncio.Semaphore(5)
        
        async def download_one(i):
            async with semaphore:
                page = await context.new_page()
                try:
                    print(f"[{i + 1}/{num_captchas}]")
                    
                    try:
                        captcha_binary = await fetch_captcha(page)
                    except Exception as e:
                        print(f"Error fetching CAPTCHA: {e}")
                        return
                    
                    hash_digest = hashlib.sha256(captcha_binary).hexdigest()
                    filename = f"{hash_digest}.png"
                    filepath = output_dir / filename
                    filepath.write_bytes(captcha_binary)

                    await asyncio.sleep(0.0)  # Throttle
                finally:
                    await page.close()

        # TODO: shoot one new download every x seconds (1.0?) instead?
        # with a maximum of N concurrent downloads?
        # TODO: reschedule failed downloads.
        tasks = [download_one(i) for i in range(num_captchas)]
        await asyncio.gather(*tasks)

        await browser.close()


if __name__ == "__main__":
    num_to_download = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    asyncio.run(download_ensap_captchas(num_to_download))