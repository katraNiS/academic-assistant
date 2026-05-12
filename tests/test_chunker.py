import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.pdf_parser import extract_text_from_pdf
from src.rag.chunker import chunk_text

# Πάρε ένα PDF
test_pdf = Path("corpus/pdfs/2002.08465v1.pdf")  # δικό σου path

text = extract_text_from_pdf(test_pdf)
print(f"Original text: {len(text)} chars")

chunks = chunk_text(text)
print(f"Number of chunks: {len(chunks)}")
print(f"Average chunk size: {sum(len(c) for c in chunks) / len(chunks):.0f} chars")
print(f"\nFirst chunk (first 300 chars):")
print(chunks[0][:300])
print(f"\nSecond chunk (first 300 chars):")
print(chunks[1][:300])

print("\n=== Overlap check ===")
print(f"Last 200 chars of chunk[0]:")
print(repr(chunks[0][-200:]))
print(f"\nFirst 200 chars of chunk[1]:")
print(repr(chunks[1][:200]))

print("\n=== Batch test ===")

from src.rag.pdf_parser import extract_all_pdfs
from src.rag.chunker import chunk_all_papers

texts = extract_all_pdfs("corpus/metadata.json")
all_chunks = chunk_all_papers(texts)

print(f"\nTotal chunks: {len(all_chunks)}")
print(f"From {len(texts)} papers")
print(f"Average chunks per paper: {len(all_chunks) / len(texts):.1f}")

# Δείγμα
print(f"\nSample chunk:")
print(f"  chunk_id: {all_chunks[0]['chunk_id']}")
print(f"  arxiv_id: {all_chunks[0]['arxiv_id']}")
print(f"  chunk_index: {all_chunks[0]['chunk_index']}")
print(f"  text preview: {all_chunks[0]['text'][:200]}...")