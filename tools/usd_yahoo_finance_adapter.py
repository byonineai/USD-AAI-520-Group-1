import yfinance as yf
from domain.usd_market_data import USDMarketData
from domain.usd_market_data_provider import USDMarketDataProvider
from tools.usd_research_tool import USDResearchTool

# @author: Marcelo Salvador

class USDYahooFinanceAdapter(USDMarketDataProvider, USDResearchTool):
  '''
   Calls an external provider and translates the provider specific response into
   one of the application's domain objects, so a normalized object can be returned.
  '''
  def fetch(
    self,
    stock_symbol: str
  ) -> USDMarketData:

    return self.get_market_data(
      stock_symbol
    )


  def get_market_data(self, stock_symbol: str) -> USDMarketData:

    ticker = yf.Ticker(stock_symbol)
    info = ticker.info

    return USDMarketData(
      stock_symbol=stock_symbol,
      price=info["regularMarketPrice"],
      volume=info["regularMarketVolume"]
    )
