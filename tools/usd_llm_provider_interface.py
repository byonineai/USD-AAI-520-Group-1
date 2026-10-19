from abc import ABC, abstractmethod

class USDLLMProviderInterface(ABC):
  '''
  This abstract class defines the contract for large language model providers.

  '''
  @abstractmethod
  def generate(
    self,
    prompt: str
  ) -> str:
    """
        Generate text from the supplied prompt.

        Args:
            prompt: The instruction or context sent to the LLM.

        Returns:
            The generated text response.

        Concrete subclasses must implement this method.
    """
    pass