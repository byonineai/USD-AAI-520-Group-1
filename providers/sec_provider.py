import os

import requests

from providers.earnings_data_provider import EarningsDataProvider

class SECProvider(EarningsDataProvider):

    TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
    SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

    def __init__(self, user_agent: str | None = None):
        self.user_agent = user_agent or os.getenv("SEC_USER_AGENT")

        if not self.user_agent:
            raise ValueError(
                "Sec user agent is not configured."
            )

    def headers(self) -> dict:
        return {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": self.user_agent,
        }

    def _get_cik(self, stock_symbol: str) -> str:
        response = requests.get(
            self.TICKERS_URL,
            headers=self.headers(),
            timeout=10,
        )

        response.raise_for_status()

        companies = response.json()

        for company in companies.values():
            if company["ticker"].upper() == stock_symbol:
                return str(company["cik_str"]).zfill(10)

        raise ValueError(
            f"Could not find SEC CIK for symbol: {stock_symbol}"
        )

    def get_earnings_information(self, systock_symbolmbol: str) -> dict:
        stock_symbol = systock_symbolmbol.strip().upper()

        if not stock_symbol:
            raise ValueError(
                "stock_symbol cannot be empty."
            )

        cik = self._get_cik(stock_symbol)

        url = self.SUBMISSIONS_URL.format(cik=cik)

        response = requests.get(
            url,
            headers=self.headers(),
            timeout=10,
        )

        response.raise_for_status()

        payload = response.json()

        recent = payload.get(
            "filings", {}
        ).get(
            "recent", {}
        )

        forms = recent.get("form", [])
        accession_numbers = recent.get(
            "accessionNumber", []
        )
        filing_dates = recent.get(
            "filingDate", []
        )
        report_dates = recent.get(
            "reportDate", []
        )
        primary_documents = recent.get(
            "primaryDocument", []
        )

        for index, form in enumerate(forms):
            if form in ("10-Q", "10-K"):
                return {
                    "symbol": stock_symbol,
                    "company_name": payload.get("name"),
                    "cik": cik,
                    "report_date": report_dates[index],
                    "accession_number": accession_numbers[index],
                    "primary_document": primary_documents[index],
                    "form": form,
                    "filing_date": filing_dates[index],
                }

        raise ValueError(
            f"No recent 10-Q or 10-K filing found for {stock_symbol}"
        )
