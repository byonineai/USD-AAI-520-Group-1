from domain.usd_final_report import USDFinalReport

class USDFinalReportBuilder:

  def build(
    self,
    stock_symbol: str,
    status: str,
    generated_analysis: dict,
    evaluation,
    retry_count: int,
    unresolved_gaps: list[str]
  ) -> USDFinalReport:

    return USDFinalReport(
      stock_symbol = stock_symbol,
      status = status,
      quality_status = (
        "passed"
        if evaluation.passed else "unresolved_gaps"
      ),
      specialist_results = generated_analysis[
        "results"
      ],
      synthesis = generated_analysis[
        "synthesis"
      ],
      retry_count = retry_count,
      unresolved_gaps = unresolved_gaps
    )