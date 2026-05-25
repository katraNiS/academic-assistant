"""
Test script για εύρεση query που ενεργοποιεί φυσιολογικά το retry loop.
Δοκιμάζει υποψήφιες ερωτήσεις και σταματάει στην πρώτη που πετυχαίνει.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.agents.retriever import retrieve_and_evaluate


# Υποψήφιες ερωτήσεις, ταξινομημένες κατά πιθανότητα να ενεργοποιήσουν retry
CANDIDATES = [
    "What was the win-loss record of the Los Angeles Lakers in 2018?",
    "How many three-pointers did Stephen Curry make in the 2015-16 season?",
    "What did Daryl Morey say about analytics in basketball management?",
    "What programming language is most commonly used for basketball analytics implementations?",
    "How does basketball analytics compare to soccer analytics in terms of methodology?",
    "What is the role of MIT Sloan Sports Analytics Conference in basketball research?",
    "What are the typical hardware requirements for running basketball video analysis models?",
]


def main():
    print("=" * 70)
    print("RETRY LOOP CANDIDATE SEARCH")
    print(f"Testing {len(CANDIDATES)} candidate queries")
    print("Will stop at first query that triggers retry (attempts >= 2)")
    print("=" * 70)
    
    found = None
    results_log = []
    
    for i, query in enumerate(CANDIDATES, 1):
        print(f"\n{'#'*70}")
        print(f"# CANDIDATE {i}/{len(CANDIDATES)}")
        print(f"# Query: {query}")
        print(f"{'#'*70}")
        
        start_time = time.time()
        
        try:
            chunks, success, attempts = retrieve_and_evaluate(query)
            duration = time.time() - start_time
            
            print(f"\n>>> Result: attempts={attempts}, success={success}, chunks={len(chunks)}")
            print(f">>> Duration: {duration:.1f}s")
            
            results_log.append({
                "candidate": i,
                "query": query,
                "attempts": attempts,
                "success": success,
                "duration": duration,
            })
            
            if attempts >= 2:
                print(f"\n{'*'*70}")
                print(f"*** FOUND IT! Candidate {i} triggers retry loop! ***")
                print(f"*** Total attempts: {attempts} ***")
                print(f"{'*'*70}")
                found = query
                break
            else:
                print(f"\n[Skipping] Passed on first attempt, trying next...")
        
        except Exception as e:
            print(f"\n[ERROR] {e}")
            results_log.append({
                "candidate": i,
                "query": query,
                "error": str(e),
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("SEARCH SUMMARY")
    print("=" * 70)
    
    for r in results_log:
        if "error" in r:
            print(f"  [{r['candidate']}] ERROR: {r['query'][:60]}")
        else:
            marker = "✓ RETRY" if r["attempts"] >= 2 else "  pass"
            print(f"  [{r['candidate']}] {marker} (attempts={r['attempts']}, {r['duration']:.0f}s): {r['query'][:60]}")
    
    print()
    
    if found:
        print(f"✓ USE THIS QUERY IN THE DEMO:")
        print(f"  {found}")
    else:
        print("✗ No candidate triggered retry loop.")
        print("  Fallback: use demo_retry_loop.py with monkey patching")


if __name__ == "__main__":
    main()