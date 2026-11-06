from pathlib import Path
from grader.adapters.base import Adapter
from grader.adapters.helpers import load_json, lower_status
from grader.models import TestCase, Report
from grader.errors import ParseError

class AllureAdapter(Adapter):
    format_name = "allure"

    @classmethod
    def matches(cls, path: Path) -> bool:
        if path.is_file(): return path.name.endswith("-result.json")
        return any(path.glob("*-result.json"))

    @classmethod
    def parse(cls, path: Path) -> Report:
        files = sorted(path.glob("*-result.json")) if path.is_dir() else [path]
        if not files: raise ParseError("No Allure *-result.json files found")
        tests = []
        for file in files:
            d = load_json(file)
            labels = {x.get("name"): x.get("value") for x in d.get("labels", [])}
            duration = max(float(d.get("stop") or 0) - float(d.get("start") or 0), 0)
            tests.append(TestCase(
                name=str(d.get("name") or d.get("fullName") or file.stem),
                suite=str(labels.get("suite") or labels.get("parentSuite") or "default"),
                status=lower_status(d.get("status")),duration_ms=duration,
                message=str((d.get("statusDetails") or {}).get("message") or ""),
                history_id=str(d.get("historyId") or ""),
                retries=len(d.get("retries") or []),
                flaky=bool(d.get("flaky") or d.get("retries")),
            ))
        return Report(cls.format_name, tests, str(path))
