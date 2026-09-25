import pytest

from domain.research_task import ResearchTaskType
from orchestration.router import DataRouter

class FakeMarketAnalyzer:
    pass

def test_router_returns_registered_analyzer():
    router = DataRouter()

    analyzer = FakeMarketAnalyzer()

    router.register(
        ResearchTaskType.MARKET,
        analyzer,
    )

    selected_analyzer = router.get_analyzer(
        ResearchTaskType.MARKET
    )

    assert selected_analyzer is analyzer
