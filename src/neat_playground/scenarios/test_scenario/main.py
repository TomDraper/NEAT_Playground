import math
import neat

from neat_playground.data.scenario import Scenario
from neat_playground.data.scenario_runner import ScenarioRunner

class Test_ScenarioRunner(ScenarioRunner):
    def __init__(self, scenario:Scenario):
        super().__init__(scenario)
        self.training_callbacks.append(self.update_progress_bar)
        self.xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
        self.xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]
        self.run_window = None

    def setup_run_window(self):
        super().setup_run_window()
        self.run_window.set_title("Test Scenario")

    def update_progress_bar(self):
        self.run_window.set_loading_percent(math.floor(self.training_percent / 200 * 100))

    def get_config():
        return super().get_config()

    def run(self):
        self.reset()
        self.update_config()

        pop = neat.Population(self.config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        
        winner = pop.run(self.fitness_function, 200)
        print(f'\nBest genome:\n{winner!s}')

        winner_net = neat.nn.FeedForwardNetwork.create(winner, self.config)
        for xi, xo in zip(self.xor_inputs, self.xor_outputs):
            output = winner_net.activate(xi)
            print(f"input {xi!r}, expected output {round(xo[0])}, got {round(output[0])}")

        return winner, winner_net

    def fitness_function(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 4.0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            for xi, xo in zip(self.xor_inputs, self.xor_outputs):
                output = net.activate(xi)
                genome.fitness -= (output[0] - xo[0]) ** 2

        self.training_percent += 1
        for callback in self.training_callbacks:
            callback()
    
    def draw_genome(self, genome):
        pass

    def draw_genomes(self, genomes):
        pass