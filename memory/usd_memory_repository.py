from abc import ABC, abstractmethod
from domain.usd_research_memory import USDResearchMemory

class USDMemoryRespository(ABC):
  '''
  Repository pattern contract
  Any memory repository must know how to save(memory) and get(stock_symbol)
  The responsibility of this class is to persist and retrieve the research memory using a JSON file.
  '''
  @abstractmethod
  def save(self, memory: USDResearchMemory) -> None:
    pass

  @abstractmethod
  def get(self, symbol: str) -> USDResearchMemory | None:
    pass