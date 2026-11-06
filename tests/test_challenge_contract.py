"""Challenge contract skeleton: these expectations should pass after agent implementation."""
from pathlib import Path
import pytest
from grader.models import Report,TestCase as GraderTestCase
from grader.storage.atomic_ingest import ingest_run_atomic

@pytest.mark.xfail(reason='Advanced concurrent ingestion is intentionally not implemented',strict=True)
def test_same_key_is_idempotent(tmp_path):
    db=str(tmp_path/'runs.sqlite3')
    r=Report('junit',[GraderTestCase('pass','passed')],'example.xml')
    first=ingest_run_atomic(db,r,run_key='pipeline-123')
    second=ingest_run_atomic(db,r,run_key='pipeline-123')
    assert first==second

@pytest.mark.xfail(reason='Advanced concurrent ingestion is intentionally not implemented',strict=True)
def test_same_key_conflicting_payload_rejected(tmp_path):
    db=str(tmp_path/'runs.sqlite3')
    r1=Report('junit',[GraderTestCase('test','passed')],'example.xml')
    r2=Report('junit',[GraderTestCase('test','failed')],'example.xml')
    ingest_run_atomic(db,r1,run_key='pipeline-123')
    with pytest.raises(ValueError): ingest_run_atomic(db,r2,run_key='pipeline-123')
