from orchestration.usd_research_state import USDResearchState
from orchestration.usd_research_planner import USDResearchPlanner
from orchestration.usd_agent_router import USDAgentRouter

from services.usd_aggregator import USDResultAggregator
from services.usd_analysis_evaluator import USDAnalysisEvaluator
from services.usd_optimizer import USDAnalysisOptimizer

from domain.usd_market_data_provider import USDMarketDataProvider
from domain.usd_research_task import USDResearchTask


class USDResearchOrchestrator:
    """
    This class is a façade. Instead of manually coordinating everything like
    it was done on the main.ipynb, this orchestrator does the coordination.

    The research planner, provider, router, aggregator, evaluator, and
    optimizer are passed to the constructor and become part of this
    entry point.

    The complete workflow can be run with:

        orchestrator.run("NVDA")

    This orchestrator will change later and conditional blocks will be
    removed. For now, one command coordinates the entire pipeline.
    """

    def __init__(
        self,
        planner: USDResearchPlanner,
        provider: USDMarketDataProvider,
        router: USDAgentRouter,
        aggregator: USDResultAggregator,
        evaluator: USDAnalysisEvaluator,
        optimizer: USDAnalysisOptimizer,
        max_retries: int = 2
    ):
        self.planner = planner
        self.provider = provider
        self.router = router
        self.aggregator = aggregator
        self.evaluator = evaluator
        self.optimizer = optimizer
        self.max_retries = max_retries

    def run(self, stock_symbol: str) -> dict:

        results = []
        state_history = []
        retry_count = 0

        # Store the newest result from each specialist.
        # This prevents retries from falsely increasing
        # the specialist count.
        results_by_agent = {}

        # --------------------------------------------------
        # Planning
        # --------------------------------------------------

        state = USDResearchState.PLANNING
        state_history.append(state.value)

        tasks = self.planner.plan(stock_symbol)

        # --------------------------------------------------
        # Execute planned tasks
        # --------------------------------------------------

        for task in tasks:

            # Collection
            state = USDResearchState.COLLECTING

            if state.value not in state_history:
                state_history.append(state.value)

            data = self._collect_data(task)

            # Analysis
            state = USDResearchState.ANALYZING

            if state.value not in state_history:
                state_history.append(state.value)

            agent = self.router.route(
                task.task_type
            )

            result = agent.analyze(
                data
            )

            results.append(result)

            # Keep latest result for each specialist
            results_by_agent[result.agent] = result

        # --------------------------------------------------
        # Aggregation
        # --------------------------------------------------

        state = USDResearchState.AGGREGATING
        state_history.append(state.value)

        the_combined_report = self.aggregator.aggregate_results(
            list(results_by_agent.values())
        )

        # --------------------------------------------------
        # Evaluation
        # --------------------------------------------------

        state = USDResearchState.EVALUATING
        state_history.append(state.value)

        evaluation = self.evaluator.evaluate(
            the_combined_report
        )

        the_optimization_actions = []

        # --------------------------------------------------
        # Evaluator -> Optimizer Retry Loop
        # --------------------------------------------------

        while not evaluation.passed:

            # Check retry budget
            if retry_count >= self.max_retries:
                break

            # --------------------------------------------------
            # Optimizing
            # --------------------------------------------------

            state = USDResearchState.OPTIMIZING
            state_history.append(state.value)

            the_optimization_actions = self.optimizer.optimize(
                evaluation
            )

            # Try to perform corrective actions
            executed_action = False

            for action in the_optimization_actions:

                if (
                    action.action == "request_more_research"
                    and action.task_type is not None
                ):

                    retry_task = USDResearchTask(
                        task_type=action.task_type,
                        stock_symbol=stock_symbol
                    )

                    # ------------------------------------------
                    # Collecting again
                    # ------------------------------------------

                    state = USDResearchState.COLLECTING
                    state_history.append(state.value)

                    data = self._collect_data(
                        retry_task
                    )

                    # ------------------------------------------
                    # Analyzing again
                    # ------------------------------------------

                    state = USDResearchState.ANALYZING
                    state_history.append(state.value)

                    agent = self.router.route(
                        retry_task.task_type
                    )

                    result = agent.analyze(
                        data
                    )

                    # Replace previous result from this specialist
                    results_by_agent[result.agent] = result

                    executed_action = True

                elif action.action == "revise_analysis":

                    # Placeholder since the analysis generator
                    # has not been built yet.
                    continue

            # If no optimizer action can be executed,
            # stop instead of looping unnecessarily.
            if not executed_action:
                break

            retry_count += 1

            # --------------------------------------------------
            # Aggregate again
            # --------------------------------------------------

            state = USDResearchState.AGGREGATING
            state_history.append(state.value)

            the_combined_report = self.aggregator.aggregate_results(
                list(results_by_agent.values())
            )

            # --------------------------------------------------
            # Evaluate again
            # --------------------------------------------------

            state = USDResearchState.EVALUATING
            state_history.append(state.value)

            evaluation = self.evaluator.evaluate(
                the_combined_report
            )

        # --------------------------------------------------
        # Completion
        # --------------------------------------------------

        state = USDResearchState.COMPLETE
        state_history.append(state.value)

        unresolved_gaps = []

        if not evaluation.passed:
            unresolved_gaps = evaluation.problems

        return {
            "stock_symbol": stock_symbol,
            "status": state.value,
            "state_history": state_history,
            "combined_report": the_combined_report,
            "the_optimization_actions": the_optimization_actions,
            "final_evaluation": evaluation,
            "retry_count": retry_count,
            "max_retries": self.max_retries,
            "unresolved_gaps": unresolved_gaps
        }
    def _collect_data(
      self,
      task: USDResearchTask
    ):

      if task.task_type == "market_analysis":

        return self.provider.get_market_data(
          task.stock_symbol
        )

      raise ValueError(
        f"This is an unsupported task type: {task.task_type}"
      )

# from orchestration.usd_research_state import USDResearchState
# from orchestration.usd_research_planner import USDResearchPlanner
# from orchestration.usd_agent_router import USDAgentRouter
# from tools.usd_yahoo_finance_adapter import USDYahooFinanceAdapter
# from services.usd_aggregator import USDResultAggregator
# from domain.usd_market_data_provider import USDMarketDataProvider
# # Add Evaluator to Orchestrator
# from services.usd_analysis_evaluator import USDAnalysisEvaluator
# from services.usd_optimizer import USDAnalysisOptimizer
# from domain.usd_research_task import USDResearchTask

# class USDResearchOrchestrator:
#   """
#   This class is a façade. Instead of manually coordinating everything like
#   it was done on the main.ipynb. This orchestrator does the coordination.
#   The research planner, provider, router and aggregator are passed to the
#   constructor and they are part of this entry point.

#   Look at the examples provided on the main.ipynb. It is manually doing what
#   this orchestrator is intended to do.

#   #Now you can run the entire workflow simply with

#   orchestrator.run("NVDA")

#   THIS ORCHESTRATOR WILL CHANGE LATER AND CONDITIONAL BLOCKS WILL BE REMOVED.
#   WE ONLY HAVE ONE DATA SOURCE SO IT'S OK. FOR now One command coordinates
#   the entire pipeline.

#   """

#   def __init__(
#     self,
#     planner: USDResearchPlanner,
#     # provider: USDYahooFinanceAdapter,
#     provider: USDMarketDataProvider,
#     router: USDAgentRouter,
#     aggregator: USDResultAggregator,
#     evaluator: USDAnalysisEvaluator,
#     optimizer: USDAnalysisOptimizer,
#     max_retries: int = 2
#   ):
#     self.planner = planner
#     self.provider = provider
#     self.router = router
#     self.aggregator = aggregator
#     self.evaluator = evaluator
#     self.optimizer = optimizer
#     self.max_retries = max_retries

#   def run(self, stock_symbol: str) -> dict:

#     results = []
#     state_history = []
#     retry_count = 0

#     # Store the newest result from each specialist
#     # preventing a retry from falsely increasing the
#     # specialist count
#     results_by_agent = {}

#     # This is the planning stage

#     state = USDResearchState.PLANNING
#     state_history.append(state.value)
#     # Collection stage

#     state = USDResearchState.COLLECTING
#     state_history.append(state.value)

#     tasks = self.planner.plan(stock_symbol)

#     # task types
#     for task in tasks:

#       state = USDResearchState.COLLECTING
#       state_history.append(state.value)

#       data = self._collect_data(task)

#     # Analyzing

#       state = USDResearchState.ANALYZING

#       if state.value not in state_history:
#         state_history.append(state.value)

#       agent = self.router.route(
#         task.task_type
#       )

#       result = agent.analyze(data)

#       results.append(result)

#     # Aggregation

#     state = USDResearchState.AGGREGATING
#     state_history.append(state.value)

#     the_combined_report = self.aggregator.aggregate_results(
#       results
#     )

#     # Evaluation state

#     state = USDResearchState.EVALUATING
#     state_history.append(state.value)

#     evaluation = self.evaluator.evaluate(
#       the_combined_report
#     )

#     the_optimization_actions = []

#     # Retry Loop

#     while not evaluation.passed:

#       # check the retry budget

#       if retry_count >= self.max_retries:
#         break

#     # Optimizing

#       state = USDResearchState.OPTIMIZING
#       state.history.append(
#         state.value
#       )

#       the_optimization_actions = self.optimizer.optimize(
#         evaluation
#       )

#       # Try to perform corrective actions

#       executed_action = False

#       for action in the_optimization_actions:

#           if (action.action == "request_more_research" and action.task_type is not None):

#               retry_task = USDResearchTask(
#                 task_type = action.task_type,
#                 stock_symbol = stock_symbol
#               )

#               # Collecting again

#               state = USDResearchState.COLLECTING
#               state_history.append(state.value)

#               data = self._collect_data(
#                 retry_task
#               )

#               # Analyzing again
#               state = USDResearchState.ANALYZING
#               state_history.append(state.value)

#               agent = self.router.route(
#                 retry_task.task_type
#               )

#               result = agent.analyze(
#                 data
#               )

#               # Swap previous result from this specialist

#               results_by_agent[result.agent] = result

#               executed_action = True

#           elif action.action == "revise_analysis":
#             # placeholder since the analysis generator has not been built
#             continue

#     # If no optimizer action can be executed, stop instead of looping without a need.
#       if not executed_action:
#        break

#       retry_count +-1

#       # Aggregate again

#       state = USDResearchState.AGGREGATING
#       state_history.append(state.value)

#       the_combined_report = self.aggregator.aggregate(
#         list(results_by_agent.values())
#       )

#       # Evaluate again

#       state = USDResearchState.EVALUATING
#       state_history.append(state.value)

#       evaluation = self.evaluator.evaluate(
#         the_combined_report
#       )

#     # Completion

#     state = USDResearchState.COMPLETE
#     state_history.append(state.value)

#     unresolved_gaps = []

#     if not evaluation.passed:
#       unresolved_gaps = evaluation.problems

#     return{
#       "stock_symbol": stock_symbol,
#       "status": state.value,
#       "state_history": state_history,
#       "combined_report": the_combined_report,
#       "the_optimization_actions": the_optimization_actions,
#       "final_evaluation": evaluation
#     }