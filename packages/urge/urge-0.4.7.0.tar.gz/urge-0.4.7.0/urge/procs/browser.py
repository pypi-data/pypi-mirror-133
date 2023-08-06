from urge.base import ProcManager, action
from path import Path


def web_screenshot(url: str, target: str = "./", use_mobile=True,**kwargs) -> str:

    from playwright.sync_api import sync_playwright
    from datetime import datetime

    print("🤖 : Chromium import is OK...")

    with sync_playwright() as p:
        iphone_11 = p.devices["iPhone 11 Pro"]
        browser_type = p.chromium
        print("🤖 : Hey, I found the chromium binary...")
        print(browser_type)
        print(
            '🤖 : Launching browser... Please wait for a while then you will see the'
            ' result.'
        )
        browser = browser_type.launch(headless=True)
        if not use_mobile:
            iphone_11 = {}

        context = browser.new_context(**iphone_11)
        page = context.new_page()
        if use_mobile:
            page.set_viewport_size({"width": 375, "height": 635})

        page.goto(url, wait_until="networkidle")
        # page.screenshot(path=f'./example-{browser_type.name}haha.png')
        target = Path(target) 
        file_name = target/f'screenshot{datetime.now().strftime("%m-%d-%H-%M-%S")}.jpeg'
        page.screenshot(path=file_name,type="jpeg",quality=20)
        print(f"🤖 : DONE")
        print(f'The file is at {file_name}')
        browser.close()
    return file_name


def get_screenshot(url):
    p = ProcManager(web_screenshot)
    return p(url)
