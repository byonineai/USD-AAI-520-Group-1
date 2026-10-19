import os

from dotenv import load_dotenv
from google import genai

from tools.usd_llm_provider_interface import USDLLMProviderInterface

load_dotenv()

class USDGeminiAdapter(USDLLMProviderInterface):
  '''
   LLM provider that adapts to the Google Gemini SDK.
   Responsible to load the Gemini API key and model configuration
   Initiate the Gemini client
   Send prompts
  '''

  def __init__(
    self,
    api_key: str | None = None,
    model: str | None = None
  ):
     self.api_key = (
       api_key
       or os.getenv("GEMINI_API_KEY")
     )

     if not self.api_key:
       raise ValueError(
         "The Gemini api key is not configured!"
       )

     self.model = (
         model
         or os.getenv(
           'GEMINI_MODEL',
           'gemini-3.8-flash'
         )
       )

     self.client = genai.Client(
         api_key = self.api_key
       )

  def generate(
         self,
         prompt: str
       ) -> str:

    llm_interaction = self.client.interactions.create(
        model = self.model,
           input = prompt
        )

    return llm_interaction.output_text
