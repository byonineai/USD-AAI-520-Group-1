import yfinance as yf
from domain.usd_market_data import USDMarketData
from domain.usd_market_data_provider import USDMarketDataProvider

# @author: Marcelo Salvador

class USDYahooFinanceAdapter(USDMarketDataProvider):

  def get_market_data(self, stock_symbol: str) -> USDMarketData:

    ticker = yf.Ticker(stock_symbol)

    info = ticker.info

    return USDMarketData(
      stock_symbol=stock_symbol,
      price=info["regularMarketPrice"],
      volume=info["regularMarketVolume"]
    )
