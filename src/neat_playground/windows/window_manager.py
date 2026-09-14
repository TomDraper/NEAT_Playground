from neat_playground.windows.main_menu import MainMenu
from neat_playground.windows.setup_window import SetupWindow
import sys
from enum import Enum

class EWindow(Enum):
    MainMenu = 0
    Setup = 1

class WindowManager():
    def __init__(self, app):
        self.app = app
        self.active_windows = {
            EWindow.Setup: []
        }

    def open_main_menu(self, scenarios):
        if EWindow.MainMenu in self.active_windows:
            raise Exception("Main menu can only be opened once!")
        
        main_menu = MainMenu(self, scenarios)
        main_menu.resize(800, 600)
        main_menu.show()
        self.active_windows[EWindow.MainMenu] = main_menu

    def open_setup_window(self, scenario):
        for setup_window in self.active_windows[EWindow.Setup]:
            if setup_window.scenario == scenario:
                setup_window.show()
                return
        self.create_new_setup_window(scenario)

    def create_new_setup_window(self, scenario):
        setup_window = SetupWindow(self, scenario)
        setup_window.parentWidget = self.active_windows[EWindow.MainMenu]
        setup_window.show()
        self.active_windows[EWindow.Setup].append(setup_window)
        print(f"Opened setup window for {scenario.scenario_name.display_name} with config {scenario.active_config.display_name}")