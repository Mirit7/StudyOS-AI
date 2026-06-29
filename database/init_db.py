import sqlite3

conn = sqlite3.connect("study.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    date TEXT,

    exam TEXT,

    score INTEGER,

    total INTEGER,

    accuracy REAL,

    strong_topics TEXT,

    weak_topics TEXT
)
""")

conn.commit()
conn.close()

print("Database Ready.")