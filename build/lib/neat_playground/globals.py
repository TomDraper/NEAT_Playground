import pygame


def init():
    global dt
    dt = 1/60

    global time_step
    time_step = 1 / 60
    
    global screen_size
    screen_size = pygame.Vector2(700, 700)

    global screen_center
    screen_center = pygame.Vector2(screen_size.x / 2, screen_size.y / 2)

    global screen
    screen = pygame.display.set_mode(screen_size)

    global preview_screen
    preview_screen = pygame.surface.Surface(screen_size, pygame.SRCALPHA)
    preview_screen.set_colorkey((255, 0, 255))

    global clock
    clock = pygame.time.Clock()

    global running
    running = True

    global gravity
    gravity = 1
