import streamlit as st
import hashlib
from backend.auth import verify_user, verify_user_by_rfid
from backend.rfid_listener import listen_rfid

def show():

    # ===== LOAD CSS =====
    with open("assets/css/login.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # ===== TITLE =====
    st.markdown('<div class="title">CareerPath AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Powered Career Guidance System</div>', unsafe_allow_html=True)

    # ===== INPUTS (STREAMLIT ONLY) =====
    username = st.text_input("Username", key="login_user", placeholder="Username")
    password = st.text_input("Password", type="password", key="login_pass", placeholder="Password")

    # ===== LOGIN BUTTON =====
    if st.button("Login", key="login_btn", use_container_width=True):
        user = verify_user(username, password)

        if user:
            user_id, role, is_active = user

            if not is_active:
                st.error("Account disabled. Contact admin.")
                return

            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.role = role
            st.session_state.history = []

            st.session_state.page = "admin_dashboard" if role == "admin" else "home"
            st.rerun()
        else:
            st.error("Invalid username or password")

    # ===== DIVIDER =====
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ===== RFID BUTTON =====
    if st.button("📶 Login with RFID Card", key="rfid_btn", use_container_width=True):
        st.info("Please tap your RFID card...")

        uid = listen_rfid()
        if not uid:
            st.error("RFID scan failed.")
            return

        uid_hash = hashlib.sha256(uid.encode()).hexdigest()
        user = verify_user_by_rfid(uid_hash)

        if user:
            user_id, role, is_active = user

            if not is_active:
                st.error("Account disabled.")
                return

            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.role = role
            st.session_state.page = "admin_dashboard" if role == "admin" else "home"
            st.rerun()
        else:
            st.error("RFID not registered.")