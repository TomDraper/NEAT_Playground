from PySide6 import QtCore, QtWidgets

from neat_playground.data.scenario import Scenario

def sort_alphabetically_default_first(string):
    return (string.lower() != "default", string)

class MainMenuButton(QtWidgets.QWidget):
    def __init__ (self, window_manager, scenario:Scenario):
        super().__init__()
        self.window_manager = window_manager
        self.scenario = scenario
        self.scenario_name = scenario.scenario_name.display_name
        self.scenario_configs = scenario.configs
        self.configs = []
        for dnp in scenario.configs:
            self.configs.append(dnp.display_name)

        self.configs.sort(key=sort_alphabetically_default_first)
        self.selected_config = scenario.active_config
        self.description = "Test description"

        self.root = QtWidgets.QHBoxLayout(self)

        self.title = QtWidgets.QLabel(self.scenario_name)

        self.config_dropdown = QtWidgets.QComboBox()
        self.config_dropdown.addItems(self.configs)
        self.config_dropdown.setCurrentText(self.selected_config.display_name)
        
        self.config_dropdown.activated.connect(self.config_changed)

        self.open_button = QtWidgets.QPushButton("Open")
        self.open_button.clicked.connect(self.open)

        self.root.addWidget(self.title)
        self.root.addWidget(self.config_dropdown)
        self.root.addWidget(self.open_button)

    @QtCore.Slot(int)
    def config_changed(self, index):
        self.selected_config = self.configs[index]
        self.scenario.set_active_config(self.selected_config)

    @QtCore.Slot()
    def open(self):
        self.window_manager.open_setup_window(self, self.scenario)
        print(f"Trying to open {self.scenario_name} with config {self.selected_config}.")

    def setEnabled(self, enabled):
        # Redraw config box if enabled == true
        # To-Do: Expand to a true redraw as we may add or remove configs as well. 
        if enabled:
            self.selected_config = self.scenario.active_config
            self.config_dropdown.setCurrentText(self.selected_config.display_name)
        self.config_dropdown.setEnabled(enabled)
        
