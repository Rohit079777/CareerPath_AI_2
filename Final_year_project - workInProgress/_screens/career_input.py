import streamlit as st
import streamlit.components.v1 as components
from backend.career_logic import calculate_matches
from backend.db import get_connection
from backend.report_pdf import generate_career_report_pdf
from utils.navigation import go_back, go_to

# ===================== CSS =====================
CSS = """
<style>
.card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    text-align: center;
    transition: all 0.3s ease-in-out;
}
.card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 18px 40px rgba(0,0,0,0.25);
}
.card img { width: 90px; margin-bottom: 10px; }
.score { font-size: 34px; font-weight: bold; }

.progress-container {
    background:#e0e0e0;
    border-radius:8px;
    height:15px;
    margin-top:6px;
}
.progress-bar {
    height:15px;
    border-radius:8px;
    transition: width 0.5s ease-in-out;
}

.learn-box {
    background:#fff8dc;
    padding:10px;
    border-radius:10px;
    margin-top:12px;
    font-size:14px;
}

.learn-btn {
    background:#ff5722;
    color:white;
    padding:10px 18px;
    border-radius:12px;
    text-decoration:none;
    display:inline-block;
    font-weight:bold;
    margin-top:10px;
}

.salary-pill {
    background:#4caf50;
    color:white;
    padding:10px 16px;
    border-radius:14px;
    font-weight:bold;
    margin-top:12px;
    display:inline-block;
}
</style>
"""

# ===================== FETCH SKILLS =====================
def get_all_skills():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT required_skills FROM careers")
    rows = cur.fetchall()
    conn.close()

    skills = set()
    for (skill_str,) in rows:
        for s in skill_str.split(","):
            skills.add(s.strip())
    return sorted(skills)

# ===================== PAGE =====================
def show():
    st.button("⬅ Back", on_click=go_back)
    st.title("🧠 Enter Your Skills")
    st.markdown("AI-powered career recommendation with skill gap analysis")

    skill_options = get_all_skills()

    selected_skills = st.multiselect(
        "Select your skills",
        skill_options,
        default=st.session_state.get("user_skills", [])
    )

    if st.button("🚀 Analyze My Career"):
        if not selected_skills:
            st.warning("Please select at least one skill")
            return
        st.session_state.user_skills = selected_skills
        st.session_state.results = calculate_matches(selected_skills)

    results = st.session_state.get("results", [])
    if not results:
        return

    st.markdown("## 🏆 Top 6 Matches")

    rows = [st.columns(3), st.columns(3)]
    user_skills = set(s.lower() for s in st.session_state["user_skills"])
    i = 0

    for row in rows:
        for col in row:
            if i >= 6:
                break

            c = results[i]
            i += 1

            required = set(s.strip().lower() for s in c["required_skills"].split(","))
            missing = required - user_skills
            score = c["match_score"]

            # ================= STATUS + UI (LOGIC SAME) =================
            if score == 100:
                status = "🏆 Excellent Fit"
                bar_color = "#2ecc71"
                learn_box = "You are ready 🚀"
                salary_html = f"""
                <div class="salary-pill">
                    💰 Estimated Salary: {c['salary']} per annum
                </div>
                """
                learn_btn = ""
            elif score >= 80:
                status = "🥇 Excellent Fit"
                bar_color = "#27ae60"
                learn_box = "Missed Skills: " + " • ".join(m.title() for m in missing)
                salary_html = ""   # ❌ salary hidden
                learn_btn = f"""
                <a href="{c['learn_link']}" target="_blank" class="learn-btn">
                    Learn Missing Skills
                </a>
                """
            elif score >= 60:
                status = "🔥 Good Fit"
                bar_color = "#f39c12"
                learn_box = "Missed Skills: " + " • ".join(m.title() for m in missing)
                salary_html = ""   # ❌ salary hidden
                learn_btn = f"""
                <a href="{c['learn_link']}" target="_blank" class="learn-btn">
                    Learn Missing Skills
                </a>
                """
            else:
                status = "⚠️ Needs Improvement"
                bar_color = "#e74c3c"
                learn_box = "Missed Skills: " + " • ".join(m.title() for m in missing)
                salary_html = ""   # ❌ salary hidden
                learn_btn = f"""
                <a href="{c['learn_link']}" target="_blank" class="learn-btn">
                    Learn Missing Skills
                </a>
                """

            html = f"""
            {CSS}
            <div class="card">
                <img src="{c['image']}"/>
                <h3>{c['career']}</h3>
                <b>{status}</b>

                <div class="score">{score:.2f}%</div>

                <div class="progress-container">
                    <div class="progress-bar"
                         style="width:{score}%; background:{bar_color};"></div>
                </div>

                <p>{c['description']}</p>

                {salary_html}

                <div class="learn-box">{learn_box}</div>

                {learn_btn}
            </div>
            """

            with col:
                components.html(html, height=620, scrolling=False)

    # ===================== BOTTOM BUTTONS =====================
    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("📊 View Career Overview", use_container_width=True):
            go_to("career_overview")

    with c2:
        pdf_bytes = generate_career_report_pdf(
            st.session_state["results"],
            st.session_state["user_skills"]
        )
        st.download_button(
            "📄 Download Career Report (PDF)",
            data=pdf_bytes,
            file_name="career_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
