from domain.research_result import ResearchResult
from domain.research_task import ResearchTask, ResearchTaskType
from orchestration.tool_registry import ToolRegistry

class TaskExecutor:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, task: ResearchTask) -> ResearchResult:
        provider = self.registry.get_provider(task.task_type)

        if task.task_type == ResearchTaskType.MARKET:
            data = provider.get_market_data(task.symbol)

            return ResearchResult(
                task_type=task.task_type,
                symbol=task.symbol,
                data=data,
            )

        raise ValueError(
            f"Unsupported task type: {task.task_type.value}"
        )