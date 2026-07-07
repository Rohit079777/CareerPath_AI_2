CREATE TABLE careers (
    career_id SERIAL PRIMARY KEY,
    career_name VARCHAR(100) NOT NULL,
    required_skills TEXT NOT NULL,
    description TEXT,
    salary VARCHAR(50),
    learn_link TEXT,
    image_url TEXT
);
