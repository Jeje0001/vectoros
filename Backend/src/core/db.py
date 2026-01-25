import psycopg2
from psycopg2.extras import RealDictCursor, Json
import json
import uuid
import os
from dotenv import load_dotenv


load_dotenv()
from src.core.config import DEFAULT_PROJECT_ID


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
            "project_id": DEFAULT_PROJECT_ID,
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
            run_id, project_id, model, input, output, tokens, cost, latency, status, error, steps
        )
        VALUES (
            %(run_id)s, %(project_id)s, %(model)s, %(input)s, %(output)s,
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
        WHERE project_id= %s
        ORDER BY created_at DESC;
    """,(DEFAULT_PROJECT_ID,))

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
            "steps": row[10], 
            "created_at": row[11].isoformat() if row[11] else None,
            "started_at": row[12].isoformat() if row[12] else None
        })

    cur.close()
    conn.close()
    return result


def list_run_summaries_from_db(limit: int, cursor: str | None):
    conn = get_connection()
    cur = conn.cursor()

    if cursor is None:
        cur.execute("""
            SELECT 
                run_id,
                model,
                status,
                tokens,
                cost,
                latency,
                error,
                created_at,
                input  
            FROM runs
            WHERE project_id = %s
            ORDER BY created_at DESC
            LIMIT %s;
        """, (DEFAULT_PROJECT_ID, limit))
    else:
        cur.execute("""
            SELECT 
                run_id,
                model,
                status,
                tokens,
                cost,
                latency,
                error,
                created_at,
                input
            FROM runs
            WHERE project_id = %s
              AND created_at < %s
            ORDER BY created_at DESC
            LIMIT %s;
        """, (DEFAULT_PROJECT_ID, cursor, limit))

    rows = cur.fetchall()

    items = []
    for row in rows:
        items.append({
            "run_id": str(row["run_id"]),
            "model": row["model"],
            "status": row["status"],
            "tokens": row["tokens"],
            "cost": row["cost"],
            "latency": row["latency"],
            "error": row["error"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else None,
            "input": row["input"]
        })



    if len(rows) == limit:
        last_created_at = rows[-1]["created_at"]
        next_cursor = last_created_at.isoformat() if last_created_at else None
    else:
        next_cursor = None


    cur.close()
    conn.close()

    return {
        "items": items,
        "next_cursor": next_cursor
    }


def get_run_by_run_id(run_id: str):
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
            diagnosis,
            created_at,
            started_at
        FROM runs
        WHERE run_id = %s
          AND project_id = %s
        LIMIT 1;
    """, (run_id, DEFAULT_PROJECT_ID))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "run_id": str(row["run_id"]),
        "model": row["model"],
        "input": row["input"],
        "output": row["output"],
        "tokens": row["tokens"],
        "cost": row["cost"],
        "latency": row["latency"],
        "status": row["status"],
        "error": row["error"],
        "steps": row["steps"],
        "diagnosis": row["diagnosis"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
        "started_at": row["started_at"].isoformat() if row["started_at"] else None
    }



def save_run_diagnosis(run_id: str, diagnosis: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE runs
        SET diagnosis = %s
        WHERE run_id = %s
          AND project_id = %s;
        """,
        (Json(diagnosis), run_id, DEFAULT_PROJECT_ID),
    )

    conn.commit()
    cur.close()
    conn.close()

