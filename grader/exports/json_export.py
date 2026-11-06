import json
from grader.models import Assessment

def as_json(result:Assessment) -> str:
    return json.dumps(result.to_dict(),indent=2,ensure_ascii=False)
