from tools.planner_tool import PlannerTool


class PlannerAgent:

    def __init__(self):

        self.tool = PlannerTool()

    def run(self, data: dict):

        exam = data["exam"]
        days_left = data["days_left"]
        study_hours = data["study_hours"]

        study_plan = self.tool.generate_plan(
            exam,
            days_left,
            study_hours
        )

        return study_plan