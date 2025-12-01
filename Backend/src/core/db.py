import psycopg2
from psycopg2.extras import RealDictCursor, Json
import json
import uuid
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    schema_path = os.path.join(
        os.path.dirname(__file__).replace("core", "runs"),
        "schema.sql"
    )
    with open(schema_path, "r") as f:
        schema = f.read()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(schema)
    conn.commit()
    cur.close()
    conn.close()

def create_run(data: dict):
    # Ensure run_id is a string
    run_id = data.get("run_id")
    if isinstance(run_id, uuid.UUID):
        run_id = str(run_id)
    elif not run_id:
        run_id = str(uuid.uuid4())
    data["run_id"] = run_id
    payload = {
            "run_id": data["run_id"],
            "model": data["model"],
            "input": data["input"],
            "output": data["output"],
            "tokens": data["tokens"],
            "cost": data["cost"],
            "latency": data["latency"],
            "status": data["status"],
            "error": data["error"],
            "steps": Json(data["steps"])
        }

   

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO runs (
            run_id, model, input, output, tokens, cost, latency, status, error, steps
        )
        VALUES (
            %(run_id)s, %(model)s, %(input)s, %(output)s,
            %(tokens)s, %(cost)s, %(latency)s, %(status)s,
            %(error)s, %(steps)s
        )
        RETURNING *;
        """,
        payload
     

    )

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row

def list_runs_from_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            run_id,
            model,
            input,
            output,
            tokens,
            cost,
            latency,
            status,
            error,
            steps,
            created_at,
            started_at
        FROM runs
        ORDER BY created_at DESC;
    """)

    rows = cur.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "run_id": str(row[1]),
            "model": row[2],
            "input": row[3],
            "output": row[4],
            "tokens": row[5],
            "cost": row[6],
            "latency": row[7],
            "status": row[8],
            "error": row[9],
            "steps": row[10],  # psycopg auto-converts JSONB → Python dict
            "created_at": row[11].isoformat() if row[11] else None,
            "started_at": row[12].isoformat() if row[12] else None
        })

    cur.close()
    conn.close()
    return result
