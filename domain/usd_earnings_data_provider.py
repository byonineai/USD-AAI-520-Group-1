from abc import ABC, abstractmethod
from domain.usd_earnings_data import USDEarningsData
# @author: Raul Muollo-Diaz
# If you want to provide earnings data to the application,
# you must implement get_earnings_data().


class USDEarningsDataProvider(ABC):

    @abstractmethod
    def get_earnings_data(self, stock_symbol: str) -> USDEarningsData:
        pass
