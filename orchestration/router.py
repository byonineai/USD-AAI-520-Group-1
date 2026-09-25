from typing import Any

from domain.research_task import ResearchTaskType

class DataRouter:

    def __init__(self):
        self._analyzers: dict[ResearchTaskType, Any] = {}

    def register(
        self,
        task_type: ResearchTaskType,
        analyzer: Any,
    ) -> None:
        self._analyzers[task_type] = analyzer

    def get_analyzer(
        self,
        task_type: ResearchTaskType,
    ) -> Any:
        if task_type not in self._analyzers:
            raise ValueError(
                f"No analyzer registered for task type: {task_type.value}"
            )

        return self._analyzers[task_type]