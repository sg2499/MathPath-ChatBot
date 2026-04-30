from pathlib import Path
from dataclasses import dataclass
import re


@dataclass
class DocumentChunk:
    source: str
    text: str


def _split_markdown(text: str, max_chars: int = 1200, overlap: int = 180) -> list[str]:
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para.strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = para.strip()
    if current:
        chunks.append(current)

    # Add light overlap for context continuity.
    overlapped: list[str] = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            overlapped.append(chunk)
        else:
            previous_tail = chunks[i - 1][-overlap:]
            overlapped.append(f"{previous_tail}\n\n{chunk}")
    return overlapped


def load_knowledge_base(kb_dir: Path) -> list[DocumentChunk]:
    documents: list[DocumentChunk] = []
    for path in sorted(kb_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(_split_markdown(text)):
            documents.append(DocumentChunk(source=f"{path.name}#chunk-{idx+1}", text=chunk))
    return documents
