from abc import ABC, abstractmethod
from domain.usd_research_memory import USDResearchMemory


class USDMemoryRespository(ABC):
  '''
  Repository pattern contract
  Any memory repository must know how to save(memory) and get(stock_symbol)
  '''
  @abstractmethod
  def save(self, memory: USDResearchMemory) -> None:
    pass

  @abstractmethod
  def get(self, symbol: str) -> USDResearchMemory | None:
    pass