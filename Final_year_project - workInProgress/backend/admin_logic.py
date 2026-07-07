from backend.db import get_connection
import hashlib

# ---------------- ADD STUDENT (SAFE) ----------------
def add_student(username, password, name):
    conn = get_connection()
    cur = conn.cursor()

    # 🔍 Check if username already exists
    cur.execute("""
        SELECT 1 FROM users
        WHERE username = %s
    """, (username,))
    
    if cur.fetchone():
        cur.close()
        conn.close()
        return False  # ❌ Username exists

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("""
        INSERT INTO users (name, username, password_hash, role, is_active)
        VALUES (%s, %s, %s, 'student', TRUE)
    """, (name, username, password_hash))

    conn.commit()
    cur.close()
    conn.close()
    return True  # ✅ Added successfully


# ---------------- GET ALL STUDENTS ----------------
def get_students():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            user_id,
            name,
            username,
            rfid_uid_hash,
            is_active
        FROM users
        WHERE role = 'student'
        ORDER BY name
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ---------------- UPDATE STUDENT ----------------
def update_student(user_id, name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET name = %s
        WHERE user_id = %s AND role = 'student'
    """, (name, user_id))

    conn.commit()
    cur.close()
    conn.close()


# ---------------- DELETE STUDENT ----------------
def delete_student(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM users
        WHERE user_id = %s AND role = 'student'
    """, (user_id,))

    conn.commit()
    cur.close()
    conn.close()


# ---------------- ASSIGN / REASSIGN RFID ----------------
def assign_rfid(user_id, uid_hash):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET rfid_uid_hash = %s
        WHERE user_id = %s AND role = 'student'
    """, (uid_hash, user_id))

    conn.commit()
    cur.close()
    conn.close()


# ---------------- ENABLE / DISABLE STUDENT ----------------
def toggle_student(user_id, status):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET is_active = %s
        WHERE user_id = %s AND role = 'student'
    """, (status, user_id))

    conn.commit()
    cur.close()
    conn.close()


# ---------------- CHECK STUDENT EXISTS ----------------
def check_student_exists(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name
        FROM users
        WHERE username = %s AND role = 'student'
    """, (username,))

    student = cur.fetchone()
    cur.close()
    conn.close()
    return student


# ---------------- RESET STUDENT PASSWORD ----------------
def reset_student_password(username, new_password):
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET password_hash = %s
        WHERE username = %s AND role = 'student'
    """, (password_hash, username))

    conn.commit()
    cur.close()
    conn.close()
