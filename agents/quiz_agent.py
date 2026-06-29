from tools.quiz_tool import QuizTool


class QuizAgent:

    def __init__(self):

        self.tool = QuizTool()

    def run(self, data: dict):

        exam = data["exam"]

        topics = data["topics"]

        difficulty = data.get(
            "difficulty",
            "Hard"
        )

        num_questions = data.get(
            "num_questions",
            10
        )

        quiz = self.tool.generate_quiz(
            exam=exam,
            topics=topics,
            difficulty=difficulty,
            num_questions=num_questions,
        )

        return quiz