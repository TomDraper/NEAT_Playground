from PySide6 import QtCore, QtWidgets, QtGui
from neat_playground.data.scenario import Scenario
from neat_playground.data.scenario_runner import ScenarioRunner

class RunWindow(QtWidgets.QMainWindow):
    def __init__(self, manager_holder, scenario:Scenario):
        super().__init__()
        self.manager_holder = manager_holder
        self.window_manager = manager_holder.window_manager
        self.scenario_manager = manager_holder.scenario_manager
        self.scenario = scenario

        self.central_widget = QtWidgets.QWidget(self)
        self.root = QtWidgets.QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.title = QtWidgets.QLabel("TITLE")
        self.run_panel = QtWidgets.QFrame()
        self.loading_bar = QtWidgets.QProgressBar()
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.clicked.connect(self.run)

        self.root.addWidget(self.title)
        self.root.addWidget(self.run_panel)
        self.root.addWidget(self.loading_bar)
        self.root.addWidget(self.run_button)

        self.setup_runner()

    def setup_runner(self):
        self.scenario_runner:ScenarioRunner = self.scenario_manager.get_runner_class(self.scenario)
        self.scenario_runner.run_window = self
        self.scenario_runner.setup_run_window()

    def set_title(self, title):
        self.title.setText(title)

    def set_loading_percent(self, percent:int):
        self.loading_bar.setValue(percent)

    def run(self):
        self.scenario_runner.run()

    def closeEvent(self, event):
        self.window_manager.window_closed(self)
        super().closeEvent(event)