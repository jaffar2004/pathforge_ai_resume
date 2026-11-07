"""SQLite persistence layer. No passwords or resume files are stored."""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "data" / "pathforge.db"

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL,
            target_role TEXT NOT NULL,
            match_score REAL NOT NULL,
            readiness TEXT NOT NULL,
            created_at TEXT NOT NULL,
            profile_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_assessments_name_date
        ON assessments(display_name, created_at);
        """)

def save_assessment(name: str, result: dict):
    init_db()
    with connect() as conn:
        conn.execute(
            """INSERT INTO assessments
            (display_name, target_role, match_score, readiness, created_at, profile_json)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (name.strip() or "Student", result["target_role"], result["match_score"],
             result["readiness"], datetime.now(timezone.utc).isoformat(),
             json.dumps(result["profile"]))
        )

def history(name: str):
    init_db()
    with connect() as conn:
        rows = conn.execute(
            """SELECT id, target_role, match_score, readiness, created_at
            FROM assessments WHERE display_name = ? ORDER BY created_at""",
            (name,)
        ).fetchall()
    return [dict(r) for r in rows]
