from tools.planner_tool import PlannerTool


class PlannerAgent:

    def __init__(self):
        self.tool = PlannerTool()

    def run(self, data: dict):

        exam = data["exam"]
        days_left = data["days_left"]
        study_hours = data["study_hours"]

        from tools.database_tool import DatabaseTool

        db = DatabaseTool()

        weak_topics = db.get_most_recent_weak_topics()

        planner_output = self.tool.generate_plan(

            exam,

            days_left,

            study_hours,

            weak_topics

        )

        return planner_output