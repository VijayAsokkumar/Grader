from pathlib import Path
from grader.adapters.base import Adapter
from grader.adapters.helpers import load_json
from grader.models import TestCase, Report
from grader.errors import ParseError

class JestAdapter(Adapter):
    format_name = "jest"

    @classmethod
    def matches(cls, path: Path) -> bool:
        if path.is_dir(): return (path / "jest-results.json").exists()
        if path.suffix != ".json": return False
        try:
            d = load_json(path)
            return isinstance(d, dict) and isinstance(d.get("testResults"), list) and "numTotalTests" in d
        except ParseError: return False

    @classmethod
    def parse(cls, path: Path) -> Report:
        file = path / "jest-results.json" if path.is_dir() else path
        d = load_json(file)
        tests = []
        for suite in d.get("testResults", []):
            for t in suite.get("assertionResults", []):
                status = str(t.get("status") or "pending")
                normalized = "passed" if status == "passed" else "failed" if status == "failed" else "skipped"
                messages = t.get("failureMessages") or []
                tests.append(TestCase(
                    name=str(t.get("fullName") or t.get("title") or "unnamed"),
                    suite=str(suite.get("name") or "default"), status=normalized,
                    duration_ms=float(t.get("duration") or 0),message="\n".join(map(str,messages)),
                    retries=int(t.get("invocations") or 1)-1,
                ))
        return Report(cls.format_name, tests, str(file))
