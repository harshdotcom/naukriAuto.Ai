import json
from app.utils.process_question import build_query
from app.utils.process_question import normalize
from app.database.db_record import makeDBItem
from app.database.db import findAnswer, add_item, save_db
from app.ai.embedding_model import get_embedding


def findAnswerFromPreviousResponse(question: str, available_options: list[str]|None)-> str|None:
    full_question = build_query(question, available_options)
    normalized_question = normalize(full_question)
    answer = findAnswer(normalized_question)
    return answer

def saveResponseToDB(question: str, available_options: list[str]|None, answer:str):
    full_question = build_query(question, available_options)
    normalized_question = normalize(full_question)
    questionEmbedding = get_embedding(normalized_question)
    dbItem = makeDBItem(question, normalized_question, questionEmbedding, answer)
    add_item(dbItem)
    save_db()
