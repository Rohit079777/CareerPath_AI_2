import streamlit as st
from _screens.career_results import show as career_results
from _screens import admin_students, admin_student_pdf

from _screens import (
    career_overview,
    login,
    home,
    career_input,
    career_results,
    resume_result,
    resume_upload,
    admin_dashboard   # ✅ ADD (NEW)
)

st.set_page_config(page_title="CareerPath AI", layout="wide")

def router():
    if "page" not in st.session_state:
        st.session_state.page = "login"

    page = st.session_state.page

    if page == "login":
        login.show()

    elif page == "home":
        home.show()

    elif page == "career_input":
        career_input.show()

    elif page == "career_results":
        career_results.show()

    elif page == "career_overview":
        career_overview.show()

    elif page == "resume_upload":
        resume_upload.show()

    elif page == "resume_result":
        resume_result.show()

    # 🔐 ADMIN ROUTE (NEW – SAFE ADD)
    elif page == "admin_dashboard":
        admin_dashboard.show()
    elif page == "admin_students":
        admin_students.show()

    elif page == "admin_student_pdf":
        admin_student_pdf.show()
        
    else:
        st.session_state.page = "login"
        st.rerun()

router()
