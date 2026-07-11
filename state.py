from typing import TypedDict, Optional

class SupportState(TypedDict):
    customer_name: str
    query: str
    intent: Optional[str]
    department: Optional[str]
    retrieved_docs: str
    approval_needed: bool
    approval_status: Optional[str]
    memory_context: str
    draft_response: str
    final_response: str