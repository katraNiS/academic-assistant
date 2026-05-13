import chromadb
from chromadb.utils import embedding_functions

# Λέει στο Chroma ποιο model να χρησιμοποιεί για embeddings
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# In-memory client (δεν αποθηκεύει στον δίσκο - απλό για test)
client = chromadb.Client()
collection = client.create_collection(
    name="test",
    embedding_function=embed_fn
)

# Πρόσθεσε 3 documents
collection.add(
    documents=[
        "The cat sat on the mat",
        "Dogs are loyal animals",
        "Basketball is a sport"
    ],
    ids=["1", "2", "3"]
)

# Search
results = collection.query(
    query_texts=["What pets do people love?"],
    n_results=2
)
print(results)

exit()