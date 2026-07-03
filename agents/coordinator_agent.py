from agents.planner_agent import PlannerAgent
from agents.quiz_agent import QuizAgent
from agents.analytics_agent import AnalyticsAgent
from agents.memory_agent import MemoryAgent
from agents.mentor_agent import MentorAgent

class CoordinatorAgent:

    def __init__(self):

        self.planner = PlannerAgent()

        self.quiz = QuizAgent()

        self.analytics = AnalyticsAgent()

        self.memory = MemoryAgent()

        self.mentor = MentorAgent()

        self.routes = {

            "study_plan": self.planner,

            "generate_quiz": self.quiz,

            "evaluate_quiz": self.analytics,

            "save_report": self.memory,

            "mentor_feedback": self.mentor

        }

    def execute(self, task: str, data: dict):

        print(f"[Coordinator] {task}")

        agent = self.routes.get(task)

        if not agent:
            raise ValueError(f"Unknown task: {task}")

        return agent.run(data)