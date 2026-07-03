import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


class PlannerTool:

    def generate_plan(
        self,
        exam,
        days_left,
        study_hours,
        weak_topics
    ):

        prompt = f"""
You are an expert academic mentor.

Create a personalized study roadmap.

Student Details

Exam:
{exam}

Days Left:
{days_left}

Daily Hours:
{study_hours}

Recent Weak Topics:

{chr(10).join("- " + t for t in weak_topics)}

If weak topics exist,

prioritize them in today's study plan.

Spend at least 60% of today's study time on weak topics.

Then schedule revision.

Return only JSON.

Format:

{{
    "study_plan":[
        "Week 1: Study Trigonometry",
        "Week 2: Study Vectors",
        "Week 3: Revision",
        "Week 4: Mock Test"
    ],

    "today_topics":[
        "Trigonometry",
        "Vectors",
        "Probability"
    ]
}}


Rules:

1. Return ONLY valid JSON.
2. study_plan MUST be an array of strings.
3. today_topics MUST be an array of strings.
4. No markdown.
5. No explanation.
6. No ```json fences.
"""

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            # Remove markdown fences if Gemini adds them
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

            planner_output = json.loads(text)

            print("=" * 80)
            print("Planner Output:")
            print(planner_output)
            print("=" * 80)

            if "study_plan" not in planner_output:
                raise Exception("study_plan key missing")

            if "today_topics" not in planner_output:
                raise Exception("today_topics key missing")

            return planner_output

        except Exception as e:

            print("[PlannerTool]", e)

            return {
                "study_plan": "Unable to generate study plan.",
                "today_topics": []
            }