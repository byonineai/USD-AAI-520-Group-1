# @author: Marcelo Salvador
import os
from tools.usd_research_tool import USDResearchTool
from dotenv import load_dotenv
from fredapi import Fred

from domain.usd_macro_data import (
  USDMacroData,
  USDMacroIndicator
)

load_dotenv()

class USDFredAdapter(USDResearchTool):

  SERIES = {
    "FEDFUNDS": "Federal Funds Rate ",
    "CPIAUCSL": "Consumer Price Index ",
    "DGS10": "10-Year Treasury Rate ",
    "UNRATE": "Unemployment Rate ",
  }

  def __init__(
    self,
    api_key: str | None = None
  ):
    self.api_key = (
      api_key or os.getenv('FRED_API_KEY')
    )

    if not self.api_key:
      raise ValueError(
        "THE FRED_API_KEY IS NOT CONFIGURED. PLEASE CHECK IT."
      )
    self.fred = Fred(
      api_key = self.api_key
    )

  def fetch(
      self,
      stock_symbol: str
    ) -> USDMacroData:

      the_indicators = []

      for series_id, name in self.SERIES.items():

        the_series = self.fred.get_series(
          series_id
        )

        the_clean_series = the_series.dropna()

        if the_clean_series.empty:
          continue

        the_latest_date = the_clean_series.index[-1]
        the_latest_value = the_clean_series.iloc[-1]

        the_indicator = USDMacroIndicator(
          name = name,
          value = float(the_latest_value),
          series_id = series_id,
          observation_date = str(the_latest_date.date())
        )

        the_indicators.append(
          the_indicator
        )

      return USDMacroData(
        stock_symbol = stock_symbol, # Keeping stock symbol to maintain the contract
        # but the stock symbol is not needed by FRED
        indicators = the_indicators
      )