from agents.usd_analysis_strategy import USDAnalysisStrategy
from domain.usd_news_data import USDNewsData
from domain.usd_analysis_result import USDAnalysisResult
from services.usd_news_pipeline import USDNewsPipeline

class USDNewsAgent(USDAnalysisStrategy):

    def __init__(
        self,
        pipeline: USDNewsPipeline
    ):
        self.pipeline = pipeline

    def analyze(
        self,
        data: USDNewsData
    ) -> USDAnalysisResult:

        if not data.articles:
            return USDAnalysisResult(
                summary=(
                    f"No recent news articles were found "
                    f"for {data.stock_symbol}."
                ),
                agent="news",
                evidence=[]
            )

        # Run:
        # Preprocess -> Classify -> Extract -> Summarize
        pipeline_result = self.pipeline.run(
            data
        )

        summary = pipeline_result[
            "summary"
        ]

        evidence = []

        # Preserve original source evidence
        for article in pipeline_result[
            "articles"
        ][:5]:

            evidence.append(
                f"{article['source']}: "
                f"{article['title']}"
            )

        # Preserve the extraction stage output
        extracted_findings = pipeline_result.get(
            "extracted_findings"
        )

        if extracted_findings:
            evidence.append(
                "PROMPT_CHAIN_EXTRACTED_FINDINGS:\n"
                f"{extracted_findings}"
            )

        return USDAnalysisResult(
            summary=summary,
            agent="news",
            evidence=evidence
        )
 