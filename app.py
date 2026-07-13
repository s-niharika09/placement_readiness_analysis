import tempfile
import os
import json
import io
import pandas as pd
import streamlit as st

# Optional: Import reportlab for PDF generation
try:
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from analyzers.resume_parser import ResumeParser
from analyzers.resume_analyzer import ResumeAnalyzer
from analyzers.job_description import JobDescriptionAnalyzer
from analyzers.skillgap_analyzer import SkillGapAnalyzer
from analyzers.feature_builder import FeatureBuilder
from analyzers.predict import PlacementPredictor
from analyzers.feedback_generator import FeedbackGenerator

# ==========================================================
# Helper Function for PDF Generation
# ==========================================================
def generate_pdf_report(prediction, match_report):
    """Generates a basic PDF report using ReportLab."""
    buffer = io.BytesIO()
    if REPORTLAB_AVAILABLE:
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "AI Placement Readiness Report")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 760, f"Readiness Score: {prediction.get('placement_readiness_score', 0):.1f}/100")
        p.drawString(100, 740, f"Readiness Level: {prediction.get('placement_readiness_level', 'N/A')}")
        p.drawString(100, 720, f"Target Role: {match_report.get('job_title', 'N/A')}")
        
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 680, "Job Match Summary")
        p.setFont("Helvetica", 10)
        
        # Simple text wrap logic for the summary
        summary = match_report.get("job_match_summary", "")
        y_pos = 660
        for line in [summary[i:i+80] for i in range(0, len(summary), 80)]:
            p.drawString(100, y_pos, line)
            y_pos -= 20
            
        p.showPage()
        p.save()
    else:
        buffer.write(b"ReportLab is not installed. Run 'pip install reportlab' to enable PDF generation.")
    
    buffer.seek(0)
    return buffer

# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Placement Readiness Analyzer",
    page_icon="🎯",
    layout="wide"
)

# ==========================================================
# Initialize Components
# ==========================================================

resume_parser = ResumeParser()
resume_analyzer = ResumeAnalyzer()
jd_analyzer = JobDescriptionAnalyzer()
skill_gap_analyzer = SkillGapAnalyzer()
feature_builder = FeatureBuilder()
predictor = PlacementPredictor()
feedback_generator = FeedbackGenerator()

# ==========================================================
# Header
# ==========================================================

st.title("🎯 AI Placement Readiness Analyzer")

st.markdown("""
This application evaluates a student's placement readiness by combining:

- 📄 Resume Analysis
- 💼 Job Description Analysis
- 🧠 Skill Gap Detection
- 🤖 Machine Learning Prediction
- 💡 AI-Powered Career Recommendations
""")

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:
    st.header("Project Workflow")
    st.markdown("""
1. Upload Resume
2. Paste Job Description
3. Resume Analysis
4. Job Description Analysis
5. Skill Gap Analysis
6. Feature Engineering
7. ML Prediction
8. AI Recommendations
""")

# ==========================================================
# Input Section
# ==========================================================

st.header("📥 Upload Inputs")

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

analyze_button = st.button(
    "🚀 Analyze Resume"
)

# ==========================================================
# Main Pipeline (Computation Only)
# ==========================================================

if analyze_button:
    if resume_file is None:
        st.error("Please upload a Resume PDF.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please paste the Job Description.")
        st.stop()

    try:
        with st.spinner("Analyzing Resume...\nThis may take 10–20 seconds."):

            # Save Uploaded Resume
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(resume_file.read())
                temp_pdf_path = temp_file.name

            # Extract Text
            resume_text = resume_parser.extract_text(temp_pdf_path)
            os.remove(temp_pdf_path) # Cleanup

            # --------------------------------------
            # SAVE TO SESSION STATE
            # --------------------------------------
            st.session_state.resume_analysis = resume_analyzer.analyze(resume_text)
            
            st.session_state.jd_analysis = jd_analyzer.analyze(job_description)
            
            st.session_state.skill_gap_analysis = skill_gap_analyzer.analyze(
                st.session_state.resume_analysis, 
                st.session_state.jd_analysis
            )
            
            st.session_state.features = feature_builder.build_features(
                st.session_state.jd_analysis, 
                st.session_state.skill_gap_analysis, 
                st.session_state.resume_analysis
            )
            
            st.session_state.prediction = predictor.predict(st.session_state.features)
            
            st.session_state.feedback = feedback_generator.generate(
                st.session_state.prediction, 
                st.session_state.resume_analysis, 
                st.session_state.jd_analysis, 
                st.session_state.skill_gap_analysis
            )

            # Set a flag to tell the app the analysis is done
            st.session_state.analysis_complete = True

    except Exception as e:
        st.error("An unexpected error occurred during analysis.")
        st.exception(e)


# ==========================================================
# Display Results (Renders safely on every rerun)
# ==========================================================

if st.session_state.get("analysis_complete", False):

    # Retrieve stored variables for easy access
    prediction = st.session_state.prediction
    features = st.session_state.features
    resume_analysis = st.session_state.resume_analysis
    jd_analysis = st.session_state.jd_analysis
    skill_gap_analysis = st.session_state.skill_gap_analysis
    feedback = st.session_state.feedback

    st.success("✅ Resume Analysis Completed Successfully!")

    # ==========================================================
    # Placement Readiness Dashboard
    # ==========================================================
    st.header("🎯 Placement Readiness Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        score = prediction.get('placement_readiness_score', 0)
        st.metric("Readiness Score", f"{score:.1f}/100")
        st.progress(float(score) / 100)

    with col2:
        level = prediction.get("placement_readiness_level", "Unknown")
        st.write("**Readiness Level**")
        if level == "Highly Ready":
            st.success(level)
        elif level == "Moderately Ready":
            st.info(level)
        elif level == "Needs Improvement":
            st.warning(level)
        else:
            st.error(level)

    with col3:
        completeness = features.get("resume_completeness_score", 0) 
        st.write("**Resume Completeness**")
        st.progress(float(completeness) / 100)
        st.caption(f"{completeness:.0f}%")

    st.divider()

    # ==========================================================
    # Visual Charts & Probabilities
    # ==========================================================
    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("📊 Prediction Probabilities")
        probabilities = prediction.get("class_probabilities", {})
        if probabilities:
            df_probs = pd.DataFrame(list(probabilities.items()), columns=["Category", "Probability"]).set_index("Category")
            st.bar_chart(df_probs, use_container_width=True)

    with colB:
        st.subheader("📄 Extracted Profile")
        st.markdown(f"**Category:** {resume_analysis.get('resume_category', 'Not Detected')}")
        
        skills = resume_analysis.get('skills', [])
        if skills:
            st.markdown("**Top Skills:**")
            for skill in skills[:8]:
                st.markdown(f"- {skill}")
            if len(skills) > 8:
                st.caption(f"+ {len(skills)-8} more...")

    st.divider()

    # ==========================================================
    # Resume-JD Match Report
    # ==========================================================
    st.header("📄 Resume - Job Description Match")

    match_report = feedback["resume_jd_match_report"]
    st.write(f"**Target Role:** {match_report.get('job_title', 'Not specified')}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        matched = match_report.get("matched_skills", [])
        if matched:
            for skill in matched:
                st.success(f"• {skill}")
        else:
            st.info("No matched skills found.")

    with col2:
        st.subheader("❌ Missing Skills")
        missing = match_report.get("missing_skills", [])
        if missing:
            for skill in missing:
                st.error(f"• {skill}")
        else:
            st.success("No missing skills.")

    critical = match_report.get("critical_missing_skills", [])
    if critical:
        st.subheader("🚨 Critical Missing Skills")
        for skill in critical:
            st.warning(f"• {skill}")

    st.subheader("📌 Job Match Summary")
    st.info(match_report.get("job_match_summary", ""))

    st.divider()

    # ==========================================================
    # AI Career Recommendations
    # ==========================================================
    st.header("💡 AI Career Recommendations")

    st.subheader("📝 Placement Readiness Summary")
    st.info(feedback.get("summary", ""))

    st.subheader("📅 7-Day Improvement Plan")
    seven_day = feedback.get("improvement_plan", {}).get("7_day_plan", [])
    if seven_day:
        for day, task in enumerate(seven_day, start=1):
            st.markdown(f"**Day {day}:** {task}")
    else:
        st.info("No 7-day plan generated.")

    st.divider()

    # ==========================================================
    # Technical Details (Hidden by Default)
    # ==========================================================
    
    # 💡 Clicking this will now safely rerun the page without losing data!
    show_tech = st.checkbox("☑ Show Technical Details")
    
    if show_tech:
        st.subheader("Machine Learning Features")
        st.json(features)
        
        st.subheader("Resume Analysis (Raw)")
        st.json(resume_analysis)
        
        st.subheader("Job Description Analysis (Raw)")
        st.json(jd_analysis)

    st.divider()

    # ==========================================================
    # Download Reports
    # ==========================================================
    st.header("📥 Download Analysis Reports")

    report_dict = {
        "prediction": prediction,
        "resume_analysis": resume_analysis,
        "job_description_analysis": jd_analysis,
        "skill_gap_analysis": skill_gap_analysis,
        "features": features,
        "feedback": feedback
    }

    col_dl1, col_dl2 = st.columns(2)
    
    with col_dl1:
        st.download_button(
            label="📄 Download Full Report (JSON)",
            data=json.dumps(report_dict, indent=4),
            file_name="placement_readiness_report.json",
            mime="application/json"
        )
        
    with col_dl2:
        pdf_buffer = generate_pdf_report(prediction, match_report)
        st.download_button(
            label="📑 Download PDF Report",
            data=pdf_buffer,
            file_name="placement_readiness_report.pdf",
            mime="application/pdf"
        )

# ==========================================================
# Footer (Always Visible)
# ==========================================================
st.divider()

st.markdown(
    """
    ---
    ### 🎓 AI Placement Readiness Analyzer

    **Developed by:**  
    Sakiley Niharika

    **Technologies:**  
    Python • Streamlit • Groq • Machine Learning • Scikit-learn • NLP • ReportLab
    """
)