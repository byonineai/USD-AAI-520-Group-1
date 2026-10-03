import os

from groq import Groq


class LLMClient:

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b"

    def complete(self, prompt, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=800,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content