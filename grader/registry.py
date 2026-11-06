from pathlib import Path
from grader.adapters.playwright import PlaywrightAdapter
from grader.adapters.allure import AllureAdapter
from grader.adapters.junit import JUnitAdapter
from grader.adapters.k6 import K6Adapter
from grader.adapters.jest import JestAdapter
from grader.errors import DetectionError

ADAPTERS = [AllureAdapter, PlaywrightAdapter, JestAdapter, K6Adapter, JUnitAdapter]

def detect(path: Path, forced: str | None = None):
    if forced:
        adapter = next((a for a in ADAPTERS if a.format_name == forced), None)
        if adapter is None: raise DetectionError(f"Unknown report format: {forced}")
        return adapter
    matches = [adapter for adapter in ADAPTERS if adapter.matches(path)]
    if len(matches) == 1: return matches[0]
    if not matches: raise DetectionError(f"No supported report detected at {path}")
    raise DetectionError(f"Ambiguous report directory; specify --format: {', '.join(a.format_name for a in matches)}")
