from dataclasses import dataclass
# @author: Marcelo Salvador

@dataclass
class USDMarketData:
  """
  A data class representing Market Data.
  """
  stock_symbol: str
  price: float
  volume: int