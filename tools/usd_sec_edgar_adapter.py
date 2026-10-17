"""
SEC EDGAR is the only outside source this file knows about.

The class inherits from two parents on purpose. The orchestrator only knows
how to call fetch(). The domain layer wants get_earnings_data(). Inheriting
both means one object answers to both callers, which is the same approach
the Yahoo adapter takes.

I limited this to 10-K and 10-Q.
"""

import os

import requests

from domain.usd_earnings_data import (
    USDEarningsData,
    USDSecFiling,
    USDEarningsMetrics,
)
from domain.usd_earnings_data_provider import USDEarningsDataProvider
from tools.usd_research_tool import USDResearchTool

# @author: Raul Muollo-Diaz


class USDSecEdgarAdapter(USDEarningsDataProvider, USDResearchTool):
    """Pulls recent 10-K and 10-Q filings for one ticker from SEC EDGAR."""

    TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
    SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
    ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data"

    COMPANY_FACTS_URL = (
    "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
)

    # The two periodic report forms. Annual and quarterly.
    EARNINGS_FORMS = ["10-K", "10-Q"]

    # A large company can have hundreds of filings on record. This caps what
    # we hand downstream so one ticker cannot flood the analysis.
    MAX_FILINGS = 5

    # SEC rejects anonymous traffic. There is no API key and no signup, just
    # a contact string, and it lives in .env so it never reaches the repo.

    FINANCIAL_TAGS = {
        "revenue": [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "Revenues",
            "SalesRevenueNet",
        ],

        "gross_profit": [
            "GrossProfit",
        ],

        "operating_income": [
            "OperatingIncomeLoss",
        ],

        "net_income": [
            "NetIncomeLoss",
        ],

        "diluted_eps": [
            "EarningsPerShareDiluted",
        ],
    }

    def __init__(self, user_agent: str | None = None):
        self.user_agent = user_agent or os.getenv("SEC_USER_AGENT")

        if not self.user_agent:
            raise ValueError(
                "SEC_USER_AGENT is not configured."
            )

    def headers(self) -> dict:
        return {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": self.user_agent,
        }

    # -----------------------------------------------------------------
    # The door the orchestrator uses
    # -----------------------------------------------------------------
    # The tool registry hands the orchestrator this object and it calls
    # fetch(). That is the only method it knows. This forwards straight
    # through so the real work has a name that says what it does.

    def fetch(self, stock_symbol: str) -> USDEarningsData:
        return self.get_earnings_data(stock_symbol)

    def get_earnings_data(self, stock_symbol: str) -> USDEarningsData:

        # -------------------------------------------------------------
        # Step 1. Translate the ticker into a CIK number
        # -------------------------------------------------------------
        # SEC has no idea what NVDA means. Everything they publish is
        # filed under a Central Index Key ("CIK"), so the first call downloads
        # their master ticker list and finds the match.

        lookup = requests.get(
            self.TICKERS_URL,
            headers=self.headers(),
            timeout=10,
        )

        # Without this, a bad User-Agent returns an HTML error page and
        # the JSON parse fails with a message that explains nothing.
        lookup.raise_for_status()

        cik = None
        company_name = None

        for company in lookup.json().values():
            if company["ticker"] == stock_symbol.upper():
                # The submissions endpoint demands exactly ten digits.
                cik = str(company["cik_str"]).zfill(10)
                company_name = company["title"]
                break

        # Fail here with a clear message.
        if cik is None:
            raise ValueError(
                f"SEC has no CIK on file for ticker: {stock_symbol}"
            )

        # -------------------------------------------------------------
        # Step 2. Pull the filing history for the CIK
        # -------------------------------------------------------------

        history = requests.get(
            self.SUBMISSIONS_URL.format(cik=cik),
            headers=self.headers(),
            timeout=10,
        )
        history.raise_for_status()

        recent = history.json().get(
            "filings", {}
        ).get(
            "recent", {}
        )

        forms = recent.get("form", [])
        filing_dates = recent.get("filingDate", [])
        report_dates = recent.get("reportDate", [])
        accession_numbers = recent.get("accessionNumber", [])
        primary_documents = recent.get("primaryDocument", [])

        # -------------------------------------------------------------
        # Step 3. Walk the filings and keep the ones we care about
        # -------------------------------------------------------------
        # SEC does not return a list of filings. It returns separate
        # lists that line up by position, so form[0], filingDate[0] and
        # accessionNumber[0] all describe the same filing. That is why
        # this loops over positions instead of over objects.

        filings = []

        for index, form in enumerate(forms):

            if form not in self.EARNINGS_FORMS:
                continue

            accession = accession_numbers[index]
            document = primary_documents[index]

            # Two quirks in the document URL. The CIK drops the padding
            # and the accession number drops the dashes.
            url = (
                f"{self.ARCHIVE_URL}/"
                f"{int(cik)}/{accession.replace('-', '')}/{document}"
            )

            filings.append(
                USDSecFiling(
                    form=form,
                    report_name=report_dates[index],
                    filing_date=filing_dates[index],
                    primary_document=document,
                    accession_number=accession,
                    url=url
                )
            )

            if len(filings) >= self.MAX_FILINGS:
                break

        metrics = None

        if filings:

            company_facts_response = requests.get(
                self.COMPANY_FACTS_URL.format(
                    cik=cik
                ),
                headers=self.headers(),
                timeout=10,
            )

            company_facts_response.raise_for_status()

            company_facts = (
                company_facts_response.json()
            )

            metrics = self._extract_financial_metrics(
                company_facts,
                filings[0]
            )

        # -------------------------------------------------------------
        # Step 4. Hand back the clean object
        # -------------------------------------------------------------
        # Nothing that leaves this method mentions SEC. The agent that
        # receives this does not need to know where the data came from.

        return USDEarningsData(
            stock_symbol=stock_symbol,
            cik=cik,
            company_name=company_name,
            metrics = metrics,
            filings=filings
        )

    def _usd_find_financial_fact(
        self,
        company_facts: dict,
        possible_tags: list[str],
        filing: USDSecFiling,
        unit: str,
    ) -> float | None:

        us_gaap = (
            company_facts
            .get("facts", {})
            .get("us-gaap", {})
        )

        for tag in possible_tags:

            concept = us_gaap.get(tag)

            if concept is None:
                continue

            values = (
                concept
                .get("units", {})
                .get(unit, [])
            )

            candidates = [
                fact
                for fact in values
                if (
                    fact.get("accn")
                    == filing.accession_number

                    and fact.get("form")
                    == filing.form

                    and fact.get("end")
                    == filing.report_name
                )
            ]

            if candidates:
                return candidates[0].get("val")

        return None

    def _extract_financial_metrics(
        self,
        company_facts: dict,
        filing: USDSecFiling,
    ) -> USDEarningsMetrics:

        return USDEarningsMetrics(

            revenue=self._usd_find_financial_fact(
                company_facts,
                self.FINANCIAL_TAGS["revenue"],
                filing,
                "USD",
            ),

             operating_income=self._usd_find_financial_fact(
                company_facts,
                self.FINANCIAL_TAGS["operating_income"],
                filing,
                "USD",
            ),

            gross_profit=self._usd_find_financial_fact(
                company_facts,
                self.FINANCIAL_TAGS["gross_profit"],
                filing,
                "USD",
            ),

            net_income=self._usd_find_financial_fact(
                company_facts,
                self.FINANCIAL_TAGS["net_income"],
                filing,
                "USD",
            ),

            diluted_eps=self._usd_find_financial_fact(
                company_facts,
                self.FINANCIAL_TAGS["diluted_eps"],
                filing,
                "USD/shares",
            ),
        )
