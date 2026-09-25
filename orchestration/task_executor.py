from domain.research_task import ResearchTask, ResearchTaskType
from orchestration.tool_registry import ToolRegistry
# The task executor executes the task

class TaskExecutor:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, task: ResearchTask):
        provider = self.registry.get_provider(task.task_type)

        if task.task_type == ResearchTaskType.MARKET:
            return provider.get_market_data(task.symbol)

        raise ValueError(
            f"Unsupported task type: {task.task_type.value}"
        )