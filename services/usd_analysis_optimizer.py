from domain.usd_evaluation_result import USDEvaluationResult
from domain.usd_optimization_action import USDOptimizationAction

class USDAnalysisOptimizer:
  def optimize(
    self,
    evaluation: USDEvaluationResult
  )-> list[USDOptimizationAction]:

    desired_actions = []

    if evaluation.passed:
      return desired_actions

    for issue in evaluation.issues:

      # Missing evidence
      if issue.startswith("missing_evidence"):

        agent_name = issue.split(":")[1]

        task_type = self._task_type_for_the_agent(
          agent_name
        )

        desired_actions.append(
          USDOptimizationAction(
            action="request_more_research",
            reason=(
              f"{agent_name} analysis."
              f"it is missing the evidence."
            ),
            task_type = task_type
          )
        )

        # Missing summary
      elif issue.startswith("missing_summary:"):
        agent_name = issue.split(":")[1]

        desired_actions.append(
          USDOptimizationAction(
            action="revise_analysis",
            reason=(
              f"{agent_name} analysis"
              f"is missing a summary"
            )
          )
        )
      elif issue == "missing_analysis":

        desired_actions.append(
          USDOptimizationAction(
            action="request_more_research",
            reason=(
              "There is not specialist analysis produced!"
            )
          )
        )
      # Insufficient specialist coverage

      elif issue == "insufficient_specialists":

          desired_actions.append(
            USDOptimizationAction(
              action="request_more_research",
              reason=(
                "A covereage for an additional specialist is required."
              )
            )
          )

      return desired_actions

  def _task_type_for_the_agent(
    self,
    agent_name: str
  ) -> str | None:

    mapping = {
      "news":"news_analysis",
      "macro":"macro_analysis",
      "market":"market_analysis",
      "earnings":"earnings_analysis",
  }