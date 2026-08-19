import asyncio
import random
from playwright.async_api import Page, Locator

from app.utils.human import human_delay, human_typing, human_mouse_move
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.utils.bot_question import getNaukriBotQuestion
from app.bot.handle_options import getAvailableOptions
from app.ai.ai_answer import getAiAnswer
from app.repository.repo import findAnswerFromPreviousResponse, saveResponseToDB
from app.utils.report import record_qa
from typing import Any



async def handle_questionnaire(page: Page, llm: ChatGroq, resume:str, system_prompt:str, human_prompt:str):
    if not llm:
        return

    try:
        chat_container = page.locator('.chatbot_MessageContainer')
        await chat_container.wait_for(state='visible', timeout=8000)
        print("🚨 Naukri AutoAI: Questionnaire detected! Analyzing...")

        while True:
            if not await chat_container.is_visible():
                print("✅ Naukri AutoAI: Questionnaire Closed.")
                break

            await asyncio.sleep(random.uniform(2.0, 3.5))

            question: str = await getNaukriBotQuestion(page)

            if question == None:
                continue

            input_box = page.locator('.textArea[contenteditable="true"]')
            is_text = await input_box.is_visible()
            available_options: list[str] = []

            if not is_text:
                available_options = await getAvailableOptions(chat_container)
                if available_options: print(f"🔘 Options detected: {available_options}")

            print("🧠 Naukri AutoAI: Thinking...")
            answer = findAnswerFromPreviousResponse(question, available_options)
            if answer == None:
                answer = await getAiAnswer(system_prompt, human_prompt, resume, available_options, question, llm)
                saveResponseToDB(question, available_options, answer)
            print(f"✅ Naukri AutoAI Answer: {answer}")
            record_qa(question, available_options, answer)

            if is_text:
                await handleTextResponse(input_box, answer, page)

            elif available_options:
                await handleOptionResponse(available_options, answer, chat_container, page)
                
            

            # SUBMIT
            await clickSaveButton(page)

    except Exception as e:
        print(f"🤖 Naukri AutoAI Error in questionnaire: {repr(e)}")


async def handleTextResponse(input_box: Locator, answer: str, page: Page):
    await input_box.click()
    await page.keyboard.press('Control+A')
    await page.keyboard.press('Backspace')
    await human_typing(page.keyboard, answer)
    await human_delay(1, 2)

async def handleOptionResponse(available_options: list[str], answer:str|Any, chat_container: Locator, page: Page):
    matched = next((opt for opt in available_options if opt.lower() in answer.lower()), None)
    if matched:
        target = chat_container.get_by_text(matched, exact=True).last
        await human_mouse_move(page)
        await target.click(force=True)
        # Force check hidden radio button to enable 'Save'
        radio_id = await target.get_attribute("for")
        if radio_id:
            try: await page.locator(f"#{radio_id}").check(force=True)
            except: pass
    else:
        await chat_container.get_by_text(answer).last.click(force=True)

async def clickSaveButton(page: Page):
    # SUBMIT
    save_btn = page.locator('.send:not(.disabled) .sendMsg')
    if await save_btn.is_visible():
        await save_btn.click()
        print("👆 Naukri AutoAI: Clicked Save.")
        await human_delay(1, 2)
    else:
        await page.keyboard.press('Enter')
    