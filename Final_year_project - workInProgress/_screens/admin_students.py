import streamlit as st
import hashlib
from backend.admin_logic import (
    add_student, get_students, update_student,
    delete_student, assign_rfid, toggle_student,
    reset_student_password, check_student_exists
)
from backend.rfid_listener import listen_rfid
from utils.navigation import go_back

def show():
    st.button("⬅ Back", on_click=go_back)
    st.header("👨‍🎓 Student Management")

    # -------- ADD STUDENT --------
    with st.expander("➕ Add Student"):
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Add Student"):
            if not name or not username or not password:
                st.error("All fields are required")
            else:
                result = add_student(username, password, name)

                if not result:
                    st.error("❌ Username already exists. Please choose a different one.")
                else:
                    st.success("✅ Student added successfully")
                    st.rerun()

    # -------- RESET STUDENT PASSWORD --------
    with st.expander("🔐 Reset Student Password (Forgot Password)"):

        reset_username = st.text_input("Student Username")

        if st.button("🔍 Search Student"):
            student = check_student_exists(reset_username)

            if not student:
                st.error("❌ Student not found")
                st.session_state.reset_student = None
            else:
                st.session_state.reset_student = {
                    "user_id": student[0],
                    "name": student[1],
                    "username": reset_username
                }
                st.success(f"✅ Student Found: {student[1]}")

        if "reset_student" in st.session_state and st.session_state.reset_student:
            new_password = st.text_input("New Password", type="password")

            if st.button("Reset Password"):
                if not new_password:
                    st.error("Please enter new password")
                else:
                    reset_student_password(
                        st.session_state.reset_student["username"],
                        new_password
                    )
                    st.success("Password reset successfully")
                    st.session_state.reset_student = None

    st.divider()

    # -------- STUDENT LIST --------
    students = get_students()

    if not students:
        st.info("No students found")
        return

    for user_id, name, username, rfid, active in students:
        with st.container(border=True):
            st.write(f"👤 **{name}** ({username})")
            st.write("RFID:", rfid if rfid else "❌ Not Assigned")
            st.write("Status:", "✅ Active" if active else "🚫 Disabled")

            col1, col2, col3, col4 = st.columns(4)

            # ---- UPDATE NAME ----
            with col1:
                new_name = st.text_input(
                    "Edit Name",
                    value=name,
                    key=f"name_{user_id}"
                )
                if st.button("Update", key=f"upd_{user_id}"):
                    update_student(user_id, new_name)
                    st.success("Updated")
                    st.rerun()

            # ---- DELETE STUDENT ----
            with col2:
                if st.button("❌ Delete", key=f"del_{user_id}"):
                    delete_student(user_id)
                    st.warning("Deleted")
                    st.rerun()

            # ---- ASSIGN / REASSIGN RFID ----
            with col3:
                if st.button("🔑 Assign / Reassign RFID", key=f"rfid_{user_id}"):
                    st.info("Scan RFID card now...")
                    uid = listen_rfid()
                    if uid:
                        uid_hash = hashlib.sha256(uid.encode()).hexdigest()
                        assign_rfid(user_id, uid_hash)
                        st.success("RFID Assigned")
                        st.rerun()

            # ---- ENABLE / DISABLE ----
            with col4:
                if st.button("Toggle Status", key=f"tog_{user_id}"):
                    toggle_student(user_id, not active)
                    st.success("Status Updated")
                    st.rerun()
