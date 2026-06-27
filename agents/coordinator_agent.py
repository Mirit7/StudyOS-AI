from agents.planner_agent import PlannerAgent


class CoordinatorAgent:

    def __init__(self):
        self.planner = PlannerAgent()

    def execute(self, task: str, data: dict):

        print(f"[Coordinator] Executing: {task}")

        if task == "study_plan":
            return self.planner.run(data)

        raise ValueError(f"Unknown task: {task}")