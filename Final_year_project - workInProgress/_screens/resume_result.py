import streamlit as st
import pandas as pd
from utils.navigation import go_back
from backend.report_pdf import generate_resume_report_pdf


def show():
    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    st.button("⬅ Back", on_click=go_back)

    st.markdown(
        """
        <h1 style="display:flex;align-items:center;gap:10px;">
            📊 Resume Analysis Result
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "This analysis compares your resume with the job description using an ATS-style approach."
    )

    # -------------------------------------------------
    # FETCH RESULT
    # -------------------------------------------------
    result = st.session_state.get("resume_result")

    if not result:
        st.error("No resume analysis data found.")
        return

    # -------------------------------------------------
    # SCORE CARDS
    # -------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="📌 Match Score",
            value=f"{result['match_score']}%"
        )

    with col2:
        st.metric(
            label="🤖 ATS Score",
            value=f"{result['ats_score']} / 100"
        )

    st.info(
        "ℹ️ **ATS score is calculated using skill match (70%) and text similarity (30%).**"
    )

    st.divider()

    # -------------------------------------------------
    # MATCHED SKILLS
    # -------------------------------------------------
    st.subheader("✅ Matched Skills")

    if result["matched_skills"]:
        st.success(", ".join(result["matched_skills"]))
    else:
        st.warning("No matching skills found between resume and job description.")

    # -------------------------------------------------
    # MISSING SKILLS
    # -------------------------------------------------
    st.subheader("❌ Missing Skills")

    if result["missing_skills"]:
        st.error(", ".join(result["missing_skills"]))
    else:
        st.success("No major skill gaps found.")

    st.divider()

    # -------------------------------------------------
    # SKILL MATCH TABLE
    # -------------------------------------------------
    st.subheader("📋 Skill Match Table")

    table_rows = []
    for skill in result["jd_skills"]:
        table_rows.append({
            "Skill": skill,
            "Status": "✅ Present" if skill in result["resume_skills"] else "❌ Missing"
        })

    skills_df = pd.DataFrame(table_rows)
    st.dataframe(skills_df, use_container_width=True, hide_index=True)

    st.divider()

    # -------------------------------------------------
    # FINAL VERDICT
    # -------------------------------------------------
    st.subheader("🏁 Final Verdict")

    if result["recommendation"] == "Strong Match":
        st.success("Overall Result: **Strong Match**")
    elif result["recommendation"] == "Moderate Match":
        st.warning("Overall Result: **Moderate Match**")
    else:
        st.error("Overall Result: **Weak Match**")

    # -------------------------------------------------
    # RESUME IMPROVEMENT TIPS
    # -------------------------------------------------
    st.subheader("🛠️ Resume Improvement Tips")

    st.markdown(
        """
        • Add missing skills from the job description  
        • Highlight relevant projects and internships  
        • Use standard section headings (Skills, Projects, Experience)  
        """
    )

    st.divider()

    # -------------------------------------------------
    # DOWNLOAD PDF
    # -------------------------------------------------
    pdf_bytes = generate_resume_report_pdf(result)

    st.download_button(
        label="📄 Download Resume Analysis PDF",
        data=pdf_bytes,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
