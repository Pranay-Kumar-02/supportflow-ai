from state import SupportState

def determine_intent(query: str) -> str:
    """Deterministic intent classification mapping queries to departments[cite: 18]."""
    query_lower = query.lower()
    
    # Memory recall check
    if "previous" in query_lower or "last issue" in query_lower:
        return "Memory"
        
    # Billing keywords
    if any(word in query_lower for word in ["invoice", "payment", "refund", "billing"]):
        return "Billing"
        
    # Account keywords
    elif any(word in query_lower for word in ["password", "profile", "account", "login", "reset"]):
        return "Account"
        
    # Technical keywords
    elif any(word in query_lower for word in ["error", "crash", "install", "bug", "technical"]):
        return "Technical Support"
        
    # Sales keywords
    elif any(word in query_lower for word in ["pricing", "plan", "subscription", "buy", "sales"]):
        return "Sales"
        
    return "Sales" # Default fallback

def route_query(state: SupportState):
    """Conditional routing function for LangGraph[cite: 12]."""
    intent = state.get("intent")
    if intent == "Sales":
        return "sales_node"
    elif intent == "Technical Support":
        return "tech_node"
    elif intent == "Billing":
        return "billing_node"
    elif intent == "Account":
        return "account_node"
    elif intent == "Memory":
        return "supervisor_node" # Skip RAG and routing, go straight to response
    return "sales_node"