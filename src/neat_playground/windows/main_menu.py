from PySide6 import QtCore, QtWidgets
from neat_playground.windows.components.main_menu_button import MainMenuButton

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self, window_manager, scenarios):
        super().__init__()
        self.window_manager = window_manager
        self.central_widget = QtWidgets.QWidget(self)
        self.root = QtWidgets.QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.title = QtWidgets.QLabel("NEAT Playground", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle = QtWidgets.QLabel("Scenarios")

        self.scenario_buttons = []
        for scenario in scenarios:
            button = MainMenuButton(self.window_manager, scenario)
            self.scenario_buttons.append(button)

        self.root.addWidget(self.title)
        self.root.addWidget(self.subtitle)
        for button in self.scenario_buttons:
            self.root.addWidget(button)

    def closeEvent(self, event):
        if self.window_manager.close_all():
            super().closeEvent(event)
        else:
            event.ignore()

    def set_button_state(self, scenario, enabled):
        for button in self.scenario_buttons:
            if button.scenario == scenario:
                if enabled:
                    button.setEnabled(enabled)