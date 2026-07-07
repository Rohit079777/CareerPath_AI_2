import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="careerpath_ai",
    user="postgres",
    password="root"
)

cur = conn.cursor()

csv_file = r"C:\Users\USER\Desktop\AI_ML\Career_prediction\career_dataset_100.csv"

with open(csv_file, newline='', encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cur.execute("""
            INSERT INTO careers
            (career, required_skills, image, description, learn_link, salary)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row["Career"],
            row["Required_Skills"],
            row["Image"],
            row["Description"],
            row["Learn_Link"],
            row["Salary"]
        ))

conn.commit()
cur.close()
conn.close()

print("✅ Data imported successfully")
