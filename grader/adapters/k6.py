from pathlib import Path
from grader.adapters.base import Adapter
from grader.adapters.helpers import load_json
from grader.models import TestCase, Report
from grader.errors import ParseError

class K6Adapter(Adapter):
    format_name = "k6"

    @classmethod
    def matches(cls, path: Path) -> bool:
        if path.is_dir(): return (path / "summary.json").exists()
        if path.suffix != ".json": return False
        try:
            d = load_json(path)
            return isinstance(d, dict) and isinstance(d.get("metrics"), dict) and ("root_group" in d or "checks" in d.get("metrics", {}))
        except ParseError: return False

    @classmethod
    def parse(cls, path: Path) -> Report:
        file = path / "summary.json" if path.is_dir() else path
        d = load_json(file)
        tests = []
        def walk(group, trail):
            name = " / ".join(trail+[group.get("name") or "root"])
            for check in group.get("checks") or []:
                passed = int(check.get("passes") or 0)
                failed = int(check.get("fails") or 0)
                for i in range(passed): tests.append(TestCase(f"{check.get('name','check')} #{i+1}","passed",name))
                for i in range(failed): tests.append(TestCase(f"{check.get('name','check')} failed #{i+1}","failed",name,message="k6 check failure"))
            for child in group.get("groups") or []: walk(child,trail+[group.get("name") or "root"])
        if isinstance(d.get("root_group"), dict): walk(d["root_group"],[])
        if not tests:
            checks = d.get("metrics",{}).get("checks",{}).get("values",{})
            total = int(checks.get("passes") or 0)+int(checks.get("fails") or 0)
            for i in range(int(checks.get("passes") or 0)): tests.append(TestCase(f"check #{i+1}","passed","k6"))
            for i in range(int(checks.get("fails") or 0)): tests.append(TestCase(f"check failed #{i+1}","failed","k6"))
            if total == 0: raise ParseError("k6 summary has no individual or aggregated checks")
        return Report(cls.format_name, tests, str(file),meta={"metrics": d.get("metrics",{})})
