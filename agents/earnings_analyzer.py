"""

Earnings specialist.

This interprets numbers, it does not produce them. Any math belongs upstream in
Python, so all this does is hand the model figures it was already given, and the
prompt tells it not to invent.

Once live data shows up this should work as-is.

"""


from domain.analysis_result import AnalysisResult
from domain.research_result import ResearchResult
from domain.research_task import ResearchTaskType


class EarningsAnalyzer:

    def __init__(self, client):
        self.client = client

    def analyze(self, result: ResearchResult) -> AnalysisResult:
        if result.task_type != ResearchTaskType.EARNINGS:
            raise ValueError(
                "EarningsAnalyzer can only analyze EARNINGS results."
            )

        #no data means the provider is not wired up yet
        if not result.data:
            return AnalysisResult(
                task_type=ResearchTaskType.EARNINGS,
                symbol=result.symbol,
                summary="No earnings data was available.",
                data={}
            )

        #turn the data dict into plain lines for the prompt
        lines = []

        for key in result.data:
            lines.append(key + ": " + str(result.data[key]))

        facts = "\n".join(lines)

        prompt = "You are an earnings analyst.\n"
        prompt = prompt + "Interpret these figures for " + result.symbol + ".\n"
        prompt = prompt + "Only comment on figures listed below.\n"
        prompt = prompt + "Do not invent numbers.\n"
        prompt = prompt + "Answer in three short sentences.\n\n"
        prompt = prompt + facts

        summary = self.client.complete(prompt, temperature=0.3)

        return AnalysisResult(
            task_type=ResearchTaskType.EARNINGS,
            symbol=result.symbol,
            summary=summary,
            data=result.data
        )