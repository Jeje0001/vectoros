CREATE TABLE IF NOT EXISTS runs (
    id SERIAL PRIMARY KEY,
    model VARCHAR(255),
    input TEXT,
    output TEXT,
    tokens INTEGER,
    cost FLOAT,
    latency FLOAT,
    status VARCHAR(50),
    error TEXT,
    steps JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
