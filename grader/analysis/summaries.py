from grader.models import Report
from grader.analysis.flakiness import flaky_tests,retry_count

def summarize(report: Report, unavailable: list[str]) -> dict:
    return {
        "total": len(report.tests), "counts": report.counts(),
        "suites": len({t.suite for t in report.tests}),
        "flaky_tests": flaky_tests(report),
        "retries": retry_count(report),
        "unavailable_dimensions": unavailable,
        "note": "Score renormalizes available weights; missing baseline inputs are not estimated." if unavailable else "All scoring inputs available.",
    }
