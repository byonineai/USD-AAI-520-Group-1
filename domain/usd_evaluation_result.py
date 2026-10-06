from dataclasses import (dataclass,field)

@dataclass
class USDEvaluationResult:

    passed: bool
    issues: list[str]
    quality_summary: str = ""
    details: list[dict] = field(
        default_factory=list
    )