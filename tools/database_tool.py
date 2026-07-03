import sqlite3
import json

class DatabaseTool:

    def __init__(self):
        self.db_name = "study.db"

    def get_last_reports(self, limit=10):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                date,
                exam,
                score,
                total,
                accuracy,
                strong_topics,
                weak_topics
            FROM quiz_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        history = cursor.fetchall()

        conn.close()

        return history
    
    def get_most_recent_weak_topics(self):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute("""
            SELECT weak_topics
            FROM quiz_history
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return []

        return json.loads(row[0])