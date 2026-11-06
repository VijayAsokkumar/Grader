from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from grader.models import Report

class Adapter(ABC):
    format_name: str

    @classmethod
    @abstractmethod
    def matches(cls, path: Path) -> bool: ...

    @classmethod
    @abstractmethod
    def parse(cls, path: Path) -> Report: ...
