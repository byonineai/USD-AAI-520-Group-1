from dataclasses import dataclass
# @author: Akua Duffour
# Data contracts between specialist agents and adapters.

@dataclass
class USDNewsArticle:
  """
  A data class representing one normalized news article.
  """
  title: str
  source: str
  description: str | None = None
  url: str | None = None
  published_at: str | None = None


@dataclass
class USDNewsData:
  """
  A data class representing normalized news for a stock symbol.
  """
  stock_symbol: str
  total_results: int
  articles: list[USDNewsArticle]