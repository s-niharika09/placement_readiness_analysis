import json
from pathlib import Path

from analyzers.llm_client import LLMClient


class FeedbackGenerator:

    def __init__(self):

        self.llm = LLMClient()

        self.prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "feedback_prompt.txt"
        )

    def load_prompt(self):

        if not self.prompt_path.exists():

            raise FileNotFoundError(
                f"""
Feedback prompt not found.

Expected location:

{self.prompt_path}
"""
            )

        return self.prompt_path.read_text(
            encoding="utf-8"
        )

    def generate(
        self,
        prediction,
        resume_analysis,
        jd_analysis,
        skill_gap_analysis
    ):

        prompt = self.load_prompt()

        prompt = prompt.replace(
            "{prediction}",
            json.dumps(prediction, indent=2)
        )

        prompt = prompt.replace(
            "{resume_analysis}",
            json.dumps(resume_analysis, indent=2)
        )

        prompt = prompt.replace(
            "{job_description_analysis}",
            json.dumps(jd_analysis, indent=2)
        )

        prompt = prompt.replace(
            "{skill_gap_analysis}",
            json.dumps(skill_gap_analysis, indent=2)
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

JSON Error:
{e}

Raw Response:

{response}
"""
            )


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    prediction = {

        "placement_readiness_score": 82,

        "placement_readiness_level": "Moderately Ready"
    }

    resume_analysis = {

        "skills": [
            "Python",
            "SQL",
            "Power BI"
        ]
    }

    jd_analysis = {

        "job_title": "Python Developer",

        "required_skills": [
            "Python",
            "SQL",
            "AWS",
            "Docker"
        ]
    }

    skill_gap_analysis = {

        "matched_skills": [
            "Python",
            "SQL"
        ],

        "missing_skills": [
            "AWS",
            "Docker"
        ],

        "critical_missing_skills": [
            "AWS"
        ]
    }

    generator = FeedbackGenerator()

    result = generator.generate(

        prediction,

        resume_analysis,

        jd_analysis,

        skill_gap_analysis
    )

    print(json.dumps(result, indent=4))