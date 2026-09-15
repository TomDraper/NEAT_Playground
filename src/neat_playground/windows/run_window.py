from PySide6 import QtCore, QtWidgets
from neat_playground.data.scenario import Scenario

class RunWindow(QtWidgets.QWidget):
    def __init__(self, window_manager, button, scenario:Scenario):
        self.scenario = scenario
        self.config = scenario.active_config
        