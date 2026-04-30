from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .document_loader import DocumentChunk


@dataclass
class RetrievalResult:
    source: str
    text: str
    score: float


class LocalTfidfVectorStore:
    """Lightweight local retrieval for Step 2.

    This keeps the first backend simple and reliable. Later, it can be replaced
    with Chroma, FAISS, Supabase pgvector, or OpenAI embeddings without changing
    the public API.
    """

    def __init__(self, documents: list[DocumentChunk]):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([doc.text for doc in documents])

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if not query.strip():
            return []
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        ranked_indices = scores.argsort()[::-1][:top_k]
        return [
            RetrievalResult(
                source=self.documents[i].source,
                text=self.documents[i].text,
                score=float(scores[i]),
            )
            for i in ranked_indices
        ]
