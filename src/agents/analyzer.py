from langchain_ollama import ChatOllama

LLM_MODEL = "llama3.1:8b"

ANALYZER_PROMPT = """You are a query analyzer for an academic research assistant on basketball analytics.

Your task is to analyze the user's question and decide how to handle it.

User question: {question}

Step 1 - Scope check:
Is this question about basketball analytics, statistics, machine learning in basketball, player/team performance, basketball strategy, or related academic topics?
- If YES, the question is IN SCOPE.
- If NO (e.g., medical advice, cooking, unrelated topics), the question is OUT OF SCOPE.

Step 2 - Complexity check (only if IN SCOPE):
Is this question simple (one focused topic) or complex (requires comparing multiple topics, or has multiple distinct parts)?
- If simple: provide one search query (rephrased for clarity if needed).
- If complex: decompose into 2-4 focused sub-queries, each searchable independently.

Examples of complex questions:
- "Compare X and Y" → two queries, one for X, one for Y
- "How do A, B, and C relate to D?" → multiple queries
- "What are the advantages and disadvantages of Z?" → could be one or two queries

Respond in EXACTLY this format:

IN_SCOPE: <YES or NO>
DECOMPOSED: <YES or NO>
QUERIES:
- <query 1>
- <query 2 if decomposed>
- <etc>

If OUT OF SCOPE, set DECOMPOSED to NO and leave QUERIES empty (no bullet points).
If IN SCOPE and simple, set DECOMPOSED to NO and provide one query.
If IN SCOPE and complex, set DECOMPOSED to YES and provide 2-4 queries.

Do not add anything else. No preamble, no explanation."""

def analyze_query(query):
    """
    Αναλύει την ερώτηση και επιστρέφει decision dict.
    """
    prompt = ANALYZER_PROMPT.format(question=query)
    
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    response = llm.invoke(prompt)
    output = response.content
    
    # Parse
    in_scope = False
    decomposed = False
    queries = []
    
    lines = [line.strip() for line in output.split("\n") if line.strip()]
    
    for line in lines:
        line_upper = line.upper()
        
        if line_upper.startswith("IN_SCOPE:"):
            value = line.split(":", 1)[1].strip().upper()
            in_scope = (value == "YES")
        
        elif line_upper.startswith("DECOMPOSED:"):
            value = line.split(":", 1)[1].strip().upper()
            decomposed = (value == "YES")
        
        elif line.startswith("-"):
            # Γραμμή με bullet → είναι query
            q = line.lstrip("-").strip()
            if q:
                queries.append(q)
    
    return {
        "in_scope": in_scope,
        "decomposed": decomposed,
        "queries": queries,
    }