from tools.mentor_tool import MentorTool
from tools.database_tool import DatabaseTool


class MentorAgent:

    def __init__(self):

        self.mentor_tool = MentorTool()
        self.db = DatabaseTool()

    def run(self, data):

        history = self.db.get_last_reports(limit=10)

        feedback = self.mentor_tool.generate_feedback(history)

        return feedback