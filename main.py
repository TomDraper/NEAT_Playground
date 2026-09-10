# Example file showing a circle moving on screen
import pygame
import globals
from scripts.particle import *
from scripts.mouse_tracker import *
import neat

# pygame setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 24)

# game setup
globals.init()
mouse_tracker = MouseTracker()
click_drag_vel_modifier = 5

attractor = Attractor(globals.screen_center, 1000)
orbitors = []

def AddNewOrbitor(pos, velocity):
    orbitors.append(Orbitor(pos, pygame.Vector2(0, 0), velocity, 1))


# ---- NEAT STUFF ----

static_start_pos = Vector2(globals.screen_center.x - 250, globals.screen_center.y)

def output_to_values(velocity_x, velocity_y):
    return velocity_x * 100.0 - 50.0, velocity_y * 100.0 - 50.0

def eval_genomes(genomes, config):
    globals.screen.fill("black")
    best_fitness = -9999999
    best_genome = None
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        output = net.activate([1.0])
        velocity_x, velocity_y = output_to_values(output[0], output[1])
        fitness = basic_fitness(static_start_pos, velocity_x, velocity_y, attractor, draw_result=False)
        genome.fitness = fitness
        if fitness > best_fitness:
            best_fitness = fitness
            best_genome = genome

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    output = net.activate([1.0])
    velocity_x, velocity_y = output_to_values(output[0], output[1])
    basic_fitness(static_start_pos, velocity_x, velocity_y, attractor, draw_result=True)
    print("Best: ", best_fitness, ". Pos: ", static_start_pos, ". Vel: ", velocity_x, " / ", velocity_y)
    pygame.display.update()
    globals.dt = globals.clock.tick(60) / 1000

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-particles-static-start.ini')

p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))

winner = p.run(eval_genomes, 100)

print('\nBest genome:\n{!s}'.format(winner))
winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
output = winner_net.activate([1.0])

values = output_to_values(output[0], output[1])
final_velocity = Vector2(values[0], values[1])

add_counter = 0
# ---- END NEAT STUFF ----

while globals.running:
    #poll for events
    #pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            globals.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_tracker.clicked(event.pos)
        if event.type == pygame.MOUSEMOTION:
            mouse_tracker.current = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            diff = mouse_tracker.released(event.pos)
            AddNewOrbitor(mouse_tracker.last_click, diff / click_drag_vel_modifier)


    globals.screen.fill("black")
    globals.preview_screen.fill((255, 0, 255))

    delete_these = []
    for orbitor in orbitors:
        orbitor.calc_force(attractor)
        orbitor.update()
        orbitor.draw()
        if orbitor.delete:
            delete_these.append(orbitor)

    for delete_entry in delete_these:
        orbitors.remove(delete_entry)

    attractor.draw()

    if mouse_tracker.held == True:
        diff = mouse_tracker.current - mouse_tracker.last_click
        vel = diff / click_drag_vel_modifier
        pygame.draw.line(globals.screen, (255, 0, 0), mouse_tracker.last_click, mouse_tracker.current)
        vel_text = "Vel: " + str(vel.x) + " / " + str(vel.y)
        vel_text = my_font.render(vel_text, False, (255, 0, 0))
        globals.screen.blit(vel_text, mouse_tracker.last_click)
        PreviewOrbitor(mouse_tracker.last_click, diff / click_drag_vel_modifier, attractor, 100, True)

    # Draw the test
    basic_fitness(static_start_pos, final_velocity.x, final_velocity.y, attractor, draw_result = True)

    text_surface = my_font.render(str(globals.clock.get_fps()), False, (255, 0, 0))
    globals.screen.blit(text_surface, (100, 100))

    globals.screen.blit(globals.preview_screen)

    pygame.display.update()
    globals.dt = globals.clock.tick(60) / 1000

    add_counter += globals.dt
    if (add_counter > 3):
        AddNewOrbitor(static_start_pos, final_velocity)
        print("Added at: ", static_start_pos, " with vel: ", final_velocity)
        add_counter = 0

pygame.quit()