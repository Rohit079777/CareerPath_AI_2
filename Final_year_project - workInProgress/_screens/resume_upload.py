import streamlit as st
from utils.navigation import go_back
from backend.resume_logic import analyze_resume
from utils.navigation import go_to

def show():
    # 🔙 BACK BUTTON (ADDED)
    st.button("⬅ Back", on_click=go_back)
    st.title("📄 Resume Analyzer")

    st.markdown("Upload your resume and paste a job description to analyze ATS match.")

    resume = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
    jd = st.text_area("📝 Paste Job Description", height=200)

    if st.button("🔍 Analyze Resume"):
        if not resume or not jd.strip():
            st.warning("Please upload resume and paste job description.")
            return

        result = analyze_resume(resume, jd)


        st.session_state.resume_result = result
        go_to("resume_result")
