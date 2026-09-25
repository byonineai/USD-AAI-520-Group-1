from domain.research_task import ResearchTask, ResearchTaskType
# What research do I need?
class ResearchPlanner:
  def plan(self, symbol: str) -> list[ResearchTask]:
    symbol = symbol.strip().upper()

    if not symbol:
      raise ValueError("The provided stock symbol cannot be empty.")

    return [
        ResearchTask(
            task_type=ResearchTaskType.MARKET,
            symbol=symbol,
        ),
        ResearchTask(
            task_type=ResearchTaskType.NEWS,
            symbol=symbol,
        ),
        ResearchTask(
            task_type=ResearchTaskType.EARNINGS,
            symbol=symbol,
        ),
        ResearchTask(
            task_type=ResearchTaskType.MACRO,
            symbol=symbol,
        ),
]
