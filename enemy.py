from settings import *


class Tank:
    def __init__(self, pos, max_health, initial_rotation):
        self.pos = pos
        self.max_health = max_health
        self.health = self.max_health
        self.rotation = initial_rotation
        self.turret_rotation = initial_rotation



