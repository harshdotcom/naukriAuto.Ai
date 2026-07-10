from app.utils.human import human_delay, human_typing, human_mouse_move
from playwright.async_api import Page
from app.config.config import EMAIL, PASSWORD

async def handleLogin(page: Page):
    print("🤖 Naukri AutoAI: Initiating Human Sequence...")
    await page.goto("https://www.naukri.com", wait_until="networkidle")
    await human_delay(2, 4)

    # login
    await page.click("text=Login")
    await human_delay(1, 2)

    

    await human_typing(
        page.locator("//input[@placeholder='Enter your active Email ID / Username']"),
        EMAIL
    )

    await human_typing(
        page.locator("//input[@placeholder='Enter your password']"),
        PASSWORD
    )

    await page.click("//button[@type='submit']")

    await page.wait_for_selector('.nI-gNb-header__logo', timeout=15000)
    print("✅ Naukri AutoAI: Logged in. Cooling down...")
    await human_mouse_move(page)
    await human_delay(6, 10)