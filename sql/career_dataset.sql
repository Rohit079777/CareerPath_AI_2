CREATE TABLE IF NOT EXISTS careers (
    career_id SERIAL PRIMARY KEY,
    career VARCHAR(100) NOT NULL,
    required_skills TEXT NOT NULL,
    image TEXT,
    description TEXT,
    learn_link TEXT,
    salary VARCHAR(50)
);
