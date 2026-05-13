import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "basketball_papers"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def build_index(chunks, papers_metadata):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
    )
    
    metadata_lookup = {p["arxiv_id"]: p for p in papers_metadata}
    
    documents = []
    ids = []
    metadatas = []
    
    for chunk in chunks:
        paper_meta = metadata_lookup[chunk["arxiv_id"]]
        
        documents.append(chunk["text"])
        ids.append(chunk["chunk_id"])
        metadatas.append({
            "arxiv_id": chunk["arxiv_id"],
            "chunk_index": chunk["chunk_index"],
            "title": paper_meta["title"],
            "year": paper_meta["year"],
            "authors": ", ".join(paper_meta["authors"]),
        })
    
    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    
    print(f"Indexed {len(documents)} chunks from {len(papers_metadata)} papers")
    
def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(
        name=COLLECTION_NAME, 
        embedding_function=get_embedding_function(),
    )
    return collection 

def search(query, top_k=5):
    collection = get_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )
    
    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i],
            "metadata": results["metadatas"][0][i],
        })
    
    return output