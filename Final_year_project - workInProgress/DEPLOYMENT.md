# Streamlit Cloud Deployment

## 1. Prepare Database

Streamlit Community Cloud does not run your local PostgreSQL database. Create a hosted PostgreSQL database first, for example Neon, Supabase, Render, or Railway.

Run the SQL files on that database:

1. `sql/schema.sql`
2. Add/import career rows into the `careers` table.

The app expects these columns:

```sql
career, required_skills, description, salary, image, learn_link
```

## 2. Add Secrets

In Streamlit Cloud, open app settings or Advanced settings and paste these secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"

DB_HOST = "your_postgres_host"
DB_PORT = "5432"
DB_NAME = "careerpath_ai"
DB_USER = "your_postgres_user"
DB_PASSWORD = "your_postgres_password"
DB_SSLMODE = "require"
```

For local testing, you can keep using `.env`, or create `.streamlit/secrets.toml` from `.streamlit/secrets.toml.example`.

## 3. Deploy

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Click `Create app`.
4. Select your GitHub repository and branch.
5. Set main file path to `app.py`.
6. Add the secrets above in Advanced settings.
7. Click `Deploy`.

## 4. Run Locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```
