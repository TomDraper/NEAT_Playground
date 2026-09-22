from neat_playground.managers.scenario_runner_manager import ScenarioRunnerManager
from neat_playground.windows.window_manager import WindowManager

class ManagerHolder:
    def __init__(self, app):
        self.app = app
        self.scenario_manager = ScenarioRunnerManager()
        self.window_manager = WindowManager(self.app, self)
        