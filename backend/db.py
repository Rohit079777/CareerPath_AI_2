import psycopg2
from backend.settings import get_setting


def get_connection():
    return psycopg2.connect(
        host=get_setting("DB_HOST", "localhost"),
        port=get_setting("DB_PORT", "5432"),
        database=get_setting("DB_NAME", "careerpath_ai"),
        user=get_setting("DB_USER", "postgres"),
        password=get_setting("DB_PASSWORD", "root"),
        sslmode=get_setting("DB_SSLMODE", "prefer"),
    )
