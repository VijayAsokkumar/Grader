from grader.models import Report
from grader.scoring.baseline import Baseline

def clamp(x: float) -> float:
    return round(max(0.0, min(100.0, x)), 2)

def dimension_scores(report: Report, baseline: Baseline | None = None) -> dict[str, float | None]:
    baseline = baseline or Baseline()
    n = len(report.tests)
    counted = sum(t.status != "skipped" for t in report.tests)
    passing = sum(t.status == "passed" for t in report.tests)
    pass_rate = 100 * passing / counted if counted else 0.0
    flakiness = 100 * (1-sum(t.flaky for t in report.tests)/n) if n else 0.0
    retry = 100 * (1-sum(t.retries > 0 for t in report.tests)/n) if n else 0.0
    suites = len({t.suite for t in report.tests})
    if baseline.expected_suites is not None and baseline.expected_suites > 0:
        breadth = clamp(100*suites/baseline.expected_suites)
    else:
        breadth = None
    if baseline.average_duration_ms is not None and baseline.average_duration_ms > 0 and n:
        avg = sum(t.duration_ms for t in report.tests)/n
        duration = clamp(100*min(1.0, baseline.average_duration_ms/max(avg,0.000001)))
    else: duration = None
    if baseline.current_coverage_percent is not None and baseline.coverage_percent is not None:
        # Each 1 percentage-point drop costs 10 points; a rise is capped at 100.
        coverage = clamp(100-10*max(0,baseline.coverage_percent-baseline.current_coverage_percent))
    else: coverage = None
    return {"pass_rate":clamp(pass_rate),"flaky_index":clamp(flakiness),
            "coverage_delta":coverage,"duration_trend":duration,
            "suite_breadth":breadth,"retry_rate":clamp(retry)}
