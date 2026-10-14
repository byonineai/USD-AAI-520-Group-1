from abc import ABC, abstractmethod

class USDLLMProviderInterface(ABC):

  @abstractmethod
  def generate(
    self,
    prompt: str
  ) -> str:
    pass