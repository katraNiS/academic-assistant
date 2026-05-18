import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import TypedDict
from langgraph.graph import StateGraph, END

from src.agents.analyzer import analyze_query
from src.agents.retriever import retrieve_and_evaluate
from src.agents.synthesizer import synthesize


class AgentState(TypedDict):
    query: str
    in_scope: bool
    decomposed: bool
    sub_queries: list
    all_chunks: list
    answer: str
    
    
def analyzer_node(state: AgentState) -> dict:
    """Node που τρέχει τον Query Analyzer."""
    query = state["query"]
    
    print(f"\n[Analyzer] Analyzing: {query}")
    result = analyze_query(query)
    
    print(f"  In scope: {result['in_scope']}")
    print(f"  Decomposed: {result['decomposed']}")
    print(f"  Sub-queries: {len(result['queries'])}")
    
    return {
        "in_scope": result["in_scope"],
        "decomposed": result["decomposed"],
        "sub_queries": result["queries"],
    }
    
    
def retriever_node(state: AgentState) -> dict:
    """Node που τρέχει τον Retriever για κάθε sub-query."""
    sub_queries = state["sub_queries"]
    all_chunks = []
    
    print(f"\n[Retriever] Processing {len(sub_queries)} sub-queries")
    
    for i, sq in enumerate(sub_queries, 1):
        print(f"\n  Sub-query {i}/{len(sub_queries)}: {sq}")
        chunks, success, attempts = retrieve_and_evaluate(sq)
        print(f"    Success: {success}, Attempts: {attempts}, Chunks: {len(chunks)}")
        
        all_chunks.extend(chunks)
    
    print(f"\n[Retriever] Total chunks collected: {len(all_chunks)}")
    
    return {"all_chunks": all_chunks}

def synthesizer_node(state: AgentState) -> dict:
    """Node που τρέχει τον Synthesizer."""
    query = state["query"]
    chunks = state["all_chunks"]
    
    print(f"\n[Synthesizer] Generating answer from {len(chunks)} chunks")
    answer = synthesize(query, chunks)
    
    return {"answer": answer}

def out_of_scope_node(state: AgentState) -> dict:
    """Node για out-of-scope ερωτήσεις."""
    print("\n[Out of scope] Returning rejection message")
    return {
        "answer": "I cannot answer this question because it is outside the scope of basketball analytics. Please ask a question related to basketball analytics, statistics, or related academic topics."
    }
    
def route_after_analyzer(state: AgentState) -> str:
    """Αποφασίζει πού πάει μετά τον Analyzer."""
    if state["in_scope"]:
        return "retriever"
    else:
        return "out_of_scope"
    
def build_graph():
    """Χτίζει και compile-άρει το LangGraph workflow."""
    
    # 1. Δημιουργία του graph object με το state schema
    workflow = StateGraph(AgentState)
    
    # 2. Προσθήκη nodes
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("out_of_scope", out_of_scope_node)
    
    # 3. Ορισμός entry point
    workflow.set_entry_point("analyzer")
    
    # 4. Conditional edge από Analyzer
    workflow.add_conditional_edges(
        "analyzer",
        route_after_analyzer,
        {
            "retriever": "retriever",
            "out_of_scope": "out_of_scope",
        }
    )
    
    # 5. Απλές edges
    workflow.add_edge("retriever", "synthesizer")
    workflow.add_edge("synthesizer", END)
    workflow.add_edge("out_of_scope", END)
    
    # 6. Compile
    return workflow.compile()

def run_agent(query: str) -> dict:
    """
    Τρέχει το full agentic pipeline για ένα query.
    Επιστρέφει το τελικό state.
    """
    # 1. Compile το graph (μία φορά)
    graph = build_graph()
    
    # 2. Initial state
    initial_state = {
        "query": query,
        "in_scope": False,
        "decomposed": False,
        "sub_queries": [],
        "all_chunks": [],
        "answer": "",
    }
    
    # 3. Run!
    final_state = graph.invoke(initial_state)
    
    return final_state

if __name__ == "__main__":
    test_query = "Compare deep learning approaches for NBA prediction with those for player tracking"
    
    print(f"\n{'='*70}")
    print(f"USER QUERY: {test_query}")
    print('='*70)
    
    result = run_agent(test_query)
    
    print(f"\n\n{'='*70}")
    print("FINAL ANSWER:")
    print('='*70)
    print(result["answer"])