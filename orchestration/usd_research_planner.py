from domain.usd_research_task import USDResearchTask
# @author: Marcelo Salvador
# Later Gemini will dynamically generate this plan
# Architecture will be validated prior LLM implementation

class USDResearchPlanner:

  def plan(self, stock_symbol: str):

    return [
      USDResearchTask(
        task_type="news_analysis",
        stock_symbol = stock_symbol
    ),
      USDResearchTask(
        task_type="market_analysis",
        stock_symbol = stock_symbol
      ),
  ]