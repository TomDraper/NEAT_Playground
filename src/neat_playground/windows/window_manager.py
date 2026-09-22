from PySide6 import QtWidgets

from neat_playground.data.scenario import Scenario
from neat_playground.windows.main_menu import MainMenu
from neat_playground.windows.run_window import RunWindow
from neat_playground.windows.setup_window import SetupWindow
from enum import Enum

class EWindow(Enum):
    MainMenu = 0
    Setup = 1
    Run = 2

class WindowManager():
    def __init__(self, app, manager_holder):
        self.app = app
        self.manager_holder = manager_holder
        self.scenario_manager = manager_holder.scenario_manager
        self.main_menu = None
        self.active_windows = {
            EWindow.Setup: [],
            EWindow.Run: []
        }

    def close_all(self):
        for value in self.active_windows.values():
            if len(value) > 0:
                messageBox = QtWidgets.QMessageBox(self.main_menu)
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setText("This will close all windows.\n Are you sure?")
                messageBox.setWindowTitle("Close All")
                messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                messageBoxValue = messageBox.exec()
        
                if messageBoxValue == QtWidgets.QMessageBox.Cancel:
                    return False
        
        for value in self.active_windows.values():
            for window in value:
                window.close()
            value = []
        self.main_menu = None
        return True
            

    def window_closed(self, window):
        if window == self.main_menu:
            self.close_all()
            return
        
        for value in self.active_windows.values():
            if window in value:
                value.remove(window)

    def open_main_menu(self, scenarios:list[Scenario]):
        if self.main_menu != None:
            raise Exception("Main menu can only be opened once!")

        self.main_menu = MainMenu(self, scenarios)
        self.main_menu.show()

    def open_setup_window(self, button, scenario:Scenario):
        for setup_window in self.active_windows[EWindow.Setup]:
            if setup_window.scenario == scenario:
                setup_window.activateWindow()
                return
        self.create_new_setup_window(button, scenario)

    def create_new_setup_window(self, button, scenario:Scenario):
        setup_window = SetupWindow(self, button, scenario)
        setup_window.show()
        self.active_windows[EWindow.Setup].append(setup_window)
        print(f"Opened setup window for {scenario.scenario_name.display_name} with config {scenario.active_config.display_name}")

    def open_run_window(self, scenario:Scenario):
        for run_window in self.active_windows[EWindow.Run]:
            if run_window.scenario == scenario:
                run_window.activateWindow()
                return
        self.create_new_run_window(scenario)

    def create_new_run_window(self, scenario:Scenario):
        run_window = RunWindow(self.manager_holder, scenario)
        run_window.show()
        self.active_windows[EWindow.Run].append(run_window)
