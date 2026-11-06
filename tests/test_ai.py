import pytest
from grader.ai.redaction import redact
from grader.ai.ollama import OllamaClient
from grader.errors import OllamaError

def test_sensitive_text_redacted():
    s=redact('Authorization: Bearer abc123 password=secret123 API_KEY=abcdef')
    assert 'abc123' not in s and 'secret123' not in s and 'abcdef' not in s

def test_refuses_remote_ollama():
    with pytest.raises(OllamaError): OllamaClient('https://example.com')
