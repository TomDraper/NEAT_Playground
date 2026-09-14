from pygame import Vector2

class MouseTracker():
    def __init__(self):
        self.last_click = Vector2(0, 0)
        self.current = Vector2(0, 0)
        self.held = False

    def clicked(self, pos):
        self.last_click = Vector2(pos)
        self.held = True

    def released(self, pos):
        self.held = False
        return pos - self.last_click