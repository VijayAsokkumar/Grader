from pathlib import Path
from grader.pipeline import analyze
from grader.scoring.baseline import Baseline
from grader.scoring.engine import calculate
from grader.models import Report, TestCase as GraderTestCase

FIXTURES=Path(__file__).parent/'fixtures'

def test_score_range_and_clusters():
    a=analyze(FIXTURES/'sample-junit.xml')
    assert 0 <= a.score <= 100
    assert a.signal in {'REVIEW','BLOCK'}
    assert a.summary['counts']['failed']==2
    assert len(a.findings)==2

def test_missing_baseline_not_invented():
    a=analyze(FIXTURES/'sample-junit.xml')
    assert 'coverage_delta' in a.summary['unavailable_dimensions']
    assert 'duration_trend' in a.summary['unavailable_dimensions']
    assert 'coverage_delta' not in a.dimensions

def test_with_baseline_scoring():
    a=analyze(FIXTURES/'test-results.json',baseline=Baseline(average_duration_ms=100,expected_suites=1,coverage_percent=80,current_coverage_percent=79))
    assert len(a.dimensions)==6
    assert a.dimensions['coverage_delta']==90

def test_clean_report_ships():
    r=Report('junit',[GraderTestCase('ok','passed')], 'mock')
    score,d,missing=calculate(r)
    assert score==100

def test_empty_report_does_not_ship():
    r=Report('junit',[], 'mock')
    from grader.scoring.policy import decision
    assert decision(100,r)=='BLOCK'
