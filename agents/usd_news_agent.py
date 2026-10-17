from agents.usd_analysis_strategy import USDAnalysisStrategy
from domain.usd_news_data import USDNewsData
from domain.usd_analysis_result import USDAnalysisResult

# @author: Akua Duffour


class USDNewsAgent(USDAnalysisStrategy):
    """
    Analyze normalized news data from USDNewsApiAdapter.

    Tests the Adapter before adding the agent.
    """
#no requests or api just the USDNewsData
    def analyze(self, data: USDNewsData) -> USDAnalysisResult:
        evidence = []

        for article in data.articles[:5]:
            evidence.append(
                f"{article.source}: {article.title}"
            )

        summary = (
            f"Found {len(data.articles)} recent "
            f"news articles for {data.stock_symbol}."
        )

        return USDAnalysisResult(
            summary=summary,
            agent="news",
            evidence=evidence,
        )