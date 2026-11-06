from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    model: str = "llama3"
    ollama_url: str = "http://127.0.0.1:11434"
    timeout_seconds: float = 8.0
    db_path: str = ".grader/grader.sqlite3"
    threshold: float = 80.0

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("GRADER_MODEL", "llama3"),
            ollama_url=os.getenv("GRADER_OLLAMA_URL", "http://127.0.0.1:11434"),
            timeout_seconds=float(os.getenv("GRADER_AI_TIMEOUT", "8")),
            db_path=os.getenv("GRADER_DB_PATH", ".grader/grader.sqlite3"),
            threshold=float(os.getenv("GRADER_THRESHOLD", "80")),
        )
