from tools.quiz_tool import generate_quiz

quiz = generate_quiz(
    exam="JEE",
    topic="Trigonometry",
    num_questions=5
)

print(quiz)