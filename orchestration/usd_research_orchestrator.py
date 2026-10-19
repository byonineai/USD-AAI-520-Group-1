import threading

from orchestration.usd_research_planner import USDResearchPlanner
from orchestration.usd_agent_router import USDAgentRouter

from services.usd_result_aggregator import USDResultAggregator
from services.usd_analysis_evaluator import USDAnalysisEvaluator
from services.usd_analysis_optimizer import USDAnalysisOptimizer
from services.usd_analysis_generator import USDAnalysisGenerator

from orchestration.usd_research_state import (USDResearchState, STATE_MESSAGES)

from domain.usd_research_task import USDResearchTask
from services.usd_final_report_builder import USDFinalReportBuilder

# Integrate memory to the Orchestrator
from domain.usd_research_memory import USDResearchMemory
from memory.usd_memory_repository import USDMemoryRespository

# Tool Registry
from orchestration.usd_tool_registry import USDToolRegistry

from utils.usd_console_status import (
    usd_animate_progress_status
)

class USDResearchOrchestrator:
    """

    Coordinates the autonomous investment research workflow.

    This class is a façade. Instead of manually coordinating everything like
    it was done on the main.ipynb, this orchestrator does the coordination.

    The research planner, provider, router, aggregator, evaluator, and
    optimizer are passed to the constructor and become part of this
    entry point.

    Note: prompt chaining is encapsulated on the news specialist and should not
    be directly implement on this class.

    The complete workflow can be run with:

        orchestrator.run("NVDA")

    This orchestrator will change later and conditional blocks will be
    removed. For now, one command coordinates the entire pipeline.

    This section of the comments has been generated with AI assistance

        Agent Functions
    ---------------
    1. Planning:
       USDResearchPlanner determines which research tasks should execute
       for the requested stock symbol.

    2. Dynamic Tool Use:
       USDToolRegistry resolves each research task to the appropriate
       external data adapter at runtime.

    3. Self-Reflection / Quality Assessment:
       USDAnalysisEvaluator evaluates the generated analysis before the
       result is accepted as complete.

    4. Learning Across Runs:
       USDMemoryRepository retrieves previous research memory and persists
       the latest research results for future runs.

    Workflow Patterns
    -----------------
    1. Prompt Chaining:
       News-specific prompt chaining is delegated to USDNewsAgent and its
       injected USDNewsPipeline. The orchestrator only routes the
       news_analysis task to that specialist.

    2. Routing:
       USDAgentRouter dynamically selects the specialist associated with
       each research task type.

    3. Evaluator-Optimizer:
       If evaluation fails, USDAnalysisOptimizer creates corrective
       actions. The orchestrator performs the requested research,
       regenerates the analysis, and evaluates it again until quality
       passes or max_retries is reached.

    High-Level Workflow
    -------------------
    PLAN
      -> COLLECT
      -> ROUTE / ANALYZE
      -> AGGREGATE
      -> GENERATE
      -> EVALUATE
      -> OPTIMIZE / RETRY if necessary
      -> BUILD FINAL REPORT
      -> SAVE MEMORY
      -> COMPLETE

    1. Planning

    """

    def __init__(
        self,
        planner: USDResearchPlanner,
        tool_registry: USDToolRegistry,
        router: USDAgentRouter,
        aggregator: USDResultAggregator,
        analysis_generator: USDAnalysisGenerator,
        evaluator: USDAnalysisEvaluator,
        optimizer: USDAnalysisOptimizer,
        final_report_builder: USDFinalReportBuilder,
        memory_repository: USDMemoryRespository,
        max_retries: int = 2
    ):
        self.planner = planner
        self.tool_registry = tool_registry
        self.router = router
        self.aggregator = aggregator
        self.analysis_generator = analysis_generator
        self.evaluator = evaluator
        self.optimizer = optimizer
        self.final_report_builder = final_report_builder
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

        self._usd_update_state(
            state,
            state_history
        )

        # Memory Influencing Behavior
        # The planner determines what research should happen
        tasks = self.planner.plan(
            stock_symbol = stock_symbol,
            previous_memory = the_previous_memory
        )

        # --------------------------------------------------
        # Execute planned tasks
        # --------------------------------------------------

        for task in tasks:

            # Collection
            state = USDResearchState.COLLECTING

            if state.value not in state_history:

                self._usd_update_state(
                    state,
                    state_history
                )

            data = self._collect_data(task)

            # Analysis
            state = USDResearchState.ANALYZING

            if state.value not in state_history:
                self._usd_update_state(
                        state,
                        state_history
                    )

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
        self._usd_update_state(
            state,
            state_history
        )

        # Every specialist returns a USDAnalysis result object that is
        # heterogeneous to domain findings to be combined by one commeon
        # result contract
        the_combined_report = self.aggregator.aggregate_results(
            list(results_by_agent.values())
        )

        # Analysis Generation

        state = USDResearchState.GENERATING

        state_history.append(state.value)

        usd_stop_event = threading.Event()

        usd_animation_thread = threading.Thread(
            target=usd_animate_progress_status,
            args = (
                STATE_MESSAGES[state],
                usd_stop_event
            ),
            daemon=True
        )

        usd_animation_thread.start()

        try:

            the_generated_analysis = (
                self.analysis_generator.generate(
                    the_combined_report
                )
            )
        finally:
            usd_stop_event.set()
            usd_animation_thread.join()

        print("Report generation complete.")

        # --------------------------------------------------
        # Evaluation
        # --------------------------------------------------

        state = USDResearchState.EVALUATING

        self._usd_update_state(
            state,
            state_history
        )

        evaluation = self.evaluator.evaluate(
            the_generated_analysis
        )

        the_optimization_actions = []

        # --------------------------------------------------
        # Evaluator -> Optimizer Retry Loop
        # --------------------------------------------------
        # This is the loop bounded by max_retries to prevent indefinite execution
        while not evaluation.passed:

            # Check retry budget and enforce the autonomous retry budget
            if retry_count >= self.max_retries:
                break

            # --------------------------------------------------
            # Optimizing
            # --------------------------------------------------

            state = USDResearchState.OPTIMIZING

            self._usd_update_state(
                state,
                state_history
            )

            # Convert the evaluator feedback into an executable corrective action
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

                    self._usd_update_state(
                                state,
                                state_history
                            )

                    data = self._collect_data(
                        retry_task
                    )

                    # ------------------------------------------
                    # Analyzing again
                    # ------------------------------------------

                    state = USDResearchState.ANALYZING

                    self._usd_update_state(
                            state,
                            state_history
                        )
                    # Let's route the task to the specialist registered for the appropriate task type.
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

            self._usd_update_state(
                state,
                state_history
            )

            the_combined_report = self.aggregator.aggregate_results(
                list(results_by_agent.values())
            )

            # --------------------------------------------------
            # Evaluate again
            # --------------------------------------------------

            # state = USDResearchState.EVALUATING
            # state_history.append(state.value)

            # evaluation = self.evaluator.evaluate(
            #     the_combined_report
            # )

            # Generate the analysis again

            state = USDResearchState.GENERATING

            state_history.append(
                state.value
            )

            # This is necessary becaue if the optimizer obtains newer research
            # the synthesis needs to be regenerated; otherwise, a stale synthesis
            # will be created.
            # Regenerate the synthesis so the evaluator does not assess a stale analysis
            # created from a previous evidence
            the_generated_analysis = self.analysis_generator.generate(
                the_combined_report
            )

            # Evaluate again

            state = USDResearchState.EVALUATING
            self._usd_update_state(
                state,
                state_history
            )
            # Do no automatically accept the generated analysis.
            evaluation = self.evaluator.evaluate(
                the_generated_analysis
            )

        unresolved_gaps = []

        if not evaluation.passed:
            unresolved_gaps = evaluation.issues

        # FINAL REPORT INCLUSION

        final_report = self.final_report_builder.build(
            stock_symbol=stock_symbol,
            status = USDResearchState.COMPLETE.value,
            generated_analysis = the_generated_analysis,
            evaluation = evaluation,
            retry_count = retry_count,
            unresolved_gaps = unresolved_gaps
        )

        current_memory_storage = self._build_the_memory(
            stock_symbol = stock_symbol,
            the_combined_report = the_combined_report,
            evaluation= evaluation
        )

        self.memory_repository.save(
            current_memory_storage
        )

        # Completion

        state = USDResearchState.COMPLETE

        self._usd_update_state(
            state,
            state_history
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
            "generated_analysis": the_generated_analysis,
            "final_report": final_report
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
            unresolved_gaps = evaluation.issues

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
        """
        Dynamically resolve and execute the data tool required by a task.
        The task type is solely a lookup key
        """

        # Agent function dynamic tool use
        tool = self.tool_registry.get(
            task.task_type
        )

        return tool.fetch(
            task.stock_symbol
        )

    def _usd_update_state(
        self,
        state: USDResearchState,
        state_history: list[str]
    ):
        state_history.append(
            state.value
        )

        print(
            STATE_MESSAGES[state],
            flush=True
        )
