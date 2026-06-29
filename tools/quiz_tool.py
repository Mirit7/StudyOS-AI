import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


class QuizTool:

    def generate_quiz(
        self,
        exam: str,
        topics: list,
        difficulty: str = "Medium",
        num_questions: int = 10,
    ):

        prompt = f"""
You are an expert {exam} examiner.

Generate exactly {num_questions} multiple choice questions.

Topics:
{chr(10).join("- " + topic for topic in topics)}

Difficulty:
{difficulty}

Return ONLY valid JSON.

Format:

[
  {{
    "topic": "...",
    "question": "...",
    "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
    }},
    "correct_answer": "...",
    "explanation": "..."
  }}
  
]

DO NOT return markdown.
DO NOT return ```json.
Return only JSON.
"""

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

# Sometimes Gemini returns ```json ... ```
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

            return json.loads(text)

        except Exception as e:

            print("[QuizTool]", e)

            return []