from langchain_groq import ChatGroq
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache


def init_llm():
    try:    
        # Using the massive 120B model for high-IQ reasoning
        local_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
        
        # Enable SQLite Caching to save tokens on repeated questions
        set_llm_cache(SQLiteCache(database_path="naukri_autoai_memory.db"))
        print("✅ Naukri AutoAI: AI Brain & Memory Cache Online.")
        return local_llm
    except Exception as e:
        print(f"⚠️ AI Initialization Error: {str(e)}")
        local_llm = None