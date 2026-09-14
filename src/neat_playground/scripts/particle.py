from pygame import Vector2
from pygame import draw
from functools import singledispatchmethod
import globals
import numpy as np

itterations = 2000

class Particle:
    def __init__(self, position, acceleration, velocity, show_path=True):
        self.pos = position.copy()
        self.acc = acceleration.copy()
        self.vel = velocity.copy()
        self.show_path = show_path
        self.lifetime = itterations * globals.time_step
        self.life = 0
        self.prev_positions = []
        self.delete = False

    def update(self):
        self.vel += self.acc * globals.time_step
        self.pos += self.vel * globals.time_step
        self.acc = Vector2(0, 0)
        if self.show_path:
            self.prev_positions.append(self.pos.copy())
            if len(self.prev_positions) > 100:
                del self.prev_positions[0]
        self.life += globals.time_step
        if self.life > self.lifetime:
            self.delete = True

    def draw(self):
        draw.circle(globals.screen, (255, 0, 0), self.pos, 5)
        if self.show_path:
            self.draw_path()

    def draw_path(self):
        prev_pos = self.pos
        for pos in reversed(self.prev_positions):
            draw.line(globals.screen, (255, 0, 0), prev_pos, pos)
            prev_pos = pos

    # def apply_force(self, force):
    #     self.acc += force

class MassParticle(Particle):
    def __init__(self, position, acceleration, velocity, mass):
        super().__init__(position, acceleration, velocity)
        self.mass = mass

class Attractor():
    def __init__(self, position, mass):
        self.pos = position
        self.mass = mass

    def draw(self):
        draw.circle(globals.screen, (0, 255, 0), self.pos, 10)

    @singledispatchmethod
    def calc_force(self, *args):
        return Vector2(0, 0)

    @calc_force.register
    def _(self, other:Particle):
        dir = self.pos - other.pos;
        dist = Vector2.magnitude(dir) ** 2
        if dist == 0:
            return Vector2(0, 0)
        total_mass = (self.mass ** 2) * (other.mass ** 2)
        force = globals.gravity * (total_mass / dist) if dist != 0 else 0
        return Vector2.normalize(dir) * force

    @calc_force.register
    def _(self, other_pos:Vector2, other_mass:int | float):
            dir = self.pos - other_pos;
            dist = Vector2.magnitude(dir) ** 2
            if dist == 0:
                return Vector2(0, 0)
            total_mass = (self.mass ** 2) * (other_mass ** 2)
            force = globals.gravity * (total_mass / dist) if dist != 0 else 0
            return Vector2.normalize(dir) * force


class Orbitor(MassParticle):
    def __init__(self, position, acceleration, velocity, mass):
        super().__init__(position, acceleration, velocity, mass)
    
    def calc_force(self, attractor):
        force = Vector2(0, 0)
        force += attractor.calc_force(self)
        self.acc += force

def PreviewOrbitor(start_pos, start_vel, attractor, itts = 20, as_line = False, ping_time = 20):
    pos = start_pos.copy()
    vel = start_vel.copy()
    positions = [pos.copy()]
    for i in range(itts):
        for j in range(ping_time):
            force = Vector2(0, 0)
            force += attractor.calc_force(pos, 1)
            vel += force * globals.time_step
            pos += vel * globals.time_step
        if not as_line:
            draw.circle(globals.preview_screen, (0, 0, 255), pos, 3)
        else:
            positions.append(pos.copy())
    if as_line:
        draw.lines(globals.preview_screen, (0, 0, 255), False, positions)

def basic_fitness(static_start_pos, vel_x, vel_y, attractor, itts = itterations, draw_result = False):
    orbitor = Orbitor(static_start_pos.copy(), Vector2(0, 0), Vector2(vel_x, vel_y), 1)
    distances = [(attractor.pos - orbitor.pos).magnitude()]
    positions = [orbitor.pos.copy()]
    target_distance = 250
    for i in range(itts):
        orbitor.calc_force(attractor)
        orbitor.update()
        distances.append((attractor.pos - orbitor.pos).magnitude()) # Square so that bigger distances are more harshly punished.
        positions.append(orbitor.pos.copy())

    distance_error = abs(target_distance - np.mean(distances))

    if (draw_result):
        prev_pos = static_start_pos
        for pos in positions:
            draw.line(globals.screen, (0, 0, 255), prev_pos, pos)
            prev_pos = pos
    
    return -distance_error