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

        earnings_metrics =  data.metrics

        summary = [
            (
                f"{data.company_name} ({data.stock_symbol}) most recently "
                f"filed a {latest.form} on {latest.filing_date}."
            ),
            (
                f"{len(data.filings)} recent periodic filings were reviewed."
            )
        ]

        if earnings_metrics is not None:

            if earnings_metrics.revenue is not None:
                summary.append(
                    f"Reported revenue was "
                    f"${earnings_metrics.revenue:,.0f}."
                )

            if earnings_metrics.net_income is not None:
                summary.append(
                    f"Reported net income was "
                    f"${earnings_metrics.net_income:,.0f}."
                )

            if earnings_metrics.diluted_eps is not None:
                summary.append(
                    f"Diluted EPS was "
                    f"${earnings_metrics.diluted_eps:.2f}."
                )

        summary = " ".join(
            summary
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

        if earnings_metrics is not None:

            if earnings_metrics.revenue is not None:
                evidence.append(
                    f"revenue={earnings_metrics.revenue}"
                )

            if earnings_metrics.gross_profit is not None:
                evidence.append(
                    f"gross_profit={earnings_metrics.gross_profit}"
                )

            if earnings_metrics.operating_income is not None:
                evidence.append(
                    f"operating_income={earnings_metrics.operating_income}"
                )

            if earnings_metrics.net_income is not None:
                evidence.append(
                    f"net_income={earnings_metrics.net_income}"
                )

            if earnings_metrics.diluted_eps is not None:
                evidence.append(
                    f"diluted_eps={earnings_metrics.diluted_eps}"
                )

            if (
                earnings_metrics.revenue is not None
                and earnings_metrics.revenue != 0
            ):

                if earnings_metrics.gross_profit is not None:
                    gross_margin = (
                        earnings_metrics.gross_profit
                        / earnings_metrics.revenue
                    ) * 100

                    evidence.append(
                        f"gross_margin={gross_margin:.2f}%"
                    )

                if earnings_metrics.operating_income is not None:
                    operating_margin = (
                        earnings_metrics.operating_income
                        / earnings_metrics.revenue
                    ) * 100

                    evidence.append(
                        f"operating_margin={operating_margin:.2f}%"
                    )

                if earnings_metrics.net_income is not None:
                    net_margin = (
                        earnings_metrics.net_income
                        / earnings_metrics.revenue
                    ) * 100

                    evidence.append(
                        f"net_margin={net_margin:.2f}%"
                    )


        return USDAnalysisResult(
            agent="earnings",
            summary=summary,
            evidence=evidence
        )
