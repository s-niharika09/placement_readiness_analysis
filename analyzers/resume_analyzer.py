import json
from pathlib import Path

from analyzers.llm_client import LLMClient


class ResumeAnalyzer:
    """
    Uses Groq to analyze a resume and return structured JSON.

    ResumeAnalyzer takes extracted resume text, 
    sends it to the Groq LLM using a predefined prompt, 
    and converts the LLM's response into structured JSON for downstream processing.
    """

    def __init__(self):
        self.llm = LLMClient()

        self.prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "resume_analyzer_prompt.txt"
        )

    def load_prompt(self):

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt file not found:\n{self.prompt_path}"
            )

        return self.prompt_path.read_text(
            encoding="utf-8"
        )

    def analyze(self, resume_text):

        prompt = self.load_prompt()

        prompt = prompt.replace(
            "{resume_text}",
            resume_text.strip()
        )

        response = self.llm.generate(prompt)

        cleaned = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            result = json.loads(cleaned)

            return result

        except json.JSONDecodeError as e:

            raise ValueError(
                f"""
Groq returned invalid JSON.

Error:
{e}

Raw Response:
{response}
"""
            )


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    sample_resume = """
Niharika

Skills
-------
Python
SQL
Machine Learning
Power BI

Projects
---------
Placement Readiness Analyzer

Customer Churn Prediction

Internship
-----------
Data Science Intern

Certifications
--------------
Google Data Analytics

Education
----------
B.Tech Electronics and Communication Engineering
"""

    analyzer = ResumeAnalyzer()

    result = analyzer.analyze(sample_resume)

    print(json.dumps(result, indent=4))