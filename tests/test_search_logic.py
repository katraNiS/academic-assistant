"""
Test ότι τα search/filter functions δουλεύουν σωστά.
"""
import sys
from pathlib import Path

# Προσθέτουμε το project root στο path για να βρει το src/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.corpus_collection.search import search_arxiv, is_relevant, get_arxiv_id

# Δοκιμάζουμε ένα query
QUERY = 'abs:basketball AND abs:prediction'
print(f"Testing query: {QUERY}\n")

results = list(search_arxiv(QUERY, max_results=10))
print(f"Got {len(results)} raw results\n")

kept = []
rejected = []

for r in results:
    relevant, reason = is_relevant(r)
    if relevant:
        kept.append(r)
        print(f"[KEEP] {get_arxiv_id(r)}: {r.title[:70]}")
    else:
        rejected.append((r, reason))
        print(f"[DROP] {get_arxiv_id(r)}: {r.title[:50]} -- {reason}")

print(f"\nSummary: {len(kept)} kept, {len(rejected)} rejected")