class GraderError(Exception):
    """Base application exception."""

class DetectionError(GraderError):
    """Report type cannot be determined."""

class ParseError(GraderError):
    """Report input is malformed or unsupported."""

class OllamaError(GraderError):
    """Local AI invocation failed."""

class AtomicIngestionNotImplemented(GraderError):
    """Advanced safe ingestion challenge has not been implemented."""
