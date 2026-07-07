from backend.db import get_connection

def calculate_matches(user_skills):
    user = set(s.strip().lower() for s in user_skills)
    results = []

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT career, required_skills, description, salary, image, learn_link
        FROM careers
    """)
    rows = cur.fetchall()
    conn.close()

    for career, required_skills, description, salary, image, learn_link in rows:
        req = set(s.strip().lower() for s in required_skills.split(","))
        score = int((len(user & req) / len(req)) * 100) if req else 0

        results.append({
            "career": career,
            "required_skills": required_skills,
            "description": description,
            "salary": salary,
            "image": image,
            "learn_link": learn_link,
            "match_score": score
        })

    return sorted(results, key=lambda x: x["match_score"], reverse=True)[:6]
