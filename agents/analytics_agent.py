from tools.analytics_tool import AnalyticsTool


class AnalyticsAgent:

    def __init__(self):
        # self.analytics = AnalyticsAgent()
        self.tool = AnalyticsTool()

    def run(self, data: dict):

        quiz = data["quiz"]

        student_answers = data["student_answers"]

        report = self.tool.evaluate_quiz(
            quiz,
            student_answers
        )

        return report