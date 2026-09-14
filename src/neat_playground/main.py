import os
import errno
from PySide6 import QtWidgets
import sys

from neat_playground.data.scenario import Scenario
from neat_playground.windows.window_manager import WindowManager
# from neat_playground.windows.main_menu import MainMenu
# from neat_playground.windows.setup_window import SetupWindow

def get_scenario_directories(scenario_root_directory):
        dirs = []
        for f in os.listdir(scenario_root_directory):
            dir_path = os.path.join(scenario_root_directory, f)
            if os.path.isdir(dir_path):
                dirs.append(dir_path)
        return dirs

def create_scenario_data(scenario_directories):
    scenarios = []
    for scenario in scenario_directories:
        try:
            scenarios.append(Scenario(scenario))
        except Exception as e:
            print(e)
            print(f"Failed to find scenario {scenario}") 
            
    return scenarios



# Get Root Path and Scenario Path - Ensure they are valid.
root_path = os.path.dirname(__file__)
scenario_root_dir = os.path.join(root_path, "scenarios")

if os.path.exists(scenario_root_dir) == False:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), scenario_root_dir)

# Retrieve the scenarios from the scenario directory.
scenario_dirs = get_scenario_directories(scenario_root_dir)
scenarios = create_scenario_data(scenario_dirs)

# Build our application and display the main menu.
app = QtWidgets.QApplication([])

window_manager = WindowManager(app)
window_manager.open_main_menu(scenarios)

sys.exit(app.exec())