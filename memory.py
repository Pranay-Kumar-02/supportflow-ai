import sqlite3
from datetime import datetime

DB_PATH = "memory.db"

def init_db():
    """Initializes the SQLite database as required by the assignment[cite: 31]."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            query TEXT,
            department TEXT,
            response TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_interaction(customer_name: str, query: str, department: str, response: str):
    """Saves the customer interaction to the memory database[cite: 31]."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO interactions (customer_name, query, department, response, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_name, query, department, response, timestamp))
    conn.commit()
    conn.close()

def get_previous_interactions(customer_name: str) -> str:
    """Retrieves previous interactions for a specific customer[cite: 33, 34]."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT query, department, response, timestamp 
        FROM interactions 
        WHERE customer_name = ? 
        ORDER BY timestamp DESC LIMIT 3
    ''', (customer_name,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No previous interactions found."
    
    memory_str = "Previous interactions:\n"
    for row in rows:
        memory_str += f"- Query: {row[0]} | Dept: {row[1]} | Response: {row[2]}\n"
    return memory_str