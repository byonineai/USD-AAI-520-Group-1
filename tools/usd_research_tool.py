from abc import ABC, abstractmethod

class USDResearchTool(ABC):

  @abstractmethod
  def fetch(self, stock_symbol: str):
    pass
