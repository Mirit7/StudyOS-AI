# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model = genai.GenerativeModel("gemini-2.5-flash")

# response = model.generate_content("Say hello in one sentence.")

# print(response)
import sqlite3

conn = sqlite3.connect("study.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM quiz_history")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()