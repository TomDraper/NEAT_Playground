import os
import errno

class Scenario:
    def __init__(self, root_dir, active_config="default"):
        self.root_dir = root_dir
        self.config_dir = os.path.join(root_dir, "configs")
        self.settings_dir = os.path.join(root_dir, "settings")
        self.main_file_path = os.path.join(root_dir, "main.py")

        self._validate_paths()

        self.scenario_name = os.path.basename(self.root_dir)
        self.scenario_display_name = self.scenario_name.replace("_", " ").title()

        self.configs = self._get_configs()
        self.configs_display_names = [name.replace(".ini", "") for name in self.configs]
        self.settings = self._get_settings()
        self.settings_display_names = [name.replace(".ini", "") for name in self.settings]
        self.active_config = self.set_active_config(active_config)

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
                files.append(f)
        return files

    def _get_settings(self):
        files = []
        for f in os.listdir(self.settings_dir):
            file_path = os.path.join(self.settings_dir, f)
            if os.path.isfile(file_path):
                files.append(f)
        return files
    
    def set_active_config(self, config_name):
        if config_name.endswith(".ini") == False:
            config_name += ".ini"
        self.active_config = os.path.join(self.config_dir, config_name)
        return self.active_config

    def __str__(self):
        return_string = "---- START SCENARIO DATA OBJECT ----\n"
        return_string += "Directory Info:\n"
        return_string += f"    {self.root_dir=}\n"
        return_string += f"    {self.config_dir=}\n"
        return_string += f"    {self.settings_dir=}\n"
        return_string += f"    {self.main_file_path=}\n"
        return_string += "Identifing Data:\n"
        return_string += f"    {self.scenario_name=}\n"
        return_string += f"    {self.scenario_display_name=}\n"
        return_string += "Configs:\n"
        return_string += f"    ACTIVE: {self.active_config}\n"
        return_string += f"    {self.configs=}\n"
        return_string += f"    {self.configs_display_names=}\n"
        return_string += "Setting Files:\n"
        return_string += f"    {self.settings}\n"
        return_string += f"    {self.settings_display_names=}\n"
        return_string += "---- END SCENARIO DATA OBJECT ----"
        return return_string


if __name__ == "__main__":
    valid_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    print(valid_scenario)
    print("END")