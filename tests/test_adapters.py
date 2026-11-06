from pathlib import Path
import pytest
from grader.discovery import discover
from grader.errors import DetectionError,ParseError

FIXTURES=Path(__file__).parent/'fixtures'

@pytest.mark.parametrize('file,format,total',[
 ('sample-junit.xml','junit',6),
 ('test-results.json','playwright',3),
 ('jest-results.json','jest',2),
 ('summary.json','k6',4),
 ('allure-results','allure',2),
])
def test_auto_detect_and_parse(file,format,total):
    adapter,path=discover(FIXTURES/file)
    report=adapter.parse(path)
    assert report.format==format
    assert len(report.tests)==total
    assert all(t.name and t.suite for t in report.tests)

def test_playwright_flaky_case():
    adapter,path=discover(FIXTURES/'test-results.json')
    report=adapter.parse(path)
    flaky=[t for t in report.tests if t.flaky]
    assert len(flaky)==1
    assert flaky[0].status=='passed'
    assert flaky[0].retries==1

def test_junit_failure_messages():
    adapter,path=discover(FIXTURES/'sample-junit.xml')
    report=adapter.parse(path)
    assert 'locator' in next(t.message for t in report.tests if t.name=='pay by card')
    assert report.counts()['skipped']==1

def test_bad_path_rejected():
    with pytest.raises(ParseError): discover(FIXTURES/'missing.json')

def test_unsupported_file_rejected(tmp_path):
    f=tmp_path/'report.txt';f.write_text('abc')
    with pytest.raises(DetectionError): discover(f)
