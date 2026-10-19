from services.usd_news_stage import USDNewsStage
import json
class USDNewsClassificationStage(USDNewsStage):
  '''
  Classifies preprocessed financial news as part of the USDNewsPipeline workflow

  '''
  def __init__(self, llm_provider):

    # Dependency injection: The language model provider is supplied from outside this class
    # which keeps the classification stage independent of the specific LLM implementation
    self.llm_provider = llm_provider

  def process(self, context: dict):

    stock_symbol = context[
      "stock_symbol"
    ]

    articles = context[
      "articles"
    ]

    articles_json = json.dumps(
      articles,
      indent=2,
      default=str
    )

    prompt = f"""
        You are a financial news classifier.

        The company being researched has stock symbol:

        {stock_symbol}

        Classify each article into one of:

        - earnings
        - product
        - market
        - technology
        - irrelevant
        - partnership
        - regulation
        - customer
        - financing
        - competition

        For every article provide:

        - title
        - category
        - relevance

        Also classify relevance as:

        - indirect
        - irrelevant
        - direct

        Rules:

        - Use only the supplied article information.
        - Do not invent facts.
        - Articles unrelated to {stock_symbol} should be
          classified as irrelevant.
        - Preserve the title so later stages can connect
          the classification to the original article.

        ARTICLES:

        {articles_json}

    """

    classification = (
      self.llm_provider.generate(
        prompt
      )
    )

    context[
      "classification"
    ] = classification

    return context
