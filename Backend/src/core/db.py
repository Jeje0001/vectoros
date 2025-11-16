import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """Create the runs table if it doesn't already exist."""
    schema_path = os.path.join(
        os.path.dirname(__file__).replace("core", "runs"),
        "schema.sql"
    )

    if not os.path.exists(schema_path):
        raise RuntimeError(f"schema.sql not found at path: {schema_path}")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
