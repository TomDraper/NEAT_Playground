import neat
from abc import ABC, abstractmethod
from neat_playground.data.scenario import Scenario

class ScenarioRunner(ABC):
    def __init__(self, scenario:Scenario):
        self.scenario = scenario
        self.training_callbacks = []
        self.training_percent = 0
        self.update_config()

    def update_config(self):
        config_path = self.scenario.get_full_config_path()
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    def reset(self):
        self.training_percent = 0

    @abstractmethod
    def setup_run_window(self):
        pass

    @abstractmethod
    def run(self):
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

