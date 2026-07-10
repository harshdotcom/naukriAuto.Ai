
from sentence_transformers import SentenceTransformer
from app.database.db_record import DBItem
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text:str)->list[float]:
    return model.encode(text).tolist()

def find_similar(question_emb: list[float], db: list[DBItem], threshold=0.85)-> str|None:
    best_score = 0
    best_answer = None

    for item in db:
        score = cosine_similarity(
            [question_emb],
            [item["embedding"]]
        )[0][0]

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score >= threshold:
        return best_answer

    return None