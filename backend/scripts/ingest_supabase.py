import os
import sys
from pathlib import Path

# Add backend directory to sys.path so we can import modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import get_settings
from rag.document_loader import load_knowledge_base
from supabase import create_client
from openai import OpenAI

def ingest():
    settings = get_settings()
    
    supabase_url = settings.supabase_url
    supabase_key = settings.supabase_service_role_key
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY missing from settings.")
        return

    if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key_here":
        print("Error: Missing OpenAI API key.")
        return

    print("Loading documents...")
    documents = load_knowledge_base(settings.knowledge_base_dir)
    print(f"Loaded {len(documents)} chunks from markdown files.")

    supabase = create_client(supabase_url, supabase_key)
    openai_client = OpenAI(api_key=settings.openai_api_key)

    for i, doc in enumerate(documents):
        print(f"Embedding chunk {i+1}/{len(documents)}...")
        try:
            response = openai_client.embeddings.create(
                input=doc.text,
                model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding
            
            # Store to Supabase
            supabase.table('documents').insert({
                "content": doc.text,
                "metadata": {"source": doc.source},
                "embedding": embedding
            }).execute()
            print(f"  -> Inserted {doc.source}")
        except Exception as e:
            print(f"Failed to embed/insert chunk {i+1}: {e}")

    print("Ingestion complete!")

if __name__ == "__main__":
    ingest()
