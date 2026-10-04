"""
Every model call in the project goes through here.

One place for the provider and model. Groq was not the first choice, Google would not issue
a key on a USD account.

Temperature is an argument and not a constant because the classifier needs the
same answer every time and the analysts do not.

"""


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