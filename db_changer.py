import csv
from django.db import connection


def db_changer():
    with open("skills.csv", "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        df = [[query, name] for name, query in reader]

    with connection.cursor() as cursor:
        query = "update skills set query=%s where skill_name=%s"
        cursor.executemany(query, df)
    connection.commit()
