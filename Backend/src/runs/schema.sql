CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS runs (
    id SERIAL PRIMARY KEY,
    run_id UUID DEFAULT gen_random_uuid(),

    model VARCHAR(255) NOT NULL,
    input TEXT NOT NULL,
    output TEXT,
    tokens INTEGER,
    cost FLOAT,
    latency FLOAT,
    status VARCHAR(50) NOT NULL,
    error TEXT,
    steps JSONB,

    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP DEFAULT NOW()
);

