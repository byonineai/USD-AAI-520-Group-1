import os
import requests
from dotenv import load_dotenv
from providers.news_data_provider import NewsDataProvider
# 1. This component uses the abstract method, calls the news API
# 2. Calls the news API
# 3. Receives the JSON
# 4. Extracts only the part needed
# 5. Returns the normalized dictionary

load_dotenv()

class FinancialNewsProvider(NewsDataProvider):

  BASE_URL = "https://newsapi.org/v2/everything"

  # Make the APi key injectable to make unit test easier
  def __init__(self, api_key: str | None = None):
    # Get environment variable API Key
    self.api_key = api_key or os.getenv("NEWS_API_KEY")

    if not self.api_key:
      raise ValueError(
        "The News API Key isn't configured."
      )

  def get_financial_news(self,stock_symbol: str) -> dict:

    # Remove extra spaces and convert letters to uppercase
    stock_symbol = stock_symbol.strip().upper()

    if not stock_symbol:
      raise ValueError("The stock symbol cannot be empty")

    financial_news_response = requests.get(
      self.BASE_URL,
      params={
        "q": stock_symbol,
        "language" : "en",
        "sortBy":"publishedAt",
        "pageSize":10,
        "apiKey": self.api_key
      },
      timeout=10
    )

    financial_news_response.raise_for_status()

    payload = financial_news_response.json()

    financial_articles = []

    for article in payload.get("articles", []):
      financial_articles.append(
        {
          "title": article.get("title"),
          "description": article.get("description"),
          "source":(
            article.get("source", {}).get("name")
          ),
          "published_at": article.get("publishedAt"),
          "url": article.get("url")
        }
      )

      return {
        "symbol": stock_symbol,
        "articles": financial_articles,
        "article_count": len(financial_articles)
      }
