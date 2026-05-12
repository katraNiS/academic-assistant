from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=2000, chunk_overlap=400):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=[". ", "? ", "! ", " ", ""],
    keep_separator=True,
    )
    chunks = splitter.split_text(text)
    return chunks 

def chunk_all_papers(texts_dict):
    all_chunks = []
    
    for arxiv_id, text in texts_dict.items():
        chunks = chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{arxiv_id}_chunk_{i}",
                "arxiv_id": arxiv_id,
                "chunk_index": i,
                "text": chunk,
            })
    
    return all_chunks