-- ==========================================================
-- SupportFlow-AI
-- SQLite Database Schema
-- ==========================================================

DROP TABLE IF EXISTS interactions;

CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    query TEXT NOT NULL,
    department TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

-- Index to improve customer lookup performance
CREATE INDEX IF NOT EXISTS idx_customer_name
ON interactions(customer_name);

-- Index to improve timestamp-based retrieval
CREATE INDEX IF NOT EXISTS idx_timestamp
ON interactions(timestamp);