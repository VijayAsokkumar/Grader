from grader.discovery import discover
from grader.models import Assessment
from grader.scoring.baseline import Baseline
from grader.scoring.engine import calculate
from grader.scoring.policy import decision
from grader.analysis.clustering import cluster_failures
from grader.analysis.summaries import summarize
from grader.analysis.insights import rule_based_insight
from grader.ai.prompts import build_prompt
from grader.ai.ollama import OllamaClient
from grader.errors import OllamaError


def analyze(path, *, format=None, baseline: Baseline | None=None, threshold=80, ai=False, model="llama3", ollama_url="http://127.0.0.1:11434"):
    adapter,source=discover(path,format)
    report=adapter.parse(source)
    score,dimensions,missing=calculate(report,baseline)
    findings=cluster_failures(report)
    insight=rule_based_insight(report,findings)
    if ai:
        try: insight=OllamaClient(ollama_url).generate(build_prompt(report,findings),model) or insight
        except OllamaError as exc: insight+=f" (AI unavailable: {exc})"
    result=Assessment(score,decision(score,report,threshold),dimensions,findings,
                      summarize(report,missing),insight,report.format,report.source)
    return result
