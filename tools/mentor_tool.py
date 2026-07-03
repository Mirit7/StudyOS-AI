import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


class MentorTool:

    def generate_feedback(self, history):

        prompt = f"""
You are an expert AI learning mentor.

Below is the student's previous quiz history.

{history}

Analyze the student's performance and provide:

1. Overall Progress
2. Strong Subjects
3. Weak Subjects
4. Learning Pattern
5. Study Recommendations for Tomorrow
6. Motivation (2-3 lines)

Write the response in Markdown.
"""

        try:

            response = model.generate_content(prompt)

            return response.text

        except Exception as e:

            print("[MentorTool]", e)

            return "Unable to generate mentor feedback."