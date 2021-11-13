import csv
import sqlite3

conn = sqlite3.connect('api_yamdb/db.sqlite3')
cursor = conn.cursor()
with open(r'C:\Users\Я\Desktop\Проекты\api_yamdb\api_yamdb\static\data\category.csv', 'r') as file:
    for row in file:
        cursor.execute("INSERT INTO reviews_category VALUES(?,?,?)", row.split(','))
        conn.commit()
conn.close()
