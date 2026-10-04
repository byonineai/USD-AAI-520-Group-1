"""

The routing pattern.

Takes a list of ResearchResult, returns a list of AnalysisResult. For each one
it asks the classifier what the content is, compares that to the label the data
layer put on it, and routes based on the answer.

Everything after this (starting with the analysis generator) works off the list
this returns.

"""


from domain.research_result import ResearchResult


class AnalysisPipeline:

    def __init__(self, router, classifier):
        self.router = router
        self.classifier = classifier

    def run(self, results):
        analyses = []

        for result in results:
            target = self.classifier.classify(str(result.data))

            #the classifier can disagree with where the data came from
            if target != result.task_type:
                print("Routed to " + target.value)
                result = ResearchResult(
                    task_type=target,
                    symbol=result.symbol,
                    data=result.data
                )

            analyzer = self.router.get_analyzer(result.task_type)
            analyses.append(analyzer.analyze(result))

        return analyses