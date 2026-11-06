from grader.models import Report
from grader.scoring.weights import WEIGHTS
from grader.scoring.dimensions import dimension_scores
from grader.scoring.baseline import Baseline

def calculate(report: Report, baseline: Baseline | None = None) -> tuple[float, dict[str,float],list[str]]:
    dimensions = dimension_scores(report,baseline)
    available = {k:v for k,v in dimensions.items() if v is not None}
    weight_sum = sum(WEIGHTS[k] for k in available)
    score = sum(WEIGHTS[k]*v for k,v in available.items())/weight_sum if weight_sum else 0.0
    unavailable = [k for k,v in dimensions.items() if v is None]
    return round(score,2),available,unavailable
