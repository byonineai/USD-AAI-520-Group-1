from orchestration.usd_research_state import USDResearchState
from orchestration.usd_research_planner import USDResearchPlanner
from orchestration.usd_agent_router import USDAgentRouter

from services.usd_aggregator import USDResultAggregator
from services.usd_analysis_evaluator import USDAnalysisEvaluator
from services.usd_optimizer import USDAnalysisOptimizer

from domain.usd_market_data_provider import USDMarketDataProvider
from domain.usd_research_task import USDResearchTask

# Integrate memory to the Orchestrator
from domain.usd_research_memory import USDResearchMemory
from memory.usd_memory_repository import USDMemoryRespository

# Tool Registry
from orchestration.usd_tool_registry import USDToolRegistry

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
        tool_registry: USDToolRegistry,
        # provider: USDMarketDataProvider,
        router: USDAgentRouter,
        aggregator: USDResultAggregator,
        evaluator: USDAnalysisEvaluator,
        optimizer: USDAnalysisOptimizer,
        memory_repository: USDMemoryRespository,
        max_retries: int = 2
    ):
        self.planner = planner
        self.tool_registry = tool_registry
        # self.provider = provider
        self.router = router
        self.aggregator = aggregator
        self.evaluator = evaluator
        self.optimizer = optimizer
        self.memory_repository = memory_repository
        self.max_retries = max_retries

    def run(self, stock_symbol: str) -> dict:

        results = []
        state_history = []
        retry_count = 0

        # Store the newest result from each specialist.
        # This prevents retries from falsely increasing
        # the specialist count.
        results_by_agent = {}

        # Now the system can determine wether it has seen a stock symbol before or not
        the_previous_memory = self.memory_repository.get(
            stock_symbol
        )

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

        current_memory_storage = self._build_the_memory(
            stock_symbol = stock_symbol,
            the_combined_report = the_combined_report,
            evaluation= evaluation
        )

        self.memory_repository.save(
            current_memory_storage
        )

        return {
            "stock_symbol": stock_symbol,
            "status": state.value,
            "state_history": state_history,
            "combined_report": the_combined_report,
            "the_optimization_actions": the_optimization_actions,
            "final_evaluation": evaluation,
            "retry_count": retry_count,
            "max_retries": self.max_retries,
            "curremt_memory_storage": current_memory_storage,
            "the_previous_memory": the_previous_memory,
            "unresolved_gaps": unresolved_gaps,
        }

    def _build_the_memory(
        self,
        stock_symbol: str,
        the_combined_report: dict,
        evaluation
    ) -> USDResearchMemory:

        evidence = {}
        summaries = {}

        for result in the_combined_report["results"]:

            summaries[result.agent] = result.summary

            evidence[result.agent] = result.evidence

        unresolved_gaps = []

        if not evaluation.passed:
            unresolved_gaps = evaluation.problems

        return USDResearchMemory(
            stock_symbol=stock_symbol,
            quality_status=(
                "passed"
                if evaluation.passed
                else "unresolved_gaps"
            ),
            summaries=summaries,
            evidence=evidence,
            unresolved_gaps=unresolved_gaps
        )



    def _collect_data(
      self,
      task: USDResearchTask
    ):
        tool = self.tool_registry.get(
            task.task_type
        )

        return tool.fetch(
            task.stock_symbol
        )

    # Removed tight coupling

    #   if task.task_type == "market_analysis":

    #     return self.provider.get_market_data(
    #       task.stock_symbol
    #     )

    #   raise ValueError(
    #     f"This is an unsupported task type: {task.task_type}"
    #   )