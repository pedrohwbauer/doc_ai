import threading
from django.conf import settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

persistent_directory = str(settings.BASE_DIR / "db" / "chroma_db")

class Database:
    _instance = None
    _lock = threading.Lock()  # Lock object to ensure thread safety

    @classmethod
    def get_instance(cls):
        # Double-checked locking to avoid race conditions
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Check again within the lock
                    cls._init_chroma_db()
                    
        return cls._instance

    @classmethod
    def _init_chroma_db(cls):
        cls._instance = Chroma(
            collection_name="documents",
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory=persistent_directory
        )