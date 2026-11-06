from grader.models import Report

def decision(score: float, report: Report, threshold: float = 80) -> str:
    """Conservative policy: any broken tests block, failures trigger review."""
    counts = report.counts()
    if not report.tests or counts["broken"] > 0: return "BLOCK"
    if score < max(50,threshold-20): return "BLOCK"
    if score < threshold or counts["failed"] > 0: return "REVIEW"
    return "SHIP"
