from agents.usd_analysis_strategy import USDAnalysisStrategy
from domain.usd_market_data import USDMarketData
from domain.usd_analysis_result import USDAnalysisResult
# @Author: Marcelo Salvador

class USDMarketAgent(USDAnalysisStrategy):
    def analyze(self, data: USDMarketData) -> USDAnalysisResult:
      summary = (
        f"{data.stock_symbol} is trading at value"
        f"${data.price:.2f}."
      )