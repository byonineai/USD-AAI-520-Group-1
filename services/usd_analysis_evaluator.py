from domain.usd_evaluation_result import USDEvaluationResult

class USDAnalysisEvaluator:
  '''
    The evaluator checks whether there are enough specialists or not.
    Whether there are any results, summary or evidence present.
  '''
  def __init__(self, minimum_specialists: int = 1):
    self.minimum_specialists = minimum_specialists
  def evaluate(self, report: dict) -> USDEvaluationResult:

    issues = []

    specialist_count = report.get(
      "specialist_count",
      0
    )

    results = report.get("results",[])

    # Are there enough specialists?

    if specialist_count < self.minimum_specialists:
      issues.append("There are insufficient specialists!")

    for result in results:
    # Have we received any analysis yet?
      if not results:
        issues.append(
          f"Missing summary: {result.agent}"
        )
      # Is there an evidence in every result?
      if not result.evidence:
        issues.append(
          f"The missing evidence: {result.agent}"
        )

    return USDEvaluationResult(
      passed=len(issues) == 0,
      issues = issues
    )