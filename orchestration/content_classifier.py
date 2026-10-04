"""

The routing pattern.

ResearchResult already has a task_type on it, but that just records which
provider the data came from. Routing is supposed to be a model reading the
content and picking a specialist. This reads the content and decides, and it can
disagree.

Temperature 0. If the same content came back with different labels on
different runs that is considered failing. Inconsistent output was one of the
pitfalls in the Module 7 lecture.

"""


from domain.research_task import ResearchTaskType


class ContentClassifier:

    def __init__(self, client):
        self.client = client

    def classify(self, text):
        prompt = "Pick one category for this financial content.\n"
        prompt = prompt + "market, news, earnings, or macro\n"
        prompt = prompt + "Reply with only the word.\n\n"
        prompt = prompt + text

        answer = self.client.complete(prompt, temperature=0)
        answer = answer.strip().lower()

        if "earnings" in answer:
            return ResearchTaskType.EARNINGS
        if "macro" in answer:
            return ResearchTaskType.MACRO
        if "market" in answer:
            return ResearchTaskType.MARKET

        #default so a strange answer never crashes the run
        return ResearchTaskType.NEWS