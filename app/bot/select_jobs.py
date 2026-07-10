from playwright.async_api import Page
import random
from app.utils.human import human_delay

async def selectJobInBulk(page: Page):
    checkboxes = page.locator('article.jobTuple .tuple-check-box')
    total = await checkboxes.count()
    jobs_selected = 0
    for i in range(total):
        if jobs_selected >= 5: break
        cb = checkboxes.nth(i)
        if await cb.is_visible():
            # Random scroll simulation
            if random.random() > 0.6: await page.mouse.wheel(0, random.randint(200, 400))
            
            is_checked = await cb.locator('.naukicon-ot-Checked').count() > 0
            if not is_checked:
                await cb.click()
                jobs_selected += 1
                print(f"✅ Selected job {jobs_selected}/5")
                await human_delay(1.5, 3.0)
                
    return jobs_selected
