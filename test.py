import sqlite3
import random

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")
item = cursor.fetchall()

print(item)