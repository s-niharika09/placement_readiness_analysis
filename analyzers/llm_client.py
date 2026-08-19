import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class LLMClient:

    """
    LLMClient = "A wrapper class that handles communication between my application and the Groq LLM API."

    It loads the API key and model configuration from environment variables using python-dotenv, 
    validates that the API key exists, 
    and initializes the Groq client. 
    Its generate() method accepts a prompt, 
    sends it to the configured LLM using the chat-completion API, 
    with a low temperature of 0.2 for consistent output, and returns the generated text. 
    I separated this functionality from the individual analyzers so that Resume Analyzer, 
    Skill Gap Analyzer and other LLM-based components can reuse the same API communication layer."

    """

    def __init__(self):

        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file."
            )

        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
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