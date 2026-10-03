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