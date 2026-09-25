from unittest.mock import patch

from providers.yahoo_finance_provider import YahooFinanceProvider

@patch("providers.yahoo_finance_provider.yf.Ticker")
def test_get_market_data(mock_ticker):
    mock_ticker.return_value.info = {
        "longName": "NVIDIA Corporation",
        "currentPrice": 150.00,
        "previousClose": 148.00,
        "marketCap": 3000000000000,
        "trailingPE": 45.0,
        "volume": 100000000,
    }

    provider = YahooFinanceProvider()

    result = provider.get_market_data("nvda")

    assert result["symbol"] == "NVDA"
    assert result["company_name"] == "NVIDIA Corporation"
    assert result["current_price"] == 150.00
    assert result["previous_close"] == 148.00
    assert result["market_cap"] == 3000000000000
    assert result["pe_ratio"] == 45.0
    assert result["volume"] == 100000000