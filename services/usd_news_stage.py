from abc import ABC, abstractmethod

class USDNewsStage(ABC):
  '''
  Defines a common interface for every stage in the financial-news prompt chaining pipeline.
  '''
  @abstractmethod
  def process(self, data):
      pass