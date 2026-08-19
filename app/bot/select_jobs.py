from playwright.async_api import Page
import random
import re
from app.utils.human import human_delay

MAX_EXPERIENCE_YEARS = 3

_REVIEW_COUNT_PATTERN = re.compile(r"^[\d,]+\s*Reviews?$", re.IGNORECASE)
_EXP_RANGE_PATTERN = re.compile(r"(\d+)\s*-\s*(\d+)\s*Yrs?", re.IGNORECASE)
_EXP_SINGLE_PATTERN = re.compile(r"\b(\d+)\s*Yrs?\b", re.IGNORECASE)
_FRESHER_PATTERN = re.compile(r"\bfresher\b", re.IGNORECASE)

_seen_job_keys: set[str] = set()


def _job_key(job_info: dict) -> str:
    if job_info.get("url"):
        return job_info["url"]
    return f"{job_info.get('title', '')}|{job_info.get('company', '')}"


async def _get_min_experience_required(article) -> int | None:
    try:
        text = await article.inner_text()
    except Exception:
        return None

    if _FRESHER_PATTERN.search(text):
        return 0

    range_match = _EXP_RANGE_PATTERN.search(text)
    if range_match:
        return int(range_match.group(1))

    single_match = _EXP_SINGLE_PATTERN.search(text)
    if single_match:
        return int(single_match.group(1))

    return None


async def _extract_job_info(article) -> dict:
    async def safe_text(selectors: list[str], reject: re.Pattern | None = None) -> str:
        for selector in selectors:
            try:
                locator = article.locator(selector)
                count = await locator.count()
                for idx in range(count):
                    raw = (await locator.nth(idx).inner_text()).strip()
                    if not raw:
                        continue
                    candidate = raw.splitlines()[0].strip() or raw
                    if candidate and not (reject and reject.match(candidate)):
                        return candidate
            except Exception:
                continue
        return "Unknown"

    async def safe_href(selectors: list[str]) -> str:
        for selector in selectors:
            try:
                locator = article.locator(selector)
                count = await locator.count()
                for idx in range(count):
                    href = await locator.nth(idx).get_attribute("href")
                    if href and "ambitionbox.com" not in href:
                        return href
            except Exception:
                continue
        return ""

    title_selectors = ['a.title', '.title a', '.title', '[data-testid="jobTupleHeader"] a', 'h2 a', 'h3 a']
    company_selectors = ['a.comp-name', '.comp-name', '.companyInfo a', '.companyInfo', '.subTitle']

    return {
        "title": await safe_text(title_selectors),
        "company": await safe_text(company_selectors, reject=_REVIEW_COUNT_PATTERN),
        "url": await safe_href(title_selectors + ['a[href*="job-listings"]', 'a']),
    }


async def _is_walkin(article) -> bool:
    try:
        return await article.get_by_text("Walk-in", exact=False).count() > 0
    except Exception:
        return False


async def selectJobInBulk(page: Page):
    checkboxes = page.locator('article.jobTuple .tuple-check-box')
    articles = page.locator('article.jobTuple')
    total = await checkboxes.count()
    selected_jobs = []
    for i in range(total):
        if len(selected_jobs) >= 5: break
        cb = checkboxes.nth(i)
        article = articles.nth(i)
        if await cb.is_visible():
            # Random scroll simulation
            if random.random() > 0.6: await page.mouse.wheel(0, random.randint(200, 400))

            is_checked = await cb.locator('.naukicon-ot-Checked').count() > 0
            if is_checked:
                continue

            if await _is_walkin(article):
                print("⏭️ Naukri AutoAI: Skipping Walk-in listing (not supported by quick apply).")
                continue

            min_experience = await _get_min_experience_required(article)
            if min_experience is not None and min_experience > MAX_EXPERIENCE_YEARS:
                print(f"⏭️ Naukri AutoAI: Skipping job requiring {min_experience}+ yrs experience (limit is {MAX_EXPERIENCE_YEARS} yrs).")
                continue

            job_info = await _extract_job_info(article)
            key = _job_key(job_info)
            if key in _seen_job_keys:
                print(f"⏭️ Naukri AutoAI: Already attempted this run, skipping: {job_info['title']} @ {job_info['company']}")
                continue

            _seen_job_keys.add(key)
            await cb.click()
            selected_jobs.append(job_info)
            print(f"✅ Selected job {len(selected_jobs)}/5: {job_info['title']} @ {job_info['company']}")
            await human_delay(1.5, 3.0)

    return selected_jobs
