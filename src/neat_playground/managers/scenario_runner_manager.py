import importlib.util
from pathlib import Path

from neat_playground.data.scenario import Scenario

class ScenarioRunnerManager():
    def __init__(self):
        pass

    def run_scenario(self, scenario: Scenario):
        runner_class = self.get_runner_class(scenario)
        full_config_path = Path.joinpath(Path(scenario.config_dir), Path(scenario.active_config.name))
        #runner_class.setup_run_window()
        return runner_class.run(full_config_path)


    def get_runner_class(self, scenario: Scenario):
        path = Path(scenario.main_file_path)
        spec = importlib.util.spec_from_file_location(path.stem, path)

        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load scenario module from: {path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        runner_cls = getattr(module, "Test_ScenarioRunner")
        return runner_cls(scenario)


if __name__ == "__main__":
    manager = ScenarioRunnerManager()
    test_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    manager.run_scenario(test_scenario)