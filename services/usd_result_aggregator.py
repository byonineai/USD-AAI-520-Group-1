from domain.usd_analysis_result import USDAnalysisResult
# @Author: Marcelo Salvador

# The specialists produce several independent agent
# outputs and the aggregator collects those results into one report.

class USDResultAggregator:

  def aggregate_results(
    self,
    results: list[USDAnalysisResult]
  )->dict:

    return {
      "results": results,
      "specialist_count": len(results)
    }
