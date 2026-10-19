from dataclasses import dataclass
# @Author: Marcelo Salvador
# This class defines the standard structure returned by the specialist agent and provides a
# stable data contract 

@dataclass
class USDAnalysisResult:
  agent: str
  evidence: list[str]
  summary: str
