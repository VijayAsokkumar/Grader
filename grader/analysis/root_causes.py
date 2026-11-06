import re

PATTERNS = [
    ("locator",r"locator|selector|element not found|strict mode violation|no such element"),
    ("authentication",r"auth|login|token|unauthorized|forbidden|401|403"),
    ("timeout",r"timed?\s*out|timeout|deadline exceeded"),
    ("assertion",r"assert|expected .* received|comparison failure"),
    ("network",r"connection refused|connection reset|dns|socket|502|503|504"),
]

def cause(message: str) -> str:
    for category, pattern in PATTERNS:
        if re.search(pattern,message,re.I): return category
    return "other"
