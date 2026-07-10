

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Any

async def getAiAnswer(system_prompt: str, human_prompt:str, resume:str, available_options:list[str], question: str, llm: ChatGroq)->str|Any:
    prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])
            
    prompt = prompt_template.format_messages(
        resume=resume if should_include_resume(question) else "N/A",
        options=available_options,
        question=question
    )
    raw_response = await llm.ainvoke(prompt)
    answer = raw_response.content.strip().replace("**", "")
    return answer


def should_include_resume(question):
    keywords = ["skill", "project", "technology", "linkedin", "github", "portfolio", "email", "phone", "contact"]
    return any(k in question.lower() for k in keywords)