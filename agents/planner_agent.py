from tools.planner_tool import PlannerTool


class PlannerAgent:

    def __init__(self):
        self.tool = PlannerTool()

    def run(self, data: dict):

        exam = data["exam"]
        days_left = data["days_left"]
        study_hours = data["study_hours"]

        planner_output = self.tool.generate_plan(
            exam,
            days_left,
            study_hours
        )

        return planner_output