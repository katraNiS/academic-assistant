import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.retriever import retrieve_and_evaluate

# Test 1: Easy case — πρέπει να πετύχει στο 1ο attempt
print("=== Test 1: Easy case ===")
chunks, success, attempts = retrieve_and_evaluate(
    "How do ML models predict NBA outcomes?"
)
print(f"\n>>> Final: success={success}, attempts={attempts}, chunks={len(chunks)}")

# Test 2: Out-of-scope — πρέπει να εξαντλήσει 3 προσπάθειες
print("\n\n=== Test 2: Out-of-scope ===")
chunks, success, attempts = retrieve_and_evaluate(
    "What is the chemical composition of water?"
)
print(f"\n>>> Final: success={success}, attempts={attempts}, chunks={len(chunks)}")