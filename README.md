# USD-AAI-520-Group-1

## University of San Diego

Master of Science in Applied Artificial Intelligence

---

## Team Members

- Marcelo D. Salvador
- Raul Muollo Diaz
- Akua Duffour

---

## Project Overview

This repository contains the source code, documentation, and supporting materials for the AAI 520 Final Team Project.

The objective of this project is to design, implement, and evaluate an AI-driven solution that addresses a real-world problem using modern artificial intelligence techniques and software engineering best practices.


# Local Development Setup

Follow these instructions to configure the Investment Research Agent on your local machine.

## 1. Prerequisites

Before starting, make sure you have the following installed:

- Git
- Python 3.11 or newer
- `pip`
- Jupyter Notebook or VS Code with the Jupyter extension

Check your Python installation:

```bash
python3 --version
```

You should see something similar to:

```text
Python 3.14.1
```

Check Git:

```bash
git --version
```

---

## 2. Clone the Repository

Clone the project from GitHub:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd investment_agent
```

Example:

```bash
git clone https://github.com/<username>/<repository-name>.git
cd <repository-name>/investment_agent
```

---

## 3. Create a Python Virtual Environment

A virtual environment keeps the project's Python packages isolated from packages installed globally on your computer.

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Once activated, your terminal should show something similar to:

```text
(.venv)
```

---

## 4. Upgrade pip

After activating the virtual environment:

```bash
python -m pip install --upgrade pip
```

---

## 5. Install Project Dependencies

Install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The project uses packages such as:

```text
pandas
numpy
yfinance
requests
python-dotenv
pydantic
langchain
langgraph
fredapi
fastapi
uvicorn
pytest
ipykernel
```

Do not install these globally. Install them while the `.venv` virtual environment is active.

---

## 6. Configure Environment Variables

The project uses a `.env` file to store API keys and other configuration values.

Create a file named:

```text
.env
```

inside the main `investment_agent` directory.

The structure should look similar to:

```text
investment_agent/
├── .env
├── main.py
├── requirements.txt
├── agents/
├── domain/
├── orchestration/
├── providers/
├── services/
├── memory/
└── tests/
```

Add the required environment variables:

```env
NEWS_API_KEY=your_newsapi_key
FRED_API_KEY=your_fred_api_key
GEMINI_API_KEY=your_gemini_api_key
SEC_USER_AGENT=InvestmentAgent your_email@example.com
```

### API Keys

#### NewsAPI

Create a NewsAPI account and obtain an API key from:

```text
https://newsapi.org/
```

Then:

```env
NEWS_API_KEY=your_actual_key
```

#### FRED

Create a FRED API key from:

```text
https://fred.stlouisfed.org/docs/api/api_key.html
```

Then:

```env
FRED_API_KEY=your_actual_key
```

#### Gemini

Create a Gemini API key using Google AI Studio:

```text
https://aistudio.google.com/apikey
```

Then:

```env
GEMINI_API_KEY=your_actual_key
```

#### SEC EDGAR

The SEC does not require a traditional API key.

Instead, requests should contain a valid `User-Agent` identifying the application and providing contact information.

Example:

```env
SEC_USER_AGENT=InvestmentAgent your_email@example.com
```

Each developer should use their own email address.

---

## 7. Protect the `.env` File

API keys must **never be committed to GitHub**.

Make sure `.env` is included in `.gitignore`.

Example:

```gitignore
# Environment variables
.env

# Python virtual environment
.venv/

# Python cache
__pycache__/
*.pyc

# Jupyter
.ipynb_checkpoints/
```

You can verify that Git is ignoring the file with:

```bash
git status
```

The `.env` file should not appear as a file ready to be committed.

---

## 8. Create a `.env.example` File

The repository should contain a `.env.example` file so developers know which variables are required.

Example:

```env
NEWS_API_KEY=
FRED_API_KEY=
GEMINI_API_KEY=
SEC_USER_AGENT=InvestmentAgent your_email@example.com
```

Unlike `.env`, `.env.example` **should be committed to GitHub**.

A new developer can then create their local configuration with:

### macOS / Linux

```bash
cp .env.example .env
```

### Windows

```powershell
Copy-Item .env.example .env
```

Then replace the placeholder values with the developer's own API keys.

---

## 9. Verify the `.env` File

The project uses `python-dotenv` to load environment variables.

Example:

```python
import os
from dotenv import load_dotenv

load_dotenv()

print("News API configured:", bool(os.getenv("NEWS_API_KEY")))
print("FRED API configured:", bool(os.getenv("FRED_API_KEY")))
print("Gemini API configured:", bool(os.getenv("GEMINI_API_KEY")))
print("SEC User Agent configured:", bool(os.getenv("SEC_USER_AGENT")))
```

Expected output:

```text
News API configured: True
FRED API configured: True
Gemini API configured: True
SEC User Agent configured: True
```

Do **not** print the actual API keys.

---

# Jupyter Notebook Setup

## 10. Install Jupyter Kernel Support

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install `ipykernel` if it was not already installed through `requirements.txt`:

```bash
pip install ipykernel
```

---

## 11. Register the Project as a Jupyter Kernel

Run:

```bash
python -m ipykernel install --user \
  --name investment-agent \
  --display-name "Python (Investment Agent)"
```

This creates a Jupyter kernel connected directly to the project's `.venv`.

You should see output similar to:

```text
Installed kernelspec investment-agent
```

---

## 12. Select the Kernel in VS Code

Open the project in VS Code.

Open a `.ipynb` notebook.

In the upper-right corner, click:

```text
Select Kernel
```

Then choose:

```text
Python (Investment Agent)
```

The notebook will now use the same Python environment and dependencies as the project.

---

## 13. Verify the Jupyter Kernel

Run this inside a notebook:

```python
import sys

print(sys.executable)
print(sys.version)
```

The executable should point to the project's `.venv`.

Example on macOS:

```text
.../investment_agent/.venv/bin/python
```

Example on Windows:

```text
...\investment_agent\.venv\Scripts\python.exe
```

---

# Verify the Project

## 14. Test Package Imports

Run:

```bash
python -c "import pandas, yfinance, requests, dotenv; print('Core dependencies OK')"
```

Expected result:

```text
Core dependencies OK
```

---

## 15. Run the Automated Tests

From the `investment_agent` directory:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

To run one test file:

```bash
pytest tests/test_data_sources.py -v
```

Example:

```bash
pytest tests/test_sec_provider.py -v
```

---

## 16. Run the Investment Agent

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Then run:

```bash
python main.py
```

---

# Returning to the Project Later

Every time you open a new terminal, you need to reactivate the virtual environment.

### macOS / Linux

```bash
cd investment_agent
source .venv/bin/activate
```

### Windows

```powershell
cd investment_agent
.venv\Scripts\Activate.ps1
```

You do **not** need to recreate the virtual environment or Jupyter kernel each time.

---

# Quick Setup Summary

For macOS/Linux:

```bash
git clone <repository-url>
cd <repository-name>/investment_agent

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

cp .env.example .env

python -m ipykernel install --user \
  --name investment-agent \
  --display-name "Python (Investment Agent)"

pytest -v
python main.py
```

For Windows PowerShell:

```powershell
git clone <repository-url>
cd <repository-name>\investment_agent

python -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

Copy-Item .env.example .env

python -m ipykernel install --user --name investment-agent --display-name "Python (Investment Agent)"

pytest -v
python main.py
```

---

# Common Problems

### `ModuleNotFoundError`

Make sure the virtual environment is active:

```bash
which python
```

macOS/Linux should point to:

```text
.../.venv/bin/python
```

On Windows:

```powershell
where python
```

It should point to:

```text
...\.venv\Scripts\python.exe
```

Then reinstall dependencies if necessary:

```bash
pip install -r requirements.txt
```

### API key returns `None`

Make sure:

1. `.env` exists inside the `investment_agent` directory.
2. The variable name is spelled correctly.
3. `python-dotenv` is installed.
4. The application calls `load_dotenv()`.

Example:

```python
from dotenv import load_dotenv

load_dotenv()
```

### VS Code is using the wrong Python environment

Open the VS Code Command Palette:

```text
Cmd + Shift + P
```

or on Windows:

```text
Ctrl + Shift + P
```

Select:

```text
Python: Select Interpreter
```

Then select the Python interpreter located inside:

```text
.venv
```

For notebooks, also make sure the selected kernel is:

```text
Python (Investment Agent)
```

### Jupyter kernel does not appear

Check installed kernels:

```bash
jupyter kernelspec list
```

If necessary, register it again:

```bash
python -m ipykernel install --user \
  --name investment-agent \
  --display-name "Python (Investment Agent)"
```
