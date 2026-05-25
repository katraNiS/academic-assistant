"""
Demo script που δείχνει το retry loop του Retriever σε δράση.
Αναγκάζει το πρώτο attempt να αποτύχει ώστε να ενεργοποιηθεί reformulation.

Usage:
    python demo_retry_loop.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.agents import retriever


# ============================================================
# Patch τον evaluator ώστε το 1ο attempt να αποτυγχάνει
# ============================================================

original_evaluate = retriever.evaluate_chunks
_call_count = {"n": 0}


def forced_first_failure_evaluator(query, chunks):
    """
    Wrapper γύρω από το evaluate_chunks.
    Στο 1ο call επιστρέφει FALSE forced, στα επόμενα καλεί το κανονικό.
    """
    _call_count["n"] += 1
    
    if _call_count["n"] == 1:
        print("  [DEMO] Forcing FIRST attempt to fail to demonstrate retry loop")
        return (
            False,
            "Forced failure for demo purposes — the chunks lack specific terminology requested"
        )
    
    print("  [DEMO] Subsequent attempts use real evaluator")
    return original_evaluate(query, chunks)


# Apply the patch
retriever.evaluate_chunks = forced_first_failure_evaluator


# ============================================================
# Run demo
# ============================================================

def main():
    print("=" * 70)
    print("RETRY LOOP DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demo forces the first retrieval attempt to fail,")
    print("triggering the reformulation logic of the Retriever agent.")
    print()
    print("Expected flow:")
    print("  Attempt 1 → REJECTED (forced)")
    print("  Reformulator → generates new query")
    print("  Attempt 2 → uses real evaluator")
    print()
    print("=" * 70)
    print()
    
    query = "How do ML models predict basketball game outcomes?"
    print(f"Query: {query}")
    print()
    
    chunks, success, attempts = retriever.retrieve_and_evaluate(query)
    
    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print(f"  Total attempts: {attempts}")
    print(f"  Final success: {success}")
    print(f"  Chunks retrieved: {len(chunks)}")
    print()
    
    if attempts >= 2:
        print("✓ Retry loop activated successfully — reformulation occurred")
    else:
        print("✗ Retry loop did not activate (unexpected)")


if __name__ == "__main__":
    main()