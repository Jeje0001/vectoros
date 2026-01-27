CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS runs (
    id SERIAL PRIMARY KEY,
    run_id UUID DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL,

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

CREATE TABLE IF NOT EXISTS memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    content TEXT NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);