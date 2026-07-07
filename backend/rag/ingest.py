import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
from openai import OpenAI
from document_loader import load_knowledge_base

load_dotenv()

def main():
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not supabase_url or not supabase_key or not openai_key:
        print("Missing API keys for Supabase or OpenAI.")
        return

    supabase = create_client(supabase_url, supabase_key)
    openai_client = OpenAI(api_key=openai_key)

    kb_dir = Path(__file__).parent.parent / "knowledge_base"
    documents = load_knowledge_base(kb_dir)
    print(f"Loaded {len(documents)} chunks from {kb_dir}")

    # Clear existing documents to avoid duplicates
    try:
        supabase.table("documents").delete().neq("id", 0).execute()
        print("Cleared existing documents.")
    except Exception as e:
        print(f"Error clearing documents: {e}")

    for i, doc in enumerate(documents):
        try:
            res = openai_client.embeddings.create(input=doc.text, model="text-embedding-3-small")
            embedding = res.data[0].embedding
            
            supabase.table("documents").insert({
                "content": doc.text,
                "metadata": {"source": doc.source},
                "embedding": embedding
            }).execute()
            print(f"Inserted chunk {i+1}/{len(documents)}: {doc.source}")
        except Exception as e:
            print(f"Error inserting chunk {i+1}: {e}")

if __name__ == "__main__":
    main()
