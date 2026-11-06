"""ADVANCED AGENT EVALUATION TASK — see challenge/AGENT_TASK.md.

This module is intentionally incomplete. Existing report parsing and basic scoring
work without it. A future agent must design reliable concurrent run ingestion.
"""
from grader.errors import AtomicIngestionNotImplemented

def ingest_run_atomic(db_path: str, report, *, run_key: str):
    """Atomically upsert a report and test identities with idempotency guarantees.

    Contract:
    - Concurrent calls with identical run_key + payload must return same run ID.
    - Same run_key + different payload must raise a domain conflict.
    - Crash/rollback must never produce half-ingested test records.
    - Persist full test observations and stable cross-framework identities.
    - Avoid race windows between checks and writes; use SQLite transactions.
    - Deterministic repeated test identity with parameterized names and retries.
    - Fully covered by integration tests including process-level contention.

    DO NOT implement this by wrapping append_run() with a Python threading.Lock.
    """
    raise AtomicIngestionNotImplemented("Atomic history ingestion is an evaluation challenge; see challenge/AGENT_TASK.md")
