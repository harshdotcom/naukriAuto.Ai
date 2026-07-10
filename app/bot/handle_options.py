from playwright.async_api import Locator

async def getAvailableOptions(chat_container: Locator):
    available_options: list[str] = []

    # Targeted search inside the chat container for option labels and buttons
    # We exclude '.ssrc__radio' to avoid capturing hidden input values directly, preferring visible labels.
    options_locator = chat_container.locator('.ssrc__label, label, button, .chip, [role="button"]')
    for i in range(await options_locator.count()):
        el = options_locator.nth(i)
        txt = await el.inner_text()
        if not txt:
            txt = await el.get_attribute("value")
            
        if txt and 0 < len(txt.strip()) < 50:
            available_options.append(txt.strip())
            
    available_options = list(dict.fromkeys(available_options))[-10:] # Deduplicate and keep most recent
    if available_options: 
        print(f"🔘 Options detected: {available_options}")
        
    return available_options
