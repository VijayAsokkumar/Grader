import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 source TEXT NOT NULL,
 format TEXT NOT NULL,
 score REAL NOT NULL,
 signal TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

def connect(path:str):
    p=Path(path).expanduser()
    p.parent.mkdir(parents=True,exist_ok=True)
    connection=sqlite3.connect(p,timeout=8)
    connection.execute("PRAGMA busy_timeout = 8000")
    connection.executescript(SCHEMA)
    return connection

def append_run(db_path:str,result) -> int:
    # Simple append-only history. NOT safe idempotent ingestion.
    with connect(db_path) as db:
        cur=db.execute("INSERT INTO runs(source,format,score,signal) VALUES(?,?,?,?)",
                       (result.source,result.format,result.score,result.signal))
        return cur.lastrowid
