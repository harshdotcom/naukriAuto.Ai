
from playwright.async_api import Page

async def getNaukriBotQuestion(page:Page)->str|None:
    #Scrape the latest Naukri bot message
    naukri_bot_messages = page.locator('.botItem .botMsg span')
    count = await naukri_bot_messages.count()
    if count == 0:
        return None

    question = await naukri_bot_messages.nth(count - 1).inner_text()
    return question
