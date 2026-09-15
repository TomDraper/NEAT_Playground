import pytest
from neat_playground.data.scenario import *
from neat_playground.managers.scenario_runner_manager import get_runner_class

def test_create_scenario_with_valid_parameters():
    valid_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    assert valid_scenario != None

def test_raise_exception_when_creating_scenario_with_invalid_parameters():
    with pytest.raises(Exception):
        invalid_scenario = Scenario("ThisShouldn'tExist")


def test_get_runner_class_returns_instance_for_valid_scenario():
    scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    runner = get_runner_class(scenario)
    assert runner is not None
    assert runner.scenario == scenario
