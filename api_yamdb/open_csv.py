import csv
import sqlite3

conn = sqlite3.connect('api_yamdb/db.sqlite3')
c = conn.cursor()

with open(r"C:\Users\Я\Desktop\Проекты\api_yamdb\api_yamdb\static\data\category.csv", "r") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            """CREATE TABLE IF NOT EXISTS category (
                id INTEGER,
                name TEXT,
                slug TEXT
            )"""
        )
        c.executemany("INSERT INTO category VALUES(?, ?, ?)", id, name, slug)
