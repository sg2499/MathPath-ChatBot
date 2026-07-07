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

class SupabaseVectorStore:
    """Production retrieval using Supabase pgvector and OpenAI embeddings."""

    def __init__(self):
        settings = get_settings()
        supabase_url = os.environ.get("SUPABASE_URL", "")
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        
        self.supabase: Client | None = None
        if supabase_url and supabase_key:
            self.supabase = create_client(supabase_url, supabase_key)
            
        self.openai_client = None
        if settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here":
            self.openai_client = OpenAI(api_key=settings.openai_api_key)

    def _get_embedding(self, text: str) -> list[float]:
        if not self.openai_client:
            return []
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def search(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if not query.strip() or not self.supabase or not self.openai_client:
            return []
            
        try:
            query_embedding = self._get_embedding(query)
            if not query_embedding:
                return []
                
            settings = get_settings()
            # Assume we have a Supabase RPC function named `match_documents`
            response = self.supabase.rpc(
                'match_documents',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': settings.min_retrieval_score,
                    'match_count': top_k
                }
            ).execute()
            
            results = []
            for item in response.data:
                results.append(
                    RetrievalResult(
                        source=item.get("metadata", {}).get("source", "Unknown"),
                        text=item.get("content", ""),
                        score=item.get("similarity", 0.0)
                    )
                )
            return results
        except Exception as e:
            print(f"Vector search failed: {e}")
            return []
