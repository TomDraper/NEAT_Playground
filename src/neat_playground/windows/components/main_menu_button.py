from PySide6 import QtCore, QtWidgets

class MainMenuButton(QtWidgets.QWidget):
    def __init__ (self, scenario_name, configs, description):
        super().__init__()
        self.scenario_name = scenario_name
        self.configs = configs
        self.selected_config = configs[0]
        self.description = description

        self.root = QtWidgets.QHBoxLayout(self)

        self.title = QtWidgets.QLabel(self.scenario_name)

        self.config_dropdown = QtWidgets.QComboBox()
        self.config_dropdown.addItems(self.configs)
        self.config_dropdown.activated.connect(self.config_changed)

        self.open_button = QtWidgets.QPushButton("Open")
        self.open_button.clicked.connect(self.open)

        self.root.addWidget(self.title)
        self.root.addWidget(self.config_dropdown)
        self.root.addWidget(self.open_button)

    @QtCore.Slot()
    def config_changed(self, index):
        self.selected_config = self.configs[index]
        print(f"Index changed to {index} -- {self.selected_config}")

    @QtCore.Slot()
    def open(self):
        print(f"Trying to open {self.scenario_name} with config {self.selected_config}.")

    def focusInEvent(self, event):
        print("Main window/widget focus IN")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        print("Main window/widget focus OUT")
        super().focusOutEvent(event)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(True)
    app.setStyle("Fusion")
    widget = MainMenuButton("Test Scenario 1", ["Config 1", "Config 2", "Config 3"], "Test Description 1")
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())