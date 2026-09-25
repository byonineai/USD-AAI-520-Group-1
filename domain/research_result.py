from dataclasses import dataclass
from typing import Any
# This class will give downstream components context
# about what kind of result they received
# Common result contract
from domain.research_task import ResearchTaskType

@dataclass
class ResearchResult:
    task_type: ResearchTaskType
    symbol: str
    data: dict[str, Any]