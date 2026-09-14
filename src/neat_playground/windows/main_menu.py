from PySide6 import QtCore, QtWidgets, QtGui
from neat_playground.windows.components.main_menu_button import MainMenuButton

class MainMenu(QtWidgets.QWidget):
    def __init__(self, window_manager, scenarios):
        super().__init__()
        self.window_manager = window_manager
        self.title = QtWidgets.QLabel("NEAT Playground", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle = QtWidgets.QLabel("Scenarios")

        self.scenario_buttons = []
        for scenario in scenarios:
            button = MainMenuButton(self.window_manager, scenario)
            self.scenario_buttons.append(button)

        self.root = QtWidgets.QVBoxLayout(self)
        self.root.addWidget(self.title)
        self.root.addWidget(self.subtitle)
        for button in self.scenario_buttons:
            self.root.addWidget(button)