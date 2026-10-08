from tools.usd_research_tool import USDResearchTool

class USDToolRegistry:
  def __init__(self):
    self._tools: dict[str, USDResearchTool] = {}

  def register(
      self,
      task_type: str,
      tool: USDResearchTool
    ) -> None:

      self._tools[task_type] = tool

  def get(
      self,
      task_type: str
    )-> USDResearchTool:
      if task_type not in self._tools:
        raise KeyError(
          f" There is no tool registered for task type: {task_type}"
          )
      return self._tools[task_type]