from pathlib import Path
from grader.cli import main

FIXTURES=Path(__file__).parent/'fixtures'

def test_cli_text(capsys):
    assert main(['--report',str(FIXTURES/'sample-junit.xml')])==0
    output=capsys.readouterr().out
    assert 'Score:' in output and 'Insight:' in output

def test_cli_ci_gate():
    assert main(['--report',str(FIXTURES/'sample-junit.xml'),'--ci','--threshold','85'])==1

def test_cli_json(capsys):
    assert main(['--report',str(FIXTURES/'test-results.json'),'--output','json'])==0
    import json
    d=json.loads(capsys.readouterr().out)
    assert d['format']=='playwright'
    assert d['summary']['total']==3

def test_history_records(tmp_path,capsys):
    db=tmp_path/'history.db'
    assert main(['--report',str(FIXTURES/'sample-junit.xml'),'--record','--db',str(db)])==0
    capsys.readouterr()
    assert main(['--history','--db',str(db)])==0
    assert 'junit' in capsys.readouterr().out
