import json
from pathlib import Path

from analyzers.llm_client import LLMClient


class JobDescriptionAnalyzer:
    """
    Uses Groq to analyze a Job Description
    and extract structured information.
    The job_description.py module is responsible for analyzing a job description 
    and converting unstructured job-description text into structured information. 
    created a JobDescriptionAnalyzer class that uses an LLMClient to communicate with the Groq API. 
    The prompt is stored separately in a text file, which is loaded using Python's Path class. 
    The actual job description is inserted into the prompt and sent to the LLM. 
    Since the LLM returns JSON, It cleans any Markdown code fences and use json.loads() 
    to convert the response into a Python dictionary. 
    Also added exception handling to catch invalid JSON responses.
    
    """

    def __init__(self):

        self.llm = LLMClient()

        self.prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "job_description_prompt.txt"
        )

    def load_prompt(self):

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt file not found:\n{self.prompt_path}"
            )

        return self.prompt_path.read_text(
            encoding="utf-8"
        )

    def analyze(self, job_description):

        prompt = self.load_prompt()

        prompt = prompt.replace(
            "{job_description}",
            job_description.strip()
        )

        response = self.llm.generate(prompt)

        cleaned = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            return json.loads(cleaned)

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

    sample_jd = """
    We are looking for a Python Data Scientist.

    Required Skills:
    Python
    SQL
    Machine Learning
    Pandas
    NumPy

    Preferred Skills:
    Power BI
    AWS

    Responsibilities:
    Build ML models
    Analyze data
    Create dashboards

    Soft Skills:
    Communication
    Teamwork
    Problem Solving
    """

    analyzer = JobDescriptionAnalyzer()

    result = analyzer.analyze(sample_jd)

    print(json.dumps(result, indent=4))