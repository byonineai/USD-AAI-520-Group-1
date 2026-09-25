import pytest

from domain.research_task import ResearchTaskType
from orchestration.tool_registry import ToolRegistry


class FakeMarketProvider:

    def get_market_data(self, symbol: str):
        return {
            "symbol": symbol,
            "price": 100.00,
        }


def test_registry_returns_registered_provider():
    registry = ToolRegistry()

    provider = FakeMarketProvider()

    registry.register(
        ResearchTaskType.MARKET,
        provider,
    )

    selected_provider = registry.get_provider(
        ResearchTaskType.MARKET
    )

    assert selected_provider is provider

# Test Missing Providers

# def test_registry_rejects_unregistered_provider():
#     registry = ToolRegistry()

#     with pytest.raises(
#         ValueError,
#         match="No provider registered"
#     ):
#         registry.get_provider(
#             ResearchTaskType.NEWS
#         )