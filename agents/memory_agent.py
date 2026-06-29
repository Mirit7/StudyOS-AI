from tools.memory_tool import MemoryTool


class MemoryAgent:

    def __init__(self):

        self.tool = MemoryTool()

    def run(self, data: dict):

        return self.tool.save_report(data)