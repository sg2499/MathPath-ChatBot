from functools import lru_cache
from config import get_settings
from .document_loader import load_knowledge_base
from .vector_store import LocalTfidfVectorStore, RetrievalResult


@lru_cache
def get_vector_store() -> LocalTfidfVectorStore:
    settings = get_settings()
    docs = load_knowledge_base(settings.knowledge_base_dir)
    return LocalTfidfVectorStore(docs)


def retrieve_context(query: str, top_k: int | None = None) -> list[RetrievalResult]:
    settings = get_settings()
    store = get_vector_store()
    return store.search(query, top_k or settings.top_k)
