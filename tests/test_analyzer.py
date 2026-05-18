import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.analyzer import analyze_query

test_cases = [
    # Simple, in-scope
    "How do ML models predict NBA game outcomes?",
    
    # Complex, in-scope (decomposition expected)
    "Compare deep learning approaches for NBA prediction with those for player tracking",
    
    # Out of scope
    "What is the best recipe for chocolate cake?",
    
    # Borderline (could go either way)
    "What are the advantages and disadvantages of using neural networks for shot prediction?",
]

for i, query in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"TEST {i}: {query}")
    print('='*70)
    
    result = analyze_query(query)
    
    print(f"In scope: {result['in_scope']}")
    print(f"Decomposed: {result['decomposed']}")
    print(f"Queries ({len(result['queries'])}):")
    for q in result['queries']:
        print(f"  - {q}")