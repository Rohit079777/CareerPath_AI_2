import streamlit as st
import plotly.express as px
from utils.navigation import go_back

def show():
    st.button("⬅ Back", on_click=go_back)
    st.title("📊 Career Overview Dashboard")

    results = st.session_state.get("results", [])
    if not results:
        st.warning("No career data available")
        return

    top = results[:7]

    careers = [c["career"] for c in top]
    scores = [c["match_score"] for c in top]

    # ===================== 1. BAR =====================
    fig1 = px.bar(
        x=careers,
        y=scores,
        title="📊 Match Score Comparison (Bar)",
        color=careers,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ===================== 2. PIE =====================
    fig2 = px.pie(
        names=careers,
        values=scores,
        title="🥧 Career Match Distribution (Pie)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ===================== 3. LINE =====================
    fig3 = px.line(
        x=careers,
        y=scores,
        markers=True,
        title="📈 Match Score Trend (Line)",
        color_discrete_sequence=["#ff5722"]
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ===================== 4. AREA =====================
    fig4 = px.area(
        x=careers,
        y=scores,
        title="📉 Skill Coverage Area",
        color_discrete_sequence=["#8e44ad"]
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ===================== 5. SCATTER =====================
    fig5 = px.scatter(
        x=careers,
        y=scores,
        size=scores,
        title="🔵 Match Score Scatter",
        color=careers,
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    st.plotly_chart(fig5, use_container_width=True)

    # ===================== 6. RADAR =====================
    fig6 = px.line_polar(
        r=scores,
        theta=careers,
        line_close=True,
        title="🕸️ Career Match Radar"
    )
    fig6.update_traces(fill="toself", line_color="#16a085")
    st.plotly_chart(fig6, use_container_width=True)

    # ===================== 7. FUNNEL =====================
    fig7 = px.funnel(
        x=scores,
        y=careers,
        title="🚀 Career Suitability Funnel",
        color_discrete_sequence=["#2980b9"]
    )
    st.plotly_chart(fig7, use_container_width=True)
