import streamlit as st
from utils.navigation import go_back, go_to


def get_missing(user_skills, required_skills):
    user = set(s.lower() for s in user_skills)
    req = set(s.strip().lower() for s in required_skills.split(","))
    return sorted(req - user)


def show():
    # 🔙 Back → Career Results
    st.button("⬅ Back", on_click=go_back)

    st.markdown("<h1>🧠 Missing Skills</h1>", unsafe_allow_html=True)
    st.write("Below are the skill gaps for the selected careers.")

    st.markdown("---")

    results = st.session_state.get("results", [])
    user_skills = st.session_state.get("user_skills", [])

    if not results or not user_skills:
        st.warning("Required data not found. Please analyze your career again.")
        return

    cols = st.columns(3)

    for idx, career in enumerate(results[:6]):
        missing = get_missing(user_skills, career["required_skills"])

        with cols[idx % 3]:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

            st.subheader(career["career"])

            if not missing:
                st.success("🎉 You are ready")
                st.write(f"💰 **Estimated Salary:** {career['salary']}")
            else:
                st.write("**Missing skills:**")
                for skill in missing:
                    st.write(f"• {skill}")

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("📊 View Career Overview"):
        go_to("career_overview")
