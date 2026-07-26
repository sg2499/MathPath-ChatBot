from functools import lru_cache
from config import get_settings
from .vector_store import LocalVectorStore, RetrievalResult

@lru_cache
def get_vector_store() -> LocalVectorStore:
    return LocalVectorStore()

def retrieve_context(query: str, top_k: int | None = None) -> list[RetrievalResult]:
    settings = get_settings()
    store = get_vector_store()
    return store.search(query, top_k or settings.top_k)
