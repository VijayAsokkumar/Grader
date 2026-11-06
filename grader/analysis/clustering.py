from collections import defaultdict
from grader.models import Report, Finding
from grader.analysis.root_causes import cause

def cluster_failures(report: Report) -> list[Finding]:
    groups = defaultdict(list)
    for test in report.tests:
        if test.status in {"failed","broken"}:
            groups[cause(test.message)].append(test)
    findings = []
    for category, cases in sorted(groups.items(),key=lambda item:-len(item[1])):
        label = f"{category.capitalize()} failure cluster"
        findings.append(Finding(
            severity="HIGH" if len(cases)>=3 or category in {"authentication","network"} else "LOW",
            title=label,count=len(cases),examples=[t.name for t in cases[:5]]))
    return findings
