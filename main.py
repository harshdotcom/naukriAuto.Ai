import sys

# On Windows, redirected output and legacy consoles default to cp1252, which
# crashes on the emoji used throughout Naukri AutoAI's logs (✅, 🤖, ⚠️). Force UTF-8
# so no print() ever raises UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Give immediate feedback: the imports below pull in langchain_groq ->
# transformers -> torch, which can take 30-60s on the first run. Without this
# line the terminal shows nothing and looks frozen, tempting a Ctrl+C mid-import.
print(
    "🤖 Naukri AutoAI: Booting up... loading AI engine "
    "(first launch can take up to a minute while PyTorch/Transformers initialize).",
    flush=True,
)

import asyncio
import os
import json

from app.ai.llm import init_llm
from app.utils.file_loader import get_resume, get_system_prompt, get_human_prompt
from app.bot.bot_runner import run_bot


async def main():
    if not os.path.exists('data/db.json'):
        with open('data/db.json', 'w') as f:
            json.dump([], f)
    llm = init_llm()
    resume = get_resume()
    system_prompt = get_system_prompt()
    human_prompt = get_human_prompt()
    

    if llm == None:
        print("❌ Naukri AutoAI: AI Initialization Failed.")
        return
    
    if resume == None:
        print("❌ Naukri AutoAI: Resume Not Found.")
        return
    
    if system_prompt == None or human_prompt == None:
        print("❌ Naukri AutoAI: Prompts Not Found.")
        return

    await run_bot(llm, resume, system_prompt, human_prompt)


if __name__ == "__main__":
    asyncio.run(main())