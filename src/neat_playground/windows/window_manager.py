from PySide6 import QtWidgets

from neat_playground.windows.main_menu import MainMenu
from neat_playground.windows.setup_window import SetupWindow
import sys
from enum import Enum

class EWindow(Enum):
    MainMenu = 0
    Setup = 1

class WindowManager():
    def __init__(self, app, scenario_manager):
        self.app = app
        self.scenario_manager = scenario_manager
        self.main_menu = None
        self.active_windows = {
            EWindow.Setup: []
        }

    def close_all(self):
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

    def open_main_menu(self, scenarios):
        if self.main_menu != None:
            raise Exception("Main menu can only be opened once!")

        self.main_menu = MainMenu(self, scenarios)
        # self.main_window = QtWidgets.QMainWindow()
        # self.main_window.setCentralWidget(main_menu)
        self.main_menu.show()

    def open_setup_window(self, button, scenario):
        for setup_window in self.active_windows[EWindow.Setup]:
            if setup_window.scenario == scenario:
                setup_window.activateWindow()
                return
        self.create_new_setup_window(button, scenario)

    def create_new_setup_window(self, button, scenario):
        setup_window = SetupWindow(self, button, scenario)
        
        #setup_window.parentWidget = self.active_windows[EWindow.MainMenu]
        setup_window.show()
        self.active_windows[EWindow.Setup].append(setup_window)
        print(f"Opened setup window for {scenario.scenario_name.display_name} with config {scenario.active_config.display_name}")

    def run_scenario(self, scenario):
        self.scenario_manager.run_scenario(scenario)