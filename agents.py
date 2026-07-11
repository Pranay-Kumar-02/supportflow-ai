from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from state import SupportState
from rag import retrieve_context
from memory import get_previous_interactions, save_interaction

# Initialize local LLM as requested [cite: 37]
llm = ChatOllama(model="qwen2.5:3b", temperature=0)

def memory_node(state: SupportState):
    """Fetches previous customer context[cite: 34]."""
    state["memory_context"] = get_previous_interactions(state["customer_name"])
    return state

def intent_node(state: SupportState):
    """Classifies the query intent[cite: 11]."""
    from router import determine_intent
    state["intent"] = determine_intent(state["query"])
    return state

# Department Nodes [cite: 18, 37]
def sales_node(state: SupportState):
    state["department"] = "Sales"
    return state

def tech_node(state: SupportState):
    state["department"] = "Technical Support"
    return state

def billing_node(state: SupportState):
    state["department"] = "Billing"
    return state

def account_node(state: SupportState):
    state["department"] = "Account"
    return state

def rag_node(state: SupportState):
    """Retrieves relevant knowledge base info[cite: 13, 20]."""
    if state.get("intent") != "Memory":
        state["retrieved_docs"] = retrieve_context(state["query"], state["department"])
    else:
        state["retrieved_docs"] = "Memory recall requested."
    return state

def approval_node(state: SupportState):
    """Checks for high-risk requests requiring human supervisor approval[cite: 26, 27, 28, 29]."""
    query = state["query"].lower()
    high_risk_keywords = ["refund", "cancel", "closure", "compensation", "manager", "escalate"]
    
    state["approval_needed"] = any(keyword in query for keyword in high_risk_keywords)
    
    if state["approval_needed"]:
        print("\n" + "!"*40)
        print("HUMAN APPROVAL REQUIRED [cite: 25]")
        print(f"Customer: {state['customer_name']}")
        print(f"Query: {state['query']}")
        print("!"*40)
        user_input = input("Approve this request? (y/n): ").strip().lower()
        if user_input == 'y':
            state["approval_status"] = "Approved"
        else:
            state["approval_status"] = "Rejected"
    else:
        state["approval_status"] = "N/A"
        
    return state

def supervisor_node(state: SupportState):
    """Supervisor agent that drafts/improves the final response[cite: 16, 38]."""
    if state.get("approval_status") == "Rejected":
        state["final_response"] = "Request rejected by supervisor."
        return state

    system_prompt = f"""You are the AI Supervisor for ABC Technologies Customer Support.
    Generate a professional and helpful final response for the customer based on the provided context.
    
    Customer Name: {state['customer_name']}
    Department: {state.get('department', 'General')}
    Previous Interactions: {state.get('memory_context', 'None')}
    Knowledge Base Docs: {state.get('retrieved_docs', 'None')}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["query"])
    ]
    
    response = llm.invoke(messages)
    state["final_response"] = response.content
    return state

def save_memory_node(state: SupportState):
    """Saves the final output to memory[cite: 14, 31]."""
    save_interaction(
        state["customer_name"], 
        state["query"], 
        state.get("department", "General"), 
        state["final_response"]
    )
    return state