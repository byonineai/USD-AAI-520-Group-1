from dataclasses import dataclass
# @Author: Marcelo Salvador
# This class defines the standard structure returned by the specialist agent

@dataclass
class USDAnalysisResult:
  agent: str
  evidence: list[str]
  summary: str
