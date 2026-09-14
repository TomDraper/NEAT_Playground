import pytest
from neat_playground.data.scenario import *

def test_create_scenario_with_valid_parameters():
    valid_scenario = Scenario("src/neat_playground/scenarios/test_scenario")
    assert valid_scenario != None

def test_raise_exception_when_creating_scenario_with_invalid_parameters():
    with pytest.raises(Exception):
        invalid_scenario = Scenario("ThisShouldn'tExist")
