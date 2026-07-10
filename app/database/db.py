import json
import os
from app.database.db_record import DBItem

# Calculate absolute path relative to the current file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
relative_db_path = os.path.join(BASE_DIR, "data", "db.json")

# In-memory cache
_db_cache: list[DBItem] | None = None

def load_db() ->None:
    global _db_cache
    if _db_cache is not None:
        return # already loaded
    try:
        with open(relative_db_path, "r") as f:
            _db_cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _db_cache = []  # initialize empty

def get_db() -> list[DBItem]:
    load_db()
    return _db_cache

def add_item(item: DBItem) -> None:
    load_db()
    _db_cache.append(item)

def save_db() -> None:
    if _db_cache is None:
        return

    with open(relative_db_path, "w") as f:
        json.dump(_db_cache, f, indent=2)

def findAnswer(normalizedQuestion: str)->str|None:
    for item in get_db():
        if item["normalized"] == normalizedQuestion:
            return item["answer"]
    return None