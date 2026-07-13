import joblib
import pandas as pd
from pathlib import Path


class PlacementPredictor:
    """
    Loads the trained ML model and predicts
    placement readiness.
    """

    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent

        model_path = (
            base_dir
            / "models"
            / "placement_readiness_model.pkl"
        )

        scaler_path = (
            base_dir
            / "models"
            / "scaler.pkl"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found:\n{model_path}"
            )

        if not scaler_path.exists():
            raise FileNotFoundError(
                f"Scaler file not found:\n{scaler_path}"
            )

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

        self.label_map = {
            0: "Not Ready Yet",
            1: "Needs Improvement",
            2: "Moderately Ready",
            3: "Highly Ready"
        }

        self.feature_order = [
            "skill_match_percentage",
            "critical_skill_match_percentage",
            "missing_skills_count",
            "critical_missing_skills_count",
            "project_relevance_score",
            "certification_relevance_score",
            "internship_relevance_score",
            "resume_completeness_score",
            "keyword_match_score",
            "role_category_match_score"
        ]

    def predict(self, features):

        # Convert to DataFrame
        df = pd.DataFrame([features])

        # Preserve feature order
        df = df[self.feature_order]

        # Scale
        scaled_features = self.scaler.transform(df)

        # Predict class
        prediction = int(
            self.model.predict(scaled_features)[0]
        )

        # Predict probabilities
        probabilities = self.model.predict_proba(
            scaled_features
        )[0]

        # ----------------------------
        # Prediction Confidence
        # ----------------------------

        prediction_confidence = round(
            max(probabilities) * 100,
            2
        )

        # ----------------------------
        # Placement Readiness Score
        # ----------------------------

        readiness_score = round(
            (
                probabilities[0] * 0 +
                probabilities[1] * 35 +
                probabilities[2] * 70 +
                probabilities[3] * 100
            ),
            2
        )

        return {

            "placement_readiness_score":
                readiness_score,

            "placement_readiness_level":
                self.label_map[prediction],

            "prediction":
                prediction,

            "prediction_confidence":
                prediction_confidence,

            "class_probabilities": {

                "Not Ready Yet":
                    round(probabilities[0] * 100, 2),

                "Needs Improvement":
                    round(probabilities[1] * 100, 2),

                "Moderately Ready":
                    round(probabilities[2] * 100, 2),

                "Highly Ready":
                    round(probabilities[3] * 100, 2)
            }

        }


# -------------------------------------------------
# Testing
# -------------------------------------------------

if __name__ == "__main__":

    predictor = PlacementPredictor()

    sample_features = {

        "skill_match_percentage": 85,

        "critical_skill_match_percentage": 82,

        "missing_skills_count": 2,

        "critical_missing_skills_count": 1,

        "project_relevance_score": 8,

        "certification_relevance_score": 7,

        "internship_relevance_score": 9,

        "resume_completeness_score": 90,

        "keyword_match_score": 88,

        "role_category_match_score": 87

    }

    result = predictor.predict(sample_features)

    print(result)