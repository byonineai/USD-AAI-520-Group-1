from dataclasses import dataclass
# @author: Marcelo Salvador

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
class USDEarningsData:
  """
  A data class representing the earnings data.
  """
  stock_symbol: str
  cik: str
  company_name: str
  filings: list[USDSecFiling]