from typing import Any

from domain.research_task import ResearchTaskType

# The key responsibility of this class is
# given a research task type, which provider
# should handle it

from typing import Any

from domain.research_task import ResearchTaskType

class ToolRegistry:

    def __init__(self):
        self._providers: dict[ResearchTaskType, Any] = {}

    def register(
        self,
        task_type: ResearchTaskType,
        provider: Any,
    ) -> None:
        self._providers[task_type] = provider

    def get_provider(
        self,
        task_type: ResearchTaskType,
    ) -> Any:
        if task_type not in self._providers:
            raise ValueError(
                f"There is no provider registered for task type: {task_type.value}"
            )

        return self._providers[task_type]
