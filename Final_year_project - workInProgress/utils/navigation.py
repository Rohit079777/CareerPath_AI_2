import streamlit as st

def go_to(page):
    history = st.session_state.get("history", [])
    current = st.session_state.get("page")

    if current:
        history.append(current)

    st.session_state.history = history
    st.session_state.page = page
    st.rerun()

def go_back():
    history = st.session_state.get("history", [])
    if history:
        st.session_state.page = history.pop()
        st.session_state.history = history
