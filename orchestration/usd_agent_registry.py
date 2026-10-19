from agents.usd_analysis_strategy import USDAnalysisStrategy
# @Author: Marcelo Salvador
# What agents are available?
# A controlled lookup table

class USDAgentRegistry:
  '''
  The role of this class is to store specialist agents by task type.
  The intended flow is:
  Research Task->USDAgentRouter->USDAgentRegistry->Correct Specialist Agent
  '''
  def __init__(self):
    self._agents: dict[str, USDAnalysisStrategy] = {}

    # key->market_analysis and maps to value MarketAgent instance
    # Later it can be asked registry.get("market_analysis") and receive Market Agent
  def register(
    self,
    task_type: str,
    agent: USDAnalysisStrategy,
  ) -> None:
    self._agents[task_type] = agent

  def get(self, task_type: str) -> USDAnalysisStrategy:
    if task_type not in self._agents:
      raise KeyError(
        f"There is no agent registered for task type: {task_type}"
      )
    return self._agents[task_type]
