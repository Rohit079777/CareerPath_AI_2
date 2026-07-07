-- =============================
-- CareerPath AI Database Schema
-- =============================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    roll_no VARCHAR(50),
    branch VARCHAR(50),
    year VARCHAR(10),
    username VARCHAR(50) UNIQUE,
    password_hash TEXT,
    rfid_uid_hash TEXT UNIQUE,
    role VARCHAR(20) CHECK (role IN ('student','admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE login_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    login_method VARCHAR(20), -- RFID / MANUAL
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE resume_analysis (
    analysis_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    resume_text TEXT,
    job_description TEXT,
    match_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================
-- INITIAL ADMIN (ONE TIME)
-- =============================
-- Password: admin123 (hashed externally)
INSERT INTO users 
(name, username, password_hash, role)
VALUES (
'Admin',
'admin',
'240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
'admin'
);
