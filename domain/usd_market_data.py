from dataclasses import dataclass
# @author: Marcelo Salvador
# Data contracts between specialist agents and adapters.
@dataclass
class USDMarketData:
  """
  A data class representing Market Data.
  """
  stock_symbol: str
  price: float
  volume: int