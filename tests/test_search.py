import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.indexer import search

# Δοκιμαστικές ερωτήσεις
test_queries = [
    "How do machine learning models predict NBA game outcomes?",
    "What methods are used for basketball player tracking?",
    "Shot selection analysis in basketball",
]

for query in test_queries:
    print(f"\n{'='*70}")
    print(f"QUERY: {query}")
    print('='*70)
    
    results = search(query, top_k=3)
    
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] distance={r['distance']:.3f}")
        print(f"    Title: {r['metadata']['title']}")
        print(f"    Year: {r['metadata']['year']}")
        print(f"    Text preview: {r['text'][:200]}...")