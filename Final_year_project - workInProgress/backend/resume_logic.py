import json
import re
import pdfplumber
from groq import Groq
from backend.settings import get_setting


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================
GROQ_API_KEY = get_setting("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


COMMON_SKILLS = [
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "php", "ruby",
    "go", "golang", "rust", "kotlin", "swift", "html", "css", "react", "angular",
    "vue", "next.js", "node.js", "express", "django", "flask", "fastapi", "spring",
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "firebase",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "gitlab",
    "linux", "rest api", "graphql", "api", "machine learning", "deep learning",
    "data analysis", "data science", "pandas", "numpy", "scikit-learn", "tensorflow",
    "pytorch", "opencv", "nlp", "power bi", "tableau", "excel", "figma",
    "ui/ux", "testing", "selenium", "pytest", "agile", "scrum", "problem solving",
    "communication", "leadership", "project management", "oops", "dbms",
    "computer networks", "data structures", "algorithms", "cybersecurity",
]

SKILL_ALIASES = {
    "nodejs": "node.js",
    "node js": "node.js",
    "node": "node.js",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "postgre sql": "postgresql",
    "mongo db": "mongodb",
    "git hub": "github",
    "google cloud": "gcp",
    "rest": "rest api",
    "apis": "api",
    "ml": "machine learning",
    "dl": "deep learning",
    "dsa": "data structures",
    "object oriented programming": "oops",
}


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
    return text.strip()


def _normalize_text(text):
    return re.sub(r"\s+", " ", str(text or "").lower())


def _skill_pattern(skill):
    escaped = re.escape(skill).replace(r"\ ", r"[\s\-/]+")
    return rf"(?<![a-z0-9+#.]){escaped}(?![a-z0-9+#.])"


def _extract_skills(text):
    normalized_text = _normalize_text(text)
    found = set()

    for skill in COMMON_SKILLS:
        if re.search(_skill_pattern(skill), normalized_text):
            found.add(SKILL_ALIASES.get(skill, skill))

    for alias, canonical in SKILL_ALIASES.items():
        if re.search(_skill_pattern(alias), normalized_text):
            found.add(canonical)

    return sorted(found)


def _keyword_similarity(resume_text, jd_text):
    resume_words = set(re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", _normalize_text(resume_text)))
    jd_words = set(re.findall(r"[a-zA-Z][a-zA-Z+#.]{2,}", _normalize_text(jd_text)))
    if not jd_words:
        return 0
    return round((len(resume_words & jd_words) / len(jd_words)) * 100)


def _fallback_analysis(resume_text, jd_text, feedback):
    resume_skills = _extract_skills(resume_text)
    jd_skills = _extract_skills(jd_text)

    matched_skills = sorted(set(resume_skills) & set(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))

    skill_score = round((len(matched_skills) / len(jd_skills)) * 100) if jd_skills else 0
    text_score = _keyword_similarity(resume_text, jd_text)
    ats_score = round((skill_score * 0.7) + (text_score * 0.3))
    match_score = round((skill_score * 0.8) + (text_score * 0.2))

    if ats_score >= 75 and match_score >= 70:
        recommendation = "Strong Match"
    elif ats_score >= 45 or match_score >= 45:
        recommendation = "Moderate Match"
    else:
        recommendation = "Weak Match"

    return {
        "match_score": match_score,
        "ats_score": ats_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "feedback": feedback,
        "analysis_source": "local_fallback",
    }


# =====================================================
# AI-BASED RESUME ANALYSIS USING GROQ
# =====================================================
def analyze_resume(resume_file, jd_text):

    resume_text = extract_text_from_pdf(resume_file)

    print(f"PDF text extracted: {len(resume_text)} characters")

    if not resume_text:
        print("ERROR: PDF se koi text nahi mila!")
        return {
            "match_score": 0,
            "ats_score": 0,
            "resume_skills": [],
            "jd_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "recommendation": "Weak Match",
            "feedback": "Resume PDF se text extract nahi ho saka. Please check your PDF.",
            "analysis_source": "pdf_text_missing",
        }

    prompt = f"""
You are an expert ATS (Applicant Tracking System) and resume evaluator.

Analyze the following resume against the job description and return ONLY a valid JSON object — no explanation, no markdown, no extra text.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Return this exact JSON structure:
{{
  "match_score": <float 0-100>,
  "ats_score": <float 0-100>,
  "resume_skills": ["skill1", "skill2"],
  "jd_skills": ["skill1", "skill2"],
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "recommendation": "<one of: Strong Match, Moderate Match, Weak Match>",
  "feedback": "<2-3 sentence honest feedback about the resume for this JD>"
}}

Rules:
- Be accurate and strict.
- Skill matching should be case-insensitive (nodejs = Node.js, javascript = JavaScript, mysql = MySQL).
- Consider synonyms: nodejs = node.js = node js, github = git, mysql = MySql.
- Do not mark a skill as missing if a close variant exists in the resume.
- Return ONLY the JSON. No markdown. No extra text.
"""

    default_result = _fallback_analysis(
        resume_text,
        jd_text,
        "AI analysis could not be completed, so this report used local skill and keyword matching.",
    )

    if not client:
        print("GROQ_API_KEY missing. Using local fallback analysis.")
        return default_result

    try:
        print("Groq se analysis ho rahi hai...")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS resume evaluator. Always respond with valid JSON only. Be case-insensitive when matching skills."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        raw_text = response.choices[0].message.content.strip()
        print(f"RAW RESPONSE: {raw_text}")

        raw_text = re.sub(r"```json|```", "", raw_text).strip()

        try:
            result = json.loads(raw_text)
        except json.JSONDecodeError as je:
            print(f"JSON parse error: {je}")
            return default_result

        for key, val in default_result.items():
            result.setdefault(key, val)

        for score_key in ("match_score", "ats_score"):
            try:
                result[score_key] = max(0, min(100, round(float(result.get(score_key, 0)))))
            except (TypeError, ValueError):
                result[score_key] = default_result[score_key]

        for list_key in ("resume_skills", "jd_skills", "matched_skills", "missing_skills"):
            if not isinstance(result.get(list_key), list):
                result[list_key] = default_result[list_key]

        if not result["jd_skills"] and default_result["jd_skills"]:
            result = default_result
        else:
            result["analysis_source"] = "groq_api"

        print("Success with Groq!")
        return result

    except Exception as e:
        print(f"Groq API error: {str(e)}")
        error_text = str(e)
        if "invalid_api_key" in error_text.lower() or "invalid api key" in error_text.lower():
            default_result["feedback"] = "Groq API key is invalid, so this report used local skill and keyword matching."
        else:
            default_result["feedback"] = "Groq API request failed, so this report used local skill and keyword matching."
        return default_result
