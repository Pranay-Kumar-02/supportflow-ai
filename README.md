# SupportFlow-AI

[cite_start]An AI-Powered Customer Support Automation System built with LangGraph for ABC Technologies[cite: 7, 8].

## Overview
[cite_start]This system automates customer support queries by routing them to specific departments, retrieving context via RAG, requiring human-in-the-loop approval for sensitive requests, and remembering previous interactions[cite: 9, 10, 11, 12, 13, 14, 15, 16]. 

## Features
- [cite_start]**Deterministic Routing**: Routes to Sales, Technical, Billing, or Account[cite: 18].
- [cite_start]**RAG Integration**: Pulls data from local text documents[cite: 19].
- [cite_start]**SQLite Memory**: Remembers past customer conversations[cite: 31].
- [cite_start]**Human-in-the-loop**: Flags high-risk queries (e.g., refunds) for manual supervisor approval via console input[cite: 26].
- **Local LLM**: Powered entirely by Ollama (`qwen2.5:3b`) without API keys.

## Architecture Workflow
```mermaid
graph TD
    Customer --> Memory
    Memory --> Intent
    Intent --> Router
    Router --> Sales
    Router --> Technical
    Router --> Billing
    Router --> Account
    Sales --> RAG
    Technical --> RAG
    Billing --> RAG
    Account --> RAG
    RAG --> Approval
    Approval --> Supervisor
    Supervisor --> Save_Memory
    Save_Memory --> Response