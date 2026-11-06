from pathlib import Path
from grader.registry import detect
from grader.util.pathing import resolve_source

def discover(path: str | Path, format: str | None = None):
    source = resolve_source(path)
    return detect(source,format),source
