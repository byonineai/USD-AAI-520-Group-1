from abc import ABC, abstractmethod

class USDResearchTool(ABC):

  @abstractmethod
  def fetch(self, symbol):
    pass

