import importlib.util
from pathlib import Path

from neat_playground.data.scenario import Scenario

class ScenarioManager():
    def __init__(self):
        pass

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
    manager = ScenarioManager()
    test_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    manager.run_scenario(test_scenario)