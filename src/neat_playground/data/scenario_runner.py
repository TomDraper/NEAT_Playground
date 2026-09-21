from abc import ABC, abstractmethod

from neat_playground.data.scenario import Scenario
from neat_playground.windows.run_window import RunWindow

class ScenarioRunner(ABC):
    def __init__(self, scenario:Scenario):
        self.scenario = scenario
        self.run_window = RunWindow()
        self.training_callbacks = []
        self.training_percent = 0
        self.run_window.show()

    @abstractmethod
    def setup_run_window(self):
        pass

    @abstractmethod
    def run(self, config):
        pass
    
    @abstractmethod
    def fitness_function(self, genomes, config):
        pass

    @abstractmethod
    def draw_genome(self, genome):
        pass

    @abstractmethod
    def draw_genomes(self, genomes):
        pass

