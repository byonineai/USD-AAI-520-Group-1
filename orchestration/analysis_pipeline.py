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