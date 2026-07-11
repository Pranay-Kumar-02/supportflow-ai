import os
from langgraph.graph import StateGraph, END, START
from state import SupportState
from agents import (
    memory_node, intent_node, sales_node, tech_node, billing_node, 
    account_node, rag_node, approval_node, supervisor_node, save_memory_node
)
from router import route_query
from memory import init_db

def build_graph():
    """Builds and compiles the LangGraph workflow[cite: 37]."""
    workflow = StateGraph(SupportState)

    # Add Nodes
    workflow.add_node("memory_node", memory_node)
    workflow.add_node("intent_node", intent_node)
    workflow.add_node("sales_node", sales_node)
    workflow.add_node("tech_node", tech_node)
    workflow.add_node("billing_node", billing_node)
    workflow.add_node("account_node", account_node)
    workflow.add_node("rag_node", rag_node)
    workflow.add_node("approval_node", approval_node)
    workflow.add_node("supervisor_node", supervisor_node)
    workflow.add_node("save_memory_node", save_memory_node)

    # Define Edges
    workflow.add_edge(START, "memory_node")
    workflow.add_edge("memory_node", "intent_node")
    
    # Conditional Routing
    workflow.add_conditional_edges(
        "intent_node",
        route_query,
        {
            "sales_node": "sales_node",
            "tech_node": "tech_node",
            "billing_node": "billing_node",
            "account_node": "account_node",
            "supervisor_node": "supervisor_node" # Direct route for memory recall
        }
    )

    # Department nodes to RAG
    for node in ["sales_node", "tech_node", "billing_node", "account_node"]:
        workflow.add_edge(node, "rag_node")

    workflow.add_edge("rag_node", "approval_node")
    workflow.add_edge("approval_node", "supervisor_node")
    workflow.add_edge("supervisor_node", "save_memory_node")
    workflow.add_edge("save_memory_node", END)

    return workflow.compile()

def run_demonstration(graph):
    """Executes the specific test queries provided in the assignment[cite: 39, 40, 41]."""
    queries = [
        {"customer": "Alice", "query": "What are the pricing plans available for your software?"},
        {"customer": "Bob", "query": "I forgot my account password."},
        {"customer": "Charlie", "query": "My application crashes whenever I upload a file."},
        {"customer": "David", "query": "I need a refund for my annual subscription."},
        {"customer": "David", "query": "What was my previous support issue?"}
    ]

    for i, q in enumerate(queries, 1):
        print("\n" + "="*50)
        print(f"Executing Demonstration Query {i}")
        print("="*50)
        
        initial_state = {
            "customer_name": q["customer"],
            "query": q["query"],
            "intent": None,
            "department": None,
            "retrieved_docs": "",
            "approval_needed": False,
            "approval_status": None,
            "memory_context": "",
            "draft_response": "",
            "final_response": ""
        }

        result = graph.invoke(initial_state)

        print(f"Customer Name: {result['customer_name']}")
        print(f"Customer Query: {result['query']}")
        print(f"Department: {result.get('department', 'N/A')}")
        print(f"Approval Needed: {result['approval_needed']} (Status: {result.get('approval_status', 'N/A')})")
        print(f"Memory Accessed: {'Yes' if len(result['memory_context']) > 30 else 'No'}")
        print("-" * 50)
        print(f"Final Response:\n{result['final_response']}")
        print("="*50)

if __name__ == "__main__":
    print("Initializing Database...")
    init_db()
    
    print("Compiling LangGraph Workflow...")
    app_graph = build_graph()
    
    print("Running SupportFlow AI...")
    run_demonstration(app_graph)