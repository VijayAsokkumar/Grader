from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Baseline:
    """External reference measurements; unknown metrics are intentionally not fabricated."""
    total_tests: int | None = None
    average_duration_ms: float | None = None
    coverage_percent: float | None = None
    current_coverage_percent: float | None = None
    expected_suites: int | None = None
