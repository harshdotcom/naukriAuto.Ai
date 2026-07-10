import random
from playwright.async_api import async_playwright
from app.utils.human import human_delay, human_typing, human_mouse_move
from app.bot.handle_questions import handle_questionnaire
import re
from langchain_groq import ChatGroq
from app.bot.handle_login import handleLogin
from app.bot.open_job_page import openJobPage
from app.bot.select_jobs import selectJobInBulk
from app.bot.apply_to_jobs import applyInBulk

async def run_bot(llm:ChatGroq, resume:str, system_prompt:str, human_prompt:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=random.randint(40, 80)
        )

        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        page = await context.new_page()

        try:
            await handleLogin(page)
            total_jobs_applied = 0
            threshold = 100


            while True:  
                await openJobPage(page)

                tabs_to_check = [
                    'div.tab-list-item:has-text("Applies")',
                    'div.tab-list-item:has-text("Top Candidate")',
                    'div.tab-list-item:has-text("Profile")',
                    'div.tab-list-item:has-text("Preferences")',
                    'div.tab-list-item:has-text("You might like")'
                ]
                
                for tab_locator in tabs_to_check:
                    if tab_locator:
                        print(f"🤖 Naukri AutoAI: Checking tab {tab_locator}...")
                        try:
                            tab = page.locator(tab_locator)
                            if await tab.is_visible():
                                await tab.click()
                                await human_delay(2, 4)
                            else:
                                print("🤖 Naukri AutoAI: 'You might like' tab not visible.")
                                continue
                        except Exception as e:
                            print(f"🤖 Naukri AutoAI: Could not click tab: {e}")
                            continue

                    # BATCH SELECTION
                    count_jobs_selected = await selectJobInBulk(page)

                    if count_jobs_selected > 0:
                        await applyInBulk(page, llm, resume, system_prompt, human_prompt)
                        total_jobs_applied += count_jobs_selected

                        break
                    else:
                        print(f"🤖 Naukri AutoAI: No unapplied jobs found on current tab.")
                
                    if count_jobs_selected == 0:
                        print("🤖 Naukri AutoAI: No unapplied jobs found on this tab. Checking another tab...")
                        await human_delay(1, 2)

                if total_jobs_applied >= threshold:
                    print(f"🤖 Naukri AutoAI: Applied to {total_jobs_applied} jobs. Threshold of {threshold} reached. Stopping bot.")
                    break  
                
                        

                

        except Exception as e:
            print(f"Error: {e}")
            await human_delay(20, 40)

        finally:
            print("🤖 Naukri AutoAI: Powering down...")
            await browser.close()