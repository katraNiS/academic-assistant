import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.indexer import search
from src.agents.retriever import evaluate_chunks

# Test 1: Good case — relevant chunks
print("=== Test 1: Should be RELEVANT ===")
query = "How do ML models predict NBA outcomes?"
chunks = search(query, top_k=5)
is_relevant, reason = evaluate_chunks(query, chunks)
print(f"Relevant: {is_relevant}")
print(f"Reason: {reason}")

# Test 2: Bad case — irrelevant chunks
print("\n=== Test 2: Should be NOT RELEVANT ===")
query = "What is the chemical composition of water?"
# Παίρνουμε basketball chunks αλλά ρωτάμε χημεία
chunks = search("basketball player tracking", top_k=5)
is_relevant, reason = evaluate_chunks(query, chunks)
print(f"Relevant: {is_relevant}")
print(f"Reason: {reason}")