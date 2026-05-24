"""
Follow-up evaluation: τρέχει 3 επιπλέον queries μετά τις βελτιώσεις.
- 1 query για retry loop activation
- 2 queries (re-run των Tests 6, 7) μετά το prompt improvement
"""

import json
import time
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.graph import run_agent


# ============================================================
# Follow-up queries
# ============================================================

FOLLOWUP_QUERIES = [
    {
        "id": "retry_test",
        "category": "retry_loop_test",
        "query": "How is reinforcement learning being used to optimize coaching decisions in basketball?",
        "expected_behavior": "in-scope but uncommon terminology; should trigger retry loop with reformulation",
        "purpose": "Demonstrate retry loop in action",
    },
    {
        "id": "test_6_rerun",
        "category": "complex_rerun",
        "query": "What are the advantages and limitations of using machine learning in basketball analytics?",
        "expected_behavior": "in-scope, decomposition. Now should have proper citations (after prompt improvement).",
        "purpose": "Verify citation fix",
    },
    {
        "id": "test_7_rerun",
        "category": "complex_rerun",
        "query": "How do traditional statistical methods differ from modern ML approaches in basketball outcome prediction?",
        "expected_behavior": "in-scope, decomposition. Now should have proper citations.",
        "purpose": "Verify citation fix",
    },
]


# ============================================================
# Output paths
# ============================================================

RESULTS_DIR = Path("evaluation_results")
JSON_FILE = RESULTS_DIR / "followup_results.json"
MARKDOWN_FILE = RESULTS_DIR / "followup_summary.md"


# ============================================================
# Runner (ίδιο pattern με το αρχικό evaluation)
# ============================================================

def run_single_query(test_case: dict) -> dict:
    print(f"\n{'#'*70}")
    print(f"# {test_case['id'].upper()} ({test_case['category']})")
    print(f"# Query: {test_case['query']}")
    print(f"# Purpose: {test_case['purpose']}")
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
    
    result = {
        "id": test_case["id"],
        "category": test_case["category"],
        "purpose": test_case["purpose"],
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
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[Saved] {JSON_FILE}")


def save_markdown(results: list) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    lines = []
    lines.append("# Follow-up Evaluation Results\n\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    lines.append("This run includes:\n")
    lines.append("- 1 retry loop demonstration query\n")
    lines.append("- 2 re-runs after Synthesizer prompt improvement (citation enforcement)\n\n")
    
    total_duration = sum(r["duration_seconds"] for r in results)
    lines.append(f"**Total time**: {total_duration:.0f}s ({total_duration/60:.1f} min)\n\n")
    
    lines.append("---\n\n")
    
    for r in results:
        lines.append(f"## {r['id']}\n\n")
        lines.append(f"**Purpose**: {r['purpose']}\n\n")
        lines.append(f"**Query**: {r['query']}\n\n")
        lines.append(f"**Expected**: {r['expected_behavior']}\n\n")
        lines.append(f"**In scope**: {r['in_scope']}\n\n")
        lines.append(f"**Decomposed**: {r['decomposed']}\n\n")
        if r["sub_queries"]:
            lines.append("**Sub-queries**:\n")
            for sq in r["sub_queries"]:
                lines.append(f"- {sq}\n")
            lines.append("\n")
        lines.append(f"**Chunks used**: {r['num_chunks_used']}\n\n")
        lines.append(f"**Duration**: {r['duration_seconds']}s\n\n")
        if r["error"]:
            lines.append(f"**ERROR**: {r['error']}\n\n")
        lines.append(f"**Answer**:\n\n{r['answer']}\n\n")
        lines.append("---\n\n")
    
    with open(MARKDOWN_FILE, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"[Saved] {MARKDOWN_FILE}")


def main():
    print("="*70)
    print("FOLLOW-UP EVALUATION")
    print(f"Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total queries: {len(FOLLOWUP_QUERIES)}")
    print("="*70)
    
    results = []
    
    for test_case in FOLLOWUP_QUERIES:
        result = run_single_query(test_case)
        results.append(result)
        save_json(results)
    
    save_json(results)
    save_markdown(results)
    
    print("\n" + "="*70)
    print("FOLLOW-UP EVALUATION COMPLETE")
    print(f"Results: {RESULTS_DIR}/followup_*.{{json,md}}")
    print("="*70)


if __name__ == "__main__":
    main()