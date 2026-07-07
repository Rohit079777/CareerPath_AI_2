import hashlib
from backend.db import get_connection

# ---------------- USERNAME / PASSWORD LOGIN ----------------
def verify_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, role, is_active
        FROM users
        WHERE username=%s AND password_hash=%s
    """, (username, password_hash))

    user = cur.fetchone()
    cur.close()
    conn.close()

    return user


# ---------------- RFID LOGIN (NEW) ----------------
def verify_user_by_rfid(uid_hash):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, role, is_active
        FROM users
        WHERE rfid_uid_hash = %s
    """, (uid_hash,))

    user = cur.fetchone()
    cur.close()
    conn.close()

    return user
