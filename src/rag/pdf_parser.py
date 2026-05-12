import fitz
import re 
from pathlib import Path
import json
from tqdm import tqdm


def extract_text_from_pdf(pdf_path):
    try:
    
        texts = []
    
        with fitz.open(pdf_path) as doc:
            for page in doc: 
                texts.append(page.get_text())
            
            
            full_text = "\n".join(texts)
        
            cleaned = re.sub(r'\s+', ' ', full_text)
            cleaned = cleaned.strip()
        
            return cleaned 
    except Exception as e:
        print(f"Error parsing{pdf_path}: {e}")
        return ""
    
def extract_all_pdfs(metadata_file):
    with open(metadata_file, "r", encoding="utf-8") as f:
        papers_list = json.load(f)
        
    results = {}
    
    for paper in tqdm(papers_list, desc="Parsing PDFs"):
        arxiv_id = paper["arxiv_id"]
        pdf_path = paper["pdf_path"]
        
        text = extract_text_from_pdf(pdf_path)
        if not text: 
            continue
        results[arxiv_id] = text
        
    print(f"\nExtracted {len(results)}/{len(papers_list)} papers")
    return results
        