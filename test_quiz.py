from agents.quiz_agent import QuizAgent

agent = QuizAgent()

quiz = agent.run(
    {
        "exam": "JEE",
        "topics": [
            "Trigonometry",
            "Vectors"
        ],
        "difficulty": "Medium",
        "num_questions": 5
    }
)

print(quiz)