from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class TestCase:
    name: str
    status: str
    suite: str = "default"
    duration_ms: float = 0.0
    message: str = ""
    retries: int = 0
    flaky: bool = False
    history_id: str = ""

    def __post_init__(self):
        allowed = {"passed", "failed", "skipped", "broken"}
        if self.status not in allowed:
            raise ValueError(f"Unsupported status: {self.status}")
        self.duration_ms = max(float(self.duration_ms or 0), 0.0)
        self.retries = max(int(self.retries or 0), 0)


@dataclass(slots=True)
class Report:
    format: str
    tests: list[TestCase]
    source: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    meta: dict[str, Any] = field(default_factory=dict)

    def counts(self) -> dict[str, int]:
        return {status: sum(t.status == status for t in self.tests)
                for status in ("passed", "failed", "skipped", "broken")}


@dataclass(slots=True)
class Finding:
    severity: str
    title: str
    count: int
    examples: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Assessment:
    score: float
    signal: str
    dimensions: dict[str, float]
    findings: list[Finding]
    summary: dict[str, Any]
    insights: str = ""
    format: str = ""
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
