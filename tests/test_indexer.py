import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.pdf_parser import extract_all_pdfs
from src.rag.chunker import chunk_all_papers
from src.rag.indexer import build_index

# Φόρτωσε metadata
with open("corpus/metadata.json", "r", encoding="utf-8") as f:
    papers_metadata = json.load(f)

# Pipeline
print("Step 1: Extracting text from PDFs...")
texts = extract_all_pdfs("corpus/metadata.json")

print("\nStep 2: Chunking...")
chunks = chunk_all_papers(texts)
print(f"Total chunks: {len(chunks)}")

print("\nStep 3: Building index...")
build_index(chunks, papers_metadata)

print("\nDone!")