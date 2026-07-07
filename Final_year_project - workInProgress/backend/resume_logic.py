import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =====================================================
# EXTRACT TEXT FROM RESUME PDF
# =====================================================
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.lower()


# =====================================================
# CLEAN TEXT
# =====================================================
def clean_text(text):
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    return text.lower()


# =====================================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# (api + rest merged as "rest api")
# =====================================================
def extract_skills_from_jd(jd_text):
    skill_keywords = [
        "python", "java", "c++", "sql", "html", "css", "javascript",
        "react", "node", "flask", "django", "git",
        "rest api",                    # ✅ merged skill
        "machine learning", "data analysis",
        "excel", "power bi",
        "oop", "problem solving"
    ]

    found = set()

    for skill in skill_keywords:
        if skill in jd_text:
            found.add(skill)

    return sorted(found)


# =====================================================
# MAIN RESUME ANALYSIS FUNCTION
# =====================================================
def analyze_resume(resume_file, jd_text):

    # -------- TEXT EXTRACTION --------
    resume_text = extract_text_from_pdf(resume_file)
    jd_text_clean = clean_text(jd_text)

    # -------- SKILLS FROM JD ---------
    jd_skills = extract_skills_from_jd(jd_text_clean)

    resume_skills = []
    for skill in jd_skills:
        if skill in resume_text:
            resume_skills.append(skill)

    matched_skills = sorted(set(resume_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))

    # -------- TF-IDF SIMILARITY ------
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, jd_text_clean])
    text_similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    # -------- ATS STYLE SCORING -------
    skill_score = len(matched_skills) / max(len(jd_skills), 1)
    final_score = (0.7 * skill_score) + (0.3 * text_similarity)

    match_score = round(final_score * 100, 2)
    ats_score = min(100, round(match_score + 10, 2))

    # =================================================
    # VERDICT THRESHOLD (Industry-level realistic)
    # =================================================
    if match_score >= 80:
        verdict = "Strong Match"
    elif match_score >= 55:
        verdict = "Moderate Match"
    else:
        verdict = "Weak Match"

    return {
        "match_score": match_score,
        "ats_score": ats_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": verdict
    }
