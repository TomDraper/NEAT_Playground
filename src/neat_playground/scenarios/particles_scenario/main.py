import neat

from neat_playground.data.scenario import Scenario
from neat_playground.data.scenario_runner import ScenarioRunner

class Test_ScenarioRunner(ScenarioRunner):
    def __init__(self, scenario:Scenario):
        super().__init__(scenario)
        self.xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
        self.xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

    def run(self, config):
        config = neat.Config(
            neat.DefaultGenome, 
            neat.DefaultReproduction, 
            neat.DefaultSpeciesSet, 
            neat.DefaultStagnation,
            config)

        pop = neat.Population(config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        
        winner = pop.run(self.fitness_function, 200)
        print(f'\nBest genome:\n{winner!s}')

        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
        for xi, xo in zip(self.xor_inputs, self.xor_outputs):
            output = winner_net.activate(xi)
            print(f"input {xi!r}, expected output {round(xo[0])}, got {round(output[0])}")

    def fitness_function(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 4.0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            for xi, xo in zip(self.xor_inputs, self.xor_outputs):
                output = net.activate(xi)
                genome.fitness -= (output[0] - xo[0]) ** 2
        
        
    
    def draw_genome(self, genome):
        pass

    def draw_genomes(self, genomes):
        pass