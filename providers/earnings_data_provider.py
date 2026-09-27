# Provider Interface
from abc import ABC, abstractmethod

class EarningsDataProvider(ABC):

  @abstractmethod
  def get_earnings_information(self, stock_symbol: str) -> dict:
      raise NotImplementedError
