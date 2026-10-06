from dataclasses import dataclass
# @author: Marcelo Salvador

@dataclass
class USDMacroObservation:
  """
  A data class representing Macro Observation.
  """
  date: str
  value: float

@dataclass
class USDMacroIndicator:
  """
  A data class representing Macro Indicator.
  """
  name: str
  unit: str
  series_id: str
  observations: list[USDMacroObservation]

@dataclass
class USDMacroData:
  """
  A data class representing Macro Data.
  """
  stock_symbol: str
  indicators: list[USDMacroIndicator]