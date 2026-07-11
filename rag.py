import os

DOCS_DIR = "docs"

def load_documents() -> dict:
    """Loads knowledge base documents from the docs folder[cite: 19, 20]."""
    docs = {}
    for filename in ["pricing.txt", "faq.txt", "manual.txt", "policy.txt"]:
        filepath = os.path.join(DOCS_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                docs[filename] = f.read()
        else:
            docs[filename] = ""
    return docs

def retrieve_context(query: str, department: str) -> str:
    """Retrieves relevant text based on department and query mapping[cite: 13, 20]."""
    docs = load_documents()
    retrieved = []
    
    query_lower = query.lower()
    
    # Simple deterministic retrieval based on department logic
    if department == "Sales":
        retrieved.append(docs.get("pricing.txt", ""))
    elif department == "Technical Support":
        retrieved.append(docs.get("manual.txt", ""))
    elif department == "Billing":
        retrieved.append(docs.get("policy.txt", ""))
    elif department == "Account":
        retrieved.append(docs.get("faq.txt", ""))
        
    return "\n\n".join(retrieved) if retrieved else "No specific documents found."