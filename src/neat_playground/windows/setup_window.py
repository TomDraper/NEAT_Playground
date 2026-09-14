from PySide6 import QtCore, QtWidgets, QtGui
from neat_playground.data.scenario import Scenario

class SetupWindow(QtWidgets.QWidget):
    def __init__(self, window_manager, button, scenario:Scenario):
        super().__init__()
        self.window_manager = window_manager
        self.opening_button = button
        self.opening_button.setEnabled(False)
        self.scenario = scenario


        self.title = QtWidgets.QLabel(self.scenario.scenario_name.display_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.active_config = QtWidgets.QLabel("Active Config: " + self.scenario.active_config.display_name)
    
        self.root = QtWidgets.QVBoxLayout(self)

        self.root.addWidget(self.title)
        self.root.addWidget(self.active_config)

    def closeEvent(self, event):
        self.opening_button.setEnabled(True)
        self.window_manager.window_closed(self)
        super().closeEvent(event)

if __name__ == "__main__":
    import os
    import sys
    app = QtWidgets.QApplication([])

    test_scenario_path = "src/neat_playground/scenarios/test_scenario"
    print(test_scenario_path)
    test_scenario = Scenario(test_scenario_path)
    print(test_scenario)

    widget = SetupWindow(test_scenario)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())