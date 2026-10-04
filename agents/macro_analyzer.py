"""

Macro specialist, one of the places the router sends work.

Same shape as the earnings analyzer with a different persona and a shorter
answer. There is no macro provider yet as of 10.4.26 so this returns the
placeholder on nearly every run. - Raul


"""

from domain.analysis_result import AnalysisResult
from domain.research_task import ResearchTaskType


class MacroAnalyzer:

    def __init__(self, client):
        self.client = client

    def analyze(self, result):
        #no macro provider yet, so there is usually no data
        if not result.data:
            return AnalysisResult(
                task_type=ResearchTaskType.MACRO,
                symbol=result.symbol,
                summary="No macro data yet.",
                data={}
            )

        lines = []

        for key in result.data:
            lines.append(key + ": " + str(result.data[key]))

        prompt = "You are a macro analyst.\n"
        prompt = prompt + "How could these conditions affect " + result.symbol + "?\n"
        prompt = prompt + "Answer in two sentences.\n\n"
        prompt = prompt + "\n".join(lines)

        summary = self.client.complete(prompt, temperature=0.3)

        return AnalysisResult(
            task_type=ResearchTaskType.MACRO,
            symbol=result.symbol,
            summary=summary,
            data=result.data
        )