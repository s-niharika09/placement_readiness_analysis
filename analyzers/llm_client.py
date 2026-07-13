import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMClient:

    def __init__(self):

        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file."
            )

        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.client = Groq(
            api_key=self.api_key
        )

    def generate(self, prompt):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content.strip()


if __name__ == "__main__":

    llm = LLMClient()

    result = llm.generate(
        "Say hello in one sentence."
    )

    print(result)