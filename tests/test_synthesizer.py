import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.indexer import search
from src.agents.synthesizer import format_context
from src.agents.synthesizer import synthesize


chunks = search("How do ML models predict NBA outcomes?", top_k=3)

print(f"Got {len(chunks)} chunks\n")

context = format_context(chunks)

print("=== Formatted context ===")
print(context)
print("\n=== End ===")
print(f"\nTotal context length: {len(context)} chars")

print("\n\n=== Now calling Synthesizer ===")

answer = synthesize("How do ML models predict NBA outcomes?", chunks)

print("\n=== ANSWER ===")
print(answer)
print("\n=== End ===")

print("\n\n=== Test: out-of-scope question ===")

chunks = search("basketball player tracking", top_k=3)
answer = synthesize("What is the chemical composition of water?", chunks)

print("\n=== ANSWER ===")
print(answer)