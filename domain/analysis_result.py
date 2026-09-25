from dataclasses import dataclass
from typing import Any

from domain.research_task import ResearchTaskType

@dataclass
class AnalysisResult:
    task_type: ResearchTaskType
    symbol: str
    summary: str
    data: dict[str, Any]