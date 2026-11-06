from pathlib import Path
import json
from grader.errors import ParseError

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as e:
        raise ParseError(f"Unable to read JSON from {path}: {e}") from e

def lower_status(status, default="skipped"):
    value = str(status or "").lower()
    if value in {"pass", "passed", "ok", "success"}: return "passed"
    if value in {"fail", "failed", "failure"}: return "failed"
    if value in {"broken", "error", "timedout", "timedout"}: return "broken"
    return default

def message_of(value):
    if isinstance(value, dict):
        return str(value.get("message") or value.get("stack") or value.get("error") or "")
    return str(value or "")
