from abc import ABC, abstractmethod
# Interface - Provider Contract

# Any  market data provider must implement the
# get_market_data() method

class MarketDataProvider(ABC):
  @abstractmethod
  def get_market_data(self, symbol:str):
    """Retrive market data for a stock symbol"""
    pass