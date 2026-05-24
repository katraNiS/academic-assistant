import json
import time
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.graph import run_agent


# ============================================================
# Test questions
# ============================================================

TEST_QUERIES = [
    # --- Simple (in-scope, no decomposition expected) ---
    {
        "id": 1,
        "category": "simple",
        "query": "What machine learning models are used to predict NBA game outcomes?",
        "expected_behavior": "in-scope, no decomposition, single search",
    },
    {
        "id": 2,
        "category": "simple",
        "query": "How is player tracking data used in basketball analytics?",
        "expected_behavior": "in-scope, no decomposition, single search",
    },
    {
        "id": 3,
        "category": "simple",
        "query": "What methods are used for shot selection analysis in basketball?",
        "expected_behavior": "in-scope, no decomposition, single search",
    },
    {
        "id": 4,
        "category": "simple",
        "query": "How are neural networks applied to basketball trajectory prediction?",
        "expected_behavior": "in-scope, no decomposition, single search",
    },
    
    # --- Complex (in-scope, decomposition expected) ---
    {
        "id": 5,
        "category": "complex",
        "query": "Compare deep learning approaches for NBA prediction with those for player tracking",
        "expected_behavior": "in-scope, decomposition into 2 sub-queries",
    },
    {
        "id": 6,
        "category": "complex",
        "query": "What are the advantages and limitations of using machine learning in basketball analytics?",
        "expected_behavior": "in-scope, decomposition into advantages/limitations",
    },
    {
        "id": 7,
        "category": "complex",
        "query": "How do traditional statistical methods differ from modern ML approaches in basketball outcome prediction?",
        "expected_behavior": "in-scope, decomposition into traditional vs modern methods",
    },
    
    # --- Out-of-scope ---
    {
        "id": 8,
        "category": "out_of_scope",
        "query": "What is the chemical composition of water?",
        "expected_behavior": "out-of-scope, rejection without retrieval",
    },
    {
        "id": 9,
        "category": "out_of_scope",
        "query": "How do I cook traditional Italian pasta carbonara?",
        "expected_behavior": "out-of-scope, rejection without retrieval",
    },
    {
        "id": 10,
        "category": "out_of_scope",
        "query": "What are the latest developments in quantum computing?",
        "expected_behavior": "out-of-scope, rejection without retrieval",
    },
]


# ============================================================
# Output paths
# ============================================================

RESULTS_DIR = Path("evaluation_results")
JSON_FILE = RESULTS_DIR / "results.json"
MARKDOWN_FILE = RESULTS_DIR / "summary.md"


# ============================================================
# Runner
# ============================================================

def run_single_query(test_case: dict) -> dict:
    """Τρέχει μία ερώτηση και επιστρέφει το αποτέλεσμα με metadata."""
    print(f"\n{'#'*70}")
    print(f"# TEST {test_case['id']} ({test_case['category'].upper()})")
    print(f"# Query: {test_case['query']}")
    print(f"# Expected: {test_case['expected_behavior']}")
    print(f"{'#'*70}")
    
    start_time = time.time()
    
    try:
        final_state = run_agent(test_case["query"])
        duration = time.time() - start_time
        error = None
    except Exception as e:
        duration = time.time() - start_time
        error = str(e)
        final_state = {
            "in_scope": None,
            "decomposed": None,
            "sub_queries": [],
            "all_chunks": [],
            "answer": f"ERROR: {e}",
        }
    
    # Συγκεντρώνουμε το result
    result = {
        "id": test_case["id"],
        "category": test_case["category"],
        "query": test_case["query"],
        "expected_behavior": test_case["expected_behavior"],
        "in_scope": final_state.get("in_scope"),
        "decomposed": final_state.get("decomposed"),
        "sub_queries": final_state.get("sub_queries", []),
        "num_chunks_used": len(final_state.get("all_chunks", [])),
        "answer": final_state.get("answer", ""),
        "duration_seconds": round(duration, 1),
        "error": error,
    }
    
    print(f"\n>>> Duration: {result['duration_seconds']}s")
    print(f">>> In scope: {result['in_scope']}")
    print(f">>> Decomposed: {result['decomposed']}")
    print(f">>> Chunks used: {result['num_chunks_used']}")
    
    return result


def save_json(results: list) -> None:
    """Αποθηκεύει results σε JSON."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[Saved] {JSON_FILE}")


def save_markdown(results: list) -> None:
    """Παράγει readable markdown summary."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    lines = []
    lines.append("# Evaluation Results\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"Total queries: {len(results)}\n")
    
    # Summary stats
    by_category = {}
    for r in results:
        cat = r["category"]
        by_category.setdefault(cat, []).append(r)
    
    lines.append("## Summary by Category\n")
    for cat, items in by_category.items():
        total_time = sum(r["duration_seconds"] for r in items)
        avg_time = total_time / len(items) if items else 0
        lines.append(f"- **{cat}**: {len(items)} queries, avg {avg_time:.1f}s\n")
    
    total_duration = sum(r["duration_seconds"] for r in results)
    lines.append(f"\n**Total evaluation time**: {total_duration:.0f}s ({total_duration/60:.1f} min)\n")
    
    # Detail per query
    lines.append("\n---\n")
    for r in results:
        lines.append(f"## Test {r['id']}: {r['category']}\n")
        lines.append(f"**Query**: {r['query']}\n")
        lines.append(f"**Expected**: {r['expected_behavior']}\n")
        lines.append(f"**In scope**: {r['in_scope']}\n")
        lines.append(f"**Decomposed**: {r['decomposed']}\n")
        if r["sub_queries"]:
            lines.append("**Sub-queries**:\n")
            for sq in r["sub_queries"]:
                lines.append(f"- {sq}\n")
        lines.append(f"**Chunks used**: {r['num_chunks_used']}\n")
        lines.append(f"**Duration**: {r['duration_seconds']}s\n")
        if r["error"]:
            lines.append(f"**ERROR**: {r['error']}\n")
        lines.append(f"\n**Answer**:\n\n{r['answer']}\n")
        lines.append("\n---\n")
    
    with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"[Saved] {MARKDOWN_FILE}")


def main():
    print("="*70)
    print("ACADEMIC ASSISTANT - EVALUATION")
    print(f"Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total queries: {len(TEST_QUERIES)}")
    print("="*70)
    
    results = []
    
    for test_case in TEST_QUERIES:
        result = run_single_query(test_case)
        results.append(result)
        
        # Save after EACH query — αν σπάσει στη μέση, δεν χάνουμε δουλειά
        save_json(results)
    
    # Final save
    save_json(results)
    save_markdown(results)
    
    print("\n" + "="*70)
    print("EVALUATION COMPLETE")
    print(f"Results: {RESULTS_DIR}/")
    print("="*70)


if __name__ == "__main__":
    main()