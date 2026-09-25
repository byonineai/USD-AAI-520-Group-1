import pytest

from agents.market_analyzer import MarketAnalyzer
from domain.research_result import ResearchResult
from domain.research_task import ResearchTaskType


def test_market_analyzer_analyzes_market_result():
    result = ResearchResult(
        task_type=ResearchTaskType.MARKET,
        symbol="NVDA",
        data={
            "symbol": "NVDA",
            "current_price": 150.00,
            "previous_close": 145.00,
            "market_cap": 3_000_000_000_000,
            "pe_ratio": 45.0,
            "volume": 100_000_000,
        },
    )

    analyzer = MarketAnalyzer()

    analysis = analyzer.analyze(result)

    assert analysis.task_type == ResearchTaskType.MARKET
    assert analysis.symbol == "NVDA"

    assert analysis.data["current_price"] == 150.00
    assert analysis.data["previous_close"] == 145.00
    assert analysis.data["price_change"] == 5.00

    assert analysis.data["price_change_percent"] == pytest.approx(
        3.4482758621
    )

    assert analysis.data["market_cap"] == 3_000_000_000_000
    assert analysis.data["pe_ratio"] == 45.0
    assert analysis.data["volume"] == 100_000_000

    assert "NVDA" in analysis.summary