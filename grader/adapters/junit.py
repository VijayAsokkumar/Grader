from pathlib import Path
from xml.etree import ElementTree as ET
from grader.adapters.base import Adapter
from grader.models import TestCase, Report
from grader.errors import ParseError

class JUnitAdapter(Adapter):
    format_name = "junit"

    @classmethod
    def matches(cls, path: Path) -> bool:
        if path.is_dir(): return any(path.glob("*.xml"))
        if path.suffix != ".xml": return False
        try: return ET.parse(path).getroot().tag in {"testsuites", "testsuite"}
        except (ET.ParseError, OSError): return False

    @classmethod
    def parse(cls, path: Path) -> Report:
        files = sorted(path.glob("*.xml")) if path.is_dir() else [path]
        tests = []
        for file in files:
            try: root = ET.parse(file).getroot()
            except (ET.ParseError, OSError) as e: raise ParseError(f"Bad JUnit XML {file}: {e}") from e
            if root.tag not in {"testsuite", "testsuites"}: raise ParseError(f"Not JUnit XML: {file}")
            for node in root.iter("testcase"):
                err = node.find("failure")
                if err is None: err = node.find("error")
                skipped = node.find("skipped") is not None
                status = ("broken" if err is not None and err.tag == "error" else
                          "failed" if err is not None else "skipped" if skipped else "passed")
                tests.append(TestCase(
                    name=node.get("name", "unnamed"), suite=node.get("classname", "default"),
                    status=status, duration_ms=float(node.get("time", "0"))*1000,
                    message=(err.get("message") or err.text or "") if err is not None else "",
                ))
        return Report(cls.format_name, tests, str(path))
