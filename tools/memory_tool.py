import sqlite3
import json
from datetime import datetime


class MemoryTool:

    def save_report(self, report: dict):

        conn = sqlite3.connect("study.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO quiz_history(

                date,
                exam,
                score,
                total,
                accuracy,
                strong_topics,
                weak_topics

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (

                datetime.now().strftime("%Y-%m-%d"),

                report["exam"],

                report["score"],

                report["total"],

                report["accuracy"],

                json.dumps(report["strong_topics"]),

                json.dumps(report["weak_topics"])

            )
        )

        conn.commit()
        conn.close()

        return True