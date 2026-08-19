from playwright.async_api import Page
import re
from langchain_groq import ChatGroq
from app.bot.handle_questions import handle_questionnaire
from app.utils.human import human_delay
from app.utils.report import record_applied_jobs, record_failed_jobs

ERROR_TOAST_PATTERN = re.compile(r"error processing your request", re.IGNORECASE)

async def applyInBulk(page: Page, llm:ChatGroq, resume:str, system_prompt:str, human_prompt:str, selected_jobs: list[dict] | None = None):
    print(f"🤖 Naukri AutoAI: Applying to batch...")
    apply_btn = page.get_by_role("button", name=re.compile(r"^Apply", re.IGNORECASE))
    if await apply_btn.count() == 0:
        return

    context = page.context
    opened_tabs = []
    def _on_new_page(new_page):
        opened_tabs.append(new_page)
    context.on("page", _on_new_page)

    await apply_btn.first.click()
    await human_delay(1.5, 2.5)

    context.remove_listener("page", _on_new_page)
    for tab in opened_tabs:
        try:
            await tab.close()
        except Exception:
            pass

    redirected_externally = bool(opened_tabs) or "naukri.com" not in page.url
    error_toast = page.get_by_text(ERROR_TOAST_PATTERN)
    has_error_toast = await error_toast.count() > 0

    if redirected_externally or has_error_toast:
        reason = (
            "Apply redirects to an external company career portal (not supported by quick apply)"
            if redirected_externally else
            "Naukri error processing the apply request"
        )
        print(f"⚠️ Naukri AutoAI: Skipping this batch — {reason}. Moving to next batch.")
        if selected_jobs:
            record_failed_jobs(selected_jobs, reason)
        if "naukri.com" not in page.url:
            try:
                await page.go_back(timeout=5000)
            except Exception:
                pass
        try:
            await page.locator('[class*="close" i], [class*="cross" i]').first.click(timeout=2000)
        except Exception:
            pass
        return

    await handle_questionnaire(page, llm, resume, system_prompt, human_prompt)
    if selected_jobs:
        record_applied_jobs(selected_jobs)
    print("🎉 Naukri AutoAI: Batch Operation Successful. Taking a short break before next batch.")
    await human_delay(1, 5)
