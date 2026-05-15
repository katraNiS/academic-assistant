from langchain_ollama import ChatOllama

LLM_MODEL = "llama3.1:8b"

SYNTHESIZER_PROMPT = """You are an academic research assistant specializing in basketball analytics.

Your task is to answer questions based STRICTLY on the provided context from academic papers.

CRITICAL RULES (must follow):
1. Use ONLY information explicitly stated in the provided context. NEVER use general knowledge, common sense, or information you learned during training.
2. For every factual claim, add an inline citation in the format [Document: <arxiv_id>].
3. If the context does not contain enough information to answer the question, respond with EXACTLY this sentence and NOTHING MORE: "The provided context does not contain sufficient information to answer this question."
4. Do NOT add disclaimers like "However, I can provide..." or "Based on general knowledge...". If you cannot answer from the context, state rule 3 and stop.
5. Write in clear, academic English. Be concise but thorough when context allows.

Context:
{context}

Question: {question}

Answer:"""
def format_context(chunks):
    sections = []
    
    for chunk in chunks:
        meta = chunk["metadata"]
        section = f'[Document: {meta["arxiv_id"]}] "{meta["title"]}" ({meta["year"]})\nText: {chunk["text"]}'
        sections.append(section)
    
    return "\n\n---\n\n".join(sections)


def synthesize(query, chunks):
    """Παράγει απάντηση από chunks + query."""
    # 1. Format context
    context = format_context(chunks)
    
    # 2. Γέμισε το prompt
    prompt = SYNTHESIZER_PROMPT.format(
        context=context,
        question=query,
    )
    
    # 3. Κάλεσε LLM
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    response = llm.invoke(prompt)
    
    # 4. Επίστρεψε
    return response.content