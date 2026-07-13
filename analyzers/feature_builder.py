class FeatureBuilder:

    def __init__(self):
        pass

    def build_features(
        self,
        jd_analysis,
        skill_gap_analysis,
        resume_analysis
    ):

        required_skills = jd_analysis.get(
            "required_skills",
            []
        )

        critical_skills = jd_analysis.get(
            "critical_skills",
            []
        )

        matched_skills = skill_gap_analysis.get(
            "matched_skills",
            []
        )

        missing_skills = skill_gap_analysis.get(
            "missing_skills",
            []
        )

        critical_missing = skill_gap_analysis.get(
            "critical_missing_skills",
            []
        )

        # -----------------------------------
        # Skill Match %
        # -----------------------------------

        if required_skills:

            skill_match = (
                len(matched_skills)
                / len(required_skills)
            ) * 100

        else:

            skill_match = 0

        # -----------------------------------
        # Critical Skill Match %
        # -----------------------------------

        matched_critical = [

            skill

            for skill in critical_skills

            if skill in matched_skills

        ]

        if critical_skills:

            critical_match = (

                len(matched_critical)

                / len(critical_skills)

            ) * 100

        else:

            critical_match = 0

        # -----------------------------------
        # Missing Counts
        # -----------------------------------

        missing_count = len(missing_skills)

        critical_missing_count = len(
            critical_missing
        )

        # -----------------------------------
        # Resume Scores
        # -----------------------------------

        project_score = resume_analysis.get(
            "project_relevance_score",
            0
        )

        certification_score = resume_analysis.get(
            "certification_relevance_score",
            0
        )

        internship_score = resume_analysis.get(
            "internship_relevance_score",
            0
        )

        # Works with BOTH key names
        resume_score = resume_analysis.get(
            "resume_completeness_score",
            resume_analysis.get(
                "resume_completeness",
                0
            )
        )

        keyword_score = resume_analysis.get(
            "keyword_match_score",
            0
        )

        role_score = resume_analysis.get(
            "role_category_match_score",
            0
        )

        # -----------------------------------
        # Feature Dictionary
        # -----------------------------------

        features = {

            "skill_match_percentage":
                round(skill_match, 2),

            "critical_skill_match_percentage":
                round(critical_match, 2),

            "missing_skills_count":
                missing_count,

            "critical_missing_skills_count":
                critical_missing_count,

            "project_relevance_score":
                project_score,

            "certification_relevance_score":
                certification_score,

            "internship_relevance_score":
                internship_score,

            # MUST match the training dataset
            "resume_completeness_score":
                resume_score,

            "keyword_match_score":
                keyword_score,

            "role_category_match_score":
                role_score

        }

        return features