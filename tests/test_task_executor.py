from domain.research_task import ResearchTask, ResearchTaskType
from orchestration.task_executor import TaskExecutor
from orchestration.tool_registry import ToolRegistry
import pytest

class FakeMarketProvider:

    def get_market_data(self, symbol: str):
        return {
            "symbol": symbol,
            "price": 100.00,
        }

def test_executor_executes_market_task():
    registry = ToolRegistry()

    registry.register(
        ResearchTaskType.MARKET,
        FakeMarketProvider(),
    )

    executor = TaskExecutor(registry)

    task = ResearchTask(
        task_type=ResearchTaskType.MARKET,
        symbol="NVDA",
    )

    result = executor.execute(task)

    assert result["symbol"] == "NVDA"
    assert result["price"] == 100.00

# Failure Tests
# def test_executor_rejects_unregistered_task():
#     registry = ToolRegistry()

#     executor = TaskExecutor(registry)

#     task = ResearchTask(
#         task_type=ResearchTaskType.NEWS,
#         symbol="NVDA",
#     )

#     with pytest.raises(
#         ValueError,
#         match="No provider registered"
#     ):
#         executor.execute(task)