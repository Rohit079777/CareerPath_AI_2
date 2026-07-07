from backend.db import get_connection

def get_login_logs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.username, l.login_method, l.login_time
        FROM login_logs l
        JOIN users u ON u.user_id = l.user_id
        ORDER BY l.login_time DESC
        LIMIT 50
    """)
    logs = cur.fetchall()
    conn.close()
    return logs
