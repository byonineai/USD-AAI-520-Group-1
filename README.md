# USD-AAI-520-Group-1

## University of San Diego

Master of Science in Applied Artificial Intelligence

---

## Team Members

- Marcelo D. Salvador
- Raul Muollo Diaz
- Akua Duffour

---

# Autonomous Investment Research Agent

This project is part of the **AAI-520 Natural Language Processing and Generative AI** course in the Applied Artificial Intelligence Program at the **University of San Diego (USD)**.

**Project Status:** Completed

---

## Project Introduction

The Autonomous Investment Research Agent is a multi-agent financial research system designed to analyze a publicly traded company from multiple perspectives using a single stock ticker as input.

The system coordinates specialist agents responsible for:

- Market analysis
- Macroeconomic analysis
- Earnings and SEC filing analysis
- Financial news analysis

Rather than relying on a single API or a single large language model prompt, the application separates planning, data retrieval, specialist analysis, prompt chaining, aggregation, generation, evaluation, optimization, and memory into modular components.

The final specialist findings are aggregated and provided to **Google Gemini**, which produces a grounded investment research synthesis based on the collected evidence.

> **Disclaimer:** This project is intended for educational and research purposes only and does not constitute financial or investment advice.

---

# Project Objectives

The primary objectives of the project are to demonstrate an autonomous agent capable of:

1. Planning research steps for a requested stock symbol.
2. Dynamically selecting external tools and data providers.
3. Routing research tasks to specialized agents.
4. Performing multi-stage prompt chaining.
5. Aggregating findings from multiple research domains.
6. Generating an LLM-based investment research synthesis.
7. Evaluating the quality of generated research.
8. Requesting additional research when quality requirements are not satisfied.
9. Persisting research memory across application runs.

---

# Agentic Workflow

The overall research lifecycle is:

```text
Stock Symbol
     ↓
USDResearchPlanner
     ↓
Research Tasks
     ↓
USDToolRegistry
     ↓
External Data Adapters
     ↓
Normalized Domain Models
     ↓
USDAgentRouter
     ↓
Specialist Agents
     ↓
USDAnalysisResult
     ↓
USDResultAggregator
     ↓
USDAnalysisGenerator
     ↓
Gemini
     ↓
USDAnalysisEvaluator
     ↓
     Pass?
    /     \
  Yes      No
   ↓        ↓
Complete  USDAnalysisOptimizer
             ↓
       Additional Research
             ↓
           Retry
```

---

# Research Specialists

The application currently contains four research specialists.

| Research Task         | Data Provider | Specialist           |
| --------------------- | ------------- | -------------------- |
| `market_analysis`   | Yahoo Finance | `USDMarketAgent`   |
| `macro_analysis`    | FRED          | `USDMacroAgent`    |
| `earnings_analysis` | SEC EDGAR     | `USDEarningsAgent` |
| `news_analysis`     | NewsAPI       | `USDNewsAgent`     |

Each specialist returns a standardized:

```python
USDAnalysisResult(
    agent=...,
    summary=...,
    evidence=...
)
```

Using a common result structure allows findings from different research domains to be aggregated consistently.

---

# Design Patterns

## Strategy Pattern

The specialist agents implement a common analysis strategy interface.

```text
USDAnalysisStrategy
        ↑
        ├── USDMarketAgent
        ├── USDMacroAgent
        ├── USDEarningsAgent
        └── USDNewsAgent
```

Each specialist provides different domain-specific analysis while conforming to the same analysis contract.

---

## Adapter Pattern

External providers expose different APIs and response formats.

Dedicated adapters isolate those differences from the specialist agents:

```text
Yahoo Finance
     ↓
USDYahooFinanceAdapter
     ↓
USDMarketData

FRED
     ↓
USDFredAdapter
     ↓
USDMacroData

SEC EDGAR
     ↓
USDSecEdgarAdapter
     ↓
USDEarningsData

NewsAPI
     ↓
USDNewsApiAdapter
     ↓
USDNewsData
```

This prevents external API details from leaking into the agent analysis layer.

---

## Registry and Routing

Tools and specialist agents are registered using research task types.

```text
market_analysis
macro_analysis
earnings_analysis
news_analysis
```

The application uses:

- `USDToolRegistry` to resolve tools
- `USDAgentRegistry` to store specialist strategies
- `USDAgentRouter` to select the appropriate specialist

For example:

```text
earnings_analysis
       ↓
USDToolRegistry
       ↓
USDSecEdgarAdapter
```

and:

```text
earnings_analysis
       ↓
USDAgentRouter
       ↓
USDAgentRegistry
       ↓
USDEarningsAgent
```

---

# Prompt Chaining

The News specialist uses a dedicated prompt-chaining pipeline rather than placing all language-model logic directly inside `USDNewsAgent`.

```text
NewsAPI
   ↓
USDNewsApiAdapter
   ↓
USDNewsData
   ↓
USDNewsAgent
   ↓
USDNewsPipeline
   ↓
USDNewsPreprocessStage
   ↓
USDNewsClassificationStage
   ↓
USDNewsExtractionStage
   ↓
USDNewsSummaryStage
   ↓
USDAnalysisResult
```

The pipeline maintains a shared context:

```python
{
    "stock_symbol": ...,
    "articles": ...,
    "classification": ...,
    "extracted_findings": ...,
    "summary": ...
}
```

This allows information produced by one stage to become input to the next stage while preserving the original article evidence.

---

# Evaluator–Optimizer Workflow

After specialist results are aggregated, Gemini generates a combined research analysis.

The generated result is evaluated before being accepted as final.

```text
Generate
   ↓
Evaluate
   ↓
   Pass?
  /    \
Yes     No
 ↓       ↓
Done   Optimize
          ↓
   Request Research
          ↓
       Collect
          ↓
       Analyze
          ↓
      Aggregate
          ↓
       Generate
          ↓
       Evaluate
```

The retry process is bounded using:

```python
max_retries = 2
```

If quality requirements are still not satisfied after the retry limit, unresolved research gaps are included in the final report.

---

# Persistent Research Memory

Research results can persist between executions using:

```text
USDResearchMemory
       ↓
USDJsonMemoryRepository
       ↓
JSON Storage
```

Stored research can include:

- Stock symbol
- Specialist summaries
- Supporting evidence
- Quality status
- Unresolved research gaps

This provides application-level memory across research runs without modifying the underlying LLM weights.

---

# Data Sources

The application uses the following external financial and economic sources.

## Yahoo Finance

Used for market information such as:

- Stock price
- Trading volume

Accessed through the `yfinance` Python library.

No API key is required for `yfinance`.

---

## Federal Reserve Economic Data — FRED

Used for macroeconomic indicators such as:

- Federal Funds Rate
- Consumer Price Index
- Unemployment Rate
- 10-Year Treasury Rate

A FRED API key is required.

---

## SEC EDGAR

Used for company filings and financial facts such as:

- 10-K
- 10-Q
- Revenue
- Gross profit
- Operating income
- Net income
- Diluted EPS

SEC EDGAR requires an appropriate user-agent header identifying the application/requestor.

---

## NewsAPI

Used to retrieve recent financial news articles related to the researched company.

A NewsAPI key is required.

---

## Google Gemini

Gemini is used for:

- News classification
- News information extraction
- News summarization
- Final multi-domain research synthesis

A Gemini API key is required.

---

# Methods Used

The project applies several artificial intelligence and software engineering techniques:

- Natural Language Processing
- Generative AI
- Large Language Models
- Agentic AI
- Multi-Agent Systems
- Prompt Chaining
- Dynamic Routing
- Evaluator–Optimizer workflows
- Financial data retrieval
- API integration
- Object-Oriented Programming
- Design Patterns
- Persistent Memory
- Prompt Engineering

---

# Technologies

The project uses:

- Python
- Google Gemini
- Yahoo Finance / `yfinance`
- FRED API
- SEC EDGAR
- NewsAPI
- Jupyter Notebook
- Git
- GitHub
- JSON
- Python virtual environments

---

# Project Structure

A representative project structure is:

```text
USD-AAI-520-Group-1/
│
├── agents/
│   ├── usd_analysis_strategy.py
│   ├── usd_market_agent.py
│   ├── usd_macro_agent.py
│   ├── usd_earnings_agent.py
│   └── usd_news_agent.py
│
├── domain/
│   ├── usd_analysis_result.py
│   ├── usd_market_data.py
│   ├── usd_macro_data.py
│   ├── usd_earnings_data.py
│   ├── usd_news_data.py
│   ├── usd_research_task.py
│   ├── usd_research_memory.py
│   └── usd_final_report.py
│
├── tools/
│   ├── usd_research_tool.py
│   ├── usd_yahoo_finance_adapter.py
│   ├── usd_fred_adapter.py
│   ├── usd_sec_edgar_adapter.py
│   ├── usd_news_api_adapter.py
│   ├── usd_llm_provider.py
│   └── usd_gemini_adapter.py
│
├── orchestration/
│   ├── usd_research_planner.py
│   ├── usd_tool_registry.py
│   ├── usd_agent_registry.py
│   ├── usd_agent_router.py
│   ├── usd_research_state.py
│   └── usd_research_orchestrator.py
│
├── services/
│   ├── usd_result_aggregator.py
│   ├── usd_analysis_generator.py
│   ├── usd_analysis_evaluator.py
│   ├── usd_analysis_optimizer.py
│   ├── usd_final_report_builder.py
│   │
│   ├── usd_news_stage.py
│   ├── usd_news_pipeline.py
│   ├── usd_news_preprocess_stage.py
│   ├── usd_news_classification_stage.py
│   ├── usd_news_extraction_stage.py
│   └── usd_news_summary_stage.py
│
├── memory/
│   ├── usd_memory_repository.py
│   └── usd_json_memory_repository.py
│
├── utils/
│   └── usd_console_status.py
│
├── tests/
│
├── main.ipynb
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Installation and Local Development Setup

## 1. Prerequisites

Install the following before beginning:

- Python 3.11+ recommended
- Git
- Visual Studio Code
- Jupyter extension for VS Code

Verify Python:

```bash
python3 --version
```

Verify Git:

```bash
git --version
```

---

## 2. Clone the Repository

Clone the project:

```bash
git clone https://github.com/byonineai/USD-AAI-520-Group-1
```

Move into the repository:

```bash
cd USD-AAI-520-Group-1
```

---

# 3. Create a Python Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

---

# 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 5. Install Project Dependencies

Install all required packages:

```bash
python -m pip install -r requirements.txt
```

If working directly from a Jupyter notebook, you can also run:

```python
%pip install -r requirements.txt
```

---

# 6. Environment Configuration

Create a `.env` file in the project root:

```text
USD-AAI-520-Group-1/
│
├── .env
├── requirements.txt
├── README.md
└── ...
```

Example:

```env
NEWS_API_KEY=your_newsapi_key_here

FRED_API_KEY=your_fred_api_key_here

GEMINI_API_KEY=your_gemini_api_key_here

SEC_USER_AGENT="Your Name your_email@example.com"
```

> **Important:** The exact Gemini environment variable should match the name expected by `USDGeminiAdapter`. If your implementation uses `GOOGLE_API_KEY` instead of `GEMINI_API_KEY`, configure that variable instead.

Never commit `.env` to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
```

---

# 7. API Key Setup

## NewsAPI

Create an API key from:

```text
https://newsapi.org/
```

Add it to `.env`:

```env
NEWS_API_KEY=your_key
```

---

## FRED

Create a FRED API key from:

```text
https://fred.stlouisfed.org/docs/api/api_key.html
```

Add:

```env
FRED_API_KEY=your_key
```

---

## Gemini

Create a Gemini API key using Google AI Studio.

Add the key using the environment-variable name expected by the Gemini adapter:

```env
GEMINI_API_KEY=your_key
```

or, if configured that way:

```env
GOOGLE_API_KEY=your_key
```

---

## SEC EDGAR

SEC EDGAR does not require a conventional API key, but requests should contain a descriptive user-agent.

Example:

```env
SEC_USER_AGENT="Student Research Project student@example.com"
```

Do not use fake contact information when making SEC requests.

---

# 8. Configure Jupyter Kernel

With the virtual environment activated, install `ipykernel`:

```bash
python -m pip install ipykernel
```

Create a Jupyter kernel:

```bash
python -m ipykernel install \
  --user \
  --name usd-aai-520 \
  --display-name "Python (USD AAI 520)"
```

In VS Code:

1. Open `main.ipynb`.
2. Click the kernel selector in the upper-right corner.
3. Select:

```text
Python (USD AAI 520)
```

Confirm the notebook is using the expected Python environment:

```python
import sys

print(sys.executable)
```

The path should point to the project's `.venv`.

---

# 9. Run Jupyter Locally

If using VS Code, open the notebook and execute the cells normally.

Alternatively, start Jupyter from the command line:

```bash
jupyter notebook
```

or:

```bash
jupyter lab
```

Jupyter will provide a local URL similar to:

```text
http://localhost:8888
```

Open that URL in a browser and select the project notebook.

> This project currently runs as a Python/Jupyter research application. `localhost:8888` refers to the local Jupyter server; it is not a separate web application server unless a UI layer is added to the project.

---

# 10. Verify Dependencies

Test Yahoo Finance:

```python
import yfinance as yf

print("yfinance working")
```

Test FRED:

```python
from fredapi import Fred

print("fredapi working")
```

Test Gemini:

```python
from google import genai

print("Google GenAI working")
```

Test project imports:

```python
from orchestration.usd_research_planner import USDResearchPlanner
from orchestration.usd_research_orchestrator import USDResearchOrchestrator

from agents.usd_market_agent import USDMarketAgent
from agents.usd_macro_agent import USDMacroAgent
from agents.usd_earnings_agent import USDEarningsAgent
from agents.usd_news_agent import USDNewsAgent

print("Project imports successful")
```

---

# 11. Run the Research Agent

Set a stock ticker:

```python
STOCK_SYMBOL = "MSFT"
```

Then run the configured orchestrator:

```python
report = orchestrator.run(
    STOCK_SYMBOL
)
```

A successful execution should transition through states similar to:

```text
planning
↓
collecting
↓
analyzing
↓
aggregating
↓
generating
↓
evaluating
↓
complete
```

A successful four-specialist run should report:

```text
STATUS: complete
SPECIALISTS: 4
RETRIES: 0
UNRESOLVED GAPS: []
```

The exact retry count can vary if the evaluator determines additional research is required.

---

# 12. Verify the News Prompt Chain

The News pipeline can also be executed independently.

```python
news_data = news_adapter.fetch(
    "MSFT"
)

pipeline_result = news_pipeline.run(
    news_data
)
```

Verify the context:

```python
print(
    pipeline_result.keys()
)
```

Expected structure:

```text
dict_keys([
    'stock_symbol',
    'articles',
    'classification',
    'extracted_findings',
    'summary'
])
```

The expected workflow is:

```text
Ingest
  ↓
Preprocess
  ↓
Classify
  ↓
Extract
  ↓
Summarize
```

---

# Local Development Troubleshooting

## `ModuleNotFoundError`

If a package is missing:

```bash
python -m pip install -r requirements.txt
```

For example:

```bash
python -m pip install fredapi
```

Inside Jupyter:

```python
%pip install fredapi
```

---

## Jupyter Uses the Wrong Python Environment

Check:

```python
import sys

print(sys.executable)
```

If the path does not point to `.venv`, switch the Jupyter kernel to the project environment.

---

## Gemini Import Error

For code using:

```python
from google import genai
```

install:

```bash
python -m pip install --upgrade google-genai
```

Do not confuse this package with the older:

```text
google-generativeai
```

SDK.

---

## Environment Variables Are Not Loading

Confirm `.env` exists in the project root.

You can test:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print(
    bool(
        os.getenv(
            "NEWS_API_KEY"
        )
    )
)
```

Do not print actual API keys in notebooks, logs, screenshots, or GitHub commits.

---

# Git Development Workflow

The team should avoid implementing features directly on `main`.

A recommended workflow is:

```text
main
 ↓
development branch
 ↓
feature branch
 ↓
pull request / merge
```

For example:

```bash
git checkout dev-4
git pull origin dev-4
```

Create a feature branch:

```bash
git checkout -b feature/news-prompt-chain
```

Make changes and commit:

```bash
git add .
git commit -m "Add staged prompt chaining to news analysis"
```

Push:

```bash
git push -u origin feature/news-prompt-chain
```

After review, merge the feature into the development branch.

Before starting new work, synchronize with the latest development branch:

```bash
git checkout dev-2
git pull origin dev-2
```

---

# Partner(s) / Contributors

Add team members here:

- **Marcelo Salvador**
- **Akua Duffour**
- **Raul Diaz**

Course:

**AAI-520 — Natural Language Processing and Generative AI**
University of San Diego
Applied Artificial Intelligence Program

---

# AI Use Disclosure

ChatGPT (OpenAI, 2026) was used as a documentation and coding assistant during the project's development phases. All experimental analysis, architectural decisions, implementation choices, validation, and interpretations remain the responsibility of the project authors.

---

# License

This project was developed for academic use as part of the University of San Diego Applied Artificial Intelligence program.

If the repository is intended for public reuse, an open-source license such as the MIT License may be added in a separate `LICENSE` file.

---

# Acknowledgments

The project authors acknowledge the University of San Diego Applied Artificial Intelligence program and course faculty for project guidance and instructional support.

The project also uses external data and services provided by:

- Yahoo Finance / `yfinance`
- Federal Reserve Economic Data (FRED)
- U.S. Securities and Exchange Commission EDGAR
- NewsAPI
- Google Gemini

---

# References

- Aroussi, R. *yfinance*. GitHub.
- Federal Reserve Bank of St. Louis. *Federal Reserve Economic Data (FRED)*.
- NewsAPI. *News API*.
- U.S. Securities and Exchange Commission. *EDGAR*.
- Google. *Gemini*.
- Shvets, A. (2021). *Dive into design patterns*. Refactoring.Guru.
- OpenAI. (2026). *ChatGPT* [Large language model].
