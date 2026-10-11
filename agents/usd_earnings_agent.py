"""
Turns SEC filing data into the standard result shape.

This is the specialist on the earnings path. It receives a USDEarningsData
object from the adapter and has no idea where that data came from, which
is the point. If we swap SEC for another filings source tomorrow, nothing
in this file changes.

Everything downstream reads result.summary and result.evidence. The
aggregator combines them, the evaluator judges them, and the memory file
stores them. So both fields have to be filled on every path through this
method, including the path where there is nothing to report.
"""

from agents.usd_analysis_strategy import USDAnalysisStrategy
from domain.usd_earnings_data import USDEarningsData
from domain.usd_analysis_result import USDAnalysisResult

# @author: Raul Muollo-Diaz


class USDEarningsAgent(USDAnalysisStrategy):
    """Analyzes SEC periodic filings for one company."""

    def analyze(self, data: USDEarningsData) -> USDAnalysisResult:

        # -------------------------------------------------------------
        # The empty case
        # -------------------------------------------------------------
        # A valid ticker with no recent 10-K or 10-Q is normal, not an
        # error. Newly listed companies hit this. We return a real
        # result so the evaluator sees a gap instead of a crash.

        if not data.filings:
             return USDAnalysisResult(
                agent="earnings",
                summary=(
                    f"No recent 10-K or 10-Q filings were found for "
                    f"{data.stock_symbol}."
                ),
                evidence=[]
            )

        # -------------------------------------------------------------
        # The summary
        # -------------------------------------------------------------
        # SEC returns newest first, so position zero is the most recent
        # filing. One sentence, because the aggregator combines this
        # with the other specialists and long text drowns them out.

        latest = data.filings[0]

        summary = (
            f"{data.company_name} ({data.stock_symbol}) most recently "
            f"filed a {latest.form} on {latest.filing_date}. "
            f"{len(data.filings)} recent periodic filings were reviewed."
        )

        # -------------------------------------------------------------
        # The evidence
        # -------------------------------------------------------------
        # Every claim in the summary has to be checkable. Each line here
        # carries a direct link to the filing on SEC, so a reader can
        # verify the analysis instead of taking it on faith.

        evidence = []

        for filing in data.filings:
            evidence.append(
                f"{filing.form} filed {filing.filing_date} ({filing.url})"
            )

        return USDAnalysisResult(
            agent="earnings",
            summary=summary,
            evidence=evidence
        )
