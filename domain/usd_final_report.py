from dataclasses import dataclass

from domain.usd_analysis_result import USDAnalysisResult

@dataclass
class USDFinalReport:
  stock_symbol: str
  status: str
  quality_status: str
  synthesis: str
  specialist_results: list[USDAnalysisResult]
  unresolved_gaps: list[str]
  retry_count: int