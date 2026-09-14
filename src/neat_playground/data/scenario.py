import os
import errno

from neat_playground.data.display_name_property import DisplayNameProperty

class Scenario:
    def __init__(self, root_dir, active_config="default.ini"):
        self.root_dir = root_dir
        self.config_dir = os.path.join(root_dir, "configs")
        self.settings_dir = os.path.join(root_dir, "settings")
        self.main_file_path = os.path.join(root_dir, "main.py")

        self._validate_paths()

        scenario_base_name = os.path.basename(self.root_dir)
        self.scenario_name = DisplayNameProperty(scenario_base_name, scenario_base_name.replace("_", " ").title()) 

        self.configs = self._get_configs()
        self.settings = self._get_settings()

        self.active_config = DisplayNameProperty("default.ini", "Default")
        self.set_active_config(active_config)

    def _validate_paths(self):
        if os.path.exists(self.root_dir) == False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.root_dir)

        if os.path.exists(self.config_dir) == False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.config_dir)

        if os.path.exists(self.settings_dir) == False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.settings_dir)

        if os.path.isfile(self.main_file_path) == False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.main_file_path)

    def _get_configs(self):
        files = []
        for f in os.listdir(self.config_dir):
            file_path = os.path.join(self.config_dir, f)
            if os.path.isfile(file_path):
                prop = DisplayNameProperty(f, f.replace(".ini", "").replace("_", " ").title())
                files.append(prop)
        return files

    def _get_settings(self):
        files = []
        for f in os.listdir(self.settings_dir):
            file_path = os.path.join(self.settings_dir, f)
            if os.path.isfile(file_path):
                prop = DisplayNameProperty(f, f.replace(".ini", "").replace("_", " ").title())
                files.append(prop)
        return files

    def get_config_by_name(self, config_name):
        for config in self.configs:
            if config.hasName(config_name):
                return config
        return None
    
    def set_active_config(self, config_name):
        new_config = self.get_config_by_name(config_name)
        if new_config == None:
            raise Exception(f"Could not find a config with the name {config_name}.")
        else:
            self.active_config = new_config
        print(f"Active config of {self.scenario_name.display_name} changed to {self.active_config.display_name}")

    def _config_list_string(self, padding = 0):
        return_string = ""
        for prop in self.configs:
            for i in range(padding):
                return_string += " "
            return_string += prop.__str__()
            return_string += "\n"
        return return_string

    def _setting_list_string(self, padding = 0):
        return_string = ""
        for prop in self.settings:
            for i in range(padding):
                return_string += " "
            return_string += prop.__str__()
            return_string += "\n"
        return return_string

    def __str__(self):
        return_string = "---- START SCENARIO DATA OBJECT ----\n"
        return_string += "Directory Info:\n"
        return_string += f"    {self.root_dir=}\n"
        return_string += f"    {self.config_dir=}\n"
        return_string += f"    {self.settings_dir=}\n"
        return_string += f"    {self.main_file_path=}\n"
        return_string += "Identifing Data:\n"
        return_string += f"    {self.scenario_name}\n"
        return_string += "Configs:\n"
        return_string += f"    ACTIVE:\n"
        return_string += f"        {self.active_config}\n"
        return_string += f"    AVAILABLE:\n"
        return_string += f"{self._config_list_string(8)}"
        return_string += "Setting Files:\n"
        return_string += f"{self._setting_list_string(4)}"
        return_string += "---- END SCENARIO DATA OBJECT ----"
        return return_string

class Scenario_Save_State:
    def __init__(self, scenario):
        self.scenario_name = scenario.scenario_name
        self.active_config = scenario.active_config

if __name__ == "__main__":
    valid_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    print(valid_scenario)
    print("END")