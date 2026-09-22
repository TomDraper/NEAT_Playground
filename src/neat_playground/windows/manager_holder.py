from neat_playground.managers.scenario_manager import ScenarioManager
from neat_playground.windows.window_manager import WindowManager

class ManagerHolder:
    def __init__(self, app):
        self.app = app
        self.scenario_manager = ScenarioManager()
        self.window_manager = WindowManager(self.app, self)
        