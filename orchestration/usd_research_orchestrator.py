from orchestration.usd_research_state import USDResearchState
from orchestration.usd_research_planner import USDResearchPlanner
from orchestration.usd_agent_router import USDAgentRouter
from tools.usd_yahoo_finance_adapter import USDYahooFinanceAdapter
from services.usd_aggregator import USDResultAggregator
from domain.usd_market_data_provider import USDMarketDataProvider

class USDResearchOrchestrator:
  """
  This class is a façade. Instead of manually coordinating everything like
  it was done on the main.ipynb. This orchestrator does the coordination.
  The research planner, provider, router and aggregator are passed to the
  constructor and they are part of this entry point.

  Look at the examples provided on the main.ipynb. It is manually doing what
  this orchestrator is intended to do.

  #Now you can run the entire workflow simply with

  orchestrator.run("NVDA")

  THIS ORCHESTRATOR WILL CHANGE LATER AND CONDITIONAL BLOCKS WILL BE REMOVED.
  WE ONLY HAVE ONE DATA SOURCE SO IT'S OK. FOR now One command coordinates
  the entire pipeline.

  """

  def __init__(
    self,
    planner: USDResearchPlanner,
    # provider: USDYahooFinanceAdapter,
    provider: USDMarketDataProvider,
    router: USDAgentRouter,
    aggregator: USDResultAggregator
  ):
    self.planner = planner
    self.provider = provider
    self.router = router
    self.aggregator = aggregator

  def run(self, stock_symbol: str) -> dict:

    results = []
    state_history = []

    # This is the planning stage

    state = USDResearchState.PLANNING
    state_history.append(state.value)

    tasks = self.planner.plan(stock_symbol)

    # Collection stage

    state = USDResearchState.COLLECTING
    state_history.append(state.value)

    # task types
    for task in tasks:

      # For now we only support market_analysis
      # and the team will be adding the missing
      if task.task_type == "market_analysis":
        data = self.provider.get_market_data(
          task.stock_symbol
        )
      else:
        raise ValueError(
          f"The task type is not supported: "
          f"{task.task_type}"
        )
    # Analyzing

      state = USDResearchState.ANALYZING

      if state.value not in state_history:
        state_history.append(state.value)

      agent = self.router.route(
        task.task_type
      )

      result = agent.analyze(data)

      results.append(result)

    # Aggregation

    state = USDResearchState.AGGREGATING
    state_history.append(state.value)

    the_combined_report = self.aggregator.aggregate_results(
      results
    )

    # Completion

    state = USDResearchState.COMPLETE
    state_history.append(state.value)

    return{
      "stock_symbol": stock_symbol,
      "status": state.value,
      "state_history": state_history,
      "combined_report": the_combined_report
    }