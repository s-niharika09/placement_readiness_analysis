import json
from pathlib import Path

from analyzers.llm_client import LLMClient


class SkillGapAnalyzer:
    """
    Uses Groq to compare the analyzed Resume and
    Job Description and identify the candidate's skill gap.
    """

    def __init__(self):

        self.llm = LLMClient()

        self.prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "skill_gap_prompt.txt"
        )

    def load_prompt(self):

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"Prompt file not found:\n{self.prompt_path}"
            )

        return self.prompt_path.read_text(
            encoding="utf-8"
        )

    def analyze(
        self,
        resume_analysis,
        jd_analysis
    ):

        # Load prompt
        prompt = self.load_prompt()

        # Replace placeholders
        prompt = prompt.replace(
            "{resume_analysis}",
            json.dumps(resume_analysis, indent=2)
        )

        prompt = prompt.replace(
            "{job_description_analysis}",
            json.dumps(jd_analysis, indent=2)
        )

        # Call Groq
        response = self.llm.generate(prompt)

        # Clean markdown if present
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


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    sample_resume_analysis = {

        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Power BI",
            "Pandas",
            "Git"
        ],

        "resume_category": "Data Science"
    }

    sample_jd_analysis = {

        "job_title": "Data Scientist",

        "required_skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "AWS",
            "Git"
        ],

        "critical_skills": [
            "Python",
            "Machine Learning",
            "AWS",
            "TensorFlow"
        ],

        "optional_skills": [
            "Docker",
            "Power BI"
        ]
    }

    analyzer = SkillGapAnalyzer()

    result = analyzer.analyze(
        sample_resume_analysis,
        sample_jd_analysis
    )

    print(json.dumps(result, indent=4))