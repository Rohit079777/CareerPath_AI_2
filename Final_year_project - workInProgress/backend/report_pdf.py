from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# ======================================================
# CAREER RECOMMENDATION PDF  ✅ (CAREER MODULE)
# ======================================================
def generate_career_report_pdf(results, user_skills):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Career Recommendation Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Your Skills</b>", styles["Heading2"]))
    elements.append(Paragraph(", ".join(user_skills), styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Top Career Matches</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    for career in results:
        elements.append(
            Paragraph(
                f"""
                <b>{career['career']}</b><br/>
                Match Score: {career['match_score']}%<br/>
                Salary: {career['salary']}<br/>
                Description: {career['description']}
                """,
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 10))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ======================================================
# RESUME ANALYSIS PDF  ✅ (RESUME ANALYZER)
# ======================================================
def generate_resume_report_pdf(result):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=10,
        )
    )

    elements = []

    elements.append(Paragraph("Resume Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(f"<b>Match Score:</b> {result['match_score']}%", styles["Normal"])
    )
    elements.append(
        Paragraph(f"<b>ATS Score:</b> {result['ats_score']} / 100", styles["Normal"])
    )
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Skill Match Analysis", styles["SectionTitle"]))

    table_data = [["Skill", "Status"]]
    for skill in result["jd_skills"]:
        status = "Matched" if skill in result["resume_skills"] else "Missing"
        table_data.append([skill, status])

    table = Table(table_data, colWidths=[260, 160])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Final Verdict", styles["SectionTitle"]))
    elements.append(Paragraph(result["recommendation"], styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# ======================================================
# GENERIC PDF WRAPPER  ✅ (ADMIN USE)
# ======================================================
def generate_pdf(filename, title, lines):
    """
    Generic PDF generator for Admin (Student List PDF).
    Does NOT break existing career / resume PDFs.
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 15))

    for line in lines:
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)

    return buffer.getvalue()
