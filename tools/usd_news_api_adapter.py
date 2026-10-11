import requests

from config.settings import NEWS_API_KEY
from domain.usd_news_data import USDNewsArticle, USDNewsData
from tools.usd_research_tool import USDResearchTool

# @author: Akua Duffour


class USDNewsApiAdapter(USDResearchTool):

  BASE_URL = "https://newsapi.org/v2/everything"

  def __init__(self, api_key: str | None = None):
    self.api_key = api_key or NEWS_API_KEY
    if not self.api_key:
      raise ValueError("NEWS_API_KEY is not configured.")

  def fetch(self, stock_symbol: str) -> USDNewsData:
    response = requests.get(
      self.BASE_URL,
      params={
        "q": stock_symbol,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": self.api_key,
      },
      timeout=10,
    )
    response.raise_for_status()
    raw_data = response.json()

    articles = []
    for article in raw_data.get("articles", []):
      source = article.get("source") or {}
      articles.append(
        USDNewsArticle(
          title=article.get("title") or "",
          source=source.get("name") or "Unknown",
          description=article.get("description"),
          url=article.get("url"),
          published_at=article.get("publishedAt"),
        )
      )

    return USDNewsData(
      stock_symbol=stock_symbol,
      total_results=raw_data.get("totalResults", len(articles)),
      articles=articles,
    )