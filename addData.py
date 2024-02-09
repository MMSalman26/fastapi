import sqlite3
import random

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT NOT NULL,
        home_town TEXT
    )
''')
conn.commit()

student_names = ["zidan", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack"]

for i in range(10):
    name = random.choice(student_names)
    student_id = f"S{random.randint(1000, 9999)}"
    home_town = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])
    cursor.execute("INSERT INTO students (name, student_id, home_town) VALUES (?, ?, ?)", (name, student_id, home_town))

conn.commit()
# conn.close()

cursor.execute("SELECT * FROM students")
item = cursor.fetchall()
print(item)