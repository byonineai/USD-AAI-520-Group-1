import json

from services.usd_news_stage import USDNewsStage


class USDNewsExtractionStage(USDNewsStage):
    """
    Extracts financial and business findings from
    classified news.

    This is Prompt 2 in the news prompt chain.
    """

    def __init__(
        self,
        llm_provider
    ):
        self.llm_provider = llm_provider

    def process(
        self,
        context: dict
    ) -> dict:

        stock_symbol = context[
            "stock_symbol"
        ]

        articles = context[
            "articles"
        ]

        classification = context[
            "classification"
        ]

        articles_json = json.dumps(
            articles,
            indent=2,
            default=str
        )

        prompt = f"""
You are the extraction stage of a financial
news analysis pipeline.

The company being researched is:

{stock_symbol}

The previous prompt classified the supplied
news articles.

Using the classification AND the original
article information below, extract relevant
financial and business findings.

For each relevant article extract when available:

- title
- company
- event
- category
- partner
- customer
- competitor
- product
- business area
- financial impact
- risk
- opportunity
- source
- relevance

Rules:

- Ignore articles classified as irrelevant.
- Do not invent information.
- If information is unavailable, use
  "not provided".
- Do not infer financial impact that is not
  explicitly supported.
- Do not infer a trend from one article.
- Preserve the source and title.

CLASSIFICATION FROM PREVIOUS PROMPT:

{classification}

ORIGINAL ARTICLES:

{articles_json}
"""

        extracted_findings = (
            self.llm_provider.generate(
                prompt
            )
        )

        context[
            "extracted_findings"
        ] = extracted_findings

        return context