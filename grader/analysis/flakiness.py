from grader.models import Report

def flaky_tests(report: Report) -> list[str]:
    return [f"{t.suite}: {t.name}" for t in report.tests if t.flaky]

def retry_count(report: Report) -> int:
    return sum(t.retries for t in report.tests)
