from dataclasses import dataclass
# @author: Marcelo Salvador
# Data contracts between specialist agents and adapters.

@dataclass
class USDSecFiling:
  """
  A data class representing the SecFiling data.
  """
  form: str
  report_name: str
  filing_date: str
  primary_document:str
  accession_number: str
  url: str

@dataclass
class USDEarningsMetrics:
    """
    Financial metrics extracted from the latest
    SEC 10-Q or 10-K filing.
    """
    revenue: float | None = None
    net_income: float | None = None
    gross_profit: float | None = None
    operating_income: float | None = None
    diluted_eps: float | None = None

@dataclass
class USDEarningsData:
  """
  A data class representing the earnings data.
  """
  stock_symbol: str
  cik: str
  company_name: str
  filings: list[USDSecFiling]
  metrics: USDEarningsMetrics | None = None