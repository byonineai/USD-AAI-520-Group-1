import pytest
from unittest.mock import patch
from providers.sec_provider import SECProvider

@patch("providers.sec_provider.requests.get")
def test_sec_provider_returns_latest_filing(mock_get):
    ticker_response = {
        "0": {
            "cik_str": 1025590,
            "ticker": "NVDA",
            "title": "NVIDIA CORP",
        }
    }

    submissions_response = {
        "name": "NVIDIA CORP",
        "filings": {
            "recent": {
                "form": [
                    "8-K",
                    "10-Q",
                ],
                "accessionNumber": [
                    "0000000000-26-000001",
                    "00010425590-26-000002",
                ],
                "filingDate": [
                    "2026-08-01",
                    "2026-07-26",
                ],
                "reportDate": [
                    "2026-08-01",
                    "2026-07-26",
                ],
                "primaryDocument": [
                    "form8k.htm",
                    "nvda-10q.htm",
                ],
            }
        },
    }

    mock_get.return_value.raise_for_status.return_value = None

    mock_get.return_value.json.side_effect = [
        ticker_response,
        submissions_response,
    ]

    provider = SECProvider(
        user_agent="InvestmentAgent test@example.com"
    )

    result = provider.get_earnings_information("nvda")

    assert result["form"] == "10-Q"
    assert result["filing_date"] == "2026-07-26"
    assert result["symbol"] == "NVDA"
    assert result["cik"] == "0001025590"

    assert mock_get.call_count == 2

    # Test Validation
    def test_sec_provider_rejects_empty_symbol():
      provider = SECProvider(
          user_agent="InvestmentAgent test@example.com"
      )

      with pytest.raises(
          ValueError,
          match="The stock symbol can't be empty",
      ):
          provider.get_earnings("")