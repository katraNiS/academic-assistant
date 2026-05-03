import sys 
import os
import time
import arxiv
import json
from tqdm import tqdm
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
    time.sleep(5)
    return papers

def download_pdfs(papers):
    
    config.PDF_DIR.mkdir(parents=True, exist_ok=True)

    successful = {}
    failed = []
    
    client = arxiv.Client(page_size=50, delay_seconds=5.0, num_retries=3)
    
    for arxiv_id in tqdm(papers, desc="Downloading"):
        target_path = config.PDF_DIR / f"{arxiv_id}.pdf" # target path
        
        if target_path.exists() and target_path.stat().st_size > 1000: # take metadata, add to pdf_path, add to successful
            successful[arxiv_id] = _register_successful_paper(papers, arxiv_id, target_path)
            continue
        
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            result = next(client.results(search))
            
            result.download_pdf(
                dirpath=str(config.PDF_DIR),
                filename=f"{arxiv_id}.pdf"
            )
            # future improvement , needs refactoring
            if target_path.exists() and target_path.stat().st_size > 1000:
                successful[arxiv_id] = _register_successful_paper(papers, arxiv_id, target_path)
            else: 
                failed.append((arxiv_id, "file too small or missing after download"))

        except Exception as e:
            failed.append((arxiv_id, str(e)))
            
            
    print(f"\nDownloaded: {len(successful)}, Failed: {len(failed)}")
    return successful

def save_metadata(papers):
    config.METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config.METADATA_FILE, "w", encoding="utf-8") as f:
       json.dump(list(papers.values()), f, indent=2, ensure_ascii=False)

def _register_successful_paper(papers, arxiv_id, target_path):
    """Helper: παίρνει το metadata, προσθέτει pdf_path, επιστρέφει."""
    metadata = papers[arxiv_id]
    metadata["pdf_path"] = str(target_path.relative_to(config.PROJECT_ROOT))
    return metadata

def main():
    papers = collect_papers()
    print(f"\nTotal unique papers: {len(papers)}")
    
    papers = download_pdfs(papers)
    print(f"Papers with PDFs: {len(papers)}")
    
    save_metadata(papers)
    print(f"Metadata saved to {config.METADATA_FILE}")
    
if __name__ == "__main__":
    main()