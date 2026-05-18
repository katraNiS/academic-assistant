from langchain_ollama import ChatOllama
from src.corpus_collection.search import is_relevant
from src.rag.indexer import search
from src.agents.synthesizer import format_context

LLM_MODEL = "llama3.1:8b"
TOP_K = 5
MAX_ATTEMPTS = 3

EVALUATOR_PROMPT = """You are an evaluator agent for an academic research assistant.

Your task is to determine whether the provided context contains information that can answer the given question about basketball analytics.

Question: {question}

Context:
{context}

Evaluate the context strictly:
- If the context contains specific, relevant information that directly addresses the question, respond YES.
- If the context is off-topic, only tangentially related, or too vague to answer the question, respond NO.

Respond in EXACTLY this format (two lines):
RELEVANT: <YES or NO>
REASON: <one short sentence explaining your decision>

Do not add anything else. No preamble, no extra explanation."""

REFORMULATOR_PROMPT = """You are a query reformulation agent for an academic search system on basketball analytics.

The user asked: "{original_query}"

We searched for: "{last_query}"

The search results were not relevant. The evaluator said: "{reason}"

Your task: rewrite the search query to improve retrieval. Consider:
- Using different terminology that academic papers might use
- Adjusting the breadth (more or less specific)
- Focusing on key concepts from the original question

Respond with ONLY the new search query on a single line. No preamble, no explanation, no quotes around it."""


def evaluate_chunks(query, chunks):
    """Αξιολογεί αν τα chunks απαντούν στο query."""
    
    # 1. Format context (χρησιμοποιώντας το import από synthesizer)
    context = format_context(chunks)
    
    # 2. Γέμισε prompt
    prompt = EVALUATOR_PROMPT.format(
        question=query,
        context=context,
    )
    
    # 3. Κάλεσε LLM
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    response = llm.invoke(prompt)
    output = response.content
    
    # Parse την απάντηση
    is_relevant = False
    reason = "could not parse response"

    lines = [line.strip() for line in output.split("\n") if line.strip()]

    for line in lines:
        line_upper = line.upper()
    
        if line_upper.startswith("RELEVANT:"):
            value = line.split(":", 1)[1].strip().upper()
            is_relevant = (value == "YES")
        elif line_upper.startswith("REASON:"):
            reason = line.split(":", 1)[1].strip()

# Fallback: αν δεν βρήκαμε REASON, πάρε την πρώτη γραμμή 
# που δεν είναι RELEVANT
    if reason == "could not parse response":
        for line in lines:
            if not line.upper().startswith("RELEVANT:"):
                reason = line
                break

    return is_relevant, reason


def reformulate_query(original_query, last_query, reason):
    """Παράγει βελτιωμένο query βάσει αποτυχίας."""
    
    prompt = REFORMULATOR_PROMPT.format(
        original_query=original_query,
        last_query=last_query,
        reason=reason,
    )
    
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    response = llm.invoke(prompt)
    
    # Το LLM επιστρέφει νέο query — απλά παίρνουμε το content
    new_query = response.content.strip()
    
    # Καθαρισμός: μερικές φορές βάζει quotes ή trailing punctuation
    new_query = new_query.strip('"\'')
    
    return new_query

def retrieve_and_evaluate(query):
    
    current_query = query
    chunks = []
    
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n[Attempt {attempt}] Query: {current_query}")
        
        # 1. Search
        chunks = search(current_query, top_k=TOP_K)
        
        # 2. Evaluate
        is_relevant, reason = evaluate_chunks(query, chunks)
        print(f"  Relevant: {is_relevant}")
        print(f"  Reason: {reason}")
        
        # 3. Decide
        if is_relevant:
            return chunks, True, attempt
        
        # 4. Reformulate (αν δεν είμαστε στο τελευταίο attempt)
        if attempt < MAX_ATTEMPTS:
            current_query = reformulate_query(query, current_query, reason)
    
    # Εξαντλήθηκαν οι προσπάθειες
    return chunks, False, MAX_ATTEMPTS