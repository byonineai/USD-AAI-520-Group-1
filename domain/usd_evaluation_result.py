from dataclasses import (dataclass,field)
# Data contracts between specialist agents and adapters.

@dataclass
class USDEvaluationResult:

    passed: bool
    issues: list[str]
    quality_summary: str = ""
    details: list[dict] = field(
        default_factory=list
    )