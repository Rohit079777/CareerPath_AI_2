import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="careerpath_ai",
        user="postgres",
        password="root"
    )
