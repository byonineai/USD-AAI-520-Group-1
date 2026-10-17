from domain.usd_research_task import USDResearchTask
from domain.usd_research_memory import USDResearchMemory
# @author: Marcelo Salvador
# Later Gemini will dynamically generate this plan
# Architecture will be validated prior LLM implementation

class USDResearchPlanner:

  def plan(self, stock_symbol: str, previous_memory: USDResearchMemory | None = None) -> list[USDResearchTask]:

    tasks =  [
      USDResearchTask(
        task_type="market_analysis",
        stock_symbol = stock_symbol
      ),
      USDResearchTask(
        task_type="macro_analysis",
        stock_symbol=stock_symbol
      ),
      USDResearchTask(
        task_type="earnings_analysis",
        stock_symbol=stock_symbol
      ),
        USDResearchTask(
            task_type="news_analysis",
            stock_symbol=stock_symbol
      ),
  ]
    # No previous run existent
    if previous_memory is None:
        return tasks

    # If the previous run passed without unresolved gaps
    # kjeep the normal plan

    if(
      previous_memory.quality_status == "passed"
      and not previous_memory.unresolved_gaps
    ):
      return tasks

    all_priority_tasks = []
    all_normal_tasks = []

    for task in tasks:
      if self._all_tasks_matches_previous_gap(
        task.task_type,
        previous_memory.unresolved_gaps
      ):
        all_priority_tasks.append(task)
      else:
        all_normal_tasks.append(task)
    return all_priority_tasks + all_normal_tasks

  def _all_tasks_matches_previous_gap(
    self,
    task_type: str,
    all_unresolved_gaps: list[str]
  ):
     mapping = {
            "market_analysis": [
                "market",
                "price",
                "volume"
            ],

            "macro_analysis": [
                "macro",
                "fred",
                "interest",
                "inflation",
                "unemployment",
                "treasury"
            ],

            "earnings_analysis": [
                "earnings",
                "filing",
                "10-k",
                "10-q",
                "sec"
            ],

         "news_analysis": [
             "news",
             "article",
             "headline",
             "press",
             "media",
         ],

        }

     keywords = mapping.get(
       task_type,
       []
     )

     for gap in all_unresolved_gaps:

         normalize_the_gap = gap.lower()

         for keyword in keywords:

             if keyword in normalize_the_gap:
                 return True

     return False
