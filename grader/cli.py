from __future__ import annotations
import argparse,json,sys
from grader.pipeline import analyze
from grader.config import Settings
from grader.scoring.baseline import Baseline
from grader.exports.json_export import as_json
from grader.exports.slack import slack_blocks
from grader.storage.sqlite import append_run
from grader.storage.trends import recent_runs
from grader.storage.atomic_ingest import ingest_run_atomic
from grader.discovery import discover
from grader.errors import GraderError

def parser():
    p=argparse.ArgumentParser(prog="grader",description="Universal test report quality grader")
    p.add_argument("--report",help="Path to supported report file or directory")
    p.add_argument("--format",choices=["playwright","allure","junit","k6","jest"])
    p.add_argument("--model",default="llama3")
    p.add_argument("--ai",action="store_true",help="Use a locally running Ollama model")
    p.add_argument("--ollama-url",default="http://127.0.0.1:11434")
    p.add_argument("--ci",action="store_true",help="Nonzero exit for score below threshold or BLOCK")
    p.add_argument("--threshold",type=float,default=80)
    p.add_argument("--output",choices=["text","json","slack"],default="text")
    p.add_argument("--record",action="store_true",help="Append basic history (not idempotent)")
    p.add_argument("--atomic-history",action="store_true",help="Challenge feature: atomic idempotent history")
    p.add_argument("--run-key",help="Stable run key for atomic ingestion")
    p.add_argument("--history",action="store_true")
    p.add_argument("--db",default=".grader/grader.sqlite3")
    p.add_argument("--baseline-duration-ms",type=float)
    p.add_argument("--previous-coverage",type=float)
    p.add_argument("--current-coverage",type=float)
    p.add_argument("--expected-suites",type=int)
    return p

def main(argv=None):
    args=parser().parse_args(argv)
    try:
        if args.history:
            print(json.dumps(recent_runs(args.db),indent=2));return 0
        if not args.report:
            parser().error("--report is required unless --history is set")
        baseline=Baseline(average_duration_ms=args.baseline_duration_ms,
                          coverage_percent=args.previous_coverage,
                          current_coverage_percent=args.current_coverage,
                          expected_suites=args.expected_suites)
        result=analyze(args.report,format=args.format,baseline=baseline,
                       threshold=args.threshold,ai=args.ai,model=args.model,ollama_url=args.ollama_url)
        if args.record: append_run(args.db,result)
        if args.atomic_history:
            if not args.run_key: parser().error("--atomic-history requires --run-key")
            adapter,path=discover(args.report,args.format)
            ingest_run_atomic(args.db,adapter.parse(path),run_key=args.run_key)
        if args.output=="json": print(as_json(result))
        elif args.output=="slack": print(json.dumps(slack_blocks(result),indent=2))
        else:
            print(f"Score: {result.score:.0f} · {result.signal}")
            print(f"Tests: {result.summary['total']} | {result.summary['counts']}")
            for f in result.findings: print(f"  {f.severity:<5} · {f.title} ({f.count} tests)")
            print(f"Flaky: {len(result.summary['flaky_tests'])} tests")
            print("Scoring: "+", ".join(f"{k}={v:.1f}" for k,v in result.dimensions.items()))
            if result.summary['unavailable_dimensions']:
                print("Not scored (no baseline): "+", ".join(result.summary['unavailable_dimensions']))
            print("Insight: "+result.insights)
        return 1 if args.ci and (result.score<args.threshold or result.signal=="BLOCK") else 0
    except (GraderError,ValueError,OSError) as exc:
        print(f"grader: {exc}",file=sys.stderr)
        return 2

if __name__=="__main__": raise SystemExit(main())
