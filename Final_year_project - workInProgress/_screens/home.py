import streamlit as st
from utils.navigation import go_to

def show():
    st.title("🎯 CareerPath AI")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Career Recommendation"):
            go_to("career_input")

    with col2:
        if st.button("📄 Resume Analyzer (Phase 2)"):
            go_to("resume_upload")
