import re

RULES = [
    (r"(?i)(authorization:\s*bearer\s+)[^\s]+", r"\1[REDACTED]"),
    (r"(?i)(api[_-]?key|password|secret|token)\s*[=:]\s*[^\s,;]+", r"\1=[REDACTED]"),
    (r"https?://[^\s/@]+:[^\s/@]+@", "https://[REDACTED]@"),
]

def redact(text: str) -> str:
    for pattern,replacement in RULES:
        text = re.sub(pattern,replacement,text)
    return text
