from dataclasses import dataclass
# Domain model for memory
# It answers how a stored research memory looks like

@dataclass
class USDResearchMemory:
  stock_symbol: str
  summaries: dict[str,str]
  quality_status: str
  unresolved_gaps: list[str]
  evidence: dict[str, list[str]]