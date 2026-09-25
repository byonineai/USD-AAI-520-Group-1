from dataclasses import dataclass
from enum import Enum

class ResearchTaskType(Enum):
  MARKET = "market_analysis",
  EARNINGS="earnings_analysis",
  MACRO="macro_analysis",
  NEWS="news_analysis"

@dataclass
class ResearchTask:
  task_type: ResearchTaskType
  symbol:str