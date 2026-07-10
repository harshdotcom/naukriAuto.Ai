from playwright.async_api import Page
import re
from langchain_groq import ChatGroq
from app.bot.handle_questions import handle_questionnaire
from app.utils.human import human_delay

async def applyInBulk(page: Page, llm:ChatGroq, resume:str, system_prompt:str, human_prompt:str):
    print(f"🤖 Naukri AutoAI: Applying to batch...")
    apply_btn = page.get_by_role("button", name=re.compile(r"^Apply", re.IGNORECASE))
    if await apply_btn.count() > 0:
        await apply_btn.first.click()
        await handle_questionnaire(page, llm, resume, system_prompt, human_prompt)
        print("🎉 Naukri AutoAI: Batch Operation Successful. Taking a short break before next batch.")
        await human_delay(1, 5)
