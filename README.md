# Ακαδημαϊκός Βοηθός με Agentic RAG για Basketball Analytics

Σύστημα Retrieval-Augmented Generation με 3 agents συνδεδεμένους σε LangGraph workflow. Δέχεται ερωτήσεις σε φυσική γλώσσα και απαντά αξιοποιώντας corpus από 51 ακαδημαϊκά papers του arXiv στο χώρο του basketball analytics. Όλα τρέχουν τοπικά, χωρίς paid APIs.

## Αρχιτεκτονική

Δύο επίπεδα: RAG pipeline (offline indexing με PyMuPDF + LangChain + ChromaDB) και agentic layer με 3 agents (Query Analyzer, Retriever & Evaluator, Synthesizer) σε LangGraph workflow. Όλοι οι agents χρησιμοποιούν το ίδιο LLM (llama3.1:8b μέσω Ollama) με διαφορετικά system prompts.

## Προαπαιτούμενα

- Python 3.12
- [Ollama](https://ollama.com) εγκατεστημένο και τρέχει
- ~10GB ελεύθερο disk space (για το LLM, embedding model, και chroma_db)
- ~16GB RAM (το LLM φορτώνεται στη μνήμη)

## Εγκατάσταση

### 1. Clone και setup environment

```bash
git clone <repo-url>
cd academic-assistant
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# ή: source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 2. Κατέβασε το LLM μέσω Ollama

```bash
ollama pull llama3.1:8b
```

(~4.7GB download, μία φορά)

### 3. Συλλογή corpus

Αυτό το script τρέχει multi-query search στο arXiv API και κατεβάζει ~51 PDFs με basketball analytics papers. Παίρνει ~5-10 λεπτά λόγω rate limiting.

```bash
python src/corpus_collection/collect.py
```

Αποτέλεσμα: `corpus/pdfs/*.pdf` και `corpus/metadata.json`.

### 4. Indexing (χτίσιμο vector store)

Αυτό parse-άρει τα PDFs, τα σπάει σε chunks, και τα βάζει σε ChromaDB. Παίρνει ~2-4 λεπτά σε CPU.

```bash
python tests/test_indexer.py
```

Αποτέλεσμα: `chroma_db/` με 1969 indexed chunks.

## Χρήση

### Single query από το graph

```bash
python src/graph.py
```

Έχει default query μέσα στο script ("How do ML models predict NBA game outcomes?"). Άλλαξε το `test_query` στο `if __name__ == "__main__":` block για διαφορετική ερώτηση.

### Full evaluation σε 10 queries

```bash
python evaluation.py
```

Παίρνει ~50 λεπτά. Αποθηκεύει αποτελέσματα σε `evaluation_results/`.

## Δομή του project

academic-assistant/
├── corpus/                   # PDFs και metadata (gitignored)
│   ├── pdfs/
│   └── metadata.json
├── chroma_db/                # Vector store (gitignored)
├── src/
│   ├── corpus_collection/    # arXiv search & download
│   │   ├── config.py         # search queries, filters, paths
│   │   ├── search.py         # API logic
│   │   └── collect.py        # main collection script
│   ├── rag/                  # RAG pipeline
│   │   ├── pdf_parser.py     # PDF text extraction (PyMuPDF)
│   │   ├── chunker.py        # text chunking (LangChain)
│   │   └── indexer.py        # ChromaDB build & search
│   ├── agents/               # 3 agents
│   │   ├── synthesizer.py    # final answer generation
│   │   ├── retriever.py      # search + evaluate + retry loop
│   │   └── analyzer.py       # scope check + decomposition
│   └── graph.py              # LangGraph orchestration
├── tests/                    # test scripts ανά module
├── evaluation_results/       # output του evaluation
├── evaluation.py             # evaluation runner
├── requirements.txt
└── README.md

## Τεχνικές επιλογές

- **LLM**: `llama3.1:8b` (καλό instruction-following για agentic workflows σε σχέση με μέγεθος)
- **Embedding model**: `all-MiniLM-L6-v2` (384-dim, ~80MB, fast σε CPU)
- **Chunk size**: 2000 chars (~500 tokens) με 400 chars overlap (~100 tokens)
- **Top-K retrieval**: 5 chunks ανά query
- **Max retry attempts**: 3 (Retriever loop)

Λεπτομέρειες και τεκμηρίωση των επιλογών στο `report.pdf`.

## Σημειώσεις performance

Το σύστημα έχει σχεδιαστεί για να τρέχει σε CPU (το AMD GPU σε Windows δεν παίζει με Ollama). Ενδεικτικοί χρόνοι:

- Out-of-scope query: ~17 sec (μόνο Analyzer)
- Simple in-scope query: ~4-7 λεπτά
- Complex query με decomposition: ~9-12 λεπτά

Σε σύστημα με GPU acceleration, αυτοί οι χρόνοι θα ήταν 5-10x ταχύτεροι.

## Reproducibility

Το corpus collection είναι reproducible — όποιος τρέξει το `collect.py` θα μαζέψει παρόμοιο corpus (~50-60 papers). Παραλλαγές μπορεί να υπάρχουν αν το arXiv προσθέσει νέα papers που ταιριάζουν στα queries. Όλες οι παράμετροι (search queries, filters, chunk sizes) είναι σε `src/corpus_collection/config.py` και στις σταθερές των modules.