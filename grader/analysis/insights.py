from grader.models import Report,Finding

def rule_based_insight(report: Report, findings: list[Finding]) -> str:
    if not report.tests: return "No tests were found. Check your report input."
    if not findings: return "No failure clusters detected in this report."
    biggest = max(findings,key=lambda f:f.count)
    return f"{biggest.count} test failures belong to the {biggest.title.lower()} group. Inspect the shared failure pattern before rerunning."
