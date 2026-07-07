import streamlit as st
from utils.navigation import go_to

def show():
    st.title("🔐 Admin Dashboard")
    st.success("Admin login successful")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👨‍🎓 Student Management", use_container_width=True):
            go_to("admin_students")

    with col2:
        if st.button("📄 Student List PDF", use_container_width=True):
            go_to("admin_student_pdf")
