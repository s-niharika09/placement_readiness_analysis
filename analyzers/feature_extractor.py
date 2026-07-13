import json
from pathlib import Path

from analyzers.llm_client import LLMClient


class FeatureExtractor:
    """
    Uses Groq to extract numerical ML features
    from the Resume and Job Description.
    """

    def __init__(self):
        self.llm = LLMClient()

        self.prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "feature_extraction_prompt.txt"
        )

    def load_prompt(self):

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt file not found:\n{self.prompt_path}"
            )

        return self.prompt_path.read_text(
            encoding="utf-8"
        )

    def extract_features(
        self,
        resume_text,
        job_description
    ):

        prompt = self.load_prompt()

        prompt = prompt.replace(
            "{resume_text}",
            resume_text.strip()
        )

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


# -----------------------------------------------------
# Testing
# -----------------------------------------------------

if __name__ == "__main__":

    sample_resume = """
    Python
    SQL
    Machine Learning
    Power BI

    Projects:
    Placement Readiness Analyzer

    Internship:
    Data Science Intern

    Certifications:
    Google Data Analytics
    """

    sample_jd = """
    Looking for a Python Developer.

    Required Skills:
    Python
    SQL
    Machine Learning
    AWS
    Docker
    Power BI
    """

    extractor = FeatureExtractor()

    result = extractor.extract_features(
        sample_resume,
        sample_jd
    )

    print(json.dumps(result, indent=4))