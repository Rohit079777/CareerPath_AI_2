import streamlit as st
from backend.admin_logic import get_students
from backend.report_pdf import generate_pdf
from utils.navigation import go_back

def show():
    st.button("⬅ Back", on_click=go_back)
    st.header("📄 Student List PDF")

    students = get_students()

    lines = []
    for _, name, username, rfid, active in students:
        lines.append(
            f"{name} | {username} | RFID: {rfid or 'NA'} | {'Active' if active else 'Disabled'}"
        )

    if st.button("Download PDF"):
        pdf_bytes = generate_pdf(
            "student_list.pdf",
            "Student List",
            lines
        )

        st.download_button(
            label="⬇ Download Student List PDF",
            data=pdf_bytes,
            file_name="student_list.pdf",
            mime="application/pdf"
        )
