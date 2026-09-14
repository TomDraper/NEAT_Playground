import pygame
import globals
from bot import *
from building import *

from pygame import Vector2
import random
import neat
import configparser
import tempfile
import time
import math

globals.init()
globals.screen.fill("black")

def get_random_screen_position():
    return Vector2(globals.screen_size.x * random.random(), (globals.screen_size.y - 32) * random.random() + 32)

number_of_buildings = 30
buildings = []
for i in range(number_of_buildings):
    buildings.append(Building(i, get_random_screen_position()))

config_parser = configparser.ConfigParser()
config_parser.read('travelling_salesman/config-travelling-salesman.ini')
config_parser['DefaultGenome']['num_outputs'] = str(number_of_buildings)

with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
    config_parser.write(f)
    config_path = f.name

def output_to_values(outputs):
    return sorted(range(number_of_buildings), key=lambda i: outputs[i])

def get_fitness(destination_list):
    for i in range(number_of_buildings):
        if i not in destination_list:
            return -9999999

    prev_index = None
    distance = 0
    for index in destination_list:
        if prev_index is not None:
            distance += (buildings[prev_index].pos - buildings[index].pos).magnitude()
        prev_index = index

    return -distance

def draw_route(destination_list):
    prev_index = None
    for index in destination_list:
        if prev_index is not None:
            draw.line(globals.screen, (255, 0, 0), buildings[prev_index].pos, buildings[index].pos)
        prev_index = index

# TO-DO: Write this in an actual neat way that definitely exists not just the first "It works" solution.
def get_percentage_text(percentage_complete):
    left_fill = ""
    right_fill = ""
    floored_percentage = math.floor(percentage_complete)
    for i in range(50):
        if i < floored_percentage:
            left_fill += "X"
        else:
            left_fill += "-"
    for j in range(50, 100):
        if j < floored_percentage:
            right_fill += "X"
        else:
            right_fill += "-"
    return f"[{left_fill}{floored_percentage:.0f}%{right_fill}]"

# TO-DO: Sort out this horribleness.
global current_best_fitness
global current_best_output
global current_loop
global loop_max
global previous_percentage_text
current_best_output = None
current_best_fitness = -999999
current_loop = 0
loop_max = 3000
previous_percentage_text = get_percentage_text(0)

def eval_genomes(genomes, config):
    global current_best_fitness
    global current_best_output
    global current_loop
    global loop_max
    global previous_percentage_text
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        output = net.activate([1.0])
        output = output_to_values(output)
        fitness = get_fitness(output)
        genome.fitness = fitness
        if fitness > current_best_fitness:
            current_best_fitness = fitness
            current_best_output = output
            print("Loop:", current_loop, "Fitness:", current_best_fitness, "Output:", current_best_output)
            globals.screen.fill("black")
            draw_route(current_best_output)
            pygame.display.update()

    current_loop += 1
    percentage_complete = current_loop / loop_max * 100
    percentage_text = get_percentage_text(percentage_complete)
    if percentage_text != previous_percentage_text:
        print(percentage_text)
        previous_percentage_text = percentage_text
    


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

config.genome_config.num_outputs = number_of_buildings
print(config.genome_config.num_outputs)
p = neat.Population(config)
#p.add_reporter(neat.StdOutReporter(True))

start_time = time.time()
winner = p.run(eval_genomes, loop_max)
end_time = time.time()
print(f"Solution found in {end_time - start_time} seconds")
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
output = winner_net.activate([1.0])

destination_list = output_to_values(output)

while globals.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            globals.running = False

    globals.screen.fill("black")

    for building in buildings:
        building.draw()

    draw_route(destination_list)

    text_surface = globals.game_font.render(str(destination_list), False, (255, 0, 0))
    globals.screen.blit(text_surface, (10, 10))
    pygame.display.update()

pygame.quit()