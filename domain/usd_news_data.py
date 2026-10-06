from dataclasses import dataclass
# @author: Marcelo Salvador

@dataclass
class USDAnalysisResult:
  """A data class representing a the standard structure returned by specialist agents.

  Attributes:
        summary: A summary of the specialist agent's analysis.
        agent: The name of the identifier of the specialist agent producing the result.
  """
  summary: str
  agent: str