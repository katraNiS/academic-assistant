import sys 
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.corpus_collection import config
from src.corpus_collection.search import search_arxiv, is_relevant, get_arxiv_id



def collect_papers():
    
    papers = {}
    total_kept = 0
    total_rejected = 0
    
    for query in config.SEARCH_QUERIES[:3]:
        print(f"\nSearching: {query}")
        
        kept_in_query = 0
        rejected_in_query = 0    
        
        try:
            results = list(search_arxiv(query, config.MAX_RESULTS_PER_QUERY))
        except Exception as e:
            print(f"ERROR: {e}")
            continue
        
        print(f"  Got {len(results)} results")
        
        for result in results: 
            relevant, reason = is_relevant(result)
            
            if not relevant:
                rejected_in_query += 1 
                continue
        
            arxiv_id = get_arxiv_id(result)

            if arxiv_id in papers:
                continue
            
            papers[arxiv_id] = {
                "arxiv_id": arxiv_id,
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "year": result.published.year,
                "abstract": result.summary,
                "categories": result.categories,
                "pdf_url": result.pdf_url,
                "source_query": query
            }
            kept_in_query += 1
            
        
        print(f"Kept: {kept_in_query}, Rejected: {rejected_in_query}")
        total_kept += kept_in_query
        total_rejected += rejected_in_query
    
    print(f"\n=== Total: {total_kept} kept, {total_rejected} rejected ===")
    time.sleep(3)
    return papers

def main():
    papers = collect_papers()
    print(f"\nTotal unique papers: {len(papers)}")
    
if __name__ == "__main__":
    main()