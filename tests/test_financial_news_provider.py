from unittest.mock import patch
import pytest
from providers.financial_news_provider import FinancialNewsProvider
# python -m pytest tests/test_financial_news_provider.py -vv
@patch("providers.financial_news_provider.requests.get")

# PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -vv -s

def test_financial_news_provider_returns_news(mock_get):
    mock_get.return_value.json.return_value = {
        "status": "ok",
        "articles": [
            {
                "title": "NVIDIA reports strong earnings this year.",
                "description": "Revenue increased..",
                "source": {
                    "name": "Example  1 Financial News"
                },
                "publishedAt": "2025-06-28T12:00:00Z",
                "url": "https://example.com/nvidia",
            }
        ],
    }

    mock_get.return_value.raise_for_status.return_value = None

    provider = FinancialNewsProvider(
        api_key="test-key"
    )

    result = provider.get_financial_news("nvda")

    assert result["symbol"] == "NVDA"
    assert result["article_count"] == 1
    assert (
        result["articles"][0]["title"]
        == "NVIDIA reports strong earnings this year."
    )

def test_news_provider_rejects_empty_symbol():
    provider = FinancialNewsProvider(
        api_key="test-key"
    )

    with pytest.raises(
        ValueError,
        match="The stock symbol cannot be empty",
    ):
        provider.get_financial_news("")