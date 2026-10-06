from agents.usd_analysis_strategy import USDAnalysisStrategy
# @Author: Marcelo Salvador
# What agents are available?
# A controlled lookup table

class USDAgentRegistry:
  def __init__(self):
    self._agents: dict[str, USDAnalysisStrategy] = {}

    # key->market_analysis and maps to value MarketAgent instance
    # Later it can be asked registry.get("market_analysis") and receive Market Agent
  def register(
    self,
    agent: USDAnalysisStrategy,
    task_type: str
  ) -> None:
    self._agents[task_type] = agent

  def get(self, task_type: str) -> USDAnalysisStrategy:
    if task_type not in self._agents:
      raise KeyError(
        f"There is no agent registered for task type: {task_type}"
      )
    return self._agents[task_type]
