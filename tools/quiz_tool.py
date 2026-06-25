from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("AQ.Ab8RN6IfxtBv_ylbOzhBNzxEuVcTLcur4-myOK7dwjeoYAco0Q")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Generate 5 JEE trigonometry questions"
)



def generate_quiz(
    exam,
    topic,
    num_questions=5
):
    prompt = f"""
    You are an expert competitive exam question setter.

    Exam: {exam}
    Topic: {topic}

    Generate {num_questions} multiple-choice questions.

    Requirements:
    - Difficulty level appropriate for {exam}
    - Four options (A, B, C, D)
    - Include correct answer after each question
    - Clear formatting

    Return ONLY valid JSON.

    Format:

    [
    {
        "question": "...",
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "...",
        "answer": "A"
    }
    ]
    """

    response = model.generate_content(prompt)

    return response.text
# Return ONLY valid JSON.

# Format:

# [
#   {
#     "question": "...",
#     "A": "...",
#     "B": "...",
#     "C": "...",
#     "D": "...",
#     "answer": "A"
#   }
# ]