from grader.scoring.policy import decision

def description(signal: str) -> str:
    return {"SHIP":"Quality gate passed", "REVIEW":"Review failures or quality trends before shipping", "BLOCK":"Release gate failed"}[signal]
