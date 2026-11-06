from pathlib import Path
from grader.adapters.base import Adapter
from grader.adapters.helpers import load_json, lower_status, message_of
from grader.models import TestCase, Report
from grader.errors import ParseError

class PlaywrightAdapter(Adapter):
    format_name = "playwright"

    @classmethod
    def matches(cls, path: Path) -> bool:
        if path.is_dir(): return (path / "test-results.json").is_file()
        if path.suffix != ".json": return False
        try:
            d = load_json(path)
            return isinstance(d, dict) and isinstance(d.get("suites"), list) and "stats" in d
        except ParseError: return False

    @classmethod
    def parse(cls, path: Path) -> Report:
        file = path / "test-results.json" if path.is_dir() else path
        data = load_json(file)
        if not isinstance(data, dict) or not isinstance(data.get("suites"), list):
            raise ParseError("Invalid Playwright JSON")
        tests = []
        def walk(suite, parents):
            labels = parents + [str(suite.get("title") or "")]
            for spec in suite.get("specs", []):
                for test in spec.get("tests", []):
                    results = test.get("results") or []
                    final = results[-1] if results else {}
                    s = str(test.get("status") or final.get("status") or "skipped")
                    # Playwright top-level status uses expected/unexpected/flaky labels.
                    if s == "expected": status = "passed"
                    elif s == "unexpected": status = "failed"
                    elif s == "flaky": status = "passed"
                    else: status = lower_status(s)
                    err = final.get("error") or next((r.get("error") for r in results if r.get("error")), "")
                    tests.append(TestCase(
                        name=str(spec.get("title") or test.get("title") or "unnamed"),
                        suite=" / ".join(t for t in labels if t), status=status,
                        duration_ms=sum(float(r.get("duration") or 0) for r in results),
                        message=message_of(err), retries=max(len(results) - 1, 0),
                        flaky=(s == "flaky" or (status == "passed" and any(lower_status(r.get("status")) in {"failed","broken"} for r in results[:-1]))),
                    ))
            for child in suite.get("suites", []): walk(child, labels)
        for s in data["suites"]: walk(s, [])
        return Report(cls.format_name, tests, str(file), meta={"stats": data.get("stats", {})})
