import streamlit as st
from utils.navigation import go_back
import streamlit.components.v1 as components

CSS = """
<style>
.card {
    background: white;
    border-radius: 18px;
    padding: 22px 22px 30px 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    text-align: center;
    transition: all 0.3s ease-in-out;
}
.card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}
.card img {
    width: 90px;
    margin-bottom: 10px;
}
.score {
    font-size: 34px;
    font-weight: bold;
}
.progress-container {
    background-color: #e0e0e0;
    border-radius: 8px;
    height: 15px;
    margin-top: 6px;
}
.progress-bar {
    height: 15px;
    border-radius: 8px;
}
.learn-box {
    background: #fff8dc;
    padding: 10px;
    border-radius: 10px;
    margin-top: 12px;
    font-size: 14px;
}
.learn-btn {
    background-color:#ff5722;
    color:white;
    padding:10px 18px;
    border-radius:12px;
    text-decoration:none;
    display:inline-block;
    font-weight:bold;
    margin-top: 14px;
}
</style>
"""

def show():
    st.button("⬅ Back", on_click=go_back)
    st.title("🏆 Top Career Matches")

    results = st.session_state.get("results", [])
    user_skills = set(s.lower() for s in st.session_state.get("user_skills", []))

    if not results:
        st.warning("No career results found")
        return

    rows = [st.columns(3), st.columns(3)]
    i = 0

    for row in rows:
        for col in row:
            if i >= len(results):
                break

            c = results[i]
            i += 1

            required = set(s.strip().lower() for s in c["required_skills"].split(","))
            missing = required - user_skills
            score = c["match_score"]

            # ✅ STATUS LOGIC
            if score >= 80:
                status_text = "🏆 Excellent Fit"
                status_color = "#2ecc71"
                bar_color = "#2ecc71"
                learn_box = "<b>You are ready 🚀</b>"
                learn_btn = ""
            else:
                status_text = "⚠️ Needs Improvement"
                status_color = "#f39c12"
                bar_color = "#ff5722"
                missing_text = " • ".join(m.title() for m in missing)
                learn_box = f"<b>Missed Skills:</b> {missing_text}"
                learn_btn = f"""
                    <a href="{c['learn_link']}" target="_blank" class="learn-btn">
                        Learn Missing Skills
                    </a>
                """

            html = f"""
            {CSS}
            <div class="card">
                <img src="{c['image']}" />

                <h3>{c['career']}</h3>
                <div style="color:{status_color}; font-weight:bold;">
                    {status_text}
                </div>

                <div class="score">{score}%</div>

                <div class="progress-container">
                    <div class="progress-bar" style="width:{score}%; background:{bar_color};"></div>
                </div>

                <p style="margin-top:10px;">{c['description']}</p>
                <p><b>💰 Salary:</b> {c['salary']}</p>

                <div class="learn-box">
                    {learn_box}
                </div>

                {learn_btn}
            </div>
            """

            with col:
                components.html(html, height=520, scrolling=False)
