from abc import ABC, abstractmethod

from neat_playground.data.scenario import Scenario

class ScenarioRunner(ABC):
    def __init__(self, scenario:Scenario):
        self.scenario = scenario

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

