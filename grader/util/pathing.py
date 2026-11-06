from pathlib import Path
from grader.errors import ParseError

def resolve_source(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise ParseError(f"Report does not exist: {path}")
    if not path.is_file() and not path.is_dir():
        raise ParseError(f"Not a file or directory: {path}")
    return path

def json_files(path: Path):
    return sorted(path.glob("*.json")) if path.is_dir() else [path]
