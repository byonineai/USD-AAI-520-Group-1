from services.usd_news_stage import USDNewsStage
from domain.usd_news_data import USDNewsData

class USDNewsPreprocessStage(USDNewsStage):
  '''
  Preprocesses raw financial news prior LLM-based analysis.
  '''
  def process(self, news_data: USDNewsData):

    all_processed_articles = list()

    for article in news_data.articles:

      title = (
        article.title or ""
      ).strip()

      source = (
        article.source or ""
      ).strip()

      url = (
        article.url or ""
      ).strip

      published_at = (
        article.published_at or ""
      )

      description = (
        article.description or ""
      ).strip()


      if not title:
        continue

      all_processed_articles.append(
        {
          "title": title,
          "description": description,
          "source": source,
          "url": url,
          "published_at": published_at
        }
      )
    return {
      "stock_symbol": news_data.stock_symbol,
      "articles": all_processed_articles,
      "classification": None,
      "extracted_findings": None,
      "summary": None
    }