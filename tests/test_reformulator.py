import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.retriever import reformulate_query

# Σενάριο 1: Query με λάθος terminology
print("=== Test 1: Wrong terminology ===")
new_query = reformulate_query(
    original_query="How do deep learning architectures work in basketball?",
    last_query="deep learning architectures basketball",
    reason="The context contains general ML methods, not deep learning specifically.",
)
print(f"New query: {new_query}")

# Σενάριο 2: Query πολύ ευρύ
print("\n=== Test 2: Too broad ===")
new_query = reformulate_query(
    original_query="How is computer vision used in basketball games?",
    last_query="basketball",
    reason="Too general, returned mixed results.",
)
print(f"New query: {new_query}")