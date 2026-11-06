from fastapi.testclient import TestClient
from grader.api import app
from pathlib import Path

client=TestClient(app)
FIXTURES=Path(__file__).parent/'fixtures'

def test_health():
    r=client.get('/health')
    assert r.status_code==200
    assert r.json()['status']=='ok'

def test_analysis_upload():
    with (FIXTURES/'sample-junit.xml').open('rb') as stream:
        r=client.post('/api/v1/analyze',files={'file':('sample-junit.xml',stream,'application/xml')})
    assert r.status_code==200
    assert r.json()['summary']['total']==6
    assert r.json()['format']=='junit'

def test_atomic_not_implemented():
    r=client.post('/api/v1/ingest/atomic')
    assert r.status_code==501
