from domain.research_result import ResearchResult
from domain.research_task import ResearchTaskType


class MarketAnalyzer:

    def analyze(self, result: ResearchResult) -> dict:
        if result.task_type != ResearchTaskType.MARKET:
            raise ValueError(
                "MarketAnalyzer can only analyze MARKET results."
            )

        data = result.data

        current_price = data.get("current_price")
        previous_close = data.get("previous_close")

        price_change = None
        price_change_percent = None

        if current_price is not None and previous_close not in (None, 0):
            price_change = current_price - previous_close
            price_change_percent = (
                price_change / previous_close
            ) * 100

        return {
            "symbol": result.symbol,
            "previous_close": previous_close,
            "current_price": current_price,
            "market_cap": data.get("market_cap"),
            "pe_ratio": data.get("pe_ratio"),
            "volume": data.get("volume"),
            "price_change": price_change,
            "price_change_percent": price_change_percent,
        }