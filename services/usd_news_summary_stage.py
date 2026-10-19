from services.usd_news_stage import USDNewsStage

class USDNewsSummaryStage(USDNewsStage):
  '''
  Produces the final financial-news summary in the USDNewsPipeline
  prompt chaining workflow.
  '''
  def __init__(self, llm_provider):
    self.llm_provider = llm_provider

  def process(
    self,
    context: dict
) -> dict:

    stock_symbol = context[
        "stock_symbol"
    ]

    classification = context[
        "classification"
    ]

    extracted_findings = context[
        "extracted_findings"
    ]
# AI-assisted prompt:
# Initial prompt wording was drafted with assistance from
# ChatGPT (OpenAI, 2026), then reviewed, revised, and tested
# by the project authors.

    prompt = f"""
You are the summarization stage of a financial
news research pipeline.

Create a concise financial-news research summary
for:

{stock_symbol}

Use only the extracted findings produced by the
previous stage.

Requirements:

- Prioritize directly relevant company news.
- Ignore irrelevant information.
- Separate facts from interpretation.
- Do not invent financial effects.
- Clearly state limitations.

CLASSIFICATION:

{classification}

EXTRACTED FINDINGS:

{extracted_findings}
"""

    summary = self.llm_provider.generate(
        prompt
    )

    context[
        "summary"
    ] = summary

    return context
