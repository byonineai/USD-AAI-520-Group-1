from abc import ABC, abstractmethod
from domain.usd_market_data import USDMarketData
# @author: Marcelo Salvador
# If you want to provide market data to the application.
# you must implement get_market_data().

class USDMarketDataProvider(ABC):

    @abstractmethod
    def get_market_data(self, stock_symbol: str) -> USDMarketData:
        pass