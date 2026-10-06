from dotenv import load_dotenv
import os

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

FRED_API_KEY = os.getenv("FRED_API_KEY")

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")