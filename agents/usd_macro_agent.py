from agents.usd_analysis_strategy import USDAnalysisStrategy
from domain.usd_macro_data import USDMacroData
from domain.usd_analysis_result import USDAnalysisResult

class USDMacroAgent(USDAnalysisStrategy):

  def analyze(
    self,
    data: USDMacroData
  ) -> USDAnalysisResult:

    the_evidence = []

    for the_indicator in data.indicators:

      the_evidence.append(
        f"{the_indicator.name} "
        f"{the_indicator.series_id} "
        f"{the_indicator.value} "
        f"as of {the_indicator.observation_date} "
      )

    final_summary = (
      f"The collected {len(data.indicators)} "
      f"The macro economic indicators for {data.stock_symbol} "
    )

    return USDAnalysisResult(
      agent="macro",
      summary = final_summary,
      evidence = the_evidence
    )
