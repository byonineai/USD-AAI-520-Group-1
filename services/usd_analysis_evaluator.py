from domain.usd_evaluation_result import (
    USDEvaluationResult
)
# @Author: Marcelo Salvador
# Its responsibility is to assess the aggregated report
# and decide whether the research output meets your quality criteria.

class USDAnalysisEvaluator:

  def evaluate(self, report):

    issues = []

    if report["specialist_count"] < 3:
      issues.append("There are insufficient sources")

    if not report["summaries"]:
      issues.append("Missing Analysis")
    return USDEvaluationResult(
      issues=issues,
      passed=len(issues) == 0
    )