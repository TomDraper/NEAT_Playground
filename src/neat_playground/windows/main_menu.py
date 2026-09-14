import sys
from PySide6 import QtCore, QtWidgets, QtGui
from windows.components.main_menu_button import *
from data.scenario import *

class MainMenu(QtWidgets.QWidget):
    def __init__(self, scenarios):
        super().__init__()

        self.title = QtWidgets.QLabel("NEAT Playground", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle = QtWidgets.QLabel("Scenarios")

        self.scenario_buttons = []
        for scenario in scenarios:
            button = MainMenuButton(scenario.scenario_display_name, scenario.configs_display_names, "Test Description 1")
            self.scenario_buttons.append(button)

        self.root = QtWidgets.QVBoxLayout(self)
        self.root.addWidget(self.title)
        self.root.addWidget(self.subtitle)
        for button in self.scenario_buttons:
            self.root.addWidget(button)