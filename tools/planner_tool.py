import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

model = genai.GenerativeModel(MODEL_NAME)


class PlannerTool:
    """
    Planner Tool

    Responsibilities:
    - Build prompt
    - Call Gemini
    - Validate response
    - Return study plan

    This tool should ONLY communicate with Gemini.
    Business logic belongs in PlannerAgent.
    """

    def generate_plan(
        self,
        exam: str,
        days_left: int,
        study_hours: int,
    ) -> str:

        prompt = f"""
You are an expert academic mentor.

Your job is to generate a personalized study roadmap.

Student Profile:
- Exam: {exam}
- Days Remaining: {days_left}
- Daily Study Hours: {study_hours}

Requirements:

1. Create a week-by-week study roadmap.
2. Prioritize high-weightage topics.
3. Include revision schedule.
4. Recommend mock test frequency.
5. Mention common mistakes to avoid.
6. Keep the roadmap realistic.
7. Format using clean Markdown.

Return ONLY the study plan.
"""

        try:

            response = model.generate_content(prompt)

            # No response returned
            if not response.candidates:
                raise RuntimeError(
                    "Gemini returned no candidates."
                )

            candidate = response.candidates[0]

            if not candidate.content:
                raise RuntimeError(
                    "Candidate contains no content."
                )

            if not candidate.content.parts:
                raise RuntimeError(
                    "Candidate contains no text parts."
                )

            text = "".join(
                part.text
                for part in candidate.content.parts
                if hasattr(part, "text")
            ).strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned empty text."
                )

            return text

        except Exception as e:
            print(f"[PlannerTool] ERROR: {e}")

            return (
                "⚠️ Unable to generate a study plan at the moment.\n"
                "Please try again later."
            )