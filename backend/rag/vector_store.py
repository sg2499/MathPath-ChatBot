import os
from dataclasses import dataclass
from supabase import create_client, Client
from openai import OpenAI
from config import get_settings

@dataclass
class RetrievalResult:
    source: str
    text: str
    score: float

import math
import json
import os
from pathlib import Path

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 * magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

class LocalVectorStore:
    """Production retrieval using a local in-memory vector store with OpenAI embeddings."""

    def __init__(self):
        settings = get_settings()
        self.openai_client = None
        if settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here":
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            
        self.kb_dir = settings.knowledge_base_dir
        self.cache_file = self.kb_dir / "embeddings.json"
        self.documents = [] # list of dicts: {"source": str, "content": str, "embedding": list[float]}
        self._load_or_compute_embeddings()

    def _get_embedding(self, text: str) -> list[float]:
        if not self.openai_client:
            return []
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception:
            return []

    def _load_or_compute_embeddings(self):
        if not self.kb_dir.exists():
            return
            
        # Load cache if exists
        cache = {}
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except Exception:
                pass
                
        dirty = False
        
        for file_path in self.kb_dir.glob("*.md"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
            except Exception:
                continue
                
            if not content:
                continue
                
            source = file_path.name
            
            # Use file name as cache key for simplicity, plus hash of content could be better, 
            # but since these files rarely change programmatically, name is fine.
            if source in cache:
                embedding = cache[source]
            else:
                embedding = self._get_embedding(content)
                if embedding:
                    cache[source] = embedding
                    dirty = True
                    
            if embedding:
                self.documents.append({
                    "source": source,
                    "content": content,
                    "embedding": embedding
                })
                
        if dirty:
            try:
                with open(self.cache_file, "w", encoding="utf-8") as f:
                    json.dump(cache, f)
            except Exception:
                pass

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if not query.strip() or not self.openai_client or not self.documents:
            return []
            
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return []
            
        results = []
        for doc in self.documents:
            score = cosine_similarity(query_embedding, doc["embedding"])
            results.append(RetrievalResult(
                source=doc["source"],
                text=doc["content"],
                score=score
            ))
            
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
